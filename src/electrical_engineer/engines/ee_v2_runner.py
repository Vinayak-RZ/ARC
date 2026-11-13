"""Dispatch problem.json to ee_v2_solvers; shared by run-ee-v2-solver and check-numeric."""

from __future__ import annotations

from typing import Any

from electrical_engineer.engines import ee_v2_solvers as v2
from electrical_engineer.engines.ed_lambda import EdCase
from electrical_engineer.engines.power_runner import _parse_complex

DEFAULT_VALUE_KEY: dict[str, str] = {
    "rc_step": "vc_V",
    "rl_step": "i_A",
    "rlc_natural": "vc_V",
    "phasor_pfc": "P_W",
    "three_phase_balanced": "P_W",
    "transformer_regulation": "regulation_percent",
    "dc_motor_shunt": "omega_rad_s",
    "induction_air_gap_split": "P_mech_W",
    "ccm_buck": "D",
    "ed_with_losses": "lam",
    "ed_naive_dispatch": "lam",
    "load_flow_json": "vm_pu",
    "z_inverse": "poles_z_inv",
    "breakaway_real_axis": "breakaway",
    "steady_state_error": "ess_selected",
}

SOLVER_IDS = frozenset(DEFAULT_VALUE_KEY)


def _num(problem: dict[str, Any], key: str, default: float | None = None) -> float:
    if key not in problem and default is not None:
        return default
    raw = problem[key]
    if isinstance(raw, dict):
        return float(raw["value"])
    return float(raw)


def _units_spec(problem: dict[str, Any]) -> Any:
    u = problem.get("units")
    if isinstance(u, str) and u == "eec301":
        return EdCase.eec301_default()
    return u or []


def _optional_num(problem: dict[str, Any], key: str, default: float) -> float:
    if key not in problem:
        return default
    return _num(problem, key)


def _complex_val(problem: dict[str, Any], key: str) -> complex:
    raw = problem.get(key, 0j)
    if isinstance(raw, dict):
        raw = raw.get("value", raw.get("re", 0))
    if isinstance(raw, complex):
        return raw
    return _parse_complex(raw)


_ALIASES = {
    "ccm_buck_duty": "ccm_buck",
    "ed_penalty_dispatch": "ed_with_losses",
    "sym_fault_z1": "sym_fault_z1",
}


def solver_id(problem: dict[str, Any]) -> str | None:
    sid = problem.get("solver") or problem.get("check_kind")
    if not sid:
        return None
    key = str(sid)
    return _ALIASES.get(key, key)


def solve_ee_v2(problem: dict[str, Any]) -> dict[str, Any]:
    sid = solver_id(problem)
    if not sid or sid not in SOLVER_IDS:
        raise ValueError(f"unknown or missing ee_v2 solver {sid!r}")
    result = _call_solver(sid, problem)
    value_key = str(problem.get("value_key") or DEFAULT_VALUE_KEY[sid])
    unit = problem.get("unit") or _default_unit(sid, value_key)
    if sid == "breakaway_real_axis":
        pts = list(result.get("breakaway_sigma", []))
        target = problem.get("pick_sigma")
        if target is not None:
            value = float(min(pts, key=lambda p: abs(p - float(target))))
        else:
            idx = int(problem.get("pick_index", 0))
            value = float(pts[idx])
    elif sid == "load_flow_json" and problem.get("bus") is not None:
        bus = int(problem["bus"])
        value = float(result["buses"][bus]["vm_pu"])
        value_key = "vm_pu"
    else:
        raw_val = result.get(value_key) if value_key in result else _scalar_from_result(sid, result)
        value = float(raw_val) if not isinstance(raw_val, list) else float(raw_val[0])
    return {
        "solver": sid,
        "value_key": value_key,
        "unit": unit,
        "value": value,
        "result": result,
    }


def recompute_scalar(problem: dict[str, Any]) -> float | None:
    sid = solver_id(problem)
    if not sid or sid not in SOLVER_IDS:
        return None
    try:
        out = solve_ee_v2({**problem, "solver": sid})
    except (ValueError, TypeError, KeyError, ZeroDivisionError):
        return None
    return float(out["value"])


def _scalar_from_result(sid: str, result: dict[str, Any]) -> float:
    if sid == "breakaway_real_axis":
        pts = result.get("breakaway_sigma") or result.get("points") or []
        idx = int(result.get("pick_index", 0))
        return float(pts[idx])
    if sid == "load_flow_json" and result.get("buses"):
        bus = int(result.get("bus", 1))
        return float(result["buses"][bus]["vm_pu"])
    key = DEFAULT_VALUE_KEY[sid]
    return float(result[key])


def _default_unit(sid: str, value_key: str) -> str:
    if value_key.endswith("_V"):
        return "V"
    if value_key.endswith("_A"):
        return "A"
    if value_key in {"D", "pf", "zeta"}:
        return "1"
    if sid == "ed_with_losses" or sid == "ed_naive_dispatch":
        return "MW/MW"
    if value_key.startswith("ess"):
        return "1"
    if value_key == "regulation_percent":
        return "%"
    if value_key == "omega_rad_s":
        return "rad/s"
    if value_key == "P_W" or value_key.endswith("_W"):
        return "W"
    if value_key == "lam":
        return "MW/MW"
    return "1"


def ed_naive_dispatch(units: Any, pd_mw: float, *, loss_guess_mw: float = 0.0) -> dict[str, Any]:
    """Trap pattern: dispatch to Pd only (optional fixed loss guess), no penalty iteration."""
    from electrical_engineer.engines.ed_lambda import solve_lambda_ed

    case = units if isinstance(units, EdCase) else EdCase(units=tuple(v2._units_from_any(units)))
    r = solve_lambda_ed(case, pd_mw + loss_guess_mw)
    return {
        "PD": pd_mw,
        "P": list(r["P"]),
        "lam": float(r["lam"]),
        "naive": True,
        "loss_guess_mw": loss_guess_mw,
        "sum_P": float(sum(r["P"])),
    }


def _call_solver(sid: str, problem: dict[str, Any]) -> dict[str, Any]:
    if sid == "rc_step":
        return v2.rc_step(_num(problem, "v"), _num(problem, "r"), _num(problem, "c"), _num(problem, "t"))
    if sid == "rl_step":
        return v2.rl_step(_num(problem, "v"), _num(problem, "r"), _num(problem, "l"), _num(problem, "t"))
    if sid == "rlc_natural":
        return v2.rlc_natural(
            _num(problem, "r"),
            _num(problem, "l"),
            _num(problem, "c"),
            _num(problem, "vc0"),
            _num(problem, "i0"),
            _num(problem, "t"),
        )
    if sid == "phasor_pfc":
        return v2.phasor_pfc(_num(problem, "v_line"), _complex_val(problem, "z_load"))
    if sid == "three_phase_balanced":
        return v2.three_phase_balanced(
            _num(problem, "v_phase"),
            _num(problem, "i_phase"),
            connection=problem.get("connection", "wye"),  # type: ignore[arg-type]
            pf=_optional_num(problem, "pf", 1.0),
        )
    if sid == "transformer_regulation":
        return v2.transformer_regulation(
            _num(problem, "v_rated"),
            _num(problem, "r_pu"),
            _num(problem, "x_pu"),
            _optional_num(problem, "pf_lag", 0.8),
            _optional_num(problem, "load_pu", 1.0),
        )
    if sid == "dc_motor_shunt":
        return v2.dc_motor_shunt(
            _num(problem, "v"),
            _num(problem, "ra"),
            _num(problem, "kt"),
            _num(problem, "ke"),
            _num(problem, "load_t"),
        )
    if sid == "induction_air_gap_split":
        return v2.induction_air_gap_split(_num(problem, "pag"), _num(problem, "s"), _num(problem, "r2p"))
    if sid == "ccm_buck":
        return v2.ccm_buck(
            _num(problem, "vin"),
            _num(problem, "vout"),
            _num(problem, "l"),
            _num(problem, "c"),
            _num(problem, "fs"),
            _optional_num(problem, "ripple_pct", 20.0),
            i_out=_optional_num(problem, "i_out", 1.0),
        )
    if sid == "ed_with_losses":
        units = _units_spec(problem)
        return v2.ed_with_losses(units, problem["B"], _num(problem, "pd_mw"))
    if sid == "ed_naive_dispatch":
        units = _units_spec(problem)
        return ed_naive_dispatch(units, _num(problem, "pd_mw"))
    if sid == "load_flow_json":
        return v2.load_flow_json(problem["network"])
    if sid == "z_inverse":
        return v2.z_inverse(problem)
    if sid == "breakaway_real_axis":
        poles = [float(x) for x in problem["poles"]]
        zeros = [float(x) for x in problem.get("zeros", [])]
        pts = v2.breakaway_real_axis(poles=poles, zeros=zeros or None)
        return {"breakaway_sigma": pts, "breakaway": pts[0] if pts else 0.0}
    if sid == "steady_state_error":
        st = int(problem.get("system_type", problem.get("type", 1)))
        gain = _num(problem, "gain")
        err = v2.steady_state_error_type(st, gain)
        key = str(problem.get("error_key") or ("ess_step" if st == 0 else "ess_ramp" if st == 1 else "ess_parabolic"))
        err["ess_selected"] = err[key]
        return err
    raise ValueError(sid)

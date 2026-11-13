"""Trap verifiers: numeric answers only, graded against engines (no self-report flags)."""

from __future__ import annotations

import math
from typing import Any

import control

from electrical_engineer.benchmark_v01.engine_cases import agc_case_from_givens, ed_case_from_givens
from electrical_engineer.engines.agc_two_area import simulate_two_area
from electrical_engineer.engines.control_margins import loop_margins
from electrical_engineer.engines.ed_lambda import incremental_cost, solve_lambda_ed
from electrical_engineer.engines.smib_swing import (
    critical_clearing_angle,
    initial_angle_pre_fault,
    simulate_clearing,
    swing_derivative,
    time_to_angle_during_fault,
)
from electrical_engineer.rlvr_env import problems as trap_problems

_GIVEN_KEYS = frozenset(
    {
        "h_mj_mva",
        "f0_hz",
        "pm_pu",
        "pmax_pre_pu",
        "pmax_fault_pu",
        "pmax_post_pu",
        "h_integrator_s",
        "tc_s",
        "t_query_s",
        "load_step_area1_MW",
        "t_end_s",
        "K_agc",
        "PD_MW",
        "unit1_MW",
        "num",
        "den",
    }
)


def _close(a: float, b: float, tol: float) -> bool:
    return abs(float(a) - float(b)) <= float(tol)


def _submission_echoes_givens(sub: dict[str, Any], givens: dict[str, Any]) -> bool:
    """Reject copies of observation givens without computed answer fields."""
    graded_keys = [k for k in sub if k not in _GIVEN_KEYS]
    if not graded_keys:
        return True
    echo = True
    for key, val in sub.items():
        if key in givens and givens[key] == val:
            continue
        if key in _GIVEN_KEYS:
            continue
        echo = False
    return echo and not any(k for k in graded_keys if k not in givens)


def grade_trap(
    trap_id: str,
    submission: dict[str, Any],
    *,
    givens: dict[str, Any] | None = None,
) -> tuple[bool, float]:
    givens = dict(givens or trap_problems.sample_trap_givens(trap_id, 0))
    if not submission or _submission_echoes_givens(submission, givens):
        return False, 0.0
    fn = _GRADERS.get(trap_id)
    if fn is None:
        return False, 0.0
    return fn(submission, givens)


def _grade_t1(sub: dict[str, Any], givens: dict[str, Any]) -> tuple[bool, float]:
    case = trap_problems.smib_case(givens)
    want = math.degrees(critical_clearing_angle(case))
    val = sub.get("delta_cr_deg")
    if val is None:
        return False, 0.0
    ok = _close(float(val), want, 0.05)
    return ok, 1.0 if ok else 0.0


def _grade_t2(sub: dict[str, Any], givens: dict[str, Any]) -> tuple[bool, float]:
    case = trap_problems.smib_case(givens)
    dcr = critical_clearing_angle(case)
    h = float(givens.get("h_integrator_s", 0.001))
    t = time_to_angle_during_fault(case, dcr, h_s=h, integrator="rk4")
    val = sub.get("t_to_delta_cr_s")
    if val is None or t is None:
        return False, 0.0
    ok = _close(float(val), t, 0.002)
    return ok, 1.0 if ok else 0.0


def _grade_t3(sub: dict[str, Any], givens: dict[str, Any]) -> tuple[bool, float]:
    case = trap_problems.smib_case(givens)
    want = case.accel_coeff()
    got = sub.get("accel_coeff")
    domega = sub.get("domega0_at_prefault")
    if got is None or domega is None:
        return False, 0.0
    d0 = initial_angle_pre_fault(case)
    _, domega0 = swing_derivative(d0, 0.0, case.pmax_pre_pu, case)
    ok = _close(float(got), want, 1e-6)
    ok = ok and _close(float(domega), domega0, 1e-8)
    ok = ok and abs(domega0) < 1e-10
    return ok, 1.0 if ok else 0.0


def _grade_t4(sub: dict[str, Any], givens: dict[str, Any]) -> tuple[bool, float]:
    case = agc_case_from_givens(givens)
    out = simulate_two_area(
        case,
        run="primary",
        t_end_s=float(givens.get("t_end_s", 30.0)),
        dpl1_pu=float(givens.get("dpl1_pu", 0.1)),
        dpl2_pu=float(givens.get("dpl2_pu", 0.0)),
        step_time_s=float(givens.get("step_time_s", 1.0)),
    )
    st = out["steady"]
    df = sub.get("primary_df1_Hz")
    p12 = sub.get("primary_P12_MW")
    if df is None or p12 is None:
        return False, 0.0
    ok = _close(float(df), st["df1_hz"], 0.002)
    ok = ok and _close(float(p12), st["P12_MW"], 0.5)
    ok = ok and float(p12) < 0
    return ok, 1.0 if ok else 0.0


def _grade_t5(sub: dict[str, Any], givens: dict[str, Any]) -> tuple[bool, float]:
    k = float(givens.get("K_agc", 0.3))
    case = agc_case_from_givens(givens).with_k(k)
    st = simulate_two_area(
        case,
        run="agc",
        t_end_s=float(givens.get("agc_t_end_s", 60.0)),
        dpl1_pu=float(givens.get("dpl1_pu", 0.1)),
        dpl2_pu=float(givens.get("dpl2_pu", 0.0)),
        step_time_s=float(givens.get("step_time_s", 1.0)),
    )["steady"]
    df = sub.get("agc_ss_df1_Hz")
    p12 = sub.get("agc_ss_P12_MW")
    if df is None or p12 is None:
        return False, 0.0
    ok = _close(float(df), st["df1_hz"], 0.002)
    ok = ok and _close(float(p12), st["P12_MW"], 0.05)
    return ok, 1.0 if ok else 0.0


def _grade_t6(sub: dict[str, Any], givens: dict[str, Any]) -> tuple[bool, float]:
    from electrical_engineer.engines.ed_lambda import EdCase

    pd = float(givens["PD_MW"])
    case = ed_case_from_givens(givens) if givens.get("units") else EdCase.eec301_default()
    r = solve_lambda_ed(case, pd)
    p2 = sub.get("unit2_MW")
    ic2 = sub.get("unit2_IC")
    lam = sub.get("lambda")
    if None in (p2, ic2, lam):
        return False, 0.0
    ok = _close(float(p2), r["P"][1], 0.05)
    ok = ok and _close(float(lam), r["lam"], 0.05)
    ok = ok and _close(float(ic2), r["IC"][1], 0.05)
    return ok, 1.0 if ok else 0.0


def _grade_t7(sub: dict[str, Any], givens: dict[str, Any]) -> tuple[bool, float]:
    case = ed_case_from_givens(givens)
    p = float(givens["unit1_MW"])
    want = incremental_cost(p, case.units[0])
    ic = sub.get("unit1_IC")
    if ic is None:
        return False, 0.0
    ok = _close(float(ic), want, 1e-4)
    wrong = case.units[0].b + case.units[0].c * p
    if _close(float(ic), wrong, 1e-4):
        return False, 0.0
    return ok, 1.0 if ok else 0.0


def _grade_t8(sub: dict[str, Any], givens: dict[str, Any]) -> tuple[bool, float]:
    sys = control.tf(givens["num"], givens["den"])
    m = loop_margins(sys)
    gm = sub.get("gain_margin_dB")
    wg = sub.get("gain_crossover_rad_s")
    if gm is None or wg is None:
        return False, 0.0
    ok = _close(float(wg), m["gain_crossover_rad_s"], 0.02)
    ok = ok and _close(float(gm), m["gain_margin_dB"], 0.05)
    return ok, 1.0 if ok else 0.0


def _grade_t9(sub: dict[str, Any], givens: dict[str, Any]) -> tuple[bool, float]:
    case = trap_problems.smib_case(givens)
    tc = float(givens["tc_s"])
    t_q = float(givens["t_query_s"])
    h = float(givens["h_integrator_s"])
    out = simulate_clearing(case, tc, h, t_q + 0.5, "rk4")
    trail = out["trail"]
    pt = min(trail, key=lambda p: abs(p[0] - t_q))
    want = math.degrees(pt[1])
    val = sub.get("delta_deg_at_t")
    if val is None:
        return False, 0.0
    ok = _close(float(val), want, 0.05)
    return ok, 1.0 if ok else 0.0


def _grade_t10(sub: dict[str, Any], givens: dict[str, Any]) -> tuple[bool, float]:
    case = trap_problems.smib_case(givens)
    want = math.degrees(initial_angle_pre_fault(case))
    val = sub.get("delta0_deg")
    if val is None:
        return False, 0.0
    ok = _close(float(val), want, 0.02)
    return ok, 1.0 if ok else 0.0


_GRADERS = {
    "T1": _grade_t1,
    "T2": _grade_t2,
    "T3": _grade_t3,
    "T4": _grade_t4,
    "T5": _grade_t5,
    "T6": _grade_t6,
    "T7": _grade_t7,
    "T8": _grade_t8,
    "T9": _grade_t9,
    "T10": _grade_t10,
}


def oracle_submission(trap_id: str, givens: dict[str, Any] | None = None) -> dict[str, Any]:
    givens = dict(givens or trap_problems.sample_trap_givens(trap_id, 0))
    case = trap_problems.smib_case(givens) if trap_id in {"T1", "T2", "T3", "T9", "T10"} else None
    if trap_id == "T1" and case:
        return {"delta_cr_deg": math.degrees(critical_clearing_angle(case))}
    if trap_id == "T2" and case:
        dcr = critical_clearing_angle(case)
        h = float(givens.get("h_integrator_s", 0.001))
        t = time_to_angle_during_fault(case, dcr, h_s=h, integrator="rk4")
        return {"t_to_delta_cr_s": t}
    if trap_id == "T3" and case:
        d0 = initial_angle_pre_fault(case)
        _, domega0 = swing_derivative(d0, 0.0, case.pmax_pre_pu, case)
        return {"accel_coeff": case.accel_coeff(), "domega0_at_prefault": domega0}
    if trap_id == "T4":
        st = simulate_two_area(
            agc_case_from_givens(givens),
            run="primary",
            t_end_s=float(givens.get("t_end_s", 30.0)),
            dpl1_pu=float(givens.get("dpl1_pu", 0.1)),
            dpl2_pu=float(givens.get("dpl2_pu", 0.0)),
            step_time_s=float(givens.get("step_time_s", 1.0)),
        )["steady"]
        return {"primary_df1_Hz": st["df1_hz"], "primary_P12_MW": st["P12_MW"]}
    if trap_id == "T5":
        k = float(givens.get("K_agc", 0.3))
        st = simulate_two_area(
            agc_case_from_givens(givens).with_k(k),
            run="agc",
            t_end_s=float(givens.get("agc_t_end_s", 60.0)),
            dpl1_pu=float(givens.get("dpl1_pu", 0.1)),
            dpl2_pu=float(givens.get("dpl2_pu", 0.0)),
        )["steady"]
        return {"agc_ss_df1_Hz": st["df1_hz"], "agc_ss_P12_MW": st["P12_MW"]}
    if trap_id == "T6":
        r = solve_lambda_ed(ed_case_from_givens(givens), float(givens["PD_MW"]))
        return {"unit2_MW": r["P"][1], "unit2_IC": r["IC"][1], "lambda": r["lam"]}
    if trap_id == "T7":
        p = float(givens["unit1_MW"])
        return {"unit1_IC": incremental_cost(p, ed_case_from_givens(givens).units[0])}
    if trap_id == "T8":
        m = loop_margins(control.tf(givens["num"], givens["den"]))
        return {"gain_margin_dB": m["gain_margin_dB"], "gain_crossover_rad_s": m["gain_crossover_rad_s"]}
    if trap_id == "T9" and case:
        tc = float(givens["tc_s"])
        t_q = float(givens["t_query_s"])
        h = float(givens["h_integrator_s"])
        out = simulate_clearing(case, tc, h, t_q + 0.5, "rk4")
        pt = min(out["trail"], key=lambda p: abs(p[0] - t_q))
        return {"delta_deg_at_t": math.degrees(pt[1])}
    if trap_id == "T10" and case:
        return {"delta0_deg": math.degrees(initial_angle_pre_fault(case))}
    raise KeyError(trap_id)


def naive_submission(trap_id: str, givens: dict[str, Any]) -> dict[str, Any]:
    """Classic bare-agent mistake per trap (low score baseline)."""
    case = trap_problems.smib_case(givens) if trap_id in {"T1", "T2", "T3", "T9", "T10"} else None
    if trap_id == "T1" and case:
        d0 = math.asin(case.pm_pu / case.pmax_pre_pu)
        wrong = math.degrees(
            d0 + (case.pm_pu / max(case.pmax_post_pu - case.pm_pu, 1e-6)) * (math.pi - d0)
        )
        return {"delta_cr_deg": wrong}
    if trap_id == "T2":
        return {"t_to_delta_cr_s": 0.0}
    if trap_id == "T3" and case:
        wrong = math.pi * case.f0_hz / case.h_mj_mva
        return {"accel_coeff": wrong / 2.0, "domega0_at_prefault": 1.0}
    if trap_id == "T4":
        return {"primary_df1_Hz": 0.0, "primary_P12_MW": 45.0}
    if trap_id == "T5":
        return {"agc_ss_df1_Hz": -0.16, "agc_ss_P12_MW": 0.0}
    if trap_id == "T6":
        return {"unit2_MW": 200.0, "unit2_IC": 5.0, "lambda": 7.39}
    if trap_id == "T7":
        p = float(givens["unit1_MW"])
        u = ed_case_from_givens(givens).units[0]
        return {"unit1_IC": u.b + u.c * p}
    if trap_id == "T8":
        return {"gain_margin_dB": 6.0, "gain_crossover_rad_s": 4.472}
    if trap_id == "T9" and case:
        return {"delta_deg_at_t": float(givens.get("pm_pu", 0.9))}
    if trap_id == "T10" and case:
        return {
            "pm_pu": case.pm_pu,
            "f0_hz": case.f0_hz,
            "pmax_pre_pu": case.pmax_pre_pu,
        }
    return {}

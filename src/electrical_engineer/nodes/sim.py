"""Verifier seams. Missing tools fail clearly — never a fake pass."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.capabilities import CD_NO_PROVIDER
from electrical_engineer.nodes.registry import register
from electrical_engineer.unchecked import UNCHECKED


def _missing(tool: str, spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    return {
        "ok": False,
        "tool": tool,
        "error": f"{tool} not available",
        "unchecked": True,
        "token": UNCHECKED,
        "cannot_do": CD_NO_PROVIDER,
        "inputs": inputs,
        "node": spec.get("id"),
    }


def _problem(spec: dict[str, Any]) -> dict[str, Any]:
    p = spec.get("problem")
    if isinstance(p, dict) and p:
        return p
    run_dir = spec.get("run_dir")
    if run_dir:
        path = Path(run_dir) / "problem.json"
        if path.is_file():
            import json

            return json.loads(path.read_text())
    return {}


@register("load-netlist")
def load_netlist(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    problem = _problem(spec)
    cir = problem.get("cir") or inputs.get("draft", {}).get("cir") or "* empty\n"
    run_dir = spec.get("run_dir")
    if run_dir:
        Path(run_dir, "netlist.cir").write_text(str(cir))
    return {"ok": True, "cir": cir}


@register("run-rlc-analytic")
def run_rlc_analytic(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.rlc_transient import solve_from_problem

    run_dir_s = spec.get("run_dir")
    if not run_dir_s:
        return _missing("rlc_analytic", spec, inputs)
    problem = _problem(spec)
    try:
        result = solve_from_problem(problem)
    except ValueError as exc:
        return {"ok": False, "error": str(exc), "unchecked": True, "tool": "rlc_analytic"}
    run_dir = Path(run_dir_s)
    _write_run_json(run_dir, "rlc_transient.json", result)
    return {
        "ok": True,
        "unchecked": False,
        "tool": "rlc_analytic",
        "value": result["Vc_peak_V"],
        "result": result,
        "capability": "lumped-circuit-sim",
    }


@register("run-primary-steady")
def run_primary_steady(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.agc_two_area import primary_response_from_load_step

    run_dir_s = spec.get("run_dir")
    if not run_dir_s:
        return _missing("primary_steady", spec, inputs)
    problem = _problem(spec)
    dpl = float(problem.get("dpl_mw") or problem.get("load_step_mw") or 50.0)
    beta1 = float(problem.get("beta1", 21.0))
    beta2 = float(problem.get("beta2", 21.0))
    f0 = float(problem.get("f0_hz", 50.0))
    s_base = float(problem.get("s_base_mva", 1000.0))
    steady = primary_response_from_load_step(dpl, beta1=beta1, beta2=beta2, f0_hz=f0, s_base_mva=s_base)
    run_dir = Path(run_dir_s)
    _write_run_json(run_dir, "primary_steady.json", steady)
    return {
        "ok": True,
        "unchecked": False,
        "value": steady["df_hz"],
        "engine": "agc_two_area",
        "steady": steady,
        "capability": "agc-two-area",
    }


@register("run-circuit-derive")
def run_circuit_derive(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.circuit_derive import derive

    problem = dict(_problem(spec))
    for v in inputs.values():
        if isinstance(v, dict) and v.get("cir"):
            problem.setdefault("cir", v["cir"])
    try:
        out = derive(problem)
    except ValueError as exc:
        return {"ok": False, "error": str(exc), "unchecked": True, "capability": "algebraic-check"}
    run_dir_s = spec.get("run_dir")
    if run_dir_s:
        _write_run_json(Path(run_dir_s), "circuit_derive.json", out)
        net = Path(run_dir_s) / "netlist.cir"
        net.write_text(str(out.get("cir") or ""), encoding="utf-8")
    return {
        "ok": True,
        "unchecked": False,
        "value": out.get("value"),
        "unit": out.get("unit"),
        "cir": out.get("cir"),
        "capability": "algebraic-check",
        "tool": "circuit_derive",
        "derived": out,
    }


@register("verify-circuit-spice")
def verify_circuit_spice(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.circuit_verify import verify_after_derive

    problem = dict(_problem(spec))
    for v in inputs.values():
        if isinstance(v, dict) and v.get("derived"):
            problem = {**problem, **(v["derived"] if isinstance(v["derived"], dict) else {})}
        if isinstance(v, dict) and v.get("value") is not None and "kind" not in problem:
            problem.update({k: v[k] for k in ("kind", "vin", "r1", "r2", "resistors") if k in v})
    run_dir_s = spec.get("run_dir")
    run_dir = Path(run_dir_s) if run_dir_s else None
    out = verify_after_derive(problem, run_dir=run_dir, rel_tol=float(problem.get("rel_tol", 1e-3)))
    if run_dir and out.get("spice"):
        _write_run_json(run_dir, "circuit_verify.json", out)
    if out.get("mismatch"):
        out["label_message"] = "derive vs simulation mismatch"
        out["spice_mismatch"] = True
    if out.get("ok") and not out.get("unchecked"):
        out["unchecked"] = False
    return {**out, "capability": "lumped-circuit-sim", "tool": "circuit_verify"}


@register("run-spice")
def run_spice(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.spice_runner import run_spice_netlist, spice_available

    if spec.get("require_confirmed"):
        run_dir = spec.get("run_dir")
        flag = Path(run_dir, "confirmed.json") if run_dir else None
        if flag is None or not flag.is_file():
            return {
                "ok": False,
                "error": "unconfirmed",
                "unchecked": True,
                "token": UNCHECKED,
                "spice": False,
            }
    repair_max = int(spec.get("repair_max", 0))
    problem = _problem(spec)
    run_dir_s = spec.get("run_dir")
    run_dir = Path(run_dir_s) if run_dir_s else None
    cir = problem.get("cir") or inputs.get("draft", {}).get("cir")
    if not cir and run_dir:
        net = run_dir / "netlist.cir"
        if net.is_file():
            cir = net.read_text(encoding="utf-8")
    if not cir:
        load_out = inputs.get("load") if isinstance(inputs.get("load"), dict) else {}
        cir = load_out.get("cir") or "* empty\n"
    last: dict[str, Any] | None = None
    for _ in range(repair_max + 1):
        if not spice_available():
            kind = str(problem.get("kind") or problem.get("circuit") or "").lower()
            if kind in {"series_rlc", "rlc"} or {"r_ohm", "l_h", "c_f"} <= set(problem.keys()):
                from electrical_engineer.engines.rlc_transient import solve_from_problem

                try:
                    result = solve_from_problem(problem)
                except ValueError as exc:
                    last = {"ok": False, "error": str(exc), "unchecked": True, "tool": "rlc_analytic"}
                else:
                    if run_dir is None:
                        last = _missing("rlc_analytic", spec, inputs)
                    else:
                        _write_run_json(run_dir, "rlc_transient.json", result)
                        last = {
                            "ok": True,
                            "unchecked": False,
                            "tool": "rlc_analytic",
                            "value": result["Vc_peak_V"],
                            "result": result,
                            "capability": "lumped-circuit-sim",
                        }
                        break
            else:
                last = _missing("ngspice/PySpice", spec, inputs)
                last["hint"] = (
                    "ngspice/PySpice not installed; for RLC use run-rlc-analytic "
                    "or problem keys r_ohm, l_h, c_f, v_step"
                )
                last["analytic_recipe"] = "run-rlc-analytic"
            continue
        if run_dir is None:
            last = _missing("ngspice/PySpice", spec, inputs)
            break
        last = run_spice_netlist(str(cir), run_dir, problem)
        if last.get("ok"):
            break
    assert last is not None
    last["repairs"] = repair_max
    last["exhausted"] = last.get("ok") is False
    return last


@register("run-python-control")
def run_python_control(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.control_runner import control_available, run_control_plots

    run_dir_s = spec.get("run_dir")
    if not run_dir_s:
        return _missing("python-control", spec, inputs)
    problem = dict(_problem(spec))
    for v in inputs.values():
        if isinstance(v, dict) and v.get("num") is not None and v.get("den") is not None:
            problem["num"] = v["num"]
            problem["den"] = v["den"]
            break
    if not control_available():
        out = _missing("python-control", spec, inputs)
        return out
    return run_control_plots(Path(run_dir_s), problem)


@register("run-matlab-if-present")
def run_matlab_if_present(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.matlab_mcp import (
        MatlabMcpError,
        MatlabMissing,
        evaluate_code,
        result_text,
        run_file,
    )

    problem = _problem(spec)
    run_dir = spec.get("run_dir")
    project = str(run_dir or Path.cwd())
    code = problem.get("matlab") or problem.get("code") or inputs.get("code")
    script = problem.get("script_path") or inputs.get("script_path")
    try:
        if code:
            raw = evaluate_code(str(code), project)
        elif script:
            raw = run_file(str(script))
        else:
            return _missing("matlab", spec, inputs)
    except (MatlabMissing, MatlabMcpError):
        return _missing("matlab", spec, inputs)
    if raw.get("isError"):
        miss = _missing("matlab", spec, inputs)
        miss["output"] = result_text(raw)
        return miss
    text = result_text(raw)
    return {
        "ok": True,
        "tool": "matlab-mcp",
        "unchecked": False,
        "output": text,
        "node": spec.get("id"),
    }


@register("run-simulink-if-present")
def run_simulink_if_present(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.matlab_mcp import (
        MatlabMcpError,
        MatlabMissing,
        call_tool,
        result_text,
        simulink_extension,
    )

    def _plant_missing() -> dict[str, Any]:
        miss = _missing("simulink", spec, inputs)
        miss["cannot_do"] = "CD-SIMULINK-PLANT"
        return miss

    if not simulink_extension():
        return _plant_missing()
    problem = _problem(spec)
    model = problem.get("model_path") or inputs.get("model_path")
    if not model:
        return _plant_missing()
    run_dir = spec.get("run_dir")
    try:
        raw = call_tool(
            "model_read",
            {"model_path": str(model)},
            run_dir=str(run_dir) if run_dir else None,
        )
    except (MatlabMissing, MatlabMcpError):
        return _plant_missing()
    if raw.get("isError"):
        miss = _plant_missing()
        miss["output"] = result_text(raw)
        return miss
    return {
        "ok": True,
        "tool": "simulink-mcp",
        "unchecked": False,
        "output": result_text(raw),
        "node": spec.get("id"),
        "cannot_do": None,
    }


def _write_run_json(run_dir: Path, name: str, data: dict[str, Any]) -> None:
    import json

    (run_dir / name).write_text(json.dumps(data, indent=2))


@register("run-smib-swing")
def run_smib_swing(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.smib_swing import (
        SmibCase,
        critical_clearing_time_bisection,
        eec301_reference,
    )

    run_dir_s = spec.get("run_dir")
    if not run_dir_s:
        return _missing("smib_swing", spec, inputs)
    problem = _problem(spec)
    case = SmibCase(**{k: problem[k] for k in problem if k in SmibCase.__dataclass_fields__})
    ref = eec301_reference(case)
    tcr = critical_clearing_time_bisection(case, h_s=0.001, tol_s=1e-6, t_hi=0.35)
    payload = {**ref, "tcr_s": tcr, "engine": "smib_swing"}
    run_dir = Path(run_dir_s)
    _write_run_json(run_dir, "psa_smib.json", payload)
    return {
        "ok": True,
        "unchecked": False,
        "value": ref["delta_cr_deg"],
        "engine": "smib_swing",
        "psa": payload,
        "capability": "smib-swing",
    }


@register("run-agc-two-area")
def run_agc_two_area(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.agc_two_area import TwoAreaAgcCase, simulate_two_area

    run_dir_s = spec.get("run_dir")
    if not run_dir_s:
        return _missing("agc_two_area", spec, inputs)
    problem = _problem(spec)
    k = float(problem.get("K", 0.3))
    case = TwoAreaAgcCase.eec301_default().with_k(k)
    primary = simulate_two_area(TwoAreaAgcCase.eec301_default(), run="primary", t_end_s=30.0)
    agc = simulate_two_area(case, run="agc", t_end_s=60.0)
    payload = {
        "engine": "agc_two_area",
        "primary_steady": primary["steady"],
        "agc_steady": agc["steady"],
        "diverged": agc.get("diverged"),
    }
    run_dir = Path(run_dir_s)
    _write_run_json(run_dir, "psa_agc.json", payload)
    return {
        "ok": True,
        "unchecked": False,
        "value": agc["steady"]["df1_hz"],
        "engine": "agc_two_area",
        "psa": payload,
        "capability": "agc-two-area",
    }


def _ed_case_from_problem(problem: dict[str, Any]) -> tuple[Any, float]:
    from electrical_engineer.engines.ed_lambda import EdCase

    pd = float(problem.get("PD", problem.get("pd_mw", 500.0)))
    if "units" in problem and isinstance(problem["units"], list):
        units = problem["units"]
        a = [float(u.get("a", 0.0)) for u in units]
        b = [float(u["b"]) for u in units]
        c = [float(u["c"]) for u in units]
        pmin = [float(u["pmin"]) for u in units]
        pmax = [float(u["pmax"]) for u in units]
        return EdCase.from_coeff_lists(a, b, c, pmin, pmax), pd
    keys = ("b", "c", "pmin", "pmax")
    if all(k in problem for k in keys):
        b = [float(x) for x in problem["b"]]
        n = len(b)
        a = [float(x) for x in problem.get("a", [0.0] * n)]
        c = [float(x) for x in problem["c"]]
        pmin = [float(x) for x in problem["pmin"]]
        pmax = [float(x) for x in problem["pmax"]]
        return EdCase.from_coeff_lists(a, b, c, pmin, pmax), pd
    return EdCase.eec301_default(), pd


@register("run-ed-lambda")
def run_ed_lambda(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.ed_lambda import solve_lambda_ed

    run_dir_s = spec.get("run_dir")
    if not run_dir_s:
        return _missing("ed_lambda", spec, inputs)
    problem = _problem(spec)
    case, pd = _ed_case_from_problem(problem)
    result = solve_lambda_ed(case, pd)
    payload = {"engine": "ed_lambda", "PD": pd, **result}
    run_dir = Path(run_dir_s)
    _write_run_json(run_dir, "psa_ed.json", payload)
    return {
        "ok": True,
        "unchecked": False,
        "value": result["lam"],
        "engine": "ed_lambda",
        "psa": payload,
        "capability": "economic-dispatch-lambda",
    }


@register("run-ee-v2-solver")
def run_ee_v2_solver(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.ee_v2_runner import SOLVER_IDS, solve_ee_v2, solver_id

    run_dir_s = spec.get("run_dir")
    problem = _problem(spec)
    sid = solver_id(problem)
    if not sid or sid not in SOLVER_IDS:
        return {
            "ok": True,
            "skipped": True,
            "unchecked": True,
            "tool": "ee_v2",
            "reason": "no solver in problem.json",
        }
    try:
        out = solve_ee_v2(problem)
    except (ValueError, TypeError, KeyError, ZeroDivisionError) as exc:
        return {"ok": False, "error": str(exc), "unchecked": True, "tool": "ee_v2"}
    if run_dir_s:
        payload = {**out, "result": out["result"]}
        _write_run_json(Path(run_dir_s), "ee_v2_result.json", _json_safe(payload))
    return {
        "ok": True,
        "unchecked": False,
        "tool": "ee_v2",
        "solver": out["solver"],
        "value": out["value"],
        "unit": out.get("unit"),
        "value_key": out.get("value_key"),
        "result": out["result"],
        "capability": "algebraic-check",
    }


def _json_safe(data: Any) -> Any:
    if isinstance(data, dict):
        return {k: _json_safe(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_json_safe(v) for v in data]
    if isinstance(data, complex):
        return {"re": float(data.real), "im": float(data.imag)}
    if isinstance(data, (int, float, str, bool)) or data is None:
        return data
    return str(data)


@register("run-symmetrical-fault-base")
def run_symmetrical_fault_base(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.pu_base import aggregate_fault_impedance

    run_dir_s = spec.get("run_dir")
    if not run_dir_s:
        return _missing("symmetrical-fault-base", spec, inputs)
    problem = _problem(spec)
    try:
        agg = aggregate_fault_impedance(
            problem.get("elements", []),
            s_system_mva=float(problem.get("s_system_mva", 100)),
            v_system_kv=float(problem.get("v_system_kv", 13.8)),
        )
    except (ValueError, TypeError, KeyError) as exc:
        return {"ok": False, "error": str(exc), "unchecked": True, "tool": "pu_base"}
    run_dir = Path(run_dir_s)
    json_safe = {k: v for k, v in agg.items() if k not in ("z1_pu", "z2_pu", "z0_pu")}
    _write_run_json(run_dir, "sym_fault_impedance.json", json_safe)
    return {
        "ok": True,
        "unchecked": False,
        "tool": "pu_base",
        "value": float(agg["z1_pu_mag"]),
        "result": agg,
        "capability": "power-network-study",
    }


@register("run-load-flow")
def run_load_flow(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.power_runner import pandapower_available, run_power_study

    run_dir_s = spec.get("run_dir")
    if not run_dir_s:
        return _missing("pandapower", spec, inputs)
    problem = _problem(spec)
    if not pandapower_available():
        problem = {**problem, "sequence": True}
    return run_power_study(Path(run_dir_s), problem)


@register("check-numeric")
def check_numeric(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    problem = _problem(spec)
    computed = _hand_value(problem)
    tol = float(problem.get("tol", 1e-6))
    expected = problem.get("expected")
    child_value: float | None = None
    for v in inputs.values():
        if not isinstance(v, dict) or v.get("value") is None:
            continue
        if v.get("skipped"):
            continue
        child_value = float(v["value"])
        if expected is not None and computed is not None:
            ok_exp = abs(computed - float(expected)) <= tol
            ok_child = abs(child_value - computed) <= tol
            if ok_exp and ok_child:
                return {
                    "ok": True,
                    "value": child_value,
                    "unchecked": False,
                    "capability": "algebraic-check",
                    "recomputed": computed,
                }
            return {
                "ok": False,
                "unchecked": True,
                "token": UNCHECKED,
                "actual": child_value,
                "expected": expected,
                "recomputed": computed,
            }
        if v.get("ok") is True or v.get("unchecked") is False:
            return {
                "ok": True,
                "value": child_value,
                "unchecked": False,
                "capability": "algebraic-check",
            }
    actual = child_value if child_value is not None else computed
    if expected is None:
        expected = computed
    if expected is None or actual is None:
        return {"ok": False, "unchecked": True, "token": UNCHECKED, "reason": "no expected value"}
    ok = abs(float(actual) - float(expected)) <= tol
    if ok:
        return {"ok": True, "value": actual, "unchecked": False, "capability": "algebraic-check"}
    return {
        "ok": False,
        "unchecked": True,
        "token": UNCHECKED,
        "actual": actual,
        "expected": expected,
    }


def _recompute_scalar(problem: dict[str, Any]) -> float | None:
    from electrical_engineer.engines.ee_v2_runner import recompute_scalar

    rec = recompute_scalar(problem)
    if rec is not None:
        return rec
    if str(problem.get("check_kind") or "") == "sym_fault_z1":
        from electrical_engineer.engines.pu_base import aggregate_fault_impedance

        agg = aggregate_fault_impedance(
            problem["elements"],
            s_system_mva=float(problem.get("s_system_mva", 100)),
            v_system_kv=float(problem.get("v_system_kv", 13.8)),
        )
        return float(agg["z1_pu_mag"])
    return None


def _hand_value(problem: dict[str, Any]) -> float | None:
    rec = _recompute_scalar(problem)
    if rec is not None:
        return rec
    kind = str(problem.get("kind") or "")
    if kind == "ohms_law" and "v" in problem and "r" in problem:
        r = float(problem["r"])
        if r == 0:
            return None
        return float(problem["v"]) / r
    return _divider_value(problem)


def _divider_value(problem: dict[str, Any]) -> float | None:
    keys = {"vin", "r1", "r2"}
    if not keys <= set(problem) and str(problem.get("kind") or "") != "voltage_divider":
        return None
    if not {"vin", "r1", "r2"} <= set(problem):
        return None
    r1, r2 = float(problem["r1"]), float(problem["r2"])
    if r1 + r2 == 0:
        return None
    return float(problem["vin"]) * r2 / (r1 + r2)

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
            last = _missing("ngspice/PySpice", spec, inputs)
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
    actual = computed
    if actual is None:
        for v in inputs.values():
            if not isinstance(v, dict):
                continue
            if v.get("unchecked") is False and v.get("value") is not None:
                actual = v.get("value")
                break
    for v in inputs.values():
        if not isinstance(v, dict) or v.get("value") is None:
            continue
        if v.get("ok") is True or v.get("unchecked") is False:
            return {
                "ok": True,
                "value": v.get("value"),
                "unchecked": False,
                "capability": "algebraic-check",
            }
    expected = problem.get("expected")
    if expected is None:
        expected = computed
    if expected is None or actual is None:
        return {"ok": False, "unchecked": True, "token": UNCHECKED, "reason": "no expected value"}
    tol = float(problem.get("tol", 1e-6))
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


def _hand_value(problem: dict[str, Any]) -> float | None:
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

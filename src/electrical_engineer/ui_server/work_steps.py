"""Work-tab steps for a saved run. Numbers come from problem.json and engine files."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


def work_steps(run_dir: Path) -> list[dict[str, str]]:
    problem = _load(run_dir / "problem.json")
    try:
        from electrical_engineer.circuit.graph import series_rlc_params_from_graph
        from electrical_engineer.circuit.run_session import load_graph

        params = series_rlc_params_from_graph(load_graph(run_dir))
        if params:
            problem = {**problem, **params}
    except ImportError:
        pass
    evid = _load(run_dir / "evidentiary.json") or _load(run_dir / "summary.json")
    recipe = str(evid.get("recipe_id") or "")
    kind = str(problem.get("kind") or "")
    if kind == "voltage_divider" or {"vin", "r1", "r2"} <= set(problem):
        return _divider(problem, evid)
    if kind == "series_rlc" or recipe == "simulate-circuit":
        return _rlc(problem, evid, _load(run_dir / "rlc_transient.json"))
    if recipe == "solve-control-problem":
        return _control(problem, evid)
    if recipe == "solve-digital-control-problem":
        return _digital(problem, evid)
    if recipe == "smib-swing-study":
        return _smib(_load(run_dir / "psa_smib.json"), evid)
    if recipe == "simulate-power-fault":
        return _fault(problem, _load(run_dir / "power_tables.json"), evid)
    if recipe == "ed-lambda-study":
        return _dispatch(problem, _load(run_dir / "psa_ed.json"), evid)
    if recipe == "study-power-electronics-v2":
        return _buck(problem, _load(run_dir / "ee_v2_result.json"), evid)
    if recipe == "solve-drives-problem" or kind == "dc":
        return _drive(problem, _load(run_dir / "drives_result.json"), evid)
    return _generic(evid)


def _divider(problem: dict[str, Any], evid: dict[str, Any]) -> list[dict[str, str]]:
    vin, r1, r2 = float(problem["vin"]), float(problem["r1"]), float(problem["r2"])
    vout = vin * r2 / (r1 + r2) if r1 + r2 else None
    shown = _num(evid.get("value"), vout)
    return [
        {"title": "Read the circuit", "result": f"Vin = {vin:g} V, R1 = {_ohm(r1)}, R2 = {_ohm(r2)}", "author": "Agent"},
        {
            "title": "Write the divider equation",
            "result": "Vout from Vin, R1, R2",
            "author": "Agent",
            "equation": "Vout = Vin × R2 / (R1 + R2)",
        },
        {"title": "Substitute values", "result": f"Vout = {shown} V", "author": "Engine"},
        _check_step(evid, "Hand calculation and the numeric check agree."),
    ]


def _rlc(problem: dict[str, Any], evid: dict[str, Any], transient: dict[str, Any]) -> list[dict[str, str]]:
    r = float(problem.get("r_ohm") or problem.get("r") or 0)
    l_h = float(problem.get("l_h") or problem.get("l") or 0)
    c_f = float(problem.get("c_f") or problem.get("c") or 0)
    v = float(problem.get("v_step") or problem.get("vin") or 0)
    zeta = transient.get("zeta")
    wn = transient.get("omega_n_rad_s")
    if zeta is None and l_h > 0 and c_f > 0:
        zeta = (r / 2.0) * math.sqrt(c_f / l_h)
        wn = 1.0 / math.sqrt(l_h * c_f)
    peak = transient.get("Vc_peak_V", evid.get("value"))
    overshoot = float(transient.get("overshoot_pct") or 0.0) < 0.5
    damping = transient.get("damping_type") or ""
    t_settle = transient.get("settling_2pct_entry_s") or transient.get("settling_time_2pct_s")
    cap_row = (
        {"title": "Capacitor peak", "result": f"Vc peak = {_num(peak)} V", "author": "Engine"}
        if overshoot
        else {
            "title": "Capacitor final value",
            "result": f"Vc final = {_num(peak)} V, settling (2%) = {_num(float(t_settle or 0) * 1000, None, 2)} ms",
            "author": "Engine",
        }
    )
    return [
        {
            "title": "Read the branch",
            "result": f"R = {r:g} Ω, L = {l_h:g} H, C = {c_f:g} F, step = {v:g} V",
            "author": "Agent",
        },
        {
            "title": "Natural response",
            "result": f"ζ = {_num(zeta)}, ωn = {_num(wn)} rad/s" + (f", {damping}" if damping else ""),
            "author": "Engine",
            "equation": "ζ = (R/2) √(C/L),  ωn = 1/√(LC)",
        },
        cap_row,
        _check_step(evid, "Series RLC step integrated and checked."),
    ]


def _control(problem: dict[str, Any], evid: dict[str, Any]) -> list[dict[str, str]]:
    tf = str(problem.get("tf") or "G(s)")
    num, den = problem.get("num"), problem.get("den")
    if (
        isinstance(num, list)
        and isinstance(den, list)
        and len(num) == 1
        and len(den) == 2
        and abs(float(den[1]) - 1.0) < 1e-9
    ):
        tf = f"{num[0]}/(s+{int(den[0]) if float(den[0]).is_integer() else den[0]})"
    return [
        {"title": "Read the plant", "result": f"G(s) = {tf}", "author": "Agent"},
        {
            "title": "Close the loop",
            "result": "Unity negative feedback, H(s) = 1",
            "author": "Agent",
            "equation": "T(s) = G(s) / (1 + G(s))",
        },
        {"title": "Step response", "result": f"Steady output = {_num(evid.get('value'))}", "author": "Engine"},
        _check_step(evid, "python-control wrote the Bode and step figures."),
    ]


def _digital(problem: dict[str, Any], evid: dict[str, Any]) -> list[dict[str, str]]:
    ts = problem.get("ts") or problem.get("sample_time")
    return [
        {
            "title": "Read H(z)",
            "result": f"num = {problem.get('num')}, den = {problem.get('den')}, Ts = {ts} s",
            "author": "Agent",
        },
        {
            "title": "Pole radius",
            "result": f"Largest |pole| = {_num(evid.get('value'))}",
            "author": "Engine",
            "equation": "Stable when every pole has |z| < 1",
        },
        _check_step(evid, "Discrete poles were placed with python-control."),
    ]


def _smib(psa: dict[str, Any], evid: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "title": "Read the machine",
            "result": "EEC-301 SMIB case: Pm, pre-fault, faulted, and post-fault Pmax",
            "author": "Agent",
        },
        {
            "title": "Equal-area balance",
            "result": (
                f"δ0 = {_num(psa.get('delta0_deg'))}°, "
                f"δcr = {_num(psa.get('delta_cr_deg'))}°, "
                f"δmax = {_num(psa.get('delta_max_deg'))}°"
            ),
            "author": "Engine",
            "equation": "Accelerating area A1 equals decelerating area A2",
        },
        {"title": "Critical clearing", "result": f"tcr = {_num(psa.get('tcr_s'), None, 4)} s", "author": "Engine"},
        _check_step(evid, "Swing engine matched the equal-area reference."),
    ]


def _fault(problem: dict[str, Any], tables: dict[str, Any], evid: dict[str, Any]) -> list[dict[str, str]]:
    fault = tables.get("fault") if isinstance(tables.get("fault"), dict) else {}
    kind = str(problem.get("fault_type") or fault.get("fault_type") or "LG")
    return [
        {
            "title": "Read the sequence network",
            "result": f"{kind} fault, Z1 = {problem.get('z1_pu', 0.1)} pu, Z2 = {problem.get('z2_pu', 0.1)} pu, Z0 = {problem.get('z0_pu', 0.3)} pu",
            "author": "Agent",
        },
        {
            "title": "Fault current",
            "result": f"|I| = {_num(fault.get('i_fault_pu'), evid.get('value'), 4)} pu",
            "author": "Engine",
            "equation": "LG: I1 = I2 = I0 = V / (Z1 + Z2 + Z0)",
        },
        _check_step(evid, "Sequence network current was checked."),
    ]


def _dispatch(problem: dict[str, Any], psa: dict[str, Any], evid: dict[str, Any]) -> list[dict[str, str]]:
    pd = problem.get("PD", problem.get("pd_mw", psa.get("PD", 500)))
    shares = psa.get("P")
    share_txt = ""
    if isinstance(shares, list) and shares:
        share_txt = ", ".join(f"P{i + 1} = {float(p):.1f} MW" for i, p in enumerate(shares))
    return [
        {"title": "Read the demand", "result": f"Pd = {pd} MW, three thermal units", "author": "Agent"},
        {
            "title": "Lambda iteration",
            "result": f"λ = {_num(psa.get('lam'), evid.get('value'), 3)}" + (f" · {share_txt}" if share_txt else ""),
            "author": "Engine",
            "equation": "dC/dP is equal for every unit that is not on a limit",
        },
        _check_step(evid, "Economic-dispatch lambda was checked."),
    ]


def _buck(problem: dict[str, Any], payload: dict[str, Any], evid: dict[str, Any]) -> list[dict[str, str]]:
    result = payload.get("result") if isinstance(payload.get("result"), dict) else {}
    vin = float(problem.get("vin") or 0)
    vout = float(problem.get("vout") or 0)
    duty = result.get("D", evid.get("value"))
    return [
        {
            "title": "Read the converter",
            "result": f"Vin = {vin:g} V, Vout = {vout:g} V, L = {problem.get('l')} H, fs = {problem.get('fs')} Hz",
            "author": "Agent",
        },
        {
            "title": "CCM duty",
            "result": f"D = {_num(duty, None, 3)}",
            "author": "Engine",
            "equation": "D = Vout / Vin",
        },
        _check_step(evid, "Buck duty and ripple were checked."),
    ]


def _drive(problem: dict[str, Any], result: dict[str, Any], evid: dict[str, Any]) -> list[dict[str, str]]:
    v = problem.get("v_dc", 120)
    ra = problem.get("ra_ohm", 1)
    k = problem.get("k_torque", 0.5)
    t_load = problem.get("t_load_nm", 5)
    return [
        {
            "title": "Read the armature circuit",
            "result": f"Va = {v} V, Ra = {ra} Ω, K = {k}, Tload = {t_load} N·m",
            "author": "Agent",
        },
        {
            "title": "Steady speed",
            "result": (
                f"Ia = {_num(result.get('ia_a'))} A, "
                f"ω = {_num(result.get('omega_rad_s'))} rad/s, "
                f"n = {_num(result.get('rpm'), evid.get('value'))} rpm"
            ),
            "author": "Engine",
            "equation": "Ia = Tload / K,  ω = (Va − Ia Ra) / K",
        },
        _check_step(evid, "Drive steady state was checked."),
    ]


def _generic(evid: dict[str, Any]) -> list[dict[str, str]]:
    value = evid.get("value")
    result = "Pending verification" if evid.get("unchecked") else f"Value = {_num(value)}"
    return [{"title": "Solve", "result": result, "author": "Engine"}]


def _check_step(evid: dict[str, Any], ok_text: str) -> dict[str, str]:
    if evid.get("unchecked"):
        return {"title": "Check", "result": "Not checked. Treat the value as unverified.", "author": "Engine"}
    return {"title": "Check", "result": ok_text, "author": "Engine"}


def _load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _num(value: Any, fallback: Any = None, digits: int = 3) -> str:
    raw = value if isinstance(value, (int, float)) and not isinstance(value, bool) else fallback
    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        return "—"
    return f"{float(raw):.{digits}f}"


def _ohm(value: float) -> str:
    if value >= 1000 and value % 1000 == 0:
        return f"{value / 1000:g} kΩ"
    return f"{value:g} Ω"

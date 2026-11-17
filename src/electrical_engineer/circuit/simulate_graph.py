"""Run ngspice (or hand oracle) on a compiled circuit graph."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.circuit.graph import parse_graph, probe_for_capacitor
from electrical_engineer.circuit.netlist import CompileError, compile_netlist
from electrical_engineer.engines.spice_runner import run_spice_netlist, simulator_status


def simulate_graph(
    graph: dict[str, Any],
    problem: dict[str, Any],
    *,
    run_dir: Path,
) -> dict[str, Any]:
    run_dir.mkdir(parents=True, exist_ok=True)
    prob = {k: v for k, v in problem.items() if k != "cir"}
    parsed = parse_graph(graph)
    step_src = str(prob.get("analysis") or "").lower() == "tran"
    try:
        base_cir = compile_netlist(parsed, step_sources=step_src)
    except CompileError as exc:
        return {"ok": False, "error": str(exc), "unchecked": True, "engine": "circuit_graph_sim"}
    analysis = str(problem.get("analysis") or "dc").lower()
    probe = str(
        problem.get("probe")
        or problem.get("probe_expr")
        or probe_for_capacitor(parsed)
        or "v(2)"
    )
    prob.update(
        {
            "analysis": analysis,
            "probe": probe,
            "f_hz": prob.get("f_hz"),
            "t_s": prob.get("t_s") or prob.get("t_stop"),
            "t_stop": prob.get("t_stop"),
            "v_step": prob.get("v_step") or prob.get("vin"),
            "kind": prob.get("kind"),
            "derive_metric": prob.get("derive_metric")
            or ("Vc_peak" if str(prob.get("kind") or "") == "series_rlc" else None),
        }
    )
    sim_status = simulator_status()
    out: dict[str, Any] = {"simulator": sim_status, "engine": "circuit_graph_sim"}
    if not sim_status.get("available"):
        out.update({"ok": False, "skipped": True, "reason": sim_status.get("reason"), "unchecked": True})
        (run_dir / "lab_simulate.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
        return out
    sim_out = run_spice_netlist(base_cir, run_dir, prob)
    out.update(sim_out)
    out["cir"] = base_cir
    if sim_out.get("ok") and sim_out.get("value") is not None:
        out["simulated"] = float(sim_out["value"])
        out["unit"] = sim_out.get("unit") or problem.get("unit") or "V"
    if sim_out.get("t_peak_s") is not None:
        out["t_peak_s"] = float(sim_out["t_peak_s"])
    if sim_out.get("settling_2pct_entry_s") is not None:
        out["settling_2pct_entry_s"] = float(sim_out["settling_2pct_entry_s"])
    if sim_out.get("trace"):
        out["trace"] = {**sim_out["trace"], **_series_rlc_constants(graph)}
    (run_dir / "lab_simulate.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


def _series_rlc_constants(graph: dict[str, Any]) -> dict[str, float]:
    """zeta and omega_n from the drawn R, L, C values (circuit constants, not simulated)."""
    import math

    from electrical_engineer.circuit.graph import series_rlc_params_from_graph

    try:
        params = series_rlc_params_from_graph(graph)
    except Exception:  # noqa: BLE001 - non-RLC graphs simply carry no constants
        return {}
    if not params:
        return {}
    r, l, c = params["r_ohm"], params["l_h"], params["c_f"]
    if l <= 0 or c <= 0:
        return {}
    return {"zeta": r / 2.0 * math.sqrt(c / l), "omega_n_rad_s": 1.0 / math.sqrt(l * c)}


def compare_derived(
    derived: float,
    simulated: float | None,
    *,
    rel_tol: float = 1e-3,
    abs_tol: float = 1e-9,
    tol: float | None = None,
) -> dict[str, Any]:
    if simulated is None:
        return {"match": False, "mismatch": True, "reason": "no_simulation"}
    denom = max(abs(derived), abs_tol)
    if tol is not None and 0 < float(tol) < 1:
        rel = float(tol)
        margin = max(abs_tol, rel * denom)
    else:
        rel = float(rel_tol)
        margin = max(abs_tol, rel * denom)
    delta = abs(simulated - derived)
    match = delta <= margin
    rel_err_pct = 100.0 * delta / denom
    return {
        "match": match,
        "mismatch": not match,
        "derived": derived,
        "simulated": simulated,
        "delta": delta,
        "tol": margin,
        "rel_err_pct": rel_err_pct,
        "rel_tol_pct": 100.0 * rel,
    }
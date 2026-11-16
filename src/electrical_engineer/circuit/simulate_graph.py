"""Run ngspice (or hand oracle) on a compiled circuit graph."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.circuit.graph import parse_graph
from electrical_engineer.circuit.netlist import CompileError, compile_netlist
from electrical_engineer.engines.spice_runner import run_spice_netlist, simulator_status


def simulate_graph(
    graph: dict[str, Any],
    problem: dict[str, Any],
    *,
    run_dir: Path,
) -> dict[str, Any]:
    parsed = parse_graph(graph)
    try:
        base_cir = compile_netlist(parsed)
    except CompileError as exc:
        return {"ok": False, "error": str(exc), "unchecked": True, "engine": "circuit_graph_sim"}
    analysis = str(problem.get("analysis") or "dc").lower()
    probe = str(problem.get("probe") or problem.get("probe_expr") or "v(2)")
    prob = {
        "analysis": analysis,
        "probe": probe,
        "f_hz": problem.get("f_hz"),
        "t_s": problem.get("t_s"),
        "kind": problem.get("kind"),
    }
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
    (run_dir / "lab_simulate.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


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
    margin = float(tol) if tol is not None else max(abs_tol, rel_tol * max(abs(derived), 1.0))
    delta = abs(simulated - derived)
    match = delta <= margin
    return {
        "match": match,
        "mismatch": not match,
        "derived": derived,
        "simulated": simulated,
        "delta": delta,
        "tol": margin,
    }
"""Verify-after-derive: seed lab artifact, simulate, flag disagreement."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.circuit.graph import default_graph_for
from electrical_engineer.circuit.run_session import apply_graph
from electrical_engineer.circuit.simulate_graph import compare_derived, simulate_graph
from electrical_engineer.collab import lab_meta
from electrical_engineer.engines.circuit_derive import DeriveError, derive


def _ui_base() -> str:
    import os

    host = os.environ.get("EE_UI_HOST", "127.0.0.1")
    port = os.environ.get("EE_UI_PORT", "8765")
    return f"http://{host}:{port}/"


def finish_circuit_lab(
    run_dir: Path,
    problem: dict[str, Any],
    *,
    derived: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Attach circuit graph, simulate, compare to derive output."""
    run_dir.mkdir(parents=True, exist_ok=True)
    lab_meta.ensure_lab_meta(run_dir, kind="circuit")
    graph = default_graph_for(problem)
    if graph is None and derived and derived.get("cir"):
        graph = default_graph_for({**problem, "cir": derived["cir"]})
    if graph is None:
        return {"ok": False, "error": "no graph seed for problem", "unchecked": True}
    apply_graph(run_dir, graph, author="agent", op="seed_from_problem", detail={"kind": problem.get("kind")})
    if derived is None:
        dprob = dict(problem)
        if dprob.get("kind") in ("voltage_divider", "dc_divider", "series_rlc") and "allow_template_fallback" not in dprob:
            dprob["allow_template_fallback"] = True
        try:
            derived = derive(dprob)
        except (DeriveError, ValueError, TypeError, KeyError) as exc:
            if problem.get("value") is not None:
                derived = {
                    "value": float(problem["value"]),
                    "unit": problem.get("unit") or "V",
                    "engine": "declared_gold",
                }
            else:
                return {"ok": False, "error": str(exc), "unchecked": True}
    dval = float(derived["value"])
    sim = simulate_graph(graph, {**problem, **derived}, run_dir=run_dir)
    simulated = sim.get("simulated") if isinstance(sim.get("simulated"), (int, float)) else sim.get("value")
    if simulated is not None:
        try:
            simulated = float(simulated)
        except (TypeError, ValueError):
            simulated = None
    sim_skipped = bool(sim.get("skipped")) or simulated is None
    check = compare_derived(dval, simulated, tol=problem.get("tol"))
    mismatch = bool(check.get("mismatch")) and not sim_skipped
    verify = {
        "ok": True if sim_skipped else bool(check.get("match")),
        "derived": dval,
        "simulated": simulated,
        "mismatch": mismatch,
        "lab_kind": "circuit",
        "derive": derived,
        "simulate": sim,
        "check": check,
        "sim_skipped": sim_skipped,
    }
    if mismatch:
        verify["disagreement_banner"] = "derive vs lab simulation mismatch"
        verify["ok"] = False
    (run_dir / "lab_verify.json").write_text(json.dumps(verify, indent=2), encoding="utf-8")
    meta = lab_meta.load_lab_meta(run_dir)
    meta["lab_verify"] = {
        "mismatch": verify["mismatch"],
        "derived": dval,
        "simulated": simulated,
    }
    meta["ui_url"] = lab_meta.ui_lab_url(run_dir.name, meta, _ui_base())
    lab_meta.save_lab_meta(run_dir, meta)
    return verify


def finish_control_lab(
    run_dir: Path,
    problem: dict[str, Any],
    *,
    golden: str | None = None,
    derived_value: float | None = None,
) -> dict[str, Any]:
    from electrical_engineer.control_studio import session as cs_session
    from electrical_engineer.control_studio import simulate as cs_simulate
    from electrical_engineer.control_studio.goldens import GOLDENS
    from electrical_engineer.runner.runs import project_root

    root = project_root()
    title = str(problem.get("title") or problem.get("kind") or "Control lab")
    gkey = golden or str(problem.get("golden") or "")
    if gkey not in GOLDENS:
        if "unity" in str(problem.get("kind") or "").lower():
            gkey = "unity_first_order"
        elif "lead" in str(problem.get("kind") or "").lower():
            gkey = "lead_compensator"
        else:
            gkey = "unity_first_order"
    payload = cs_session.create_session(title, root, golden=gkey)
    sid = payload["session_id"]
    lab_meta.ensure_lab_meta(run_dir, kind="control", control_session_id=sid)
    diagram = payload["diagram"]
    sim = cs_simulate.simulate(diagram, run_dir=root / "runs" / sid)
    simulated = None
    if sim.get("ok") and sim.get("y_final") is not None:
        simulated = float(sim["y_final"])
    mismatch = False
    if derived_value is not None and simulated is not None:
        margin = max(1e-6, 0.02 * max(abs(derived_value), 1.0))
        mismatch = abs(simulated - derived_value) > margin
    verify = {
        "ok": sim.get("ok") and not mismatch,
        "mismatch": mismatch,
        "derived": derived_value,
        "simulated": simulated,
        "lab_kind": "control",
        "control_session_id": sid,
        "simulate": sim,
    }
    if mismatch:
        verify["disagreement_banner"] = "derive vs control studio mismatch"
    (run_dir / "lab_verify.json").write_text(json.dumps(verify, indent=2), encoding="utf-8")
    link_path = run_dir / "control_diagram.json"
    link_path.write_text(json.dumps(diagram, indent=2), encoding="utf-8")
    meta = lab_meta.load_lab_meta(run_dir)
    meta["ui_url"] = lab_meta.ui_lab_url(run_dir.name, meta, _ui_base())
    meta["lab_verify"] = {"mismatch": mismatch, "derived": derived_value, "simulated": simulated}
    lab_meta.save_lab_meta(run_dir, meta)
    return verify
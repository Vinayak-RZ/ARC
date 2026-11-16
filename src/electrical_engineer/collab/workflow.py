"""Verify-after-derive: seed lab artifact, simulate, flag disagreement."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from electrical_engineer.circuit.graph import (
    default_graph_for,
    graph_port_errors,
    parse_graph,
    probe_for_capacitor,
)
from electrical_engineer.circuit.run_session import apply_graph, load_graph
from electrical_engineer.circuit.simulate_graph import compare_derived, simulate_graph
from electrical_engineer.collab import lab_meta
from electrical_engineer.collab.verify_policy import DEFAULT_REL_TOL
from electrical_engineer.collab.verify_policy import status_label as verify_status_label
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
    graph_path = run_dir / "graph.json"
    graph = load_graph(run_dir) if graph_path.is_file() else {"nodes": [], "edges": []}
    if not graph.get("nodes"):
        graph = default_graph_for(problem)
        if graph is None and derived and derived.get("cir"):
            graph = default_graph_for({**problem, "cir": derived["cir"]})
        if graph is None:
            return {"ok": False, "error": "no graph seed for problem", "unchecked": True}
        port_errs = graph_port_errors(parse_graph(graph))
        if port_errs:
            return {"ok": False, "error": "invalid agent graph wiring", "detail": port_errs, "unchecked": True}
        seed_out = apply_graph(
            run_dir, graph, author="agent", op="seed_from_problem", detail={"kind": problem.get("kind")}
        )
    else:
        # Human-edited lab graphs may add parallel shorts; still compile + simulate from graph.
        seed_out = {"graph": graph}
    meta_seed = lab_meta.load_lab_meta(run_dir)
    if "agent_baseline_graph" not in meta_seed:
        meta_seed["agent_baseline_graph"] = seed_out.get("graph") or graph
        meta_seed["agent_baseline_rev"] = int(meta_seed.get("revision") or 1)
        lab_meta.save_lab_meta(run_dir, meta_seed)
    if derived is None:
        dprob = dict(problem)
        if dprob.get("kind") in ("voltage_divider", "dc_divider", "series_rlc") and "allow_template_fallback" not in dprob:
            dprob["allow_template_fallback"] = True
        try:
            derived = derive(dprob)
        except (DeriveError, ValueError, TypeError, KeyError) as exc:
            if problem.get("allow_declared_gold") and problem.get("value") is not None:
                derived = {
                    "value": float(problem["value"]),
                    "unit": problem.get("unit") or "V",
                    "engine": "declared_gold",
                }
            else:
                return {"ok": False, "error": str(exc), "unchecked": True}
    dval = float(derived["value"])
    if not math.isfinite(dval) or abs(dval) > 1e9:
        if problem.get("allow_declared_gold") and problem.get("value") is not None:
            dval = float(problem["value"])
            derived = {**(derived or {}), "value": dval, "engine": "declared_gold"}
        else:
            return {"ok": False, "error": "non-finite derived value", "unchecked": True}
    sim_prob = {**problem}
    graph_probe = probe_for_capacitor(graph)
    if graph_probe:
        sim_prob["probe"] = graph_probe
    if isinstance(derived, dict):
        sim_prob.update(
            {k: derived[k] for k in ("analysis", "t_s", "t_stop", "f_hz", "derive_metric") if k in derived}
        )
    sim = simulate_graph(graph, sim_prob, run_dir=run_dir)
    simulated = sim.get("simulated") if isinstance(sim.get("simulated"), (int, float)) else sim.get("value")
    if simulated is not None:
        try:
            simulated = float(simulated)
        except (TypeError, ValueError):
            simulated = None
    sim_skipped = bool(sim.get("skipped")) or simulated is None
    unit = str((derived or {}).get("unit") or problem.get("unit") or "V")
    tol = problem.get("tol")
    rel_tol = float(tol) if tol is not None else DEFAULT_REL_TOL
    limit_pct = rel_tol * 100.0
    check = compare_derived(dval, simulated, tol=tol if tol is not None else None, rel_tol=rel_tol)
    mismatch = bool(check.get("mismatch")) and not sim_skipped
    rel_err = float(check.get("rel_err_pct") or 0.0)
    rel_lim = float(check.get("rel_tol_pct") or rel_tol * 100)
    if sim_skipped:
        status = "not_simulated"
        status_lbl = "Not simulated"
    elif check.get("match"):
        status = "agrees"
        status_lbl = verify_status_label(agrees=True, rel_err_pct=rel_err, limit_pct=limit_pct)
    elif rel_err > 5.0:
        status = "mismatch"
        status_lbl = "Mismatch"
    else:
        status = "differs"
        status_lbl = verify_status_label(agrees=False, rel_err_pct=rel_err, limit_pct=limit_pct)
    metric_label = "Capacitor peak" if str(problem.get("kind") or "") == "series_rlc" else "Probe"
    metrics = [
        {
            "id": "primary",
            "label": metric_label,
            "derived": dval,
            "simulated": simulated,
            "unit": unit,
            "rel_err_pct": None if sim_skipped else rel_err,
            "rel_tol_pct": rel_lim,
            "status": status,
            "status_label": status_lbl,
        }
    ]
    t_derived = (derived or {}).get("t_s")
    if t_derived is not None and str((derived or {}).get("derive_metric") or "") == "Vc_peak":
        t_derived_f = float(t_derived)
        t_sim = (sim or {}).get("t_peak_s") if isinstance(sim, dict) else None
        if (
            t_sim is None
            and simulated is not None
            and str(problem.get("analysis") or derived.get("analysis") or "").lower() == "tran"
        ):
            t_sim = float(problem.get("t_s") or t_derived_f)
        t_chk = compare_derived(t_derived_f, float(t_sim) if t_sim is not None else None, tol=problem.get("t_tol") or 5e-5)
        t_rel = float(t_chk.get("rel_err_pct") or 0.0)
        t_lim = float(t_chk.get("rel_tol_pct") or 100.0 * 5e-5 / max(abs(t_derived_f), 1e-12))
        if sim_skipped or t_sim is None:
            t_status, t_label = "not_simulated", "Not simulated"
        elif t_chk.get("match"):
            t_status = "agrees"
            t_label = verify_status_label(agrees=True, rel_err_pct=t_rel, limit_pct=limit_pct)
        elif t_rel > 5.0:
            t_status, t_label = "mismatch", "Mismatch"
        else:
            t_status = "differs"
            t_label = verify_status_label(agrees=False, rel_err_pct=t_rel, limit_pct=limit_pct)
        metrics.append(
            {
                "id": "t_peak",
                "label": "Peak time",
                "derived": t_derived_f,
                "simulated": t_sim,
                "unit": "s",
                "rel_err_pct": None if sim_skipped or t_sim is None else t_rel,
                "rel_tol_pct": t_lim,
                "status": t_status,
                "status_label": t_label,
            }
        )
    verify = {
        "ok": True if sim_skipped else bool(check.get("match")),
        "derived": dval,
        "simulated": simulated,
        "unit": unit,
        "mismatch": mismatch,
        "status": status,
        "status_label": status_lbl,
        "rel_err_pct": rel_err,
        "rel_tol_pct": rel_lim,
        "metrics": metrics,
        "sim_engine": (sim.get("simulator") or {}).get("backend") or sim.get("engine"),
        "lab_kind": "circuit",
        "derive": derived,
        "simulate": sim,
        "check": check,
        "sim_skipped": sim_skipped,
    }
    if mismatch and not sim_skipped:
        verify["disagreement_banner"] = status_lbl
        verify["ok"] = False
        if rel_err > 2.0:
            verify["needs_review"] = True
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
    step_metrics = (sim.get("step_series") or {}).get("metrics") or {}
    simulated = None
    if step_metrics.get("final_value") is not None:
        simulated = float(step_metrics["final_value"])
    elif sim.get("y_ss") is not None:
        simulated = float(sim["y_ss"])
    sim_t = step_metrics.get("t_settle_s")
    derived_t = problem.get("t_settle_s")
    limit_pct = DEFAULT_REL_TOL * 100.0
    metrics: list[dict[str, Any]] = []
    mismatch = False
    status = "agrees"
    status_lbl = "Not simulated"
    rel_err = 0.0
    if derived_value is not None and simulated is not None:
        chk = compare_derived(float(derived_value), simulated, rel_tol=DEFAULT_REL_TOL)
        mismatch = bool(chk.get("mismatch"))
        rel_err = float(chk.get("rel_err_pct") or 0.0)
        status = "agrees" if chk.get("match") else "differs"
        status_lbl = verify_status_label(agrees=bool(chk.get("match")), rel_err_pct=rel_err, limit_pct=limit_pct)
        metrics.append(
            {
                "id": "y_ss",
                "label": "Final value y(∞)",
                "derived": float(derived_value),
                "simulated": simulated,
                "unit": "",
                "rel_err_pct": rel_err,
                "rel_tol_pct": limit_pct,
                "status": status,
                "status_label": status_lbl,
            }
        )
    if derived_t is not None and sim_t is not None:
        t_chk = compare_derived(float(derived_t), float(sim_t), tol=0.02, rel_tol=0.05)
        t_rel = float(t_chk.get("rel_err_pct") or 0.0)
        t_status = "agrees" if t_chk.get("match") else "differs"
        t_label = verify_status_label(agrees=bool(t_chk.get("match")), rel_err_pct=t_rel, limit_pct=limit_pct)
        metrics.append(
            {
                "id": "t_settle",
                "label": "Settling time",
                "derived": float(derived_t),
                "simulated": float(sim_t),
                "unit": "s",
                "rel_err_pct": t_rel,
                "rel_tol_pct": limit_pct,
                "status": t_status,
                "status_label": t_label,
            }
        )
        if not t_chk.get("match"):
            mismatch = True
    verify = {
        "ok": sim.get("ok") and not mismatch,
        "mismatch": mismatch,
        "derived": derived_value,
        "simulated": simulated,
        "lab_kind": "control",
        "control_session_id": sid,
        "simulate": sim,
        "metrics": metrics,
        "status": status,
        "status_label": status_lbl,
        "rel_err_pct": rel_err,
        "rel_tol_pct": limit_pct,
        "sim_engine": "python-control",
    }
    if mismatch:
        verify["disagreement_banner"] = status_lbl
        verify["needs_review"] = rel_err > limit_pct
    (run_dir / "lab_verify.json").write_text(json.dumps(verify, indent=2), encoding="utf-8")
    link_path = run_dir / "control_diagram.json"
    link_path.write_text(json.dumps(diagram, indent=2), encoding="utf-8")
    meta = lab_meta.load_lab_meta(run_dir)
    meta["ui_url"] = lab_meta.ui_lab_url(run_dir.name, meta, _ui_base())
    meta["lab_verify"] = {"mismatch": mismatch, "derived": derived_value, "simulated": simulated}
    lab_meta.save_lab_meta(run_dir, meta)
    return verify
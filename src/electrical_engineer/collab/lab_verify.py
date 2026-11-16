"""Lab verify freshness: revision stamping, stale detection, human-edit re-sim."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def graph_resistor_values(graph: dict[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    for node in graph.get("nodes") or []:
        if str(node.get("type") or "").lower() != "resistor":
            continue
        ref = str(node.get("refdes") or node.get("id") or "").upper()
        if node.get("value") is None:
            continue
        try:
            out[ref or str(node.get("id"))] = float(node["value"])
        except (TypeError, ValueError):
            continue
    return out


def human_edit_notes(
    baseline_graph: dict[str, Any] | None,
    current_graph: dict[str, Any],
) -> list[str]:
    if not baseline_graph:
        return []
    base = graph_resistor_values(baseline_graph)
    cur = graph_resistor_values(current_graph)
    notes: list[str] = []
    for key in sorted(set(base) | set(cur)):
        if key not in base or key not in cur:
            continue
        b, c = base[key], cur[key]
        if abs(b - c) <= 1e-9 * max(abs(b), abs(c), 1.0):
            continue
        notes.append(f"Your edit changed {key} from {b:g} to {c:g} Ω")
    return notes


def attach_verify_freshness(verify: dict[str, Any] | None, meta: dict[str, Any]) -> dict[str, Any] | None:
    if not verify:
        return verify
    rev = int(meta.get("revision") or 0)
    vrev = int(verify.get("graph_revision") or verify.get("computed_at_revision") or 0)
    out = dict(verify)
    if vrev <= 0:
        out.setdefault("stale", True)
        out["status"] = "out_of_date"
        out["status_label"] = "Out of date — re-simulate the lab"
        return out
    if rev > vrev:
        out["stale"] = True
        out["graph_revision"] = vrev
        out["current_graph_revision"] = rev
        if out.get("status") == "agrees" and not out.get("mismatch"):
            out["status"] = "out_of_date"
            out["status_label"] = "Out of date — lab changed since this check"
        out.setdefault(
            "stale_reason",
            "The circuit no longer matches the graph this verification used.",
        )
    else:
        out["stale"] = False
    return out


def mark_circuit_verify_stale(run_dir: Path) -> None:
    """Bump revision without a new sim — GET /lab will report stale until re-verify."""
    path = run_dir / "lab_verify.json"
    if not path.is_file():
        return
    verify = _read_json(path)
    from electrical_engineer.collab import lab_meta

    meta = lab_meta.load_lab_meta(run_dir)
    verify = attach_verify_freshness(verify, meta) or verify
    verify["stale"] = True
    verify["status"] = "out_of_date"
    verify["status_label"] = "Out of date — re-simulate to refresh"
    notes = human_edit_notes(meta.get("agent_baseline_graph"), _read_json(run_dir / "graph.json"))
    if notes:
        verify["human_edit_notes"] = notes
        verify["stale_reason"] = (
            f"{notes[0]}; the agent's derivation no longer applies to this circuit."
        )
        verify["needs_review"] = True
    path.write_text(json.dumps(verify, indent=2), encoding="utf-8")


def reverify_circuit_lab(run_dir: Path) -> dict[str, Any]:
    """Re-simulate current graph; keep agent derivation snapshot."""
    from electrical_engineer.circuit.run_session import load_graph
    from electrical_engineer.collab import lab_meta
    from electrical_engineer.collab.workflow import refresh_circuit_lab_verify

    meta = lab_meta.load_lab_meta(run_dir)
    problem = _read_json(run_dir / "problem.json")
    if not problem:
        raise ValueError("missing problem.json")
    derived = _read_json(run_dir / "circuit_derive.json")
    if not derived:
        old = _read_json(run_dir / "lab_verify.json")
        if isinstance(old.get("derive"), dict):
            derived = old["derive"]
    graph = load_graph(run_dir)
    verify = refresh_circuit_lab_verify(run_dir, problem, derived=derived or None, graph=graph)
    notes = human_edit_notes(meta.get("agent_baseline_graph"), graph)
    if notes:
        verify["human_edit_notes"] = notes
        if verify.get("mismatch") or verify.get("status") != "agrees":
            verify["stale_reason"] = (
                f"{notes[0]}; the agent's derivation no longer applies to this circuit."
            )
            verify["needs_review"] = True
    verify["graph_revision"] = int(meta.get("revision") or verify.get("graph_revision") or 0)
    verify["stale"] = False
    (run_dir / "lab_verify.json").write_text(json.dumps(verify, indent=2), encoding="utf-8")
    meta = lab_meta.load_lab_meta(run_dir)
    meta["lab_verify"] = {
        "mismatch": verify.get("mismatch"),
        "derived": verify.get("derived"),
        "simulated": verify.get("simulated"),
    }
    lab_meta.save_lab_meta(run_dir, meta)
    return verify
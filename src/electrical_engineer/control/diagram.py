"""UG control block diagrams for the localhost UI (read-only seed from problem.json)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA = "arc.control_diagram.v1"


def _block_node(bid: str, label: str, tf: str, x: float, y: float) -> dict[str, Any]:
    return {
        "id": bid,
        "type": "block",
        "label": label,
        "tf": tf,
        "x": x,
        "y": y,
    }


def control_diagram_from_problem(problem: dict[str, Any] | None) -> dict[str, Any] | None:
    problem = problem or {}
    blocks = problem.get("blocks") or []
    if not blocks:
        return None
    by_id = {str(b.get("id") or f"b{i}"): b for i, b in enumerate(blocks)}
    uf = problem.get("unity_feedback")
    if not isinstance(uf, dict):
        return None
    fwd_id = str(uf.get("forward") or blocks[0].get("id"))
    fb_id = str(uf.get("feedback") or "")
    fwd = by_id.get(fwd_id)
    if not fwd:
        return None
    fb = by_id.get(fb_id) if fb_id else None
    g_tf = str(fwd.get("tf") or fwd.get("transfer_function") or "1")
    h_tf = str((fb or {}).get("tf") or (fb or {}).get("transfer_function") or "1")
    negative = bool(uf.get("negative", True))
    nodes = [
        {"id": "sum", "type": "sum", "label": "Σ", "x": 72, "y": 140, "negative": negative},
        _block_node(fwd_id, str(fwd.get("id") or "G"), g_tf, 240, 140),
    ]
    if fb_id and fb:
        nodes.append(_block_node(fb_id, str(fb.get("id") or "H"), h_tf, 240, 260))
    edges = [
        {"id": "e_r", "from": "r", "fromPort": "out", "to": "sum", "toPort": "in"},
        {"id": "e_sum_g", "from": "sum", "fromPort": "out", "to": fwd_id, "toPort": "in"},
        {"id": "e_g_y", "from": fwd_id, "fromPort": "out", "to": "y", "toPort": "in"},
    ]
    if fb_id and fb:
        edges.extend(
            [
                {"id": "e_y_h", "from": "y", "fromPort": "out", "to": fb_id, "toPort": "in"},
                {"id": "e_h_sum", "from": fb_id, "fromPort": "out", "to": "sum", "toPort": "feedback"},
            ]
        )
    return {"schema": SCHEMA, "nodes": nodes, "edges": edges}


def control_diagram_for_recipe(recipe_id: str, problem: dict[str, Any] | None) -> dict[str, Any] | None:
    if recipe_id != "control-diagram-to-model":
        return None
    return control_diagram_from_problem(problem)


def write_control_diagram(run_dir: Path, diagram: dict[str, Any]) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "control_diagram.json").write_text(json.dumps(diagram, indent=2), encoding="utf-8")

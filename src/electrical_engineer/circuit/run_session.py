"""Revisioned circuit graph on a run (shared by UI and MCP)."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from electrical_engineer.circuit.graph import GraphError, parse_graph, write_graph
from electrical_engineer.collab import lab_meta as lab_meta_mod


def _append_op(meta: dict[str, Any], op: dict[str, Any], author: str) -> dict[str, Any]:
    next_rev = int(meta.get("revision") or 0) + 1
    actor_label = "You" if author == "human" else "Agent"
    entry = {
        "id": f"op-{len(meta.get('op_log') or []) + 1}",
        "rev": next_rev,
        "ts_ms": int(time.time() * 1000),
        "author": author if author in ("human", "agent") else "agent",
        "actor_label": actor_label,
        **op,
    }
    meta.setdefault("op_log", []).append(entry)
    meta["revision"] = next_rev
    meta["updated_at_ms"] = entry["ts_ms"]
    presence = meta.setdefault(
        "presence",
        {"last_author": author, "agent_editing": author == "agent", "highlight_until_ms": 0},
    )
    presence["last_author"] = author
    presence["agent_editing"] = author == "agent"
    presence["highlight_until_ms"] = int(time.time() * 1000) + (4000 if author == "agent" else 1500)
    return entry


def load_graph(run_dir: Path) -> dict[str, Any]:
    path = run_dir / "graph.json"
    if not path.is_file():
        return {"schema": "arc.circuit.v1", "nodes": [], "edges": []}
    try:
        return parse_graph(json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, GraphError):
        return {"schema": "arc.circuit.v1", "nodes": [], "edges": []}


def apply_graph(
    run_dir: Path,
    graph: dict[str, Any],
    *,
    author: str,
    op: str,
    target: str | None = None,
    detail: dict[str, Any] | None = None,
) -> dict[str, Any]:
    parsed = parse_graph(graph)
    write_out = write_graph(run_dir, parsed)
    meta = lab_meta_mod.ensure_lab_meta(run_dir, kind=lab_meta_mod.load_lab_meta(run_dir).get("kind") or "circuit")
    body: dict[str, Any] = {"op": op, "target": target}
    if detail:
        body["detail"] = detail
    entry = _append_op(meta, body, author)
    lab_meta_mod.save_lab_meta(run_dir, meta)
    try:
        from electrical_engineer.collab.run_events import publish

        publish(
            run_dir.name,
            {
                "type": "graph",
                "revision": meta["revision"],
                "presence": meta.get("presence"),
                "last_op": entry,
            },
        )
    except ImportError:
        pass
    return {
        "run_id": run_dir.name,
        "revision": meta["revision"],
        "graph": parsed,
        "last_op": entry,
        "presence": meta.get("presence"),
        "compiled": write_out.get("compiled"),
        "ok": write_out.get("ok"),
    }


def add_part(run_dir: Path, part: dict[str, Any], *, author: str = "agent") -> dict[str, Any]:
    graph = load_graph(run_dir)
    nid = str(part.get("id") or "")
    if not nid:
        raise GraphError("part needs id")
    if any(n["id"] == nid for n in graph["nodes"]):
        raise GraphError(f"duplicate node {nid}")
    graph["nodes"].append(
        {
            "id": nid,
            "type": str(part["type"]),
            "refdes": str(part.get("refdes") or nid),
            "value": part.get("value"),
            "unit": str(part.get("unit") or ""),
            "x": float(part.get("x") or 0),
            "y": float(part.get("y") or 0),
            "rot": int(part.get("rot") or 0),
        }
    )
    return apply_graph(run_dir, graph, author=author, op="add_part", target=nid)


def connect_ports(run_dir: Path, edge: dict[str, Any], *, author: str = "agent") -> dict[str, Any]:
    graph = load_graph(run_dir)
    eid = str(edge.get("id") or f"e{len(graph['edges']) + 1}")
    graph["edges"].append(
        {"id": eid, "from": str(edge["from"]), "to": str(edge["to"])}
    )
    return apply_graph(run_dir, graph, author=author, op="connect", target=eid)
"""Allowlisted circuit graph. Caps match compose (16/24)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ALLOWED_TYPES = frozenset({"resistor", "capacitor", "inductor", "source_v", "ground"})
MAX_NODES = 16
MAX_EDGES = 24
SCHEMA = "arc.circuit.v1"


class GraphError(ValueError):
    pass


def parse_graph(data: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise GraphError("graph must be an object")
    nodes = data.get("nodes") or []
    edges = data.get("edges") or []
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise GraphError("nodes and edges must be lists")
    if len(nodes) > MAX_NODES or len(edges) > MAX_EDGES:
        raise GraphError("16 parts or 24 wires is the cap for this lab.")
    out_nodes = []
    seen = set()
    for raw in nodes:
        if not isinstance(raw, dict):
            raise GraphError("node must be an object")
        nid = str(raw.get("id") or "")
        kind = str(raw.get("type") or "")
        if not nid or kind not in ALLOWED_TYPES:
            raise GraphError("node needs id and allowlisted type")
        if nid in seen:
            raise GraphError("duplicate node id")
        seen.add(nid)
        out_nodes.append(
            {
                "id": nid,
                "type": kind,
                "refdes": str(raw.get("refdes") or nid),
                "value": raw.get("value"),
                "unit": str(raw.get("unit") or ""),
                "x": float(raw.get("x") or 0),
                "y": float(raw.get("y") or 0),
            }
        )
    out_edges = []
    for raw in edges:
        if not isinstance(raw, dict):
            raise GraphError("edge must be an object")
        eid = str(raw.get("id") or "")
        frm = str(raw.get("from") or "")
        to = str(raw.get("to") or "")
        if not eid or "." not in frm or "." not in to:
            raise GraphError("edge needs id, from, to ports")
        out_edges.append({"id": eid, "from": frm, "to": to})
    return {"schema": SCHEMA, "nodes": out_nodes, "edges": out_edges}


def write_graph(run_dir: Path, data: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.circuit.netlist import CompileError, compile_netlist

    parsed = parse_graph(data)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "graph.json").write_text(json.dumps(parsed, indent=2), encoding="utf-8")
    try:
        cir = compile_netlist(parsed)
    except CompileError as exc:
        (run_dir / "compile.json").write_text(
            json.dumps({"ok": False, "error": str(exc)}), encoding="utf-8"
        )
        obs_path = run_dir / "observation.json"
        if obs_path.is_file():
            try:
                obs = json.loads(obs_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                obs = {}
            if isinstance(obs, dict):
                obs["unchecked_reason"] = "compile-error"
                obs["compile_error"] = str(exc)
                obs_path.write_text(json.dumps(obs, indent=2), encoding="utf-8")
        return {"ok": True, "compiled": False, "error": str(exc)}
    (run_dir / "netlist.cir").write_text(cir, encoding="utf-8")
    (run_dir / "compile.json").write_text(json.dumps({"ok": True}), encoding="utf-8")
    return {"ok": True, "compiled": True}

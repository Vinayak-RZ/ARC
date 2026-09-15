"""Allowlisted circuit graph. Caps match compose (16/24)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_CONTRACT = json.loads(Path(__file__).with_name("arc.circuit.v1.json").read_text(encoding="utf-8"))
SCHEMA = str(_CONTRACT["properties"]["schema"]["const"])
ALLOWED_TYPES = frozenset(_CONTRACT["$defs"]["partType"]["enum"])
ALLOWED_ROT = frozenset(_CONTRACT["$defs"]["rot"]["enum"])
MAX_NODES = int(_CONTRACT["properties"]["nodes"]["maxItems"])
MAX_EDGES = int(_CONTRACT["properties"]["edges"]["maxItems"])


def divider_graph(vin: float = 10, r1: float = 1000, r2: float = 1000) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "nodes": [
            {"id": "vin", "type": "source_v", "refdes": "Vin", "value": vin, "unit": "V", "x": 80, "y": 40},
            {"id": "r1", "type": "resistor", "refdes": "R1", "value": r1, "unit": "ohm", "x": 220, "y": 40},
            {"id": "r2", "type": "resistor", "refdes": "R2", "value": r2, "unit": "ohm", "x": 220, "y": 160},
            {"id": "gnd", "type": "ground", "refdes": "Gnd", "value": 0, "unit": "", "x": 80, "y": 160},
        ],
        "edges": [
            {"id": "e1", "from": "vin.n1", "to": "r1.n1"},
            {"id": "e2", "from": "r1.n2", "to": "r2.n1"},
            {"id": "e3", "from": "r2.n2", "to": "gnd.n1"},
            {"id": "e4", "from": "vin.n2", "to": "gnd.n1"},
        ],
    }


def default_graph_for(problem: dict[str, Any] | None) -> dict[str, Any] | None:
    problem = problem or {}
    if str(problem.get("kind") or "") != "voltage_divider":
        return None
    return divider_graph(
        vin=float(problem.get("vin") or 10),
        r1=float(problem.get("r1") or 1000),
        r2=float(problem.get("r2") or 1000),
    )


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
        rot_raw = raw.get("rot", 0)
        try:
            rot = int(rot_raw)
        except (TypeError, ValueError) as exc:
            raise GraphError("rot must be 0 or 90") from exc
        if rot not in ALLOWED_ROT:
            raise GraphError("rot must be 0 or 90")
        out_nodes.append(
            {
                "id": nid,
                "type": kind,
                "refdes": str(raw.get("refdes") or nid),
                "value": raw.get("value"),
                "unit": str(raw.get("unit") or ""),
                "x": float(raw.get("x") or 0),
                "y": float(raw.get("y") or 0),
                "rot": rot,
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

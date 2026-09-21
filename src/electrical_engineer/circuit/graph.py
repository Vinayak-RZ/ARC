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


def series_rlc_graph(
    vin: float = 10,
    r_ohm: float = 1000,
    l_h: float = 1e-3,
    c_f: float = 1e-6,
) -> dict[str, Any]:
    """Series R-L-C with DC source (schematic seed for simulate-circuit UI)."""
    return {
        "schema": SCHEMA,
        "nodes": [
            {"id": "vin", "type": "source_v", "refdes": "Vin", "value": vin, "unit": "V", "x": 60, "y": 120},
            {"id": "r1", "type": "resistor", "refdes": "R1", "value": r_ohm, "unit": "ohm", "x": 180, "y": 120},
            {"id": "l1", "type": "inductor", "refdes": "L1", "value": l_h, "unit": "H", "x": 300, "y": 120},
            {"id": "c1", "type": "capacitor", "refdes": "C1", "value": c_f, "unit": "F", "x": 420, "y": 120},
            {"id": "gnd", "type": "ground", "refdes": "Gnd", "value": 0, "unit": "", "x": 540, "y": 200},
        ],
        "edges": [
            {"id": "e1", "from": "vin.n1", "to": "r1.n1"},
            {"id": "e2", "from": "r1.n2", "to": "l1.n1"},
            {"id": "e3", "from": "l1.n2", "to": "c1.n1"},
            {"id": "e4", "from": "c1.n2", "to": "gnd.n1"},
            {"id": "e5", "from": "vin.n2", "to": "gnd.n1"},
        ],
    }


def divider_graph(vin: float = 10, r1: float = 1000, r2: float = 1000) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "nodes": [
            {"id": "vin", "type": "source_v", "refdes": "Vin", "value": vin, "unit": "V", "x": 80, "y": 40},
            {"id": "r1", "type": "resistor", "refdes": "R1", "value": r1, "unit": "ohm", "x": 220, "y": 40},
            {"id": "r2", "type": "resistor", "refdes": "R2", "value": r2, "unit": "ohm", "x": 220, "y": 160, "rot": 90},
            {"id": "gnd", "type": "ground", "refdes": "Gnd", "value": 0, "unit": "", "x": 80, "y": 160},
        ],
        "edges": [
            {"id": "e1", "from": "vin.n1", "to": "r1.n1"},
            {"id": "e2", "from": "r1.n2", "to": "r2.n1"},
            {"id": "e3", "from": "r2.n2", "to": "gnd.n1"},
            {"id": "e4", "from": "vin.n2", "to": "gnd.n1"},
        ],
    }


def _cir_has_series_rlc(cir: str) -> bool:
    import re

    text = cir.upper()
    return bool(re.search(r"\bL\d", text) and re.search(r"\bC\d", text))


def default_graph_for(problem: dict[str, Any] | None) -> dict[str, Any] | None:
    problem = problem or {}
    kind = str(problem.get("kind") or problem.get("graph_kind") or "")
    if kind == "voltage_divider":
        return divider_graph(
            vin=float(problem.get("vin") or 10),
            r1=float(problem.get("r1") or 1000),
            r2=float(problem.get("r2") or 1000),
        )
    if kind == "series_rlc":
        return series_rlc_graph(
            vin=float(problem.get("vin") or 10),
            r_ohm=float(problem.get("r") or problem.get("r_ohm") or 1000),
            l_h=float(problem.get("l") or problem.get("l_h") or 1e-3),
            c_f=float(problem.get("c") or problem.get("c_f") or 1e-6),
        )
    cir = str(problem.get("cir") or "")
    if cir and _cir_has_series_rlc(cir):
        return series_rlc_graph()
    return None


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

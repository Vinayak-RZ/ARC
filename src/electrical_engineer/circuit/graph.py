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
    """Series R-L-C: V+ → R → L → C → return rail → V−, GND on V−."""
    return {
        "schema": SCHEMA,
        "nodes": [
            {"id": "vin", "type": "source_v", "refdes": "V1", "value": vin, "unit": "V", "x": 56, "y": 104, "rot": 0},
            {"id": "r1", "type": "resistor", "refdes": "R1", "value": r_ohm, "unit": "ohm", "x": 176, "y": 56, "rot": 0},
            {"id": "l1", "type": "inductor", "refdes": "L1", "value": l_h, "unit": "H", "x": 296, "y": 56, "rot": 0},
            {"id": "c1", "type": "capacitor", "refdes": "C1", "value": c_f, "unit": "F", "x": 416, "y": 56, "rot": 0},
            {"id": "gnd", "type": "ground", "refdes": "GND", "value": 0, "unit": "", "x": 56, "y": 220, "rot": 0},
        ],
        "edges": [
            {"id": "e1", "from": "vin.n1", "to": "r1.n1"},
            {"id": "e2", "from": "r1.n2", "to": "l1.n1"},
            {"id": "e3", "from": "l1.n2", "to": "c1.n1"},
            {"id": "e4", "from": "c1.n2", "to": "gnd.n1"},
            {"id": "e5", "from": "vin.n2", "to": "gnd.n1"},
        ],
    }


def _node_by_role(parsed: dict[str, Any], role: str) -> dict[str, Any] | None:
    for node in parsed.get("nodes") or []:
        nid = str(node.get("id") or "").lower()
        rtype = str(node.get("type") or "").lower()
        if role == "source_v" and rtype == "source_v":
            return node
        if role == "r1" and rtype == "resistor" and nid in ("r1", "r_1"):
            return node
        if role == "r1" and rtype == "resistor" and node.get("refdes", "").upper() == "R1":
            return node
    by_type: dict[str, list] = {}
    for node in parsed.get("nodes") or []:
        by_type.setdefault(str(node.get("type") or ""), []).append(node)
    if role == "source_v":
        return (by_type.get("source_v") or [None])[0]
    if role == "resistor":
        return (by_type.get("resistor") or [None])[0]
    if role == "inductor":
        return (by_type.get("inductor") or [None])[0]
    if role == "capacitor":
        return (by_type.get("capacitor") or [None])[0]
    return None


def format_series_rlc_param_strip(graph: dict[str, Any]) -> str | None:
    """Human strip from compiled netlist values: ``V 10 V · R 10 Ω · L 10.0 mH · C 100 µF``."""
    params = series_rlc_params_from_graph(graph)
    if not params:
        return None
    v = float(params["v_step"])
    r = float(params["r_ohm"])
    l_mh = float(params["l_h"]) * 1000.0
    c_uf = float(params["c_f"]) * 1e6
    return f"V {v:g} V · R {r:g} Ω · L {l_mh:.1f} mH · C {c_uf:.0f} µF"


def series_rlc_params_from_graph(graph: dict[str, Any]) -> dict[str, float] | None:
    """Read V/R/L/C from the drawn series RLC graph (first of each kind)."""
    parsed = parse_graph(graph)
    src = _node_by_role(parsed, "source_v")
    res = _node_by_role(parsed, "resistor")
    ind = _node_by_role(parsed, "inductor")
    cap = _node_by_role(parsed, "capacitor")
    if not all((src, res, ind, cap)):
        return None
    try:
        return {
            "v_step": float(src.get("value") or 10.0),
            "r_ohm": float(res.get("value") or 10.0),
            "l_h": float(ind.get("value") or 1e-3),
            "c_f": float(cap.get("value") or 1e-6),
        }
    except (TypeError, ValueError):
        return None


def _electrical_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for node in sorted(nodes, key=lambda n: str(n.get("id") or "")):
        out.append(
            {
                "id": node.get("id"),
                "type": node.get("type"),
                "value": node.get("value"),
                "unit": node.get("unit"),
                "refdes": node.get("refdes"),
            }
        )
    return out


def graph_resistor_values(graph: dict[str, Any]) -> dict[str, float]:
    """Map refdes (or id) to resistance for change notes."""
    parsed = parse_graph(graph)
    out: dict[str, float] = {}
    for node in parsed.get("nodes") or []:
        if node.get("type") != "resistor":
            continue
        key = str(node.get("refdes") or node.get("id") or "R")
        try:
            out[key] = float(node.get("value"))
        except (TypeError, ValueError):
            continue
    return out


def graph_electrical_signature(graph: dict[str, Any]) -> str:
    parsed = parse_graph(graph)
    edges = sorted(
        [{"id": e.get("id"), "from": e.get("from"), "to": e.get("to")} for e in parsed.get("edges") or []],
        key=lambda e: str(e.get("id") or ""),
    )
    payload = {"nodes": _electrical_nodes(parsed.get("nodes") or []), "edges": edges}
    return json.dumps(payload, sort_keys=True)


def graphs_electrically_equal(a: dict[str, Any], b: dict[str, Any]) -> bool:
    return graph_electrical_signature(a) == graph_electrical_signature(b)


def probe_for_capacitor(graph: dict[str, Any]) -> str | None:
    """SPICE probe expression for the first capacitor in the graph."""
    parsed = parse_graph(graph)
    caps = [n for n in parsed["nodes"] if n["type"] == "capacitor"]
    if not caps:
        return None
    cid = caps[0]["id"]
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        parent[find(a)] = find(b)

    for edge in parsed["edges"]:
        union(str(edge["from"]), str(edge["to"]))
    for node in parsed["nodes"]:
        if node["type"] == "junction":
            jid = str(node["id"])
            ports = [f"{jid}.{p}" for p in ("n", "e", "s", "w")]
            for other in ports[1:]:
                union(ports[0], other)
    spice_of: dict[str, int] = {}
    next_id = 1
    ground_roots: set[str] = set()
    for node in parsed["nodes"]:
        if node["type"] == "ground":
            ground_roots.add(find(f"{node['id']}.n1"))

    def spice(port: str) -> int:
        nonlocal next_id
        root = find(port)
        if root in ground_roots:
            return 0
        if root not in spice_of:
            spice_of[root] = next_id
            next_id += 1
        return spice_of[root]

    for node in parsed["nodes"]:
        if node["type"] != "junction":
            spice(f"{node['id']}.n1")
            if node["type"] != "ground":
                spice(f"{node['id']}.n2")
        else:
            for p in "nesw":
                spice(f"{node['id']}.{p}")
    n = spice(f"{cid}.n1")
    return f"v({n})"


def series_rlc_netlist_signature(cir: str) -> tuple[str, ...]:
    """Sorted branch keys for topology regression (refdes and spice nodes)."""

    lines = []
    for raw in cir.splitlines():
        line = raw.strip()
        if not line or line.startswith("*") or line.upper().startswith("."):
            continue
        parts = line.split()
        if len(parts) >= 4:
            lines.append(f"{parts[0]}:{parts[1]}-{parts[2]}")
    return tuple(sorted(lines))


def graph_port_errors(graph: dict[str, Any]) -> list[str]:
    """Dangling or duplicate-free port wiring checks for agent seeds."""
    parsed = parse_graph(graph)
    nodes = {n["id"]: n for n in parsed["nodes"]}
    port_use: dict[str, int] = {}
    for edge in parsed["edges"]:
        for end in (edge["from"], edge["to"]):
            port_use[end] = port_use.get(end, 0) + 1
    errors: list[str] = []
    for nid, node in nodes.items():
        if node["type"] == "ground":
            p = f"{nid}.n1"
            if port_use.get(p, 0) < 1:
                errors.append(f"{p} unconnected")
            continue
        if node["type"] == "junction":
            hits = 0
            for port in ("n", "e", "s", "w"):
                p = f"{nid}.{port}"
                used = port_use.get(p, 0)
                if used > 1:
                    errors.append(f"junction {p} has {used} wires (expected 1)")
                elif used == 1:
                    hits += 1
            if hits < 2:
                errors.append(f"junction {nid} needs at least 2 connections")
            continue
        for port in ("n1", "n2"):
            p = f"{nid}.{port}"
            used = port_use.get(p, 0)
            if used == 0:
                errors.append(f"dangling port {p}")
            elif used > 1:
                errors.append(f"port {p} has {used} wires (expected 1)")
    return errors


def rc_lowpass_graph(vin: float = 5, r_ohm: float = 1000, c_f: float = 1e-6) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "nodes": [
            {"id": "vin", "type": "source_v", "refdes": "V1", "value": vin, "unit": "V", "x": 40, "y": 100},
            {"id": "r1", "type": "resistor", "refdes": "R1", "value": r_ohm, "unit": "ohm", "x": 200, "y": 40},
            {"id": "c1", "type": "capacitor", "refdes": "C1", "value": c_f, "unit": "F", "x": 360, "y": 120, "rot": 90},
            {"id": "gnd", "type": "ground", "refdes": "Gnd", "value": 0, "unit": "", "x": 40, "y": 220},
        ],
        "edges": [
            {"id": "e1", "from": "vin.n1", "to": "r1.n1"},
            {"id": "e2", "from": "r1.n2", "to": "c1.n1"},
            {"id": "e3", "from": "c1.n2", "to": "gnd.n1"},
            {"id": "e4", "from": "vin.n2", "to": "gnd.n1"},
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
    if kind in {"rc_lowpass", "rc_low_pass"}:
        return rc_lowpass_graph(
            vin=float(problem.get("vin") or 5),
            r_ohm=float(problem.get("r") or problem.get("r_ohm") or 1000),
            c_f=float(problem.get("c") or problem.get("c_f") or 1e-6),
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

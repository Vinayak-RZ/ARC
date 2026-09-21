"""Validate agent-authored UI diagram artifacts (graph.json, control_diagram.json)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.circuit.graph import MAX_EDGES, MAX_NODES
from electrical_engineer.circuit.graph import SCHEMA as CIRCUIT_SCHEMA

CONTROL_SCHEMA = "arc.control_diagram.v1"
ALLOWED_DIAGRAM_KINDS = frozenset(
    {"unity_feedback", "power_fault", "protection_5051", "drives_dc"},
)
SERIES_RLC_IDS = frozenset({"vin", "r1", "l1", "c1", "gnd"})
SERIES_RLC_TYPES = {
    "vin": "source_v",
    "r1": "resistor",
    "l1": "inductor",
    "c1": "capacitor",
    "gnd": "ground",
}


class DiagramCheckError(ValueError):
    pass


def _load(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DiagramCheckError(f"{path.name}: invalid JSON") from exc
    if not isinstance(data, dict):
        raise DiagramCheckError(f"{path.name}: root must be object")
    return data


def check_rlc_graph(data: dict[str, Any], *, path: str = "graph.json") -> list[str]:
    errors: list[str] = []
    if data.get("schema") != CIRCUIT_SCHEMA:
        errors.append(f"{path}: schema must be {CIRCUIT_SCHEMA}")
    nodes = data.get("nodes")
    edges = data.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        errors.append(f"{path}: nodes and edges must be lists")
        return errors
    if len(nodes) > MAX_NODES or len(edges) > MAX_EDGES:
        errors.append(f"{path}: exceeds UI cap ({MAX_NODES} parts / {MAX_EDGES} wires)")
    if len(nodes) < 2:
        errors.append(f"{path}: blank-risk — fewer than 2 nodes")
    by_id = {str(n.get("id")): n for n in nodes if isinstance(n, dict)}
    if SERIES_RLC_IDS <= set(by_id):
        for nid, kind in SERIES_RLC_TYPES.items():
            node = by_id.get(nid) or {}
            if node.get("type") != kind:
                errors.append(f"{path}: node {nid} must be type {kind}")
            ref = str(node.get("refdes") or "")
            if nid != "gnd" and not ref:
                errors.append(f"{path}: node {nid} missing refdes (IIT label law)")
    for n in nodes:
        if not isinstance(n, dict):
            errors.append(f"{path}: node must be object")
            continue
        if not n.get("id") or not n.get("type"):
            errors.append(f"{path}: node needs id and type")
    return errors


def check_control_diagram(data: dict[str, Any], *, path: str = "control_diagram.json") -> list[str]:
    errors: list[str] = []
    if data.get("schema") != CONTROL_SCHEMA:
        errors.append(f"{path}: schema must be {CONTROL_SCHEMA}")
    kind = str(data.get("diagramKind") or "")
    if kind not in ALLOWED_DIAGRAM_KINDS:
        errors.append(f"{path}: diagramKind must be one of {sorted(ALLOWED_DIAGRAM_KINDS)}")
    title = str(data.get("title") or "").strip()
    if not title:
        errors.append(f"{path}: missing title (student-facing caption)")
    nodes = data.get("nodes")
    edges = data.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        errors.append(f"{path}: nodes and edges must be lists")
        return errors
    if len(nodes) < 2:
        errors.append(f"{path}: blank-risk — fewer than 2 nodes")
    if len(edges) < 1 and kind == "unity_feedback":
        errors.append(f"{path}: unity feedback needs signal edges")
    if kind == "unity_feedback":
        if not any(n.get("type") == "sum" for n in nodes if isinstance(n, dict)):
            errors.append(f"{path}: unity feedback requires summing junction (type sum)")
        if not any(n.get("type") == "block" for n in nodes if isinstance(n, dict)):
            errors.append(f"{path}: unity feedback requires G(s) block")
    if kind == "power_fault" and not isinstance(data.get("sequence"), dict):
        errors.append(f"{path}: power_fault requires sequence {{z1,z2,z0,fault}} for LG inset")
    if kind == "protection_5051" and not isinstance(data.get("meta"), dict):
        errors.append(f"{path}: protection_5051 requires meta (CT ratio, pickup)")
    if kind == "drives_dc" and not isinstance(data.get("meta"), dict):
        errors.append(f"{path}: drives_dc requires meta (v_dc, ra_ohm, t_load)")
    for n in nodes:
        if not isinstance(n, dict):
            continue
        if n.get("type") == "equip" and not str(n.get("label") or "").strip():
            errors.append(f"{path}: equip node {n.get('id')} missing label")
        if n.get("type") == "block" and not str(n.get("tf") or "").strip():
            errors.append(f"{path}: block {n.get('id')} missing transfer function text")
    return errors


def check_artifact_file(path: Path) -> list[str]:
    path = path.resolve()
    name = path.name.lower()
    data = _load(path)
    if name == "graph.json":
        return check_rlc_graph(data, path=name)
    if name == "control_diagram.json":
        return check_control_diagram(data, path=name)
    raise DiagramCheckError(f"unsupported artifact: {path.name}")


def check_run_dir(run_dir: Path) -> list[str]:
    run_dir = run_dir.resolve()
    errors: list[str] = []
    graph = run_dir / "graph.json"
    cd = run_dir / "control_diagram.json"
    if graph.is_file():
        errors.extend(check_rlc_graph(_load(graph)))
    if cd.is_file():
        errors.extend(check_control_diagram(_load(cd)))
    if not graph.is_file() and not cd.is_file():
        errors.append(f"{run_dir.name}: no graph.json or control_diagram.json (blank UI risk)")
    return errors

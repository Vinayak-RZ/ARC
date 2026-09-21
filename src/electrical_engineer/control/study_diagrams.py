"""One-line study diagrams (power, protection, drives) for the localhost UI."""

from __future__ import annotations

from typing import Any

from electrical_engineer.control.diagram import SCHEMA


def _equip(eid: str, label: str, detail: str, x: float, y: float) -> dict[str, Any]:
    return {"id": eid, "type": "equip", "label": label, "tf": detail, "x": x, "y": y}


def power_oneline_diagram(problem: dict[str, Any] | None) -> dict[str, Any]:
    problem = problem or {}
    fault = str(problem.get("fault_type") or "LG")
    z1 = float(problem.get("z1_pu") or 0.1)
    z2 = float(problem.get("z2_pu") or 0.1)
    z0 = float(problem.get("z0_pu") or 0.3)
    nodes = [
        _equip("gen", "Generator", "1.0 pu", 48, 100),
        _equip("bus", "Bus 1", "slack", 200, 100),
        _equip("line", "Transmission", f"Z1={z1} Z2={z2} pu", 352, 100),
        _equip("load", "Load", f"Z0={z0} pu", 504, 100),
        _equip("fault", f"{fault} fault", "sequence network", 352, 220),
    ]
    edges = [
        {"id": "e1", "from": "gen", "fromPort": "out", "to": "bus", "toPort": "in"},
        {"id": "e2", "from": "bus", "fromPort": "out", "to": "line", "toPort": "in"},
        {"id": "e3", "from": "line", "fromPort": "out", "to": "load", "toPort": "in"},
        {"id": "e4", "from": "line", "fromPort": "out", "to": "fault", "toPort": "in"},
    ]
    return {
        "schema": SCHEMA,
        "diagramKind": "power_fault",
        "title": f"{fault} fault study — single-line diagram (pu)",
        "sequence": {"fault": fault, "z1": z1, "z2": z2, "z0": z0},
        "nodes": nodes,
        "edges": edges,
    }


def protection_oneline_diagram(problem: dict[str, Any] | None) -> dict[str, Any]:
    problem = problem or {}
    ct_p = float(problem.get("ct_primary_a") or 300)
    ct_s = float(problem.get("ct_secondary_a") or 5)
    pickup = float(problem.get("relay_pickup_a") or 2)
    nodes = [
        _equip("bus", "Bus", "faulted feeder", 48, 120),
        _equip("ct", "CT", f"{ct_p:g}/{ct_s:g} A", 200, 120),
        _equip("relay", "50/51 relay", f"pickup {pickup:g} A sec", 352, 120),
        _equip("brk", "Breaker", "trip coil", 504, 120),
        _equip("line", "Feeder", "to fault", 656, 120),
    ]
    edges = [
        {"id": "e1", "from": "bus", "fromPort": "out", "to": "ct", "toPort": "in"},
        {"id": "e2", "from": "ct", "fromPort": "out", "to": "relay", "toPort": "in"},
        {"id": "e3", "from": "relay", "fromPort": "out", "to": "brk", "toPort": "in"},
        {"id": "e4", "from": "brk", "fromPort": "out", "to": "line", "toPort": "in"},
    ]
    return {
        "schema": SCHEMA,
        "diagramKind": "protection_5051",
        "title": "Feeder protection — CT, 50/51 relay, breaker",
        "meta": {
            "ct_ratio": f"{ct_p:g}/{ct_s:g} A",
            "pickup_sec": f"{pickup:g} A sec",
        },
        "nodes": nodes,
        "edges": edges,
    }


def drives_oneline_diagram(problem: dict[str, Any] | None) -> dict[str, Any]:
    problem = problem or {}
    v = float(problem.get("v_dc") or 120)
    ra = float(problem.get("ra_ohm") or 1)
    t_load = float(problem.get("t_load_nm") or 5)
    nodes = [
        _equip("dc", "DC bus", f"{v:.0f} V", 48, 120),
        _equip("inv", "Converter", "average model", 200, 120),
        _equip("mot", "Motor", "DC / IM", 352, 120),
        _equip("load", "Load", f"{t_load:g} N·m", 504, 120),
    ]
    edges = [
        {"id": "e1", "from": "dc", "fromPort": "out", "to": "inv", "toPort": "in"},
        {"id": "e2", "from": "inv", "fromPort": "out", "to": "mot", "toPort": "in"},
        {"id": "e3", "from": "mot", "fromPort": "out", "to": "load", "toPort": "in"},
    ]
    return {
        "schema": SCHEMA,
        "diagramKind": "drives_dc",
        "title": "DC drive — armature circuit and load torque",
        "meta": {"v_dc": v, "ra_ohm": ra, "t_load": t_load},
        "nodes": nodes,
        "edges": edges,
    }


def control_diagram_from_tf_problem(problem: dict[str, Any] | None) -> dict[str, Any] | None:
    from electrical_engineer.control.diagram import control_diagram_from_problem

    problem = problem or {}
    tf = problem.get("tf")
    if not tf and problem.get("num") and problem.get("den"):
        num = problem["num"]
        den = problem["den"]
        if isinstance(num, list) and isinstance(den, list) and len(den) >= 2:
            tf = f"{num[0]}/(s+{den[1]})" if len(num) == 1 and len(den) == 2 else "G(s)"
    if not tf:
        return None
    return control_diagram_from_problem(
        {
            "blocks": [{"id": "G", "tf": str(tf)}, {"id": "H", "tf": "1"}],
            "unity_feedback": {"forward": "G", "feedback": "H", "negative": True},
        }
    )

"""One-line study diagrams (power, protection, drives) for the localhost UI."""

from __future__ import annotations

from typing import Any

from electrical_engineer.control.diagram import SCHEMA


def _equip(eid: str, label: str, detail: str, x: float, y: float) -> dict[str, Any]:
    return {"id": eid, "type": "equip", "label": label, "tf": detail, "x": x, "y": y}


def power_oneline_diagram(problem: dict[str, Any] | None) -> dict[str, Any]:
    from electrical_engineer.engines.power_runner import _parse_complex

    problem = problem or {}
    fault = str(problem.get("fault_type") or "LG")
    z1 = abs(_parse_complex(problem.get("z1_pu", 0.1)))
    z2 = abs(_parse_complex(problem.get("z2_pu", 0.1)))
    z0 = abs(_parse_complex(problem.get("z0_pu", 0.3)))
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


def smib_swing_diagram(problem: dict[str, Any] | None) -> dict[str, Any]:
    """One-line of the machine the swing engine actually integrates."""
    from electrical_engineer.engines.smib_swing import SmibCase

    problem = problem or {}
    case = SmibCase(
        **{k: problem[k] for k in problem if k in SmibCase.__dataclass_fields__}
    )
    nodes = [
        _equip("gen", "Generator", f"H={case.h_mj_mva:g} s", 48, 120),
        _equip("xfmr", "Transformer", "step-up", 200, 120),
        _equip("line", "Line", "double circuit", 360, 120),
        _equip("inf", "Infinite bus", f"{case.f0_hz:g} Hz", 520, 120),
    ]
    edges = [
        {"id": "e1", "from": "gen", "fromPort": "out", "to": "xfmr", "toPort": "in"},
        {"id": "e2", "from": "xfmr", "fromPort": "out", "to": "line", "toPort": "in"},
        {"id": "e3", "from": "line", "fromPort": "out", "to": "inf", "toPort": "in"},
    ]
    return {
        "schema": SCHEMA,
        "diagramKind": "smib_swing",
        "title": "SMIB — generator, transformer, line, infinite bus",
        "meta": {
            "pm": case.pm_pu,
            "pmax_pre": case.pmax_pre_pu,
            "pmax_fault": case.pmax_fault_pu,
            "pmax_post": case.pmax_post_pu,
            "h": case.h_mj_mva,
            "f0": case.f0_hz,
        },
        "nodes": nodes,
        "edges": edges,
    }


def digital_loop_diagram(problem: dict[str, Any] | None) -> dict[str, Any]:
    problem = problem or {}
    num = problem.get("num") or [0.1]
    den = problem.get("den") or [1.0, -0.5]
    ts = float(problem.get("ts") or problem.get("sample_time") or 0.01)
    gz = f"{num} / {den}"
    nodes = [
        {"id": "sum", "type": "sum", "label": "Σ", "x": 72, "y": 120, "negative": True},
        _equip("zoh", "ZOH", f"Ts={ts:g} s", 200, 120),
        {"id": "G", "type": "block", "label": "G(z)", "tf": gz, "x": 380, "y": 120},
    ]
    edges = [
        {"id": "e1", "from": "sum", "fromPort": "out", "to": "zoh", "toPort": "in"},
        {"id": "e2", "from": "zoh", "fromPort": "out", "to": "G", "toPort": "in"},
        {"id": "e3", "from": "G", "fromPort": "out", "to": "sum", "toPort": "feedback"},
    ]
    return {
        "schema": SCHEMA,
        "diagramKind": "digital_loop",
        "title": "Discrete loop — zero-order hold and G(z)",
        "meta": {"gz": gz, "ts": ts},
        "nodes": nodes,
        "edges": edges,
    }


def dispatch_diagram(problem: dict[str, Any] | None) -> dict[str, Any]:
    problem = problem or {}
    pd = float(problem.get("PD") or problem.get("pd_mw") or 500)
    nodes = [
        _equip("g1", "Gen 1", "IC curve", 48, 64),
        _equip("g2", "Gen 2", "IC curve", 48, 148),
        _equip("g3", "Gen 3", "IC curve", 48, 232),
        _equip("bus", "Load bus", f"Pd = {pd:g} MW", 320, 148),
    ]
    edges = [
        {"id": "e1", "from": "g1", "fromPort": "out", "to": "bus", "toPort": "in"},
        {"id": "e2", "from": "g2", "fromPort": "out", "to": "bus", "toPort": "in"},
        {"id": "e3", "from": "g3", "fromPort": "out", "to": "bus", "toPort": "in"},
    ]
    return {
        "schema": SCHEMA,
        "diagramKind": "dispatch_ed",
        "title": "Economic dispatch — three units, one load",
        "meta": {"pd_mw": pd},
        "nodes": nodes,
        "edges": edges,
    }


def buck_diagram(problem: dict[str, Any] | None) -> dict[str, Any]:
    problem = problem or {}
    vin = float(problem.get("vin") or 12)
    vout = float(problem.get("vout") or 5)
    l_h = float(problem.get("l") or 47e-6)
    fs = float(problem.get("fs") or 1e5)
    nodes = [
        _equip("src", "Vin", f"{vin:g} V", 40, 120),
        _equip("sw", "Switch", f"{fs / 1e3:g} kHz", 180, 120),
        _equip("l", "Inductor", f"{l_h * 1e6:g} µH", 340, 120),
        _equip("out", "Vout", f"{vout:g} V", 500, 120),
    ]
    edges = [
        {"id": "e1", "from": "src", "fromPort": "out", "to": "sw", "toPort": "in"},
        {"id": "e2", "from": "sw", "fromPort": "out", "to": "l", "toPort": "in"},
        {"id": "e3", "from": "l", "fromPort": "out", "to": "out", "toPort": "in"},
    ]
    return {
        "schema": SCHEMA,
        "diagramKind": "buck_ccm",
        "title": "Buck converter — switch, diode, L, C",
        "meta": {"vin": vin, "vout": vout, "l_uh": l_h * 1e6, "fs_khz": fs / 1e3},
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

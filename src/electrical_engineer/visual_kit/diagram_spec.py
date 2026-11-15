"""Emit arc.diagram.v1 for runs (browser studio-engine)."""

from __future__ import annotations

import logging
import math
from pathlib import Path
from typing import Any

from electrical_engineer.visual_kit.diagram_study import STUDY_BUILDERS
from electrical_engineer.visual_kit.diagram_validate import SCHEMA, validate_diagram

_LOG = logging.getLogger(__name__)


def _wrap(title: str, panels: list[dict[str, Any]]) -> dict[str, Any]:
    return {"schema": SCHEMA, "title": title, "panels": panels}


def voltage_divider(problem: dict[str, Any]) -> dict[str, Any]:
    vin = float(problem.get("vin") or 10)
    r1 = float(problem.get("r1") or 1000)
    r2 = float(problem.get("r2") or 1000)
    return _wrap(
        "Voltage divider",
        [
            {
                "kind": "schematic",
                "title": "Circuit",
                "grid": 40,
                "components": [
                    {"id": "vin", "type": "vsource", "at": [0, 1], "rot": 0, "label": "Vin", "value": f"{vin:g} V"},
                    {"id": "r1", "type": "resistor", "at": [2, 0], "rot": 90, "label": "R1", "value": f"{r1:g} Ω"},
                    {"id": "r2", "type": "resistor", "at": [2, 2], "rot": 90, "label": "R2", "value": f"{r2:g} Ω"},
                    {"id": "gnd", "type": "ground", "at": [2, 3.5], "rot": 0},
                ],
                "wires": [
                    {"from": "vin.p", "to": "r1.a"},
                    {"from": "r1.b", "to": "r2.a"},
                    {"from": "r2.b", "to": "gnd.a"},
                    {"from": "vin.n", "to": "gnd.a"},
                ],
                "probes": [{"at": "r1.b", "label": "Vout"}],
            }
        ],
    )


def series_rlc(problem: dict[str, Any]) -> dict[str, Any]:
    return _wrap(
        "Series RLC",
        [
            {
                "kind": "schematic",
                "title": "Circuit",
                "grid": 40,
                "components": [
                    {"id": "vin", "type": "vsource", "at": [0, 1], "label": "Vin"},
                    {"id": "r1", "type": "resistor", "at": [2, 0], "rot": 0, "label": "R"},
                    {"id": "l1", "type": "inductor", "at": [4, 0], "rot": 0, "label": "L"},
                    {"id": "c1", "type": "capacitor", "at": [6, 0], "rot": 0, "label": "C"},
                    {"id": "gnd", "type": "ground", "at": [6, 2], "rot": 0},
                ],
                "wires": [
                    {"from": "vin.p", "to": "r1.a"},
                    {"from": "r1.b", "to": "l1.a"},
                    {"from": "l1.b", "to": "c1.a"},
                    {"from": "c1.b", "to": "gnd.a"},
                    {"from": "vin.n", "to": "gnd.a"},
                ],
            }
        ],
    )


def unity_feedback(problem: dict[str, Any]) -> dict[str, Any]:
    tf = str(problem.get("tf") or "1/(s+1)")
    return _wrap(
        "Unity feedback",
        [
            {
                "kind": "block",
                "title": "Loop",
                "nodes": [
                    {"id": "r", "type": "input", "at": [0, 0], "label": "R(s)"},
                    {"id": "sum", "type": "sum", "at": [1, 0]},
                    {"id": "g", "type": "block", "at": [3, 0], "label": "G(s)", "tf": tf},
                    {"id": "y", "type": "output", "at": [5, 0], "label": "Y(s)"},
                    {"id": "h", "type": "block", "at": [3, 2], "label": "H", "tf": "1"},
                ],
                "edges": [
                    {"from": "r", "to": "sum"},
                    {"from": "sum", "to": "g"},
                    {"from": "g", "to": "y"},
                    {"from": "y", "to": "h"},
                    {"from": "h", "to": "sum"},
                ],
            }
        ],
    )


def power_fault(_problem: dict[str, Any]) -> dict[str, Any]:
    return _wrap(
        "Fault study",
        [
            {
                "kind": "oneline",
                "title": "Network",
                "buses": [
                    {"id": "b1", "at": [0, 0], "label": "Bus 1", "kv": 13.8},
                    {"id": "b2", "at": [3, 0], "label": "Bus 2", "kv": 13.8},
                ],
                "elements": [
                    {"id": "g1", "type": "gen", "bus": "b1", "label": "G"},
                    {"id": "l12", "type": "line", "from": "b1", "to": "b2", "label": "Z"},
                    {"id": "f1", "type": "fault", "bus": "b2", "label": "LG"},
                ],
            }
        ],
    )


def protection_5051(_problem: dict[str, Any]) -> dict[str, Any]:
    return _wrap(
        "50/51 protection",
        [
            {
                "kind": "oneline",
                "buses": [{"id": "b1", "at": [0, 0], "label": "Feeder"}],
                "elements": [
                    {"id": "src", "type": "gen", "bus": "b1", "label": "Src"},
                    {"id": "r51", "type": "relay", "bus": "b1", "label": "51"},
                    {"id": "cb", "type": "breaker", "bus": "b1"},
                ],
            }
        ],
    )


def drives_dc(_problem: dict[str, Any]) -> dict[str, Any]:
    return _wrap(
        "DC drive",
        [
            {
                "kind": "schematic",
                "grid": 40,
                "components": [
                    {"id": "v", "type": "vsource", "at": [0, 1], "label": "Vdc"},
                    {"id": "ra", "type": "resistor", "at": [2, 0], "label": "Ra"},
                    {"id": "m", "type": "motor", "at": [4, 0], "label": "M"},
                    {"id": "g", "type": "ground", "at": [4, 2]},
                ],
                "wires": [
                    {"from": "v.p", "to": "ra.a"},
                    {"from": "ra.b", "to": "m.a"},
                    {"from": "m.b", "to": "g.a"},
                    {"from": "v.n", "to": "g.a"},
                ],
            }
        ],
    )


def smib_swing(problem: dict[str, Any]) -> dict[str, Any]:
    pts = [[i, math.sin(math.radians(i)) * float(problem.get("pmax") or 1)] for i in range(0, 181, 5)]
    return _wrap(
        "SMIB swing",
        [
            {
                "kind": "oneline",
                "buses": [
                    {"id": "inf", "at": [0, 0], "label": "Infinite"},
                    {"id": "m", "at": [3, 0], "label": "Machine"},
                ],
                "elements": [
                    {"id": "g", "type": "gen", "bus": "m", "label": "G"},
                    {"id": "line", "type": "line", "from": "m", "to": "inf"},
                    {"id": "f", "type": "fault", "bus": "m", "label": "F"},
                ],
            },
            {
                "kind": "waveform",
                "title": "P–δ",
                "x": {"label": "δ", "unit": "deg", "scale": "linear"},
                "y": {"label": "P", "unit": "pu", "scale": "linear"},
                "series": [{"id": "pe", "label": "Pe", "points": pts, "style": "primary"}],
            },
        ],
    )


def digital_loop(_problem: dict[str, Any]) -> dict[str, Any]:
    return _wrap(
        "Digital loop",
        [
            {
                "kind": "block",
                "nodes": [
                    {"id": "r", "type": "input", "at": [0, 0], "label": "r"},
                    {"id": "c", "type": "block", "at": [2, 0], "label": "C(z)"},
                    {"id": "zoh", "type": "block", "at": [4, 0], "label": "ZOH"},
                    {"id": "p", "type": "block", "at": [6, 0], "label": "P(s)"},
                    {"id": "y", "type": "output", "at": [8, 0], "label": "y"},
                ],
                "edges": [
                    {"from": "r", "to": "c"},
                    {"from": "c", "to": "zoh"},
                    {"from": "zoh", "to": "p"},
                    {"from": "p", "to": "y"},
                ],
            }
        ],
    )


def dispatch_ed(problem: dict[str, Any]) -> dict[str, Any]:
    pd = float(problem.get("PD") or problem.get("pd_mw") or 500)
    pts = [[i, 10 + 0.02 * i] for i in range(0, int(pd) + 1, max(1, int(pd) // 40))]
    return _wrap(
        "Economic dispatch",
        [
            {
                "kind": "waveform",
                "title": "λ vs P",
                "x": {"label": "P", "unit": "MW", "scale": "linear"},
                "y": {"label": "λ", "unit": "MW/MW", "scale": "linear"},
                "series": [{"id": "lam", "label": "λ", "points": pts, "style": "primary"}],
                "markers": [{"x": pd, "label": "PD"}],
            }
        ],
    )


def buck_ccm(problem: dict[str, Any]) -> dict[str, Any]:
    vin = float(problem.get("vin") or 12)
    vout = float(problem.get("vout") or 5)
    d = vout / vin if vin else 0.4
    return _wrap(
        "Buck CCM",
        [
            {
                "kind": "schematic",
                "grid": 40,
                "components": [
                    {"id": "vin", "type": "vsource", "at": [0, 1], "label": "Vin", "value": f"{vin:g} V"},
                    {"id": "sw", "type": "switch", "at": [2, 0], "label": "S"},
                    {"id": "d1", "type": "diode", "at": [3, 1.5], "rot": 90, "label": "D"},
                    {"id": "l", "type": "inductor", "at": [4, 0], "label": "L"},
                    {"id": "c", "type": "capacitor", "at": [6, 1], "rot": 90, "label": "C"},
                    {"id": "r", "type": "resistor", "at": [7.5, 1], "rot": 90, "label": "R"},
                    {"id": "g", "type": "ground", "at": [6, 2.5]},
                ],
                "wires": [
                    {"from": "vin.p", "to": "sw.a"},
                    {"from": "sw.b", "to": "l.a"},
                    {"from": "l.b", "to": "c.a"},
                    {"from": "c.a", "to": "r.a"},
                    {"from": "c.b", "to": "g.a"},
                    {"from": "r.b", "to": "g.a"},
                    {"from": "vin.n", "to": "g.a"},
                    {"from": "d1.a", "to": "g.a"},
                    {"from": "d1.k", "to": "l.a"},
                ],
            },
            {
                "kind": "waveform",
                "title": "iL triangle",
                "x": {"label": "t", "unit": "s", "scale": "linear"},
                "y": {"label": "iL", "unit": "A", "scale": "linear"},
                "series": [
                    {
                        "id": "il",
                        "label": "iL",
                        "style": "primary",
                        "points": [[0, 1], [d, 1.2], [1, 1]],
                    }
                ],
            },
        ],
    )


_BUILDERS = {
    "voltage_divider": voltage_divider,
    "series_rlc": series_rlc,
    "unity_feedback": unity_feedback,
    "power_fault": power_fault,
    "protection_5051": protection_5051,
    "drives_dc": drives_dc,
    "smib_swing": smib_swing,
    "digital_loop": digital_loop,
    "dispatch_ed": dispatch_ed,
    "buck_ccm": buck_ccm,
}


def _kind_from(recipe_id: str, problem: dict[str, Any]) -> str | None:
    solver = str(problem.get("solver") or "")
    kind = str(problem.get("kind") or "")
    if kind == "voltage_divider" or {"vin", "r1", "r2"} <= set(problem):
        return "voltage_divider"
    if kind == "series_rlc" or recipe_id == "simulate-circuit":
        return "series_rlc"
    if recipe_id in {"solve-control-problem", "study-control-exam"} or "tf" in problem:
        return "unity_feedback"
    if recipe_id == "simulate-power-fault" or recipe_id == "symmetrical-fault-study":
        return "power_fault"
    if recipe_id == "study-protection-setting":
        return "protection_5051"
    if recipe_id == "solve-drives-problem":
        return "drives_dc"
    if recipe_id == "smib-swing-study":
        return "smib_swing"
    if recipe_id == "solve-digital-control-problem":
        return "digital_loop"
    if recipe_id in {"ed-lambda-study", "ed-penalty-study"}:
        return "dispatch_ed"
    if solver == "ccm_buck" or recipe_id == "study-power-electronics-v2":
        return "buck_ccm"
    return None


def diagram_for_run(run_dir: Path, recipe_id: str, problem: dict[str, Any]) -> dict[str, Any] | None:
    del run_dir
    study = STUDY_BUILDERS.get(recipe_id)
    if study is not None:
        return study(problem)
    key = _kind_from(recipe_id, problem)
    if not key:
        return None
    builder = _BUILDERS.get(key)
    if not builder:
        return None
    return builder(problem)


def write_diagram_json(run_dir: Path, diagram: dict[str, Any] | None) -> None:
    path = run_dir / "diagram.json"
    if diagram is None:
        if path.is_file():
            path.unlink()
        return
    errs = validate_diagram(diagram)
    if errs:
        _LOG.warning("diagram.json invalid, skipped: %s", errs)
        return
    path.write_text(__import__("json").dumps(diagram, indent=2), encoding="utf-8")

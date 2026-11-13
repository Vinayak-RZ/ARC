"""Reference diagrams for regression parity."""

from __future__ import annotations

from typing import Any


def unity_first_order() -> dict[str, Any]:
    return {
        "schema": "arc.control_studio.v1",
        "id": "golden-unity-first-order",
        "title": "Unity feedback first-order",
        "blocks": [
            {"id": "r", "type": "step", "x": 40, "y": 120, "params": {"amplitude": 1.0}},
            {"id": "sum1", "type": "sum", "x": 200, "y": 120, "params": {"signs": "+-"}},
            {"id": "G", "type": "plant_first_order", "x": 360, "y": 120, "params": {"k": 10.0, "tau": 1.0}},
            {"id": "y", "type": "scope", "x": 540, "y": 120, "params": {}},
        ],
        "wires": [
            {"id": "w1", "from": "r:out", "to": "sum1:in1"},
            {"id": "w2", "from": "sum1:out", "to": "G:in"},
            {"id": "w3", "from": "G:out", "to": "y:in"},
            {"id": "w4", "from": "G:out", "to": "sum1:feedback"},
        ],
        "meta": {
            "unity_feedback": {
                "blocks": [{"id": "G", "tf": "10/(s+1)"}, {"id": "H", "tf": "1"}],
                "unity_feedback": {"forward": "G", "feedback": "H", "negative": True},
            }
        },
    }


def pid_dc_motor() -> dict[str, Any]:
    return {
        "schema": "arc.control_studio.v1",
        "id": "golden-pid-dc-motor",
        "title": "PID on DC motor",
        "blocks": [
            {"id": "r", "type": "step", "x": 24, "y": 80, "params": {}, "label": "Step"},
            {"id": "sum1", "type": "sum", "x": 168, "y": 72, "params": {"signs": "+-"}},
            {"id": "pid1", "type": "pid", "x": 312, "y": 64, "params": {"kp": 50.0, "ki": 100.0, "kd": 5.0}},
            {"id": "motor", "type": "plant_dc_motor", "x": 528, "y": 64, "params": {}, "label": "DC motor"},
            {"id": "y", "type": "scope", "x": 672, "y": 72, "params": {}},
        ],
        "wires": [
            {"id": "w1", "from": "r:out", "to": "sum1:in1"},
            {"id": "w2", "from": "sum1:out", "to": "pid1:in"},
            {"id": "w3", "from": "pid1:out", "to": "motor:in"},
            {"id": "w4", "from": "motor:out", "to": "y:in"},
            {"id": "w5", "from": "motor:tap", "to": "sum1:feedback"},
        ],
        "meta": {
            "reference": "University of Michigan CTMS — DC Motor Speed: System Modeling",
            "reference_url": "https://ctms.engin.umich.edu/CTMS/index.php?example=MotorSpeed&section=SystemModeling",
            "pid_note": "Default gains scaled from CTMS example (Kp 100, Ki 200, Kd 10) for a visible step within 10 s.",
        },
    }


def lead_compensator() -> dict[str, Any]:
    return {
        "schema": "arc.control_studio.v1",
        "id": "golden-lead",
        "title": "Lead compensator margins",
        "blocks": [
            {"id": "r", "type": "step", "x": 40, "y": 120, "params": {}},
            {"id": "lead", "type": "transfer_function", "x": 200, "y": 120, "params": {"tf": "(s+2)/(s+10)"}},
            {"id": "plant", "type": "transfer_function", "x": 380, "y": 120, "params": {"tf": "1/(s*(s+1))"}},
            {"id": "y", "type": "scope", "x": 560, "y": 120, "params": {}},
        ],
        "wires": [
            {"id": "w1", "from": "r:out", "to": "lead:in"},
            {"id": "w2", "from": "lead:out", "to": "plant:in"},
            {"id": "w3", "from": "plant:out", "to": "y:in"},
        ],
        "meta": {
            "num": [2.0, 2.0],
            "den": [1.0, 11.0, 10.0, 0.0],
        },
    }


def two_area_agc() -> dict[str, Any]:
    return {
        "schema": "arc.control_studio.v1",
        "id": "golden-agc",
        "title": "Two-area AGC (aggregate)",
        "blocks": [
            {"id": "r", "type": "step", "x": 40, "y": 120, "params": {"amplitude": 0.01}},
            {"id": "area1", "type": "plant_agc_area", "x": 220, "y": 80, "params": {"case": "eec301_default", "area": 1}},
            {"id": "tie", "type": "gain", "x": 220, "y": 180, "params": {"k": 2.0, "unit": "1"}},
            {"id": "area2", "type": "plant_agc_area", "x": 400, "y": 120, "params": {"case": "eec301_default", "area": 2}},
            {"id": "y", "type": "scope", "x": 580, "y": 120, "params": {}},
        ],
        "wires": [
            {"id": "w1", "from": "r:out", "to": "area1:in"},
            {"id": "w2", "from": "area1:out", "to": "tie:in"},
            {"id": "w3", "from": "tie:out", "to": "area2:in"},
            {"id": "w4", "from": "area2:out", "to": "y:in"},
        ],
        "meta": {
            "num": [1.0],
            "den": [5.0, 4.0, 1.0],
            "agc": "eec301_two_area",
        },
    }


def open_loop_low_gain() -> dict[str, Any]:
    """Open loop with magnitude below 0 dB across the analysis sweep (margin regression capture)."""
    return {
        "schema": "arc.control_studio.v1",
        "id": "golden-open-low-gain",
        "title": "Low gain open loop",
        "blocks": [
            {"id": "r", "type": "step", "x": 40, "y": 120, "params": {"amplitude": 1.0}},
            {"id": "g", "type": "plant_first_order", "x": 280, "y": 120, "params": {"k": 0.001, "tau": 1.0}},
            {"id": "y", "type": "scope", "x": 440, "y": 120, "params": {}},
        ],
        "wires": [
            {"id": "w1", "from": "r:out", "to": "g:in"},
            {"id": "w2", "from": "g:out", "to": "y:in"},
        ],
        "meta": {"num": [0.001], "den": [1.0, 1.0]},
    }


GOLDENS = {
    "unity_first_order": unity_first_order,
    "pid_dc_motor": pid_dc_motor,
    "lead_compensator": lead_compensator,
    "two_area_agc": two_area_agc,
    "open_loop_low_gain": open_loop_low_gain,
}

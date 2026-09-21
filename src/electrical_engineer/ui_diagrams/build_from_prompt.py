"""Build diagram artifacts from short student prompts (no example JSON copy)."""

from __future__ import annotations

from typing import Any

from electrical_engineer.circuit.graph import series_rlc_graph
from electrical_engineer.control.diagram import control_diagram_from_problem
from electrical_engineer.control.study_diagrams import (
    drives_oneline_diagram,
    power_oneline_diagram,
    protection_oneline_diagram,
)

# Normative student prompts → structured fields (skill worked examples).
STUDENT_PROMPTS: dict[str, dict[str, Any]] = {
    "rlc": {
        "text": "Series RLC with V1=12 V, R1=470 Ω, L1=2 mH, C1=0.5 µF for transient check.",
        "fields": {"vin": 12, "r_ohm": 470, "l_h": 2e-3, "c_f": 0.5e-6},
    },
    "control": {
        "text": "Unity negative feedback: G(s)=5/(s+2), H(s)=1. Plot Bode and step.",
        "fields": {
            "blocks": [{"id": "G", "tf": "5/(s+2)"}, {"id": "H", "tf": "1"}],
            "unity_feedback": {"forward": "G", "feedback": "H", "negative": True},
        },
    },
    "power": {
        "text": "LG fault on a feeder: Z1=0.15 pu, Z2=0.15 pu, Z0=0.35 pu.",
        "fields": {"fault_type": "LG", "z1_pu": 0.15, "z2_pu": 0.15, "z0_pu": 0.35},
    },
    "protection": {
        "text": "CT 400/5 A, 50/51 pickup 2.5 A secondary, feeder fault 900 A.",
        "fields": {
            "ct_primary_a": 400,
            "ct_secondary_a": 5,
            "relay_pickup_a": 2.5,
            "fault_current_a": 900,
        },
    },
    "drives": {
        "text": "DC drive Va=110 V, Ra=0.8 Ω, load torque 8 N·m.",
        "fields": {"v_dc": 110, "ra_ohm": 0.8, "t_load_nm": 8},
    },
}


def build_artifact_from_prompt(domain: str) -> dict[str, Any]:
    """Return graph.json or control_diagram.json payload for a domain."""
    if domain not in STUDENT_PROMPTS:
        raise ValueError(f"unknown domain: {domain}")
    fields = STUDENT_PROMPTS[domain]["fields"]
    if domain == "rlc":
        return series_rlc_graph(
            vin=float(fields["vin"]),
            r_ohm=float(fields["r_ohm"]),
            l_h=float(fields["l_h"]),
            c_f=float(fields["c_f"]),
        )
    if domain == "control":
        diagram = control_diagram_from_problem(fields)
        if diagram is None:
            raise ValueError("control prompt did not compose")
        return diagram
    if domain == "power":
        return power_oneline_diagram(fields)
    if domain == "protection":
        return protection_oneline_diagram(fields)
    if domain == "drives":
        return drives_oneline_diagram({**fields, "kind": "dc"})
    raise ValueError(f"no builder for {domain}")


def perturb_baseline_payload(domain: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Agent-edited values on top of a valid template (not a raw file copy)."""
    import copy

    data = copy.deepcopy(payload)
    if domain == "rlc":
        for n in data.get("nodes", []):
            if n.get("id") == "r1":
                n["value"] = 2200
            if n.get("id") == "vin":
                n["value"] = 9
    elif domain == "control":
        for n in data.get("nodes", []):
            if n.get("type") == "block" and n.get("id") == "G":
                n["tf"] = "8/(s+3)"
    elif domain == "power" and isinstance(data.get("sequence"), dict):
        data["sequence"]["z1"] = 0.18
        data["sequence"]["z0"] = 0.4
    elif domain == "protection" and isinstance(data.get("meta"), dict):
        data["meta"]["ct_ratio"] = "400/5 A"
    elif domain == "drives" and isinstance(data.get("meta"), dict):
        data["meta"]["v_dc"] = 96
        data["meta"]["t_load"] = 7
    return data

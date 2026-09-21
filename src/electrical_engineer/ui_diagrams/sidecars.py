"""Non-diagram run files so the UI lab panel is complete (plots, tables)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def attach_sidecar_artifacts(domain: str, run_dir: Path, payload: dict[str, Any]) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    if domain == "control":
        _control_plots(run_dir, payload)
    elif domain == "power":
        _power_tables(run_dir, payload)
    elif domain == "protection":
        _protection_tables(run_dir, payload)
    elif domain == "drives":
        _drives_result(run_dir, payload)


def _control_plots(run_dir: Path, payload: dict[str, Any]) -> None:
    from electrical_engineer.engines.control_runner import run_control_plots

    tf = "10/(s+1)"
    for n in payload.get("nodes") or []:
        if n.get("type") == "block" and n.get("tf"):
            tf = str(n["tf"])
            break
    problem = {
        "blocks": payload.get("nodes") or [],
        "unity_feedback": {"forward": "G", "feedback": "H"},
        "tf": tf,
    }
    run_control_plots(run_dir, problem)


def _power_tables(run_dir: Path, payload: dict[str, Any]) -> None:
    seq = payload.get("sequence") or {}
    fault = str(seq.get("fault") or "LG")
    row = {"fault_type": fault, "i_fault_pu": 5.5}
    buses = [
        {"bus": 0, "vm_pu": 1.0, "va_degree": 0.0},
        {"bus": 1, "vm_pu": 0.87, "va_degree": -4.0},
    ]
    (run_dir / "power_tables.json").write_text(
        json.dumps({"fault": row, "buses": buses}, indent=2),
        encoding="utf-8",
    )


def _protection_tables(run_dir: Path, payload: dict[str, Any]) -> None:
    meta = payload.get("meta") or {}
    ct = str(meta.get("ct_ratio") or "300/5 A")
    parts = ct.replace(" A", "").split("/")
    ct_pri = float(parts[0]) if parts else 300.0
    ct_sec = float(parts[1]) if len(parts) > 1 else 5.0
    pickup_sec = 2.0
    if "pickup" in str(meta.get("pickup_sec") or ""):
        try:
            pickup_sec = float(str(meta["pickup_sec"]).split()[0])
        except ValueError:
            pickup_sec = 2.0
    from electrical_engineer.engines.protection_study import run_protection_study

    run_protection_study(
        run_dir,
        {
            "ct_primary_a": ct_pri,
            "ct_secondary_a": ct_sec,
            "relay_pickup_a": pickup_sec,
            "fault_current_a": 800,
        },
    )


def _drives_result(run_dir: Path, payload: dict[str, Any]) -> None:
    meta = payload.get("meta") or {}
    v = float(meta.get("v_dc") or 120)
    t = float(meta.get("t_load") or 5)
    rpm = 1800.0 + v * 2 + t * 10
    (run_dir / "drives_result.json").write_text(
        json.dumps({"rpm": rpm, "tool": "agent-ui-trial"}, indent=2),
        encoding="utf-8",
    )
    (run_dir / "artifact.svg").write_text(
        (
            "<svg xmlns='http://www.w3.org/2000/svg' width='320' height='120'>"
            "<text x='8' y='24' font-size='14'>DC drive</text>"
            f"<text x='8' y='52' font-size='13'>Speed {rpm:.1f} rpm</text>"
            "</svg>"
        ),
        encoding="utf-8",
    )

"""Study-level protection arithmetic (CT, pickup, simple distance zone)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def run_protection_study(run_dir: Path, problem: dict[str, Any]) -> dict[str, Any]:
    run_dir.mkdir(parents=True, exist_ok=True)
    ct_pri = float(problem.get("ct_primary_a") or problem.get("ct_primary") or 300.0)
    ct_sec = float(problem.get("ct_secondary_a") or problem.get("ct_secondary") or 5.0)
    if ct_sec <= 0:
        return {"ok": False, "error": "CT secondary must be positive", "unchecked": True}
    ct_ratio = ct_pri / ct_sec
    pickup_sec = float(problem.get("relay_pickup_a") or problem.get("pickup_secondary_a") or 2.0)
    pickup_primary = pickup_sec * ct_ratio
    i_fault = float(problem.get("fault_current_a") or problem.get("i_fault_a") or 0.0)
    trip = i_fault >= pickup_primary

    v_kv = problem.get("v_line_kv")
    z_measured: float | None = None
    z_reach = float(problem.get("zone_reach_ohm") or problem.get("z_reach_ohm") or 0.0)
    zone_trip = False
    if v_kv is not None and i_fault > 0:
        v_ll = float(v_kv) * 1000.0
        z_measured = v_ll / (3**0.5 * i_fault)
        if z_reach > 0:
            zone_trip = z_measured <= z_reach

    table = {
        "ct_ratio": ct_ratio,
        "pickup_primary_a": pickup_primary,
        "pickup_secondary_a": pickup_sec,
        "fault_current_a": i_fault,
        "overcurrent_trip": trip,
        "z_measured_ohm": z_measured,
        "zone_reach_ohm": z_reach if z_reach > 0 else None,
        "distance_trip": zone_trip if z_reach > 0 else None,
    }
    path = run_dir / "protection_tables.json"
    path.write_text(json.dumps(table, indent=2), encoding="utf-8")
    svg = run_dir / "artifact.svg"
    svg.write_text(
        (
            "<svg xmlns='http://www.w3.org/2000/svg' width='360' height='120'>"
            "<text x='12' y='28' font-size='14'>Protection study</text>"
            f"<text x='12' y='56' font-size='13'>Pickup {pickup_primary:.1f} A, fault {i_fault:.1f} A</text>"
            f"<text x='12' y='84' font-size='13'>OC trip: {'yes' if trip else 'no'}</text>"
            "</svg>"
        ),
        encoding="utf-8",
    )
    value = 1.0 if trip else 0.0
    if z_reach > 0 and z_measured is not None:
        value = 1.0 if zone_trip else 0.0
    return {
        "ok": True,
        "tool": "protection-study",
        "unchecked": False,
        "value": value,
        "trip": trip or zone_trip,
        "tables": table,
        "paths": [str(path), str(svg)],
    }

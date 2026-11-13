"""Transformer vector-group phase shift."""

from __future__ import annotations

from electrical_engineer.reference.catalog import get_record


def phase_shift_deg(*, group_id: str) -> dict:
    rec = get_record(group_id)
    if rec is None:
        raise ValueError(f"unknown vector group {group_id}")
    shift = float(rec["values"]["phase_shift_hv_to_lv_deg"])
    return {
        "group_id": group_id,
        "phase_shift_hv_to_lv_deg": shift,
        "label": rec["title"],
        "source_id": group_id,
        "trap_note": rec["values"].get(
            "trap_note",
            "Dyn11 is -30 deg HV-to-LV; do not flip sign vs lecture convention.",
        ),
    }

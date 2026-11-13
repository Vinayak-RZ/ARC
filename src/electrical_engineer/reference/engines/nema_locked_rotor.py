"""NEMA code-letter locked-rotor current estimate."""

from __future__ import annotations

import math

from electrical_engineer.reference.catalog import get_record


def locked_rotor_current_a(
    *,
    code_id: str,
    hp: float,
    line_voltage_v: float,
    use: str = "mid",
) -> dict:
    """use: min, mid, max of code-letter kVA/hp band."""
    rec = get_record(code_id)
    if rec is None:
        raise ValueError(f"unknown code id {code_id}")
    vals = rec["values"]
    lo = float(vals["kva_per_hp_min"])
    hi = float(vals["kva_per_hp_max"])
    kva_per_hp = {"min": lo, "max": hi, "mid": (lo + hi) / 2.0}.get(use, (lo + hi) / 2.0)
    if hp <= 0 or line_voltage_v <= 0:
        raise ValueError("hp and line_voltage_v must be positive")
    kva = kva_per_hp * hp
    i_lr = kva * 1000.0 / (math.sqrt(3.0) * line_voltage_v)
    return {
        "code_id": code_id,
        "hp": hp,
        "line_voltage_v": line_voltage_v,
        "kva_per_hp_used": kva_per_hp,
        "locked_rotor_kva": kva,
        "i_lr_a": i_lr,
        "source_id": code_id,
    }

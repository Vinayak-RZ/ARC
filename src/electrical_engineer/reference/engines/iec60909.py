"""IEC 60909 initial symmetrical short-circuit current (study-level)."""

from __future__ import annotations

import math

from electrical_engineer.reference.catalog import get_record


def initial_symmetrical_ka(
    *,
    voltage_kv: float,
    z_ohm: complex,
    c_factor_id: str = "IEC60909_CMAX_LV",
    kt: float = 1.0,
) -> dict:
    """Ik'' at far-from-generator buses: c * U_n / (sqrt(3) * |Z|) with K_T on transformer Z."""
    if voltage_kv <= 0:
        raise ValueError("voltage_kv must be positive")
    crec = get_record(c_factor_id)
    if crec is None:
        raise ValueError(f"unknown c factor id {c_factor_id}")
    c = float(crec["values"]["c"])
    z_eff = complex(z_ohm) * kt
    if abs(z_eff) < 1e-12:
        raise ValueError("zero impedance")
    ik_a = c * voltage_kv * 1e3 / (math.sqrt(3) * abs(z_eff))
    return {
        "ik_ka": ik_a / 1000.0,
        "c": c,
        "kt": kt,
        "z_ohm": {"re": z_eff.real, "im": z_eff.imag},
        "c_factor_id": c_factor_id,
        "u_kv": voltage_kv,
    }

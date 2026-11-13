"""IEC 60909 peak short-circuit current from Ik'' and kappa."""

from __future__ import annotations

import math

from electrical_engineer.reference.catalog import get_record
from electrical_engineer.reference.engines.iec60909 import initial_symmetrical_ka


def peak_short_circuit_ka(
    *,
    voltage_kv: float,
    z_ohm: complex,
    c_factor_id: str = "IEC60909_CMAX_LV",
    kt: float = 1.0,
    kappa_id: str = "IEC60909_KAPPA_XR10",
) -> dict:
    sym = initial_symmetrical_ka(
        voltage_kv=voltage_kv, z_ohm=z_ohm, c_factor_id=c_factor_id, kt=kt
    )
    krec = get_record(kappa_id)
    if krec is None:
        raise ValueError(f"unknown kappa id {kappa_id}")
    kappa = float(krec["values"]["kappa"])
    ik_pp_ka = sym["ik_ka"]
    ip_ka = kappa * math.sqrt(2.0) * ik_pp_ka
    return {
        **sym,
        "kappa_id": kappa_id,
        "kappa": kappa,
        "ip_ka": ip_ka,
        "formula": "ip = kappa * sqrt(2) * Ik''",
    }

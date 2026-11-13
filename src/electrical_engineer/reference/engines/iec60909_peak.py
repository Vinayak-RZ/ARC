"""IEC 60909 peak short-circuit current from Ik'' and kappa."""

from __future__ import annotations

import math

from electrical_engineer.reference.catalog import get_record
from electrical_engineer.reference.engines.iec60909 import initial_symmetrical_ka

KAPPA_FORMULA = "kappa = 1.02 + 0.98*exp(-3*R/X)"
KAPPA_TABULATED_ID = "IEC60909_KAPPA_XR10"
_RX_MATCH_REL = 0.02


def kappa_from_rx_ratio(rx_ratio: float) -> float:
    if rx_ratio < 0:
        raise ValueError("R/X must be non-negative")
    return 1.02 + 0.98 * math.exp(-3.0 * rx_ratio)


def _resolve_kappa(*, z_ohm: complex, kappa_id: str) -> tuple[float, str, dict]:
    krec = get_record(kappa_id)
    if krec is None:
        raise ValueError(f"unknown kappa id {kappa_id}")
    x_abs = abs(z_ohm.imag)
    if x_abs <= 0:
        raise ValueError("zero reactance: cannot form R/X for kappa")
    rx = max(z_ohm.real, 0.0) / x_abs
    tab_rx = float(krec["values"]["xr_ratio"])
    use_tabulated = kappa_id == KAPPA_TABULATED_ID and abs(rx - tab_rx) <= _RX_MATCH_REL * max(tab_rx, 1e-9)
    if use_tabulated:
        kappa = float(krec["values"]["kappa"])
        method = "catalog_tabulated_XR10"
        note = "Tabulated kappa applies only at X/R≈10 (R/X=0.1)"
    else:
        kappa = kappa_from_rx_ratio(rx)
        method = "IEC60909_figure_formula"
        note = f"Computed for R/X={rx:.4f}; record {kappa_id} is for X/R=10 only"
    return kappa, method, {"rx_ratio": rx, "kappa_method": method, "kappa_note": note, "formula": KAPPA_FORMULA}


def peak_short_circuit_ka(
    *,
    voltage_kv: float,
    z_ohm: complex,
    c_factor_id: str = "IEC60909_CMAX_LV",
    kt: float = 1.0,
    kappa_id: str = KAPPA_TABULATED_ID,
) -> dict:
    sym = initial_symmetrical_ka(
        voltage_kv=voltage_kv, z_ohm=z_ohm, c_factor_id=c_factor_id, kt=kt
    )
    kappa, method, kmeta = _resolve_kappa(z_ohm=z_ohm, kappa_id=kappa_id)
    ik_pp_ka = sym["ik_ka"]
    ip_ka = kappa * math.sqrt(2.0) * ik_pp_ka
    return {
        **sym,
        "kappa_id": kappa_id,
        "kappa": kappa,
        "kappa_method": method,
        **kmeta,
        "ip_ka": ip_ka,
        "formula": "ip = kappa * sqrt(2) * Ik''",
    }

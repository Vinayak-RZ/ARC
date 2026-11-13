"""IEC 60909 peak short-circuit current from Ik'' and kappa."""

from __future__ import annotations

import math

from electrical_engineer.reference.engines.iec60909 import initial_symmetrical_ka

KAPPA_FORMULA = "kappa = 1.02 + 0.98*exp(-3*R/X)"


def kappa_from_rx_ratio(rx_ratio: float) -> float:
    if rx_ratio < 0:
        raise ValueError("R/X must be non-negative")
    if math.isinf(rx_ratio):
        return 1.02
    return 1.02 + 0.98 * math.exp(-3.0 * rx_ratio)


def rx_ratio_from_z(z_ohm: complex) -> float:
    x_abs = abs(z_ohm.imag)
    if x_abs <= 0:
        if z_ohm.real <= 0:
            return 0.0
        return math.inf
    return max(z_ohm.real, 0.0) / x_abs


def peak_short_circuit_ka(
    *,
    voltage_kv: float,
    z_ohm: complex,
    c_factor_id: str = "IEC60909_CMAX_LV",
    kt: float = 1.0,
    kappa_id: str | None = None,
) -> dict:
    sym = initial_symmetrical_ka(
        voltage_kv=voltage_kv, z_ohm=z_ohm, c_factor_id=c_factor_id, kt=kt
    )
    rx = rx_ratio_from_z(z_ohm)
    kappa = kappa_from_rx_ratio(rx)
    ik_pp_ka = sym["ik_ka"]
    ip_ka = kappa * math.sqrt(2.0) * ik_pp_ka
    return {
        **sym,
        "kappa_id": kappa_id,
        "kappa": kappa,
        "rx_ratio": rx if not math.isinf(rx) else None,
        "kappa_method": "IEC60909-0_figure_formula",
        "formula": KAPPA_FORMULA,
        "kappa_note": "Always from IEC 60909-0 kappa(R/X); catalog record is cross-check only",
        "ip_ka": ip_ka,
        "standard_clause": "IEC 60909-0 peak factor kappa(R/X)",
    }

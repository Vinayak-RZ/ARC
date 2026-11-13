"""Transmission line R, L, C from conductor catalog id and geometry."""

from __future__ import annotations

import math

from electrical_engineer.reference.catalog import get_record

MU0 = 4e-7 * math.pi


def _bundled_gmr_m(gmr_m: float, n_bundled: int, spacing_m: float) -> float:
    if n_bundled <= 1:
        return gmr_m
    return (n_bundled * gmr_m * spacing_m ** (n_bundled - 1)) ** (1.0 / n_bundled)


def line_sequence_per_km(
    conductor_id: str,
    *,
    length_km: float,
    spacing_m: float | None = None,
    n_bundled: int = 1,
    freq_hz: float = 50.0,
    temp_c: float | None = None,
) -> dict:
    rec = get_record(conductor_id)
    if rec is None:
        raise ValueError(f"unknown conductor {conductor_id}")
    vals = rec["values"]
    gmr_m = float(vals["gmr_m"])
    spacing = spacing_m if spacing_m is not None else float(vals.get("default_spacing_m", 0.5))
    r_key = None
    if temp_c is not None and abs(temp_c - 75.0) < 0.5 and "r_ac_ohm_per_km_75c" in vals:
        r_key = "r_ac_ohm_per_km_75c"
    elif temp_c is not None and abs(temp_c - 20.0) < 0.5 and "r_ac_ohm_per_km_20c" in vals:
        r_key = "r_ac_ohm_per_km_20c"
    else:
        r_key = "r_ac_ohm_per_km_75c" if "r_ac_ohm_per_km_75c" in vals else "r_ac_ohm_per_km_20c"
    r_per_km = float(vals[r_key])
    gmr_b = _bundled_gmr_m(gmr_m, n_bundled, spacing)
    # L = mu0/(2pi) * ln(GMD/GMR); X_ohm_per_km = 2*pi*f*L with length in km -> factor 1000
    x_per_km = freq_hz * MU0 * math.log(spacing / gmr_b) * 1000.0
    dia_m = float(vals.get("diameter_m", 0.02))
    c_nf_per_km = None
    if "c_nf_per_km_nominal" in vals:
        c_nf_per_km = float(vals["c_nf_per_km_nominal"])
    else:
        # crude parallel-plate equivalent; syllabus prefers named table when present
        c_nf_per_km = 24.0 / math.log(spacing / (dia_m / 2)) if spacing > dia_m / 2 else 10.0
    return {
        "conductor_id": conductor_id,
        "length_km": length_km,
        "r_ohm": r_per_km * length_km,
        "x_ohm": x_per_km * length_km,
        "c_nF": c_nf_per_km * length_km,
        "r_ohm_per_km": r_per_km,
        "x_ohm_per_km": x_per_km,
        "c_nf_per_km": c_nf_per_km,
        "gmr_bundled_m": gmr_b,
        "temp_c_used": temp_c,
        "r_lookup_key": r_key,
        "source_id": conductor_id,
    }

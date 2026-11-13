"""Resistance consistency checks for overhead conductor catalog records."""

from __future__ import annotations

from typing import Any

from electrical_engineer.reference.catalog import get_record, load_catalog

ALPHA_DEFAULT = 0.00403
BASE_TEMP_C = 20.0
TARGET_TEMP_C = 75.0
REL_TOLERANCE = 0.025


def dc_resistance_at_temp(
    r20_ohm_per_km: float, *, temp_c: float, alpha_per_c: float = ALPHA_DEFAULT
) -> float:
    return r20_ohm_per_km * (1.0 + alpha_per_c * (temp_c - BASE_TEMP_C))


def check_conductor_resistance_consistency(
    *,
    rel_tolerance: float = REL_TOLERANCE,
) -> list[dict[str, Any]]:
    """Return inconsistencies; empty if all records pass or document AC/skin basis."""
    issues: list[dict[str, Any]] = []
    alpha_rec = get_record("TEMP_COEFF_AL")
    alpha = float((alpha_rec or {}).get("values", {}).get("alpha_per_c", ALPHA_DEFAULT))
    for rid, rec in load_catalog().items():
        if rec.get("domain") != "overhead_conductors":
            continue
        vals = rec.get("values") or {}
        r20 = vals.get("r_dc_ohm_per_km_20c")
        r75_key = "r_ac_ohm_per_km_75c"
        r75 = vals.get(r75_key)
        if r20 is None or r75 is None:
            continue
        r20_f = float(r20)
        r75_f = float(r75)
        expected = dc_resistance_at_temp(r20_f, temp_c=TARGET_TEMP_C, alpha_per_c=alpha)
        rel_err = abs(r75_f - expected) / expected if expected else float("inf")
        basis = vals.get("r_75c_resistance_basis")
        if rel_err <= rel_tolerance:
            continue
        if basis in ("ac_tabulated_skin_effect", "dc_temperature_corrected"):
            continue
        issues.append(
            {
                "conductor_id": rid,
                "r20_ohm_per_km": r20_f,
                "r75_recorded": r75_f,
                "r75_dc_expected": expected,
                "relative_error": rel_err,
                "message": (
                    f"{rid}: {r75_key} must match R20*(1+alpha*(75-20)) within "
                    f"{rel_tolerance:.1%} or set r_75c_resistance_basis"
                ),
            }
        )
    return issues

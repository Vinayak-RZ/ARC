"""Cross-check catalog tabulated values against closed-form standards formulas."""

from __future__ import annotations

from typing import Any

from electrical_engineer.reference.catalog import get_record
from electrical_engineer.reference.engines.iec60909_peak import kappa_from_rx_ratio
from electrical_engineer.reference.engines.nec_ampacity import ambient_correction_factor

IEEE80_K_EXPECTED = {50: 0.116, 70: 0.157}
KAPPA_RX_TOL = 1e-4


def crosscheck_tabulated_formulas() -> list[dict[str, Any]]:
    """Return mismatches between catalog records and formula-derived values."""
    issues: list[dict[str, Any]] = []
    for mass, k_exp in IEEE80_K_EXPECTED.items():
        rid = f"IEEE80_BODY_{mass}KG"
        rec = get_record(rid)
        if not rec:
            issues.append({"record_id": rid, "message": "missing record"})
            continue
        k = float(rec["values"]["k"])
        if abs(k - k_exp) > 1e-9:
            issues.append(
                {
                    "record_id": rid,
                    "field": "k",
                    "tabulated": k,
                    "formula_expected": k_exp,
                    "message": f"IEEE 80 k for {mass} kg",
                }
            )
    krec = get_record("IEC60909_KAPPA_XR10")
    if krec:
        vals = krec["values"]
        rx = float(vals["xr_ratio"])
        k_tab = float(vals["kappa"])
        k_form = kappa_from_rx_ratio(rx)
        if abs(k_tab - k_form) > KAPPA_RX_TOL:
            issues.append(
                {
                    "record_id": "IEC60909_KAPPA_XR10",
                    "field": "kappa",
                    "tabulated": k_tab,
                    "formula_expected": k_form,
                    "message": f"kappa at R/X={rx}",
                }
            )
    amb45 = ambient_correction_factor(ambient_c=45, insulation_column="90")
    if amb45["ambient_factor"] != 0.87:
        issues.append(
            {
                "record_id": "NEC_TABLE_310_15B1_AMBIENT",
                "field": "factor_90 at 45 C",
                "tabulated": amb45["ambient_factor"],
                "formula_expected": 0.87,
                "message": "NEC ambient 41-45 row at 90 C",
            }
        )
    amb46 = ambient_correction_factor(ambient_c=46, insulation_column="90")
    if amb46["ambient_factor"] != 0.82:
        issues.append(
            {
                "record_id": "NEC_TABLE_310_15B1_AMBIENT",
                "field": "factor_90 at 46 C",
                "tabulated": amb46["ambient_factor"],
                "formula_expected": 0.82,
                "message": "NEC ambient 46-50 row at 90 C",
            }
        )
    return issues


def assert_catalog_formula_consistency() -> None:
    issues = crosscheck_tabulated_formulas()
    if issues:
        detail = "; ".join(i["message"] for i in issues)
        raise AssertionError(f"catalog formula crosscheck failed: {detail}")

"""Regression tests for arc-v4 reference engine fixes."""

from __future__ import annotations

import math

import pytest

from electrical_engineer.reference.catalog import clear_catalog_cache
from electrical_engineer.reference.conductors import check_conductor_resistance_consistency
from electrical_engineer.reference.engines.iec60909_peak import (
    kappa_from_rx_ratio,
    peak_short_circuit_ka,
)
from electrical_engineer.reference.engines.ieee80 import tolerable_voltage
from electrical_engineer.reference.engines.ieee519 import tdd_limit_percent
from electrical_engineer.web_verify.citations import append_standard_formula_lines


@pytest.fixture(autouse=True)
def _fresh_catalog() -> None:
    clear_catalog_cache()


@pytest.mark.parametrize(
    ("kind", "body_kg", "k"),
    [
        ("touch", 50, 0.116),
        ("step", 50, 0.116),
        ("touch", 70, 0.157),
        ("step", 70, 0.313),
    ],
)
def test_ieee80_four_kind_body_combinations(kind: str, body_kg: int, k: float) -> None:
    rho, cs, t = 250.0, 1.0, 0.35
    out = tolerable_voltage(kind=kind, body_mass_kg=body_kg, rho_s_ohm_m=rho, cs=cs, t_s=t)
    assert out["kind"] == kind
    assert out["body_mass_kg"] == body_kg
    rs_coeff = 1.5 if kind == "touch" else 6.0
    expected = (1000.0 + rs_coeff * cs * rho) * k / math.sqrt(t)
    assert out["e_v"] == pytest.approx(expected, rel=1e-6)
    assert out["inputs_used"]["kind"] == kind
    assert out["inputs_used"]["body_mass_kg"] == body_kg


def test_ieee80_blind_exam_step_50kg() -> None:
    out = tolerable_voltage(kind="step", body_mass_kg=50, rho_s_ohm_m=250.0, cs=1.0, t_s=0.35)
    assert out["e_v"] == pytest.approx(490.2, rel=1e-3)


def test_ieee80_requires_kind_and_mass() -> None:
    with pytest.raises(ValueError, match="kind"):
        tolerable_voltage(kind="bad", body_mass_kg=50, rho_s_ohm_m=100.0, cs=1.0, t_s=1.0)
    with pytest.raises(ValueError, match="body_mass_kg"):
        tolerable_voltage(kind="touch", body_mass_kg=60, rho_s_ohm_m=100.0, cs=1.0, t_s=1.0)


@pytest.mark.parametrize(
    ("ratio", "limit", "band"),
    [
        (15.0, 5.0, "IEEE519_TDD_BAND_LT20"),
        (20.0, 8.0, "IEEE519_TDD_BAND_20_50"),
        (50.0, 12.0, "IEEE519_TDD_BAND_50_100"),
        (100.0, 15.0, "IEEE519_TDD_BAND_100_1000"),
        (1000.0, 20.0, "IEEE519_TDD_BAND_GT1000"),
        (1500.0, 20.0, "IEEE519_TDD_BAND_GT1000"),
    ],
)
def test_ieee519_table2_boundaries(ratio: float, limit: float, band: str) -> None:
    out = tdd_limit_percent(isc_il_ratio=ratio)
    assert out["tdd_limit_percent"] == limit
    assert out["ratio_id"] == band
    assert "IEEE 519-2022 Table 2" in out["table_row_label"]


def test_iec60909_kappa_tabulated_only_at_xr10() -> None:
    z = 0.05 + 0.5j
    peak = peak_short_circuit_ka(voltage_kv=11.0, z_ohm=z)
    assert peak["kappa_method"] == "catalog_tabulated_XR10"
    assert peak["kappa"] == pytest.approx(1.632, rel=1e-4)
    z2 = 0.1 + 0.2j
    peak2 = peak_short_circuit_ka(voltage_kv=11.0, z_ohm=z2)
    assert peak2["kappa_method"] == "IEC60909_figure_formula"
    rx = 0.1 / 0.2
    assert peak2["kappa"] == pytest.approx(kappa_from_rx_ratio(rx), rel=1e-9)
    assert peak2["kappa"] != peak["kappa"]


def test_conductor_catalog_resistance_consistency() -> None:
    issues = check_conductor_resistance_consistency()
    assert issues == [], issues


def test_web_verify_standard_formula_section() -> None:
    lines: list[str] = ["Answer line"]
    append_standard_formula_lines(
        lines,
        {
            "standard_clause": "IEEE Std 80-2013 Eq. 32",
            "inputs_used": {"kind": "step", "body_mass_kg": 50, "t_s": 0.35},
            "e_v": 490.2,
        },
    )
    text = "\n".join(lines)
    assert "Standard formula check" in text
    assert "Eq. 32" in text
    assert "body_mass_kg=50" in text

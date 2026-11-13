"""Golden tests for NEC 310.16 + 310.15(B)(1) + 310.15(C)(1) engine."""

from __future__ import annotations

import pytest

from electrical_engineer.reference.catalog import clear_catalog_cache
from electrical_engineer.reference.engines.nec_ampacity import (
    allowable_ampacity,
    ambient_correction_factor,
)


@pytest.fixture(autouse=True)
def _fresh_catalog() -> None:
    clear_catalog_cache()


def test_exam_v6_three_awg_thwn2_45c_8ccc() -> None:
    """Exam v6 miss case: 3 AWG Cu THWN-2 90 C column, 45 C ambient, 8 CCC -> 70 A."""
    out = allowable_ampacity(
        size_awg="3",
        material="cu",
        insulation_column="90",
        ambient_c=45,
        n_current_carrying=8,
    )
    assert out["base_ampacity_a"] == 115
    assert out["ambient_factor"] == 0.87
    assert out["adjustment_factor"] == 0.70
    assert out["corrected_ampacity_a"] == pytest.approx(115 * 0.87 * 0.70, rel=1e-9)
    assert out["allowable_ampacity_a"] == 70


def test_four_awg_40c_4_to_6_conductors() -> None:
    out = allowable_ampacity(
        size_awg="4 AWG",
        material="copper",
        insulation_column="90",
        ambient_c=40,
        n_current_carrying=5,
    )
    assert out["base_ampacity_a"] == 95
    assert out["ambient_factor"] == 0.91
    assert out["adjustment_factor"] == 0.80
    assert out["allowable_ampacity_a"] == 69


@pytest.mark.parametrize(
    ("ambient_c", "factor"),
    [(45, 0.87), (46, 0.82)],
)
def test_ambient_band_edges_inclusive(ambient_c: int, factor: float) -> None:
    out = ambient_correction_factor(ambient_c=ambient_c, insulation_column="90")
    assert out["ambient_factor"] == factor

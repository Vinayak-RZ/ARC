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
    assert out["ampacity_record_id"] == "NEC_TABLE_310_16_CU_90C"
    assert out["ambient_record_id"] == "NEC_TABLE_310_15B1_AMBIENT"
    assert out["adjustment_record_id"] == "NEC_TABLE_310_15C1_ADJUSTMENT"
    assert "record_id" not in out
    assert "boundary_policy" not in out


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


def test_non_integer_ambient_raises_without_round_mode() -> None:
    with pytest.raises(ValueError, match="whole degree"):
        allowable_ampacity(
            size_awg="3",
            material="cu",
            insulation_column="90",
            ambient_c=45.6,
            n_current_carrying=8,
        )


def test_non_integer_ambient_round_up_uses_conservative_band() -> None:
    """45.6 C with round_ambient=up -> 46 C band (0.82), lower than 45 C (0.87)."""
    out = allowable_ampacity(
        size_awg="3",
        material="cu",
        insulation_column="90",
        ambient_c=45.6,
        n_current_carrying=8,
        round_ambient="up",
    )
    assert out["ambient_c"] == 46
    assert out["ambient_c_given"] == 45.6
    assert out["ambient_factor"] == 0.82
    assert out["allowable_ampacity_a"] == 66

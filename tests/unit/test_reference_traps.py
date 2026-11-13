"""Regression traps for reference-backed engines (eval-aligned)."""

from electrical_engineer.reference.catalog import clear_catalog_cache
from electrical_engineer.reference.engines.idmt import idmt_operating_time_s
from electrical_engineer.reference.engines.line_params import line_sequence_per_km


def setup_function() -> None:
    clear_catalog_cache()
from electrical_engineer.reference.engines.vector_group import phase_shift_deg


def test_iec_vs_ieee_curve_divergence_at_same_multiple() -> None:
    iec = idmt_operating_time_s("IEC_SI", tms=1.0, i_ratio=5.0)["time_s"]
    ieee = idmt_operating_time_s("IEEE_CO8", tms=1.0, i_ratio=5.0)["time_s"]
    assert iec != ieee


def test_conductor_temp_key_changes_r() -> None:
    at75 = line_sequence_per_km("ACSR_ZEBRA", length_km=1.0, temp_c=75.0)
    assert at75["r_lookup_key"] == "r_ac_ohm_per_km_75c"
    dog = line_sequence_per_km("ACSR_DOG", length_km=1.0, temp_c=75.0)
    assert dog["r_ohm_per_km"] > at75["r_ohm_per_km"]


def test_dyn11_not_positive_30() -> None:
    dyn = phase_shift_deg(group_id="VECTOR_DYN11")["phase_shift_hv_to_lv_deg"]
    yd = phase_shift_deg(group_id="VECTOR_YD1")["phase_shift_hv_to_lv_deg"]
    assert dyn == -30.0
    assert yd == 30.0
    assert dyn != yd

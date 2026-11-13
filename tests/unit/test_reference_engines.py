import math

import pytest

from electrical_engineer.reference.engines.idmt import idmt_operating_time_s
from electrical_engineer.reference.engines.iec60909 import initial_symmetrical_ka
from electrical_engineer.reference.engines.ieee80 import tolerable_voltages
from electrical_engineer.reference.engines.ieee519 import tdd_limit_percent
from electrical_engineer.reference.engines.line_params import line_sequence_per_km
from electrical_engineer.reference.engines.load_flow import run_case_load_flow
from electrical_engineer.reference.engines.mcb import magnetic_trip_in_band
from electrical_engineer.reference.engines.vector_group import phase_shift_deg


def test_iec_si_idmt_hand_math() -> None:
    m = 10.0
    tms = 1.0
    expected = 0.14 * tms / (m**0.02 - 1.0)
    out = idmt_operating_time_s("IEC_SI", tms=tms, i_ratio=m)
    assert out["time_s"] == pytest.approx(expected, rel=1e-9)


def test_iect60909_symmetrical() -> None:
    z = 0.5 + 0j
    u = 11.0
    c = 1.1
    ik = c * u * 1e3 / (math.sqrt(3) * abs(z)) / 1000.0
    out = initial_symmetrical_ka(voltage_kv=u, z_ohm=z, c_factor_id="IEC60909_CMAX_LV")
    assert out["ik_ka"] == pytest.approx(ik, rel=1e-6)


def test_line_params_zebra_length() -> None:
    out = line_sequence_per_km("ACSR_ZEBRA", length_km=1.0, spacing_m=0.6, temp_c=75.0)
    assert out["r_ohm_per_km"] == pytest.approx(0.0789, rel=1e-3)
    assert out["r_ohm"] == pytest.approx(0.0789, rel=1e-3)
    assert out["gmr_bundled_m"] == pytest.approx(0.01058, rel=1e-3)


def test_ieee519_band() -> None:
    out = tdd_limit_percent(isc_il_ratio=35.0)
    assert out["tdd_limit_percent"] == 8.0


def test_ieee80_touch_step_same() -> None:
    out = tolerable_voltages(rho_s_ohm_m=100.0, cs=1.0, t_s=1.0)
    expected = (1000.0 + 1.5 * 1.0 * 100.0) * 0.157 / math.sqrt(1.0)
    assert out["e_step_v"] == pytest.approx(expected, rel=1e-6)


def test_mcb_type_c_band() -> None:
    out = magnetic_trip_in_band(mcb_type_id="MCB_TYPE_C", i_a=80.0, rated_in_a=16.0)
    assert out["in_magnetic_band"] is True


def test_dyn11_negative_shift_trap() -> None:
    out = phase_shift_deg(group_id="VECTOR_DYN11")
    assert out["phase_shift_hv_to_lv_deg"] == -30.0


def test_load_flow_case14() -> None:
    out = run_case_load_flow("IEEE_CASE_14")
    if out.get("unchecked"):
        pytest.skip("pandapower not installed")
    assert out["converged"] is True
    assert out["bus_count"] == 14

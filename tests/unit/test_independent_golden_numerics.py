"""Ground-truth numerics: closed forms and engine parity (independent test engineer)."""

from __future__ import annotations

import math

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from electrical_engineer.control_studio.goldens import GOLDENS
from electrical_engineer.control_studio.simulate import simulate
from electrical_engineer.engines.rlc_transient import series_rlc_step
from electrical_engineer.engines.solvers.power import idmt_relay_time
from electrical_engineer.engines.solvers.power_electronics import rectifier_3ph
from tests.golden_numerics_refs import (
    HEADLINE_CONTROL_TS_S,
    HEADLINE_CONTROL_Y_SS,
    HEADLINE_IDMT_T_S,
    HEADLINE_RECTIFIER_VO_V,
    HEADLINE_RLC_C_F,
    HEADLINE_RLC_L_H,
    HEADLINE_RLC_R_OHM,
    HEADLINE_RLC_T_PEAK_S,
    HEADLINE_RLC_VC_PEAK_V,
    HEADLINE_RLC_VIN,
    HEADLINE_RLC_WN_RAD_S,
    HEADLINE_RLC_ZETA,
    hw3_discontinuous_vo_v,
)


def test_headline_series_rlc_zeta_wn_peak_time() -> None:
    r = series_rlc_step(HEADLINE_RLC_R_OHM, HEADLINE_RLC_L_H, HEADLINE_RLC_C_F, HEADLINE_RLC_VIN)
    assert abs(r["zeta"] - HEADLINE_RLC_ZETA) < 1e-6
    assert abs(r["omega_n_rad_s"] - HEADLINE_RLC_WN_RAD_S) < 1.0
    assert abs(r["Vc_peak_V"] - HEADLINE_RLC_VC_PEAK_V) < 0.01
    assert abs(r["t_Vc_peak_s"] - HEADLINE_RLC_T_PEAK_S) < 0.05e-3
    zeta = HEADLINE_RLC_ZETA
    exact_peak = HEADLINE_RLC_VIN * (1.0 + math.exp(-math.pi * zeta / math.sqrt(1.0 - zeta**2)))
    assert abs(r["Vc_peak_V"] - exact_peak) < 0.01


def test_three_phase_hw3_rectifier_discontinuous_alpha_45() -> None:
    vo = hw3_discontinuous_vo_v(415.0, 45.0)
    assert abs(vo - HEADLINE_RECTIFIER_VO_V) < 0.5


def test_rectifier_3ph_half_discontinuous_matches_ui_at_45() -> None:
    out = rectifier_3ph(415.0, 45.0, "half")
    ref = hw3_discontinuous_vo_v(415.0, 45.0)
    assert abs(out["Vo_V"] - ref) < 0.5
    assert abs(out["Vo_V"] - HEADLINE_RECTIFIER_VO_V) < 0.5


def test_rectifier_3ph_half_continuous_below_30_deg() -> None:
    alpha = 20.0
    vm = math.sqrt(2) * 415.0 / math.sqrt(3)
    expected = (3.0 * math.sqrt(3) * vm / (2.0 * math.pi)) * math.cos(math.radians(alpha))
    out = rectifier_3ph(415.0, alpha, "half")
    assert abs(out["Vo_V"] - expected) < 0.5


def test_rectifier_3ph_half_switches_at_30_deg_boundary() -> None:
    at_30 = rectifier_3ph(415.0, 30.0, "half")["Vo_V"]
    above = rectifier_3ph(415.0, 30.1, "half")["Vo_V"]
    vm = math.sqrt(2) * 415.0 / math.sqrt(3)
    cont_30 = (3.0 * math.sqrt(3) * vm / (2.0 * math.pi)) * math.cos(math.radians(30.0))
    disc_301 = hw3_discontinuous_vo_v(415.0, 30.1)
    assert abs(at_30 - cont_30) < 0.6
    assert abs(above - disc_301) < 0.6
    assert above < at_30


def test_unity_feedback_k10_step_ss_and_settling() -> None:
    pytest.importorskip("control")
    diagram = GOLDENS["unity_first_order"]()
    out = simulate(diagram)
    assert out.get("ok")
    y_ss = float(out["y_ss"])
    assert abs(y_ss - HEADLINE_CONTROL_Y_SS) < 0.02
    t_s = out.get("t_settle_s") or out.get("settling_time_s")
    if t_s is not None:
        assert abs(float(t_s) - HEADLINE_CONTROL_TS_S) < 0.08


def test_iec_standard_inverse_idmt_psm10_tms1() -> None:
    out = idmt_relay_time(
        i_fault_a=1000.0,
        ct_primary_a=100.0,
        tms=1.0,
        curve="standard",
        plug_setting=1.0,
    )
    assert abs(out["psm"] - 10.0) < 1e-6
    assert abs(out["t_op_s"] - HEADLINE_IDMT_T_S) < 0.01


@given(
    r_ohm=st.floats(min_value=5.0, max_value=200.0, allow_nan=False, allow_infinity=False),
    l_h=st.floats(min_value=1e-4, max_value=0.05, allow_nan=False, allow_infinity=False),
    c_f=st.floats(min_value=1e-7, max_value=1e-4, allow_nan=False, allow_infinity=False),
)
@settings(max_examples=20, deadline=2000)
def test_rlc_zeta_energy_sign_sanity(r_ohm: float, l_h: float, c_f: float) -> None:
    wn = 1.0 / math.sqrt(l_h * c_f)
    zeta = (r_ohm / 2.0) * math.sqrt(c_f / l_h)
    assert wn > 0
    assert zeta >= 0
    zeta2 = (r_ohm / 2.0) / math.sqrt(l_h / c_f)
    assert abs(zeta - zeta2) < 1e-9 * max(1.0, zeta)


@given(
    r_ohm=st.floats(min_value=10.0, max_value=200.0, allow_nan=False, allow_infinity=False),
)
@settings(max_examples=25, deadline=None)
def test_voltage_divider_monotone_in_r1(r_ohm: float) -> None:
    v1 = 10.0 * 1000.0 / (r_ohm + 1000.0)
    v2 = 10.0 * 1000.0 / (r_ohm * 1.5 + 1000.0)
    assert v1 >= v2
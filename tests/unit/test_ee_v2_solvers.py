from __future__ import annotations

import math

from electrical_engineer.engines.ed_lambda import EdCase
from electrical_engineer.engines.ee_v2_solvers import (
    breakaway_real_axis,
    ccm_buck,
    dc_motor_shunt,
    ed_with_losses,
    induction_air_gap_split,
    load_flow_json,
    phasor_pfc,
    rc_step,
    rl_step,
    rlc_natural,
    steady_state_error_type,
    three_phase_balanced,
    transformer_regulation,
    z_inverse,
)


def test_rc_step_one_tau() -> None:
    r = rc_step(10.0, 1000.0, 1e-3, 1.0)
    assert abs(r["tau_s"] - 1.0) < 1e-9
    assert abs(r["vc_V"] - 10.0 * (1.0 - math.exp(-1.0))) < 1e-6
    assert abs(r["i_A"] - 10.0 * math.exp(-1.0) / 1000.0) < 1e-6


def test_rl_step_one_tau() -> None:
    r = rl_step(12.0, 4.0, 0.5, 0.125)
    assert abs(r["tau_s"] - 0.125) < 1e-9
    assert abs(r["i_A"] - 3.0 * (1.0 - math.exp(-1.0))) < 1e-6


def test_rlc_natural_parallel_underdamped() -> None:
    r = rlc_natural(200.0, 0.1, 1e-5, 12.0, 0.05, 0.001)
    assert r["damping"] == "underdamped"
    assert r["topology"] == "parallel"
    assert abs(r["zeta"] - 0.25) < 1e-9
    assert abs(r["vc_V"] + 0.004949) < 1e-3


def test_phasor_pfc_series_rl() -> None:
    z = complex(10.0, 10.0)
    r = phasor_pfc(400.0, z)
    v_ph = 400.0 / math.sqrt(3.0)
    z_mag_sq = 200.0
    assert abs(r["V_phase_V"] - v_ph) < 1e-6
    assert abs(r["P_W"] - 3.0 * v_ph * v_ph * 10.0 / z_mag_sq) < 1e-3
    assert abs(r["Q_VAR"] - 3.0 * v_ph * v_ph * 10.0 / z_mag_sq) < 1e-3
    assert abs(r["Q_c_for_unity_VAR"] + r["Q_VAR"]) < 1e-6


def test_three_phase_wye_power() -> None:
    r = three_phase_balanced(230.0, 10.0, connection="wye")
    assert abs(r["V_line_V"] - 230.0 * math.sqrt(3.0)) < 1e-6
    assert abs(r["P_W"] - math.sqrt(3.0) * r["V_line_V"] * 10.0) < 1e-3


def test_three_phase_delta_power() -> None:
    r = three_phase_balanced(400.0, 5.0, connection="delta")
    assert abs(r["V_line_V"] - 400.0) < 1e-6
    assert abs(r["I_line_A"] - 5.0 * math.sqrt(3.0)) < 1e-6
    p = math.sqrt(3.0) * 400.0 * 5.0 * math.sqrt(3.0)
    assert abs(r["P_W"] - p) < 1e-3


def test_transformer_regulation_lag_pf() -> None:
    r = transformer_regulation(11000.0, 0.01, 0.05, 0.8, 1.0)
    sin_phi = 0.6
    reg_frac = 0.01 * 0.8 + 0.05 * sin_phi
    assert abs(r["regulation_fraction"] - reg_frac) < 1e-9
    assert abs(r["regulation_percent"] - 100.0 * reg_frac) < 1e-6
    assert abs(r["V_full_load_V"] - 11000.0 * (1.0 - reg_frac)) < 1e-3


def test_dc_motor_shunt_steady() -> None:
    r = dc_motor_shunt(120.0, 2.0, 0.1, 0.1, 1.0)
    assert abs(r["Ia_A"] - 10.0) < 1e-9
    assert abs(r["omega_rad_s"] - 1000.0) < 1e-6
    assert abs(r["Ea_V"] - 100.0) < 1e-6


def test_induction_air_gap_split() -> None:
    r = induction_air_gap_split(10_000.0, 0.04, 0.5)
    assert abs(r["P_rotor_copper_W"] - 400.0) < 1e-6
    assert abs(r["P_mech_W"] - 9600.0) < 1e-6


def test_ccm_buck_duty_and_l() -> None:
    r = ccm_buck(12.0, 5.0, 100e-6, 47e-6, 100e3, 30.0, i_out=2.0)
    d = 5.0 / 12.0
    assert abs(r["D"] - d) < 1e-9
    delta_i = (12.0 - 5.0) * d / (100e-6 * 100e3)
    assert abs(r["delta_I_A"] - delta_i) < 1e-6
    l_min = (12.0 - 5.0) * (1.0 - d) / (2.0 * 100e3 * 2.0)
    assert abs(r["L_min_CCM_H"] - l_min) < 1e-9


def test_ed_with_losses_penalty_not_naive_pd() -> None:
    case = EdCase.eec301_default()
    b_full = [
        [1e-4, 2e-5, 1e-5],
        [2e-5, 1.5e-4, 2e-5],
        [1e-5, 2e-5, 1.2e-4],
    ]
    r = ed_with_losses(case, b_full, 500.0)
    assert r["P_loss"] > 0.0
    assert abs(r["sum_P_minus_loss"] - 500.0) < 0.5
    limits = case.units
    for i in range(3):
        u = limits[i]
        if u.pmin < r["P"][i] < u.pmax:
            assert abs(r["IC"][i] * r["penalty_factor"][i] - r["lam"]) < 0.05


def test_load_flow_json_dc_two_bus() -> None:
    net = {
        "force_dc": True,
        "buses": [{"id": 0, "type": "slack"}, {"id": 1, "type": "pq"}],
        "lines": [{"from": 0, "to": 1, "x_pu": 0.2}],
        "loads": [{"bus": 1, "p_mw": 2.0}],
    }
    r = load_flow_json(net)
    assert r["ok"] is True
    assert r["tool"] == "dc-approx"
    assert abs(r["buses"][1]["va_degree"] - math.degrees(-0.4)) < 1e-3


def test_z_inverse_first_order() -> None:
    r = z_inverse({"den": [1.0, -0.5], "num": [1.0]})
    assert len(r["poles_z_inv"]) == 1
    assert abs(r["poles_z_inv"][0]["re"] - 0.5) < 1e-9


def test_breakaway_three_pole_locus() -> None:
    pts = breakaway_real_axis(poles=[0.0, -3.0, -6.0], zeros=[])
    assert any(-3.0 < p < 0.0 and abs(p + 1.268) < 0.05 for p in pts)


def test_steady_state_errors() -> None:
    t0 = steady_state_error_type(0, 9.0)
    assert abs(t0["ess_step"] - 0.1) < 1e-9
    t1 = steady_state_error_type(1, 4.0)
    assert t1["ess_step"] == 0.0
    assert abs(t1["ess_ramp"] - 0.25) < 1e-9
    t2 = steady_state_error_type(2, 2.0)
    assert abs(t2["ess_parabolic"] - 0.5) < 1e-9

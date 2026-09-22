"""Golden numerics for EEC-301 Exp 6 SMIB (equal-area + CCT)."""

from __future__ import annotations

import math

from electrical_engineer.engines.eec301_goldens import load_exp06_golden
from electrical_engineer.engines.smib_swing import (
    SmibCase,
    critical_clearing_time_bisection,
    eec301_reference,
    initial_angle_pre_fault,
    simulate_clearing,
    swing_derivative,
    time_to_angle_during_fault,
)


def _exp06() -> dict:
    return load_exp06_golden()


def test_exp06_equal_area_matches_lab_json() -> None:
    gold = _exp06()["equal_area"]
    ref = eec301_reference()
    assert abs(ref["delta0_deg"] - gold["delta0_deg"]) < 1e-9
    assert abs(ref["delta_cr_deg"] - gold["delta_cr_deg"]) < 1e-9
    assert abs(ref["delta_max_deg"] - gold["deltamax_deg"]) < 1e-9
    assert abs(ref["cos_delta_cr"] - gold["cos_delta_cr"]) < 1e-9
    assert abs(ref["delta0_deg"] - 26.743683950403007) < 1e-9
    assert abs(ref["delta_cr_deg"] - 79.53240997193419) < 1e-9


def test_exp06_cct_time_to_delta_cr_matches_lab_json() -> None:
    gold = _exp06()
    case = SmibCase()
    dcr = gold["equal_area"]["delta_cr_rad"]
    h = float(gold["time_to_delta_cr"]["h"])
    expected_t = gold["time_to_delta_cr"]["t_to_dcr"]
    t_at = time_to_angle_during_fault(case, dcr, h_s=h, integrator="rk4")
    assert t_at is not None
    assert abs(t_at - expected_t) < 1e-4
    assert abs(t_at - 0.309688) < 0.0001


def test_exp06_cct_bisection_lab_value_documented() -> None:
    """Lab pack bisection golden (PDF table 0.3097 s); kernel bisection may differ slightly."""
    gold = _exp06()["cct_bisection"]
    assert abs(gold["tcr_s"] - 0.3096875) < 1e-9
    case = SmibCase()
    t_kernel = critical_clearing_time_bisection(case, h_s=0.001, tol_s=gold["tol_s"], t_hi=0.35)
    assert abs(t_kernel - gold["tcr_s"]) < 0.002


def test_swing_rhs_accel_coeff_trap_t3() -> None:
    case = SmibCase()
    expected = math.pi * case.f0_hz / case.h_mj_mva
    assert case.accel_coeff() == expected
    d0 = initial_angle_pre_fault(case)
    _, domega0 = swing_derivative(d0, 0.0, case.pmax_pre_pu, case)
    assert abs(domega0) < 1e-12


def test_integrators_rk4_delta_at_030_matches_lab() -> None:
    gold = _exp06()["reference"]
    case = SmibCase()
    out = simulate_clearing(case, 0.15, 0.01, 0.30, "rk4")
    trail = out["trail"]
    pt = min(trail, key=lambda p: abs(p[0] - 0.30))
    delta_deg = math.degrees(pt[1])
    assert abs(delta_deg - gold["delta_0p30_deg"]) < 0.01


def test_tc_032_unstable_rk4() -> None:
    verdict = next(r for r in _exp06()["tc_sweep_rk4"] if r["tc"] == 0.32)
    assert verdict["verdict"].startswith("Unstable")
    out = simulate_clearing(SmibCase(), 0.32, 0.001, 2.0, "rk4")
    assert out["unstable"] is True

"""Golden numerics for EEC-301 Exp 6 SMIB (equal-area + CCT)."""

from __future__ import annotations

import math

from electrical_engineer.engines.smib_swing import (
    SmibCase,
    critical_clearing_time_bisection,
    eec301_reference,
    simulate_clearing,
    time_to_angle_during_fault,
)


def test_eec301_equal_area_reference() -> None:
    ref = eec301_reference()
    assert abs(ref["delta0_deg"] - 26.74) < 0.05
    assert abs(ref["delta_max_deg"] - 143.13) < 0.05
    assert abs(ref["delta_cr_deg"] - 79.53) < 0.05
    assert abs(ref["cos_delta_cr"] - 0.1817) < 0.002


def test_eec301_cct_bisection_matches_lab() -> None:
    case = SmibCase()
    tcr = critical_clearing_time_bisection(case, h_s=0.0005, tol_s=0.0001, t_hi=0.35)
    assert abs(tcr - 0.3097) < 0.002
    dcr = eec301_reference(case)["delta_cr_rad"]
    t_at = time_to_angle_during_fault(case, dcr, h_s=0.0005)
    assert t_at is not None
    assert abs(t_at - tcr) < 0.003


def test_integrators_bracket_rk4_at_tc_015() -> None:
    """Stable tc=0.15 s: all three methods give finite peak < 180°."""
    case = SmibCase()
    tc = 0.15
    h = 0.01
    for method in ("euler", "modified_euler", "rk4"):
        out = simulate_clearing(case, tc, h, 2.0, method)
        assert out["unstable"] is False
        assert out["peak_delta_rad"] < math.pi


def test_tc_032_unstable_rk4() -> None:
    out = simulate_clearing(SmibCase(), 0.32, 0.001, 2.0, "rk4")
    assert out["unstable"] is True

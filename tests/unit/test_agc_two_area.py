"""Golden checks for EEC-301 Exp 7 two-area AGC twin."""

from __future__ import annotations

from electrical_engineer.engines.agc_two_area import TwoAreaAgcCase, simulate_two_area
from electrical_engineer.engines.eec301_goldens import load_exp07_golden


def test_primary_steady_matches_exp07() -> None:
    gold = load_exp07_golden()
    case = TwoAreaAgcCase.eec301_default()
    out = simulate_two_area(case, run="primary", t_end_s=30.0)
    st = out["steady"]
    ref = gold["run1_primary"]["steady"]
    assert abs(st["df1_hz"] - ref["df1_Hz"]) < 0.002
    assert abs(st["P12_MW"] - ref["P12_MW"]) < 0.5
    assert abs(st["Pm1_MW"] - ref["Pm1_MW"]) < 0.5


def test_agc_steady_frequency_and_tie_near_zero() -> None:
    gold = load_exp07_golden()
    case = TwoAreaAgcCase.eec301_default().with_k(0.3)
    out = simulate_two_area(case, run="agc", t_end_s=60.0)
    st = out["steady"]
    ref = gold["run2_agc"]["steady"]
    assert abs(st["df1_hz"] - ref["df1_Hz"]) < 1e-4
    assert abs(st["P12_MW"] - ref["P12_MW"]) < 0.01
    assert abs(st["Pm1_MW"] - 100.0) < 0.05


def test_agc_first_dip_and_peak_tie() -> None:
    gold = load_exp07_golden()
    case = TwoAreaAgcCase.eec301_default().with_k(0.3)
    out = simulate_two_area(case, run="agc", t_end_s=60.0)
    dip = out["first_dip"]
    peak = out["peak_P12"]
    assert abs(dip["f1_Hz"] - gold["run2_agc"]["first_dip"]["f1_Hz"]) < 0.002
    assert abs(peak["P12_MW"] - gold["run2_agc"]["peak_P12"]["P12_MW"]) < 0.05


def test_gain_one_diverges() -> None:
    gold = load_exp07_golden()
    row = next(r for r in gold["run4_gain_sweep"] if r["K"] == 1.0)
    case = TwoAreaAgcCase.eec301_default()
    out = simulate_two_area(case.with_k(1.0), run="agc", t_end_s=60.0)
    assert row["diverged"] is True
    assert out["diverged"] is True

import math

from electrical_engineer.engines.rlc_transient import series_rlc_step


def test_p6_sheet_rlc() -> None:
    r = series_rlc_step(4.0, 0.5, 0.02, 12.0)
    assert r["damping_type"] == "underdamped"
    assert abs(r["Vc_peak_V"] - 15.045920575021169) < 0.01
    assert abs(r["t_Vc_peak_s"] - 0.3428) < 0.01
    assert abs(r["settling_time_2pct_s"] - 0.8409) < 0.02


def test_home_example_rlc_peak() -> None:
    """R=10 Ω, L=10 mH, C=100 µF, 10 V step — checked headline example."""
    r = series_rlc_step(10.0, 0.01, 100e-6, 10.0)
    zeta = 0.5
    wn = 1000.0
    exact_peak = 10.0 * (1.0 + math.exp(-math.pi * zeta / math.sqrt(1.0 - zeta**2)))
    assert abs(r["Vc_peak_V"] - exact_peak) < 0.01
    assert abs(r["Vc_peak_V"] - 11.630) < 0.01
    assert abs(r["t_Vc_peak_s"] - 3.628e-3) < 0.05e-3

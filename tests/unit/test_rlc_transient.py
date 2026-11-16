from electrical_engineer.engines.rlc_transient import series_rlc_step


def test_series_rlc_headline_closed_form() -> None:
    """Critique P0-5: R=10 Ω, L=10 mH, C=100 µF, 10 V step."""
    r = series_rlc_step(10.0, 0.01, 100e-6, 10.0)
    assert abs(r["Vc_peak_V"] - 11.630) < 0.01
    assert abs(r["t_Vc_peak_s"] - 0.003628) < 0.00005


def test_p6_sheet_rlc() -> None:
    r = series_rlc_step(4.0, 0.5, 0.02, 12.0)
    assert r["damping_type"] == "underdamped"
    assert abs(r["Vc_peak_V"] - 15.045920575021169) < 0.01
    assert abs(r["t_Vc_peak_s"] - 0.3428) < 0.01
    assert abs(r["settling_time_2pct_s"] - 1.1837) < 0.05

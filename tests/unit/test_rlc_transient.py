from electrical_engineer.engines.rlc_transient import series_rlc_step


def test_p6_sheet_rlc() -> None:
    r = series_rlc_step(4.0, 0.5, 0.02, 12.0)
    assert r["damping_type"] == "underdamped"
    assert abs(r["Vc_peak_V"] - 15.045920575021169) < 0.01
    assert abs(r["t_Vc_peak_s"] - 0.3428) < 0.01
    assert abs(r["settling_time_2pct_s"] - 0.8409) < 0.02

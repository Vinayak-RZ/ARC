from electrical_engineer.engines.agc_two_area import primary_response_from_load_step


def test_p4_sheet_f0_50() -> None:
    s = primary_response_from_load_step(50.0, beta1=21.0, beta2=21.0, f0_hz=50.0, s_base_mva=1000.0)
    assert abs(s["df_hz"] - (-0.05952380952380953)) < 1e-6
    assert abs(s["P12_MW"] - (-25.0)) < 1e-6

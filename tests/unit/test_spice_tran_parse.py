from electrical_engineer.engines.spice_runner import _parse_tran_series


def test_parse_ngspice_print_tran_table() -> None:
    stdout = """
Index   time            v(3)
0       0.000000e+00    0.000000e+00
1       8.706240e-06    1.234560e-01
2       3.627599e-03    1.162500e+01
"""
    rows = _parse_tran_series(stdout, "v(3)")
    assert len(rows) >= 2
    peak = max(v for _, v in rows)
    assert abs(peak - 11.625) < 0.1

def test_parse_print_all_uses_header_columns() -> None:
    # `print all v(3)` emits every node; time is column 1, v(3) is the last column.
    stdout = """
Index   time            V(1)            V(2)            V(3)
--------------------------------------------------------------------------------
0\t1.000000e-14\t1.000000e-01\t1.000000e-01\t1.000000e-23\t
1\t3.627599e-03\t1.000000e+01\t9.999167e+00\t1.163034e+01\t
Index   time            V(1)            V(2)            V(3)
--------------------------------------------------------------------------------
2\t5.000000e-03\t1.000000e+01\t1.000000e+01\t1.100000e+01\t
"""
    rows = _parse_tran_series(stdout, "v(3)")
    assert [r[0] for r in rows] == [1e-14, 3.627599e-03, 5e-03]
    t_peak, v_peak = max(rows, key=lambda r: r[1])
    assert t_peak == 3.627599e-03
    assert v_peak == 11.63034


def test_settling_is_last_band_entry_for_underdamped_rlc() -> None:
    # zeta = 0.5, wn = 1000 rad/s, 10 V step: analytic 2% settling is about 8.08 ms.
    # The response enters the band near 5.7 ms but leaves it again on the undershoot.
    import math

    from electrical_engineer.engines.spice_runner import _settling_2pct_last_entry

    zeta, wn, vs = 0.5, 1000.0, 10.0
    wd = wn * math.sqrt(1 - zeta * zeta)
    phi = math.acos(zeta)
    rows = []
    for i in range(1, 9070):
        t = i * 1e-6
        v = vs * (1 - math.exp(-zeta * wn * t) * math.sin(wd * t + phi) / math.sqrt(1 - zeta * zeta))
        rows.append((t, v))
    t_set = _settling_2pct_last_entry(rows, vs)
    assert t_set is not None
    assert abs(t_set * 1000 - 8.08) < 0.02

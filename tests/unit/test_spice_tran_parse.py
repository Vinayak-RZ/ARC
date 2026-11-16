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
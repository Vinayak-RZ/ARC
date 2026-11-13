from electrical_engineer.engines.power_runner import _parse_complex


def test_j_prefix_and_sum() -> None:
    assert abs(_parse_complex("j0.2") - 0.2j) < 1e-12
    assert abs(_parse_complex("0.1+0.2j") - (0.1 + 0.2j)) < 1e-12

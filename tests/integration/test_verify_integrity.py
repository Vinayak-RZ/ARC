"""Derived must not be copied from golden simulation fixtures."""

from __future__ import annotations

import math

import pytest

from electrical_engineer.collab.control_derive import derive_control_metrics


def test_control_derived_follows_problem_not_golden_fixture() -> None:
    """Perturbing the golden diagram must not move hand-derived values; only problem params matter."""
    problem = {
        "kind": "unity_feedback",
        "golden": "unity_first_order",
        "num": [10],
        "den": [1, 1],
        "tf": "10/(s+1)",
    }
    base = derive_control_metrics(problem)
    assert base is not None
    assert float(base["y_ss"]) == pytest.approx(10.0 / 11.0)
    assert float(base["t_settle_s"]) == pytest.approx(math.log(50.0) / 11.0, rel=0.02)

    bumped = derive_control_metrics({**problem, "num": [8]})
    assert bumped is not None
    assert float(bumped["y_ss"]) == pytest.approx(8.0 / 9.0)
    assert base["y_ss"] != bumped["y_ss"]

    same = derive_control_metrics(problem)
    assert float(same["y_ss"]) == float(base["y_ss"])
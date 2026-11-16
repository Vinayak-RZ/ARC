"""Verify badge copy matches tolerance logic."""

from __future__ import annotations

from electrical_engineer.collab.verify_policy import status_label


def test_peak_time_agrees_when_values_equal_within_limit() -> None:
    label = status_label(agrees=False, rel_err_pct=0.04, limit_pct=2.0)
    assert label.startswith("Agrees")


def test_differs_shown_when_above_limit() -> None:
    label = status_label(agrees=False, rel_err_pct=2.5, limit_pct=2.0)
    assert "Differs by 2.5%" in label
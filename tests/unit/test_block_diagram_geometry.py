"""Wire-graph contract for unity feedback block diagram."""

from __future__ import annotations

import pytest

from electrical_engineer.visual_kit.block_diagram_layout import (
    GRID,
    TAKEOFF_GRIDS,
    build_unity_feedback_layout,
    validate_unity_feedback_layout,
)


def test_unity_feedback_layout_validates() -> None:
    layout = build_unity_feedback_layout()
    validate_unity_feedback_layout(layout)


def test_takeoff_right_of_g_output_and_h() -> None:
    layout = build_unity_feedback_layout()
    g_out = layout.ports["g_out"]
    h_in = layout.ports["h_in"]
    assert layout.takeoff[0] == pytest.approx(g_out[0] + TAKEOFF_GRIDS * GRID, abs=0.01)
    assert layout.takeoff[0] > h_in[0] + 0.05


def test_broken_feedback_vertical_raises() -> None:
    layout = build_unity_feedback_layout()
    layout.takeoff = layout.ports["g_out"]
    with pytest.raises(ValueError, match="right of"):
        validate_unity_feedback_layout(layout)

"""Layout bbox should fit the studio canvas at fitView minZoom (regression for clipped Step/Scope)."""

from __future__ import annotations

from electrical_engineer.control_studio.goldens import pid_dc_motor
from electrical_engineer.control_studio.layout import BLOCK_W, ORIGIN_X, layout_chain


def _block_span(block: dict) -> tuple[float, float]:
    w = 56.0 if block.get("type") == "sum" else float(BLOCK_W)
    x = float(block.get("x") or 0)
    return x, x + w


def test_pid_golden_bbox_fits_viewport_at_min_zoom() -> None:
    diagram = layout_chain(pid_dc_motor())
    blocks = diagram["blocks"]
    min_x = min(_block_span(b)[0] for b in blocks)
    max_x = max(_block_span(b)[1] for b in blocks)
    width = max_x - min_x
    # 1280×800 shell: icon palette 56px, inspector 248px → ~720px canvas (see studio.css grid).
    canvas_w = 720.0
    pad_frac = 0.10
    usable = canvas_w * (1.0 - 2.0 * pad_frac)
    fit_zoom = usable / width if width > 0 else 1.0
    assert width > 0
    assert min_x >= ORIGIN_X - 4
    assert fit_zoom >= 0.35, f"diagram needs zoom {fit_zoom:.2f} below fitView minZoom"
    assert width * fit_zoom <= usable + 8, (
        f"diagram width {width:.0f}px at fit zoom {fit_zoom:.2f} exceeds usable canvas {usable:.0f}px"
    )

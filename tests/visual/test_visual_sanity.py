"""Structural checks on Visual Kit goldens (size, blank, metadata)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from electrical_engineer.visual_kit.registry import list_component_ids
from electrical_engineer.visual_kit.render import render_component

ROOT = Path(__file__).resolve().parents[2]

MIN_WIDTH_PX: dict[str, int] = {
    "schematic.divider": 1200,
    "schematic.rlc_series": 1200,
    "control.block_diagram": 800,
    "power.oneline_bus": 900,
}

MIN_FILE_BYTES: dict[str, int] = {
    "schematic.divider": 12_000,
    "schematic.rlc_series": 12_000,
}


@pytest.fixture
def mpl_ok():
    pytest.importorskip("matplotlib")


def _png_stats(path: Path) -> tuple[int, int, float, int]:
    img = Image.open(path).convert("L")
    w, h = img.size
    arr = np.asarray(img, dtype=np.float32)
    ink_px = int(np.count_nonzero(arr < 235))
    return w, h, float(arr.std()), ink_px


@pytest.mark.parametrize("component_id", list_component_ids())
def test_golden_sanity(mpl_ok, tmp_path: Path, component_id: str) -> None:
    pytest.importorskip("matplotlib")
    if component_id.endswith("animation"):
        return
    out = render_component(component_id, tmp_path, {"theme": "light"})
    png = Path(out["png"])
    assert png.is_file(), f"render missing png for {component_id}"
    w, h, std, ink_px = _png_stats(png)
    assert w >= 200 and h >= 100, f"{component_id}: image too small {w}x{h}"
    assert ink_px >= 800, f"{component_id}: too few ink pixels ({ink_px})"
    assert std >= 3.0 or ink_px >= 2000, f"{component_id}: image appears blank (std={std:.2f})"
    min_w = MIN_WIDTH_PX.get(component_id, 400)
    assert w >= min_w, f"{component_id}: width {w}px < required {min_w}px"
    min_bytes = MIN_FILE_BYTES.get(component_id, 1500)
    assert png.stat().st_size >= min_bytes, f"{component_id}: file too small for publication"
    meta = out.get("meta") or {}
    if component_id == "control.block_diagram":
        assert int(meta.get("wire_segments", 0)) >= 7
    if component_id == "power.oneline_bus":
        assert int(meta.get("connected_buses", 0)) >= 3

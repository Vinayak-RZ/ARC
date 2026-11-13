"""Image-diff regression for Visual Kit goldens."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image, ImageChops, ImageStat

from electrical_engineer.visual_kit.registry import golden_path, list_component_ids
from electrical_engineer.visual_kit.render import render_component

ROOT = Path(__file__).resolve().parents[2]
THRESH_MEAN = 4.0  # mean abs diff per channel (144 dpi engineering plots)


@pytest.fixture(scope="module")
def mpl_ok():
    pytest.importorskip("matplotlib")
    pytest.importorskip("control")


def _mean_diff(a: Path, b: Path) -> float:
    img_a = Image.open(a).convert("RGB")
    img_b = Image.open(b).convert("RGB")
    if img_a.size != img_b.size:
        img_b = img_b.resize(img_a.size, Image.Resampling.LANCZOS)
    diff = ImageChops.difference(img_a, img_b)
    stat = ImageStat.Stat(diff)
    return sum(stat.mean) / len(stat.mean)


@pytest.mark.parametrize("component_id", [c for c in list_component_ids() if not c.endswith("animation")])
def test_visual_matches_golden(mpl_ok, tmp_path: Path, component_id: str) -> None:
    rel = golden_path(component_id)
    assert rel is not None
    golden = ROOT / rel
    assert golden.is_file(), f"missing golden {golden}"
    out = render_component(component_id, tmp_path)
    cand = Path(out["png"])
    assert cand.is_file()
    diff = _mean_diff(golden, cand)
    assert diff <= THRESH_MEAN, f"{component_id} visual drift mean={diff:.2f}"

"""Image-diff regression for Visual Kit goldens."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image, ImageChops, ImageStat

from electrical_engineer.visual_kit.registry import golden_path, list_component_ids, load_manifest
from electrical_engineer.visual_kit.render import render_component

ROOT = Path(__file__).resolve().parents[2]
THRESH_MEAN = 4.5


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


def _golden_rel(component_id: str, *, dark: bool = False) -> Path | None:
    for c in load_manifest().get("components", []):
        if c.get("id") == component_id:
            key = "golden_dark" if dark else "golden"
            rel = c.get(key)
            if rel:
                return ROOT / "artifacts" / "visual-goldens" / str(rel)
    rel = golden_path(component_id)
    return ROOT / rel if rel else None


@pytest.mark.parametrize("component_id", [c for c in list_component_ids() if not c.endswith("animation")])
def test_visual_matches_golden(mpl_ok, tmp_path: Path, component_id: str) -> None:
    rel = _golden_rel(component_id, dark=False)
    assert rel is not None and rel.is_file(), f"missing golden {rel}"
    out = render_component(component_id, tmp_path, {"theme": "light"})
    cand = Path(out["png"])
    diff = _mean_diff(rel, cand)
    assert diff <= THRESH_MEAN, f"{component_id} visual drift mean={diff:.2f}"


@pytest.mark.parametrize(
    "component_id",
    [
        c["id"]
        for c in load_manifest().get("components", [])
        if c.get("golden_dark") and not str(c["id"]).endswith("animation")
    ],
)
def test_visual_dark_matches_golden(mpl_ok, tmp_path: Path, component_id: str) -> None:
    rel = _golden_rel(component_id, dark=True)
    assert rel is not None and rel.is_file(), f"missing dark golden {rel}"
    out = render_component(component_id, tmp_path, {"theme": "dark"})
    cand = Path(out["png"])
    diff = _mean_diff(rel, cand)
    assert diff <= THRESH_MEAN, f"{component_id} dark drift mean={diff:.2f}"

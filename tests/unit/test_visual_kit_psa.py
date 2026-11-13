from __future__ import annotations

from pathlib import Path

import pytest

from electrical_engineer.visual_kit.registry import list_component_ids
from electrical_engineer.visual_kit.render import render_component


@pytest.fixture
def mpl_ok():
    pytest.importorskip("matplotlib")


def test_registry_lists_psa_components() -> None:
    ids = list_component_ids()
    assert "power.swing_equal_area" in ids
    assert "power.agc_trace" in ids


def test_render_swing_produces_png(mpl_ok, tmp_path: Path) -> None:
    out = render_component("power.swing_equal_area", tmp_path)
    png = Path(out["png"])
    assert png.is_file() and png.stat().st_size > 1000
    assert "delta_cr_deg" in out["meta"]

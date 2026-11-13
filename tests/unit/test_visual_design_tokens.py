"""Learning Lab tokens for Visual Kit."""

from __future__ import annotations

from electrical_engineer.visual_kit.design_tokens import (
    DK_CANVAS,
    FONT_SANS_STACK,
    LIGHT,
    LL_CANVAS,
    LL_COBALT,
    get_theme,
)


def test_light_theme_learning_lab_palette() -> None:
    t = get_theme("light")
    assert t.canvas == LL_CANVAS == "#FAFAF9"
    assert t.surface == "#FFFFFF"
    assert t.ink == "#202020"
    assert t.muted == "#5F5F5C"
    assert t.primary == LL_COBALT == "#2F6FEB"
    assert t.primary_dark == "#1D47A3"
    assert t.copper == "#E07A3F"
    assert t.success == "#2F9E6A"
    assert t.fault == t.critical == "#D0312D"
    assert t.hairline == "#E4E4E2"
    assert t.bg == t.surface
    assert t.font_family == "Inter"
    assert "Geist" in FONT_SANS_STACK
    assert "Inter" in FONT_SANS_STACK


def test_dark_theme_is_paired() -> None:
    d = get_theme("dark")
    assert d.name == "dark"
    assert d.canvas == DK_CANVAS
    assert d.primary != LIGHT.primary

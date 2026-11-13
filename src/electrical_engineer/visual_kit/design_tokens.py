"""Arc Visual Kit design tokens (aligned with ui/src/tokens.css and tokens.js)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ThemeName = Literal["light", "dark"]

# Learning Lab / Cobalt palette (light)
_CANVAS = "#FAFAF9"
_INK = "#202020"
_MUTED = "#8A8A86"
_BODY = "#5F5F5C"
_PRIMARY = "#2F6FEB"
_SUCCESS = "#2F9E6A"
_CRITICAL = "#D0312D"
_HAIRLINE = "#E4E4E2"
_GRID = "#EFEFED"


@dataclass(frozen=True)
class ArcTheme:
    name: ThemeName
    bg: str
    ink: str
    muted: str
    primary: str
    accent: str
    fault: str
    post: str
    pre: str
    mech: str
    area_accel: tuple[float, float, float, float]
    area_decel: tuple[float, float, float, float]
    grid: str
    hairline: str
    font_family: str
    title_size: float
    label_size: float
    tick_size: float
    annotation_size: float
    dpi: int
    fig_w: float
    fig_h: float


LIGHT = ArcTheme(
    name="light",
    bg=_CANVAS,
    ink=_INK,
    muted=_MUTED,
    primary=_PRIMARY,
    accent=_SUCCESS,
    fault=_CRITICAL,
    post=_PRIMARY,
    pre="#1D47A3",
    mech=_INK,
    area_accel=(208 / 255, 49 / 255, 45 / 255, 0.16),
    area_decel=(47 / 255, 158 / 255, 106 / 255, 0.18),
    grid=_GRID,
    hairline=_HAIRLINE,
    font_family="DejaVu Sans",
    title_size=13.0,
    label_size=11.0,
    tick_size=9.5,
    annotation_size=9.0,
    dpi=144,
    fig_w=7.5,
    fig_h=4.6,
)

DARK = ArcTheme(
    name="dark",
    bg="#202020",
    ink="#FAFAF9",
    muted="#A3A3A0",
    primary="#5C8EF2",
    accent="#2F9E6A",
    fault="#E85C58",
    post="#5C8EF2",
    pre="#8FA4D4",
    mech="#FAFAF9",
    area_accel=(232 / 255, 92 / 255, 88 / 255, 0.22),
    area_decel=(47 / 255, 158 / 255, 106 / 255, 0.24),
    grid="#2A2A28",
    hairline="#3A3A37",
    font_family="DejaVu Sans",
    title_size=13.0,
    label_size=11.0,
    tick_size=9.5,
    annotation_size=9.0,
    dpi=144,
    fig_w=7.5,
    fig_h=4.6,
)


def get_theme(name: ThemeName = "light") -> ArcTheme:
    return DARK if name == "dark" else LIGHT

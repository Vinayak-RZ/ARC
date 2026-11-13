"""Arc Visual Kit design tokens (aligned with ui/src/tokens.css)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ThemeName = Literal["light", "dark"]


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
    bg="#ffffff",
    ink="#0a0b0d",
    muted="#5b616e",
    primary="#0052ff",
    accent="#05b169",
    fault="#cf202f",
    post="#0052ff",
    pre="#3d4f7c",
    mech="#0a0b0d",
    area_accel=(207 / 255, 32 / 255, 47 / 255, 0.18),
    area_decel=(5 / 255, 177 / 255, 105 / 255, 0.20),
    grid="#eef0f3",
    hairline="#dee1e6",
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
    bg="#0a0b0d",
    ink="#f7f7f7",
    muted="#9aa0aa",
    primary="#5b8cff",
    accent="#3dd68c",
    fault="#ff6b6b",
    post="#5b8cff",
    pre="#8fa4d4",
    mech="#f7f7f7",
    area_accel=(255 / 255, 107 / 255, 107 / 255, 0.22),
    area_decel=(61 / 255, 214 / 255, 140 / 255, 0.24),
    grid="#1c1f26",
    hairline="#2a2f3a",
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

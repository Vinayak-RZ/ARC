"""Learning Lab design tokens — canonical palette for Arc Visual Kit plots.

UI (`ui/src/tokens.css`) may mirror these on a stacked PR; keep plot colors here
so diagram goldens and the redesigned Learning Lab stay merge-friendly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ThemeName = Literal["light", "dark"]

# --- Learning Lab light ---
LL_CANVAS = "#FAFAF9"
LL_SURFACE = "#FFFFFF"
LL_INK = "#202020"
LL_SECONDARY = "#5F5F5C"
LL_BORDER = "#E4E4E2"
LL_COBALT = "#2F6FEB"
LL_COBALT_700 = "#1D47A3"
LL_COPPER = "#E07A3F"
LL_SUCCESS = "#2F9E6A"
LL_WARNING = "#E0A526"
LL_CRITICAL = "#D0312D"
LL_GRID = "#EEECEA"

FONT_SANS_STACK: tuple[str, ...] = ("Geist", "Inter", "DejaVu Sans", "Liberation Sans", "sans-serif")
SCHEMDRAW_FONT = "Inter"

# --- Learning Lab dark (matched contrast / hue) ---
DK_CANVAS = "#121211"
DK_SURFACE = "#1A1A18"
DK_INK = "#F4F4F3"
DK_SECONDARY = "#A3A39E"
DK_BORDER = "#353532"
DK_COBALT = "#6B93F5"
DK_COBALT_700 = "#2F6FEB"
DK_COPPER = "#E8935F"
DK_SUCCESS = "#3DB87E"
DK_WARNING = "#E8B84A"
DK_CRITICAL = "#E85A56"
DK_GRID = "#2A2A28"


def _rgba_hex(hex_color: str, alpha: float) -> tuple[float, float, float, float]:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return (r / 255, g / 255, b / 255, alpha)


@dataclass(frozen=True)
class ArcTheme:
    name: ThemeName
    canvas: str
    surface: str
    ink: str
    muted: str
    primary: str
    primary_dark: str
    copper: str
    success: str
    warning: str
    critical: str
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
    font_sans: tuple[str, ...]
    title_size: float
    label_size: float
    tick_size: float
    annotation_size: float
    dpi: int
    fig_w: float
    fig_h: float

    @property
    def bg(self) -> str:
        """Plot/card fill (surface). Legacy name used by schemdraw and patches."""
        return self.surface


LIGHT = ArcTheme(
    name="light",
    canvas=LL_CANVAS,
    surface=LL_SURFACE,
    ink=LL_INK,
    muted=LL_SECONDARY,
    primary=LL_COBALT,
    primary_dark=LL_COBALT_700,
    copper=LL_COPPER,
    success=LL_SUCCESS,
    warning=LL_WARNING,
    critical=LL_CRITICAL,
    accent=LL_COPPER,
    fault=LL_CRITICAL,
    post=LL_COBALT,
    pre=LL_COBALT_700,
    mech=LL_INK,
    area_accel=_rgba_hex(LL_CRITICAL, 0.16),
    area_decel=_rgba_hex(LL_SUCCESS, 0.18),
    grid=LL_GRID,
    hairline=LL_BORDER,
    font_family=SCHEMDRAW_FONT,
    font_sans=FONT_SANS_STACK,
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
    canvas=DK_CANVAS,
    surface=DK_SURFACE,
    ink=DK_INK,
    muted=DK_SECONDARY,
    primary=DK_COBALT,
    primary_dark=DK_COBALT_700,
    copper=DK_COPPER,
    success=DK_SUCCESS,
    warning=DK_WARNING,
    critical=DK_CRITICAL,
    accent=DK_COPPER,
    fault=DK_CRITICAL,
    post=DK_COBALT,
    pre=DK_COBALT_700,
    mech=DK_INK,
    area_accel=_rgba_hex(DK_CRITICAL, 0.22),
    area_decel=_rgba_hex(DK_SUCCESS, 0.24),
    grid=DK_GRID,
    hairline=DK_BORDER,
    font_family=SCHEMDRAW_FONT,
    font_sans=FONT_SANS_STACK,
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

"""Apply Arc theme to matplotlib figures."""

from __future__ import annotations

from typing import Any


def apply_theme(ax: Any, theme) -> None:
    import matplotlib as mpl

    fig = ax.figure
    fig.patch.set_facecolor(theme.bg)
    ax.set_facecolor(theme.bg)
    ax.tick_params(colors=theme.muted, labelsize=theme.tick_size)
    for spine in ax.spines.values():
        spine.set_color(theme.hairline)
    ax.xaxis.label.set_color(theme.ink)
    ax.yaxis.label.set_color(theme.ink)
    ax.title.set_color(theme.ink)
    ax.title.set_fontsize(theme.title_size)
    ax.xaxis.label.set_fontsize(theme.label_size)
    ax.yaxis.label.set_fontsize(theme.label_size)
    ax.grid(True, color=theme.grid, linewidth=0.6, alpha=0.9)
    mpl.rcParams.update(
        {
            "font.family": theme.font_family,
            "mathtext.fontset": "dejavusans",
            "figure.dpi": theme.dpi,
            "savefig.facecolor": theme.bg,
            "savefig.edgecolor": theme.bg,
        }
    )


def direct_label(ax, x, y, text: str, theme, *, color: str | None = None, dy: int = 0) -> None:
    ax.annotate(
        text,
        xy=(x, y),
        xytext=(4, 4 + dy),
        textcoords="offset points",
        fontsize=theme.annotation_size,
        color=color or theme.ink,
        bbox={
            "boxstyle": "round,pad=0.2",
            "facecolor": theme.bg,
            "edgecolor": theme.hairline,
            "linewidth": 0.5,
        },
    )

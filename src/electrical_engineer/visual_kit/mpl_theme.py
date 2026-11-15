"""Apply Arc theme to matplotlib figures."""

from __future__ import annotations

from typing import Any


def arc_rcparams(theme) -> dict[str, Any]:
    """Global matplotlib rc matching Learning Lab tokens."""
    from cycler import cycler

    return {
        "font.family": "sans-serif",
        "font.sans-serif": list(theme.font_sans),
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": theme.hairline_strong,
        "axes.labelcolor": theme.ink,
        "axes.titlecolor": theme.ink,
        "axes.labelsize": 11,
        "axes.titlesize": 13,
        "xtick.color": theme.ink,
        "ytick.color": theme.ink,
        "text.color": theme.ink,
        "lines.linewidth": 1.75,
        "axes.prop_cycle": cycler(color=[theme.primary, theme.copper, theme.success, theme.muted]),
        "axes.grid": True,
        "grid.color": theme.hairline,
        "grid.linewidth": 0.5,
        "figure.facecolor": theme.canvas,
        "axes.facecolor": theme.canvas,
        "savefig.dpi": 200,
        "savefig.facecolor": theme.canvas,
        "savefig.edgecolor": theme.canvas,
        "mathtext.fontset": "dejavusans",
    }


def apply_theme(ax: Any, theme) -> None:
    import matplotlib as mpl

    fig = ax.figure
    fig.patch.set_facecolor(theme.canvas)
    ax.set_facecolor(theme.canvas)
    ax.tick_params(colors=theme.muted, labelsize=theme.tick_size)
    for spine in ax.spines.values():
        spine.set_color(theme.hairline_strong)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.label.set_color(theme.ink)
    ax.yaxis.label.set_color(theme.ink)
    ax.title.set_color(theme.ink)
    ax.title.set_fontsize(theme.title_size)
    ax.xaxis.label.set_fontsize(theme.label_size)
    ax.yaxis.label.set_fontsize(theme.label_size)
    ax.grid(True, color=theme.hairline, linewidth=0.5, alpha=0.9)
    mpl.rcParams.update(arc_rcparams(theme))


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
            "facecolor": theme.surface,
            "edgecolor": theme.hairline,
            "linewidth": 0.5,
        },
    )

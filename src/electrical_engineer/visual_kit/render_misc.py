"""Block diagram and one-line diagram renders (matplotlib SVG-friendly)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.visual_kit.design_tokens import ThemeName, get_theme
from electrical_engineer.visual_kit.mpl_theme import apply_theme


def render_control_block_diagram(out_dir: Path, *, theme_name: ThemeName = "light") -> dict[str, Any]:
    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt

    theme = get_theme(theme_name)
    fig, ax = plt.subplots(figsize=(theme.fig_w, theme.fig_h * 0.55))
    apply_theme(ax, theme)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    def box(x, y, w, h, text):
        rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", linewidth=1.2, edgecolor=theme.primary, facecolor=theme.bg)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=theme.label_size, color=theme.ink)

    box(0.5, 1.5, 1.4, 0.9, r"$R(s)$")
    box(3.0, 1.5, 1.6, 0.9, r"$G(s)=\frac{10}{s+1}$")
    box(6.5, 1.5, 1.4, 0.9, r"$Y(s)$")
    box(3.0, 0.2, 1.6, 0.9, r"$H(s)=1$")
    ap = {"arrowstyle": "-|>", "color": theme.ink}
    ax.annotate("", xy=(2.9, 1.95), xytext=(1.9, 1.95), arrowprops=ap)
    ax.annotate("", xy=(6.4, 1.95), xytext=(4.6, 1.95), arrowprops=ap)
    ax.annotate("", xy=(5.3, 1.45), xytext=(5.3, 1.1), arrowprops={"arrowstyle": "-|>", "color": theme.accent})
    ax.annotate(
        "",
        xy=(1.2, 1.45),
        xytext=(1.2, 0.65),
        arrowprops={"arrowstyle": "-|>", "color": theme.accent, "connectionstyle": "arc3,rad=0.3"},
    )
    ax.set_title("Unity-feedback block diagram")
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / "control.block_diagram.png"
    fig.savefig(png, dpi=theme.dpi, bbox_inches="tight", facecolor=theme.bg)
    plt.close(fig)
    return {"png": str(png), "meta": {"component_id": "control.block_diagram"}}


def render_power_oneline(out_dir: Path, *, theme_name: ThemeName = "light") -> dict[str, Any]:
    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt

    theme = get_theme(theme_name)
    fig, ax = plt.subplots(figsize=(theme.fig_w, theme.fig_h * 0.5))
    apply_theme(ax, theme)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis("off")
    for x, label in ((1, "Slack"), (5, "Load"), (8.5, "Fault bus")):
        circ = mpatches.Circle((x, 1.5), 0.35, edgecolor=theme.primary, facecolor=theme.bg, linewidth=1.5)
        ax.add_patch(circ)
        ax.text(x, 1.5, label[0], ha="center", va="center", fontsize=theme.label_size, color=theme.ink)
        ax.text(x, 0.7, label, ha="center", fontsize=theme.annotation_size, color=theme.muted)
    ax.plot([1.35, 4.65], [1.5, 1.5], color=theme.ink, linewidth=2)
    ax.plot([5.35, 8.15], [1.5, 1.5], color=theme.ink, linewidth=2)
    ax.set_title("Three-bus one-line diagram (study template)")
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / "power.oneline_bus.png"
    fig.savefig(png, dpi=theme.dpi, bbox_inches="tight", facecolor=theme.bg)
    plt.close(fig)
    return {"png": str(png), "meta": {"component_id": "power.oneline_bus"}}

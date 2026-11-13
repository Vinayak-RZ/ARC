"""Unity-feedback block diagram (ortho routing, engine tf labels)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

from electrical_engineer.visual_kit.block_diagram_spec import plant_meta, unity_feedback_problem
from electrical_engineer.visual_kit.design_tokens import ThemeName, get_theme
from electrical_engineer.visual_kit.mpl_theme import apply_theme


def _h_line(ax, x0, x1, y, color, lw=1.6):
    ax.plot([x0, x1], [y, y], color=color, linewidth=lw, solid_capstyle="round")


def _v_line(ax, x, y0, y1, color, lw=1.6):
    ax.plot([x, x], [y0, y1], color=color, linewidth=lw, solid_capstyle="round")


def _arrow(ax, x0, y0, x1, y1, color):
    ax.annotate(
        "",
        xy=(x1, y1),
        xytext=(x0, y0),
        arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.4, "shrinkA": 0, "shrinkB": 0},
    )


def _signal(ax, x, y, text: str, theme, ha="center"):
    ax.text(x, y, text, ha=ha, va="center", fontsize=theme.annotation_size, color=theme.ink)


def render_control_block_diagram(
    out_dir: Path,
    *,
    theme_name: ThemeName = "light",
    props: dict[str, Any] | None = None,
) -> dict[str, Any]:
    problem = unity_feedback_problem(props)
    meta = plant_meta(problem)
    theme = get_theme(theme_name)
    fig, ax = plt.subplots(figsize=(theme.fig_w, theme.fig_h * 0.62))
    apply_theme(ax, theme)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    ax.set_title("Unity negative feedback")

    y_main = 2.6
    y_fb = 0.85
    x_r = 0.35
    x_sum = 2.0
    x_g = 4.2
    x_tap = 7.55
    x_h = 4.2

    # Reference input wire
    _h_line(ax, x_r + 0.3, x_sum - 0.28, y_main, theme.ink)
    _signal(ax, (x_r + x_sum) / 2, y_main + 0.22, r"$R(s)$", theme)

    # Summing junction
    circ = Circle((x_sum, y_main), 0.28, fill=False, edgecolor=theme.primary, linewidth=2.0)
    ax.add_patch(circ)
    ax.text(x_sum, y_main, r"$\Sigma$", ha="center", va="center", fontsize=theme.label_size, color=theme.ink)
    ax.text(x_sum - 0.42, y_main + 0.12, r"$+$", fontsize=theme.label_size, color=theme.accent)
    ax.text(x_sum - 0.42, y_main - 0.22, r"$-$", fontsize=theme.label_size, color=theme.fault)

    # Forward path E(s) -> G(s) -> Y(s)
    _h_line(ax, x_sum + 0.28, x_g - 0.15, y_main, theme.ink)
    _signal(ax, (x_sum + x_g) / 2, y_main + 0.22, r"$E(s)$", theme)
    g_w, g_h = 1.65, 0.72
    rect = FancyBboxPatch(
        (x_g, y_main - g_h / 2),
        g_w,
        g_h,
        boxstyle="round,pad=0.06",
        edgecolor=theme.primary,
        facecolor=theme.bg,
        linewidth=1.5,
    )
    ax.add_patch(rect)
    ax.text(x_g + g_w / 2, y_main, rf"$G(s)={meta['G_tf']}$", ha="center", va="center", fontsize=theme.annotation_size)
    _h_line(ax, x_g + g_w, x_tap, y_main, theme.ink)
    _signal(ax, (x_g + g_w + x_tap) / 2, y_main + 0.22, r"$Y(s)$", theme)

    # Feedback takeoff at output
    _v_line(ax, x_tap, y_fb + 0.5, y_main, theme.ink)
    _h_line(ax, x_h + 0.82, x_tap, y_fb, theme.ink)
    _v_line(ax, x_h + 0.82, y_fb, y_fb + 0.36, theme.ink)

    h_w, h_h = 1.1, 0.65
    hrect = FancyBboxPatch(
        (x_h - 0.1, y_fb - h_h / 2),
        h_w,
        h_h,
        boxstyle="round,pad=0.05",
        edgecolor=theme.accent,
        facecolor=theme.bg,
        linewidth=1.3,
    )
    ax.add_patch(hrect)
    ax.text(x_h + h_w / 2 - 0.1, y_fb, rf"$H(s)={meta['H_tf']}$", ha="center", va="center", fontsize=theme.annotation_size)
    _h_line(ax, x_h + h_w + 0.02, x_sum, y_fb, theme.ink)
    _v_line(ax, x_sum, y_fb, y_main - 0.28, theme.ink)
    _signal(ax, x_sum + 0.55, (y_fb + y_main) / 2, r"$B(s)$", theme)

    _arrow(ax, x_tap, y_main, x_tap + 0.35, y_main, theme.ink)

    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / "control.block_diagram.png"
    fig.savefig(png, dpi=theme.dpi, bbox_inches="tight", facecolor=theme.bg)
    plt.close(fig)
    return {
        "png": str(png),
        "meta": {"component_id": "control.block_diagram", "props_source": "block_diagram", **meta},
    }

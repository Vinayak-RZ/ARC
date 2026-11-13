"""Unity-feedback block diagram (ortho routing, engine tf labels)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

from electrical_engineer.visual_kit.block_diagram_spec import plant_meta, unity_feedback_problem
from electrical_engineer.visual_kit.design_tokens import ThemeName, get_theme
from electrical_engineer.visual_kit.mpl_theme import apply_theme


def _h(ax, x0, x1, y, color, lw=1.8, z=6):
    ax.plot([x0, x1], [y, y], color=color, linewidth=lw, solid_capstyle="round", zorder=z)


def _v(ax, x, y0, y1, color, lw=1.8, z=6):
    ax.plot([x, x], [y0, y1], color=color, linewidth=lw, solid_capstyle="round", zorder=z)


def _arrowhead(ax, x, y, color):
    ax.annotate(
        "",
        xy=(x, y),
        xytext=(x - 0.35, y),
        arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.6, "shrinkA": 0, "shrinkB": 0},
        zorder=2,
    )


def render_control_block_diagram(
    out_dir: Path,
    *,
    theme_name: ThemeName = "light",
    props: dict[str, Any] | None = None,
) -> dict[str, Any]:
    problem = unity_feedback_problem(props)
    meta = plant_meta(problem)
    theme = get_theme(theme_name)
    fig, ax = plt.subplots(figsize=(10.0, 4.2))
    apply_theme(ax, theme)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    ax.set_title("Unity negative feedback")

    y = 3.2
    y_fb = 0.95
    x_r0 = 0.4
    x_sum = 2.15
    r_sum = 0.32
    x_g = 3.55
    g_w, g_h = 1.85, 0.78
    x_g_out = x_g + g_w
    x_y_end = 9.2
    x_h0 = x_g
    h_w = g_w
    x_tap = x_g_out

    # R(s) reference on wire (not a block)
    _h(ax, x_r0, x_sum - r_sum, y, theme.ink)
    ax.text((x_r0 + x_sum - r_sum) / 2, y + 0.25, r"$R(s)$", ha="center", fontsize=theme.annotation_size, color=theme.ink)

    # Summer (+ / -)
    ax.add_patch(Circle((x_sum, y), r_sum, fill=False, edgecolor=theme.primary, linewidth=2.2, zorder=3))
    ax.text(x_sum, y, r"$\Sigma$", ha="center", va="center", fontsize=theme.label_size, color=theme.ink, zorder=4)
    ax.text(x_sum - r_sum - 0.12, y + 0.08, r"$+$", fontsize=theme.label_size, color=theme.ink)
    ax.text(x_sum - r_sum * 0.35, y - r_sum - 0.14, r"$-$", fontsize=theme.label_size, color=theme.ink, ha="center")

    # E(s) -> G(s)
    _h(ax, x_sum + r_sum, x_g, y, theme.ink)
    ax.text((x_sum + r_sum + x_g) / 2, y + 0.25, r"$E(s)$", ha="center", fontsize=theme.annotation_size, color=theme.ink)
    ax.add_patch(
        FancyBboxPatch(
            (x_g, y - g_h / 2),
            g_w,
            g_h,
            boxstyle="round,pad=0.06",
            edgecolor=theme.primary,
            facecolor=theme.bg,
            linewidth=1.6,
            zorder=3,
        )
    )
    ax.text(x_g + g_w / 2, y, rf"$G(s)={meta['G_tf']}$", ha="center", va="center", fontsize=theme.annotation_size, zorder=4)

    # Y(s) on output wire
    _h(ax, x_g_out, x_y_end, y, theme.ink)
    ax.text((x_g_out + x_y_end) / 2, y + 0.25, r"$Y(s)$", ha="center", fontsize=theme.annotation_size, color=theme.ink)
    _arrowhead(ax, x_y_end, y, theme.ink)

    # Takeoff at G output -> down -> H (R->L under G) -> B(s) up to summer minus
    ax.plot(x_tap, y, "o", color=theme.ink, markersize=5, zorder=4)
    _v(ax, x_tap, y_fb, y, theme.ink)
    _h(ax, x_h0, x_tap, y_fb, theme.ink)
    _h(ax, x_h0, x_sum, y_fb, theme.ink)
    ax.add_patch(
        FancyBboxPatch(
            (x_h0, y_fb - 0.42),
            h_w,
            0.84,
            boxstyle="round,pad=0.05",
            edgecolor=theme.primary,
            facecolor=theme.bg,
            linewidth=1.4,
            zorder=3,
        )
    )
    ax.text(x_h0 + h_w / 2, y_fb, rf"$H(s)={meta['H_tf']}$", ha="center", va="center", fontsize=theme.annotation_size, zorder=4)
    _v(ax, x_sum, y_fb, y - r_sum, theme.ink)
    ax.text(x_sum + 0.35, (y_fb + y) / 2, r"$B(s)$", fontsize=theme.annotation_size, color=theme.ink)

    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / "control.block_diagram.png"
    fig.savefig(png, dpi=theme.dpi, bbox_inches="tight", facecolor=theme.canvas)
    plt.close(fig)
    return {
        "png": str(png),
        "meta": {
            "component_id": "control.block_diagram",
            "props_source": "block_diagram",
            "wire_segments": 8,
            **meta,
        },
    }

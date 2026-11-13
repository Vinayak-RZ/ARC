"""Unity-feedback block diagram (Simulink-style ortho routing, explicit ports)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

from electrical_engineer.visual_kit.block_diagram_layout import (
    GRID,
    build_unity_feedback_layout,
    validate_unity_feedback_layout,
)
from electrical_engineer.visual_kit.block_diagram_spec import plant_meta, unity_feedback_problem
from electrical_engineer.visual_kit.design_tokens import ThemeName, get_theme
from electrical_engineer.visual_kit.mpl_theme import apply_theme

_WIRE_Z = 2
_SHADOW_Z = 14
_BLOCK_Z = 16
_PORT_Z = 18
_LABEL_Z = 19
_SIGN_Z = 20
_CORNER_RAD = 0.14


def _rounded_ortho_wire(
    ax,
    points: list[tuple[float, float]],
    color: str,
    *,
    arrow_end: bool = False,
    zorder: int = _WIRE_Z,
) -> int:
    segs = 0
    if len(points) < 2:
        return segs
    for i in range(len(points) - 1):
        a, b = points[i], points[i + 1]
        last = i == len(points) - 2
        use_arrow = arrow_end and last
        if a[0] == b[0] or a[1] == b[1]:
            ax.plot(
                [a[0], b[0]],
                [a[1], b[1]],
                color=color,
                linewidth=1.65,
                solid_capstyle="round",
                zorder=zorder,
            )
            segs += 1
            if use_arrow:
                _arrow_at(ax, a, b, color, zorder=zorder + 1)
            continue
        style = f"angle,angleA=0,angleB=90,rad={_CORNER_RAD}"
        patch = FancyArrowPatch(
            a,
            b,
            connectionstyle=style,
            arrowstyle="-|>" if use_arrow else "-",
            color=color,
            linewidth=1.65,
            mutation_scale=11 if use_arrow else 1,
            shrinkA=0,
            shrinkB=0,
            zorder=zorder,
        )
        ax.add_patch(patch)
        segs += 1
    return segs


def _arrow_at(
    ax,
    a: tuple[float, float],
    b: tuple[float, float],
    color: str,
    *,
    zorder: int,
) -> None:
    ax.annotate(
        "",
        xy=b,
        xytext=a,
        arrowprops={
            "arrowstyle": "-|>",
            "color": color,
            "lw": 1.55,
            "shrinkA": 2,
            "shrinkB": 2,
        },
        zorder=zorder,
    )


def _port(ax, xy: tuple[float, float], theme, *, zorder: int = _PORT_Z) -> None:
    x, y = xy
    ax.add_patch(
        Circle(
            (x, y),
            0.06,
            facecolor=theme.surface,
            edgecolor=theme.primary,
            linewidth=1.2,
            zorder=zorder,
        )
    )


def _block(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    theme,
    *,
    label: str,
    inputs: list[tuple[float, float]],
    outputs: list[tuple[float, float]],
) -> None:
    shadow = FancyBboxPatch(
        (x + 0.07, y - h / 2 - 0.07),
        w,
        h,
        boxstyle="round,pad=0.06",
        facecolor="#00000012" if theme.name == "light" else "#ffffff18",
        edgecolor="none",
        linewidth=0,
        zorder=_SHADOW_Z,
    )
    ax.add_patch(shadow)
    ax.add_patch(
        FancyBboxPatch(
            (x, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.06",
            edgecolor=theme.primary,
            facecolor=theme.surface,
            linewidth=1.6,
            zorder=_BLOCK_Z,
        )
    )
    ax.text(
        x + w / 2,
        y,
        label,
        ha="center",
        va="center",
        fontsize=theme.annotation_size,
        color=theme.ink,
        zorder=_LABEL_Z,
    )
    for p in inputs:
        _port(ax, p, theme)
    for p in outputs:
        _port(ax, p, theme)


def _summer(
    ax,
    cx: float,
    cy: float,
    r: float,
    theme,
    *,
    port_plus: tuple[float, float],
    port_minus: tuple[float, float],
    port_out: tuple[float, float],
) -> None:
    shadow = Circle(
        (cx + 0.06, cy - 0.06),
        r,
        facecolor="#00000010" if theme.name == "light" else "#ffffff15",
        edgecolor="none",
        zorder=_SHADOW_Z,
    )
    ax.add_patch(shadow)
    ax.add_patch(
        Circle(
            (cx, cy),
            r,
            facecolor=theme.surface,
            edgecolor=theme.primary,
            linewidth=2.0,
            zorder=_BLOCK_Z,
        )
    )
    ax.text(
        cx,
        cy,
        r"$\Sigma$",
        ha="center",
        va="center",
        fontsize=theme.label_size,
        color=theme.ink,
        zorder=_LABEL_Z,
    )
    for p in (port_plus, port_minus, port_out):
        _port(ax, p, theme)
    ax.text(
        port_plus[0] - 0.38,
        port_plus[1] + 0.22,
        r"$+$",
        fontsize=theme.label_size,
        color=theme.ink,
        ha="center",
        va="bottom",
        zorder=_SIGN_Z,
    )
    ax.text(
        port_minus[0] + 0.02,
        port_minus[1] - 0.22,
        r"$-$",
        fontsize=theme.label_size,
        color=theme.ink,
        ha="left",
        va="top",
        zorder=_SIGN_Z,
    )


def render_control_block_diagram(
    out_dir: Path,
    *,
    theme_name: ThemeName = "light",
    props: dict[str, Any] | None = None,
) -> dict[str, Any]:
    problem = unity_feedback_problem(props)
    meta = plant_meta(problem)
    layout = build_unity_feedback_layout(props)
    validate_unity_feedback_layout(layout)

    theme = get_theme(theme_name)
    fig, ax = plt.subplots(figsize=(10.0, 4.2))
    apply_theme(ax, theme)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    ax.set_title("Unity negative feedback", zorder=_LABEL_Z)

    p = layout.ports
    color = theme.ink
    wire_segs = 0
    y = layout.ports["g_in"][1]

    for w in layout.wires:
        wire_segs += _rounded_ortho_wire(ax, w.points, color, arrow_end=w.arrow_end)

    ax.plot(layout.takeoff[0], layout.takeoff[1], "o", color=theme.ink, markersize=6, zorder=_PORT_Z + 1)

    ax.text(
        (layout.ref[0] + p["summer_plus"][0]) / 2,
        y + 0.26,
        r"$R(s)$",
        ha="center",
        fontsize=theme.annotation_size,
        color=theme.ink,
        zorder=_LABEL_Z,
    )
    ax.text(
        (p["summer_out"][0] + p["g_in"][0]) / 2,
        y + 0.26,
        r"$E(s)$",
        ha="center",
        fontsize=theme.annotation_size,
        color=theme.ink,
        zorder=_LABEL_Z,
    )
    ax.text(
        (p["g_out"][0] + layout.y_end[0]) / 2,
        y + 0.26,
        r"$Y(s)$",
        ha="center",
        fontsize=theme.annotation_size,
        color=theme.ink,
        zorder=_LABEL_Z,
    )
    ax.text(
        (p["h_out"][0] + layout.bus_junction[0]) / 2,
        layout.bus_junction[1] - 0.22,
        r"$B(s)$",
        ha="center",
        fontsize=theme.annotation_size,
        color=theme.ink,
        zorder=_LABEL_Z,
    )

    cx, cy, r_sum = layout.summer
    bw, bh = 2.0, 0.8
    x_g = layout.block_rects["G"].x0
    y_fb = layout.ports["h_in"][1]
    _summer(
        ax,
        cx,
        cy,
        r_sum,
        theme,
        port_plus=p["summer_plus"],
        port_minus=p["summer_minus"],
        port_out=p["summer_out"],
    )
    _block(
        ax,
        x_g,
        y,
        bw,
        bh,
        theme,
        label=rf"$G(s)={meta['G_tf']}$",
        inputs=[p["g_in"]],
        outputs=[p["g_out"]],
    )
    _block(
        ax,
        x_g,
        y_fb,
        bw,
        bh,
        theme,
        label=rf"$H(s)={meta['H_tf']}$",
        inputs=[p["h_in"]],
        outputs=[p["h_out"]],
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / "control.block_diagram.png"
    fig.savefig(png, dpi=theme.dpi, bbox_inches="tight", facecolor=theme.canvas)
    plt.close(fig)
    return {
        "png": str(png),
        "meta": {
            "component_id": "control.block_diagram",
            "props_source": "block_diagram",
            "wire_segments": wire_segs,
            "grid": GRID,
            **meta,
        },
    }

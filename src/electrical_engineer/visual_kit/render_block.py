"""Unity-feedback block diagram (Simulink-style ortho routing, explicit ports)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

from electrical_engineer.visual_kit.block_diagram_spec import plant_meta, unity_feedback_problem
from electrical_engineer.visual_kit.design_tokens import ThemeName, get_theme
from electrical_engineer.visual_kit.mpl_theme import apply_theme

_GRID = 0.2
_WIRE_Z = 2
_SHADOW_Z = 14
_BLOCK_Z = 16
_PORT_Z = 18
_LABEL_Z = 19
_SIGN_Z = 20

_CORNER_RAD = 0.14


def _snap(x: float) -> float:
    return round(x / _GRID) * _GRID


def _rounded_ortho_wire(
    ax,
    points: list[tuple[float, float]],
    color: str,
    *,
    arrow_end: bool = False,
    zorder: int = _WIRE_Z,
) -> int:
    """Manhattan polyline with rounded elbows; arrow only on the last segment."""
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
        port_plus[0] - 0.22,
        port_plus[1] + 0.02,
        r"$+$",
        fontsize=theme.label_size,
        color=theme.ink,
        ha="right",
        va="center",
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
    theme = get_theme(theme_name)
    fig, ax = plt.subplots(figsize=(10.0, 4.2))
    apply_theme(ax, theme)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    ax.set_title("Unity negative feedback", zorder=_LABEL_Z)

    y = _snap(3.2)
    y_fb = _snap(1.0)
    x_ref = _snap(0.4)
    cx = _snap(2.4)
    r_sum = _snap(0.34)
    bw, bh = _snap(2.0), _snap(0.8)
    x_g = _snap(4.0)
    x_y = _snap(9.2)
    stub = _snap(0.4)

    port_r = (cx - r_sum, y)
    port_sum_out = (cx + r_sum, y)
    port_minus = (cx, y - r_sum)
    port_g_in = (x_g, y)
    port_g_out = (x_g + bw, y)
    port_h_in = (x_g + bw, y_fb)
    port_h_out = (x_g, y_fb)
    tap = port_g_out

    color = theme.ink
    wire_segs = 0

    # 1) R(s) -> summer +
    wire_segs += _rounded_ortho_wire(ax, [(x_ref, y), port_r], color, arrow_end=True)
    ax.text(
        (x_ref + port_r[0]) / 2,
        y + 0.26,
        r"$R(s)$",
        ha="center",
        fontsize=theme.annotation_size,
        color=theme.ink,
        zorder=_LABEL_Z,
    )

    # 2) summer out -> G in
    wire_segs += _rounded_ortho_wire(ax, [port_sum_out, port_g_in], color, arrow_end=True)
    ax.text(
        (port_sum_out[0] + port_g_in[0]) / 2,
        y + 0.26,
        r"$E(s)$",
        ha="center",
        fontsize=theme.annotation_size,
        color=theme.ink,
        zorder=_LABEL_Z,
    )

    # 3) G out -> Y (tap dot on output)
    wire_segs += _rounded_ortho_wire(ax, [port_g_out, (x_y, y)], color, arrow_end=True)
    ax.plot(tap[0], tap[1], "o", color=theme.ink, markersize=6, zorder=_PORT_Z + 1)
    ax.text(
        (port_g_out[0] + x_y) / 2,
        y + 0.26,
        r"$Y(s)$",
        ha="center",
        fontsize=theme.annotation_size,
        color=theme.ink,
        zorder=_LABEL_Z,
    )

    # 4) Feedback: tap -> below forward path -> H right in -> H left out -> summer minus
    wire_segs += _rounded_ortho_wire(
        ax,
        [
            tap,
            (tap[0], y_fb),
            (port_h_in[0] + stub, y_fb),
            port_h_in,
        ],
        color,
        arrow_end=True,
    )
    wire_segs += _rounded_ortho_wire(ax, [port_h_out, (port_minus[0], y_fb), port_minus], color, arrow_end=True)
    ax.text(
        (port_h_out[0] + port_minus[0]) / 2,
        y_fb - 0.22,
        r"$B(s)$",
        ha="center",
        fontsize=theme.annotation_size,
        color=theme.ink,
        zorder=_LABEL_Z,
    )

    _summer(
        ax,
        cx,
        y,
        r_sum,
        theme,
        port_plus=port_r,
        port_minus=port_minus,
        port_out=port_sum_out,
    )
    _block(
        ax,
        x_g,
        y,
        bw,
        bh,
        theme,
        label=rf"$G(s)={meta['G_tf']}$",
        inputs=[port_g_in],
        outputs=[port_g_out],
    )
    _block(
        ax,
        x_g,
        y_fb,
        bw,
        bh,
        theme,
        label=rf"$H(s)={meta['H_tf']}$",
        inputs=[port_h_in],
        outputs=[port_h_out],
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
            "grid": _GRID,
            **meta,
        },
    }

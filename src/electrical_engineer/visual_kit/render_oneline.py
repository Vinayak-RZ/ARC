"""IEEE-style one-line diagram from pandapower snapshot."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow, Polygon, Rectangle

from electrical_engineer.visual_kit.design_tokens import ThemeName, get_theme
from electrical_engineer.visual_kit.mpl_theme import apply_theme
from electrical_engineer.visual_kit.oneline_pandapower import load_flow_snapshot


def _bus_bar(ax, x, y, w, theme):
    ax.add_patch(Rectangle((x - w / 2, y - 0.06), w, 0.12, facecolor=theme.ink, edgecolor=theme.ink))


def render_power_oneline(out_dir: Path, *, theme_name: ThemeName = "light") -> dict[str, Any]:
    snap = load_flow_snapshot()
    theme = get_theme(theme_name)
    fig, ax = plt.subplots(figsize=(theme.fig_w * 1.2, theme.fig_h * 0.8))
    apply_theme(ax, theme)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    ax.set_title("Three-bus one-line (pandapower load flow)")

    y = 2.75
    buses = [
        ("Bus 1", 2.6, "slack"),
        ("Bus 2", 5.4, "load"),
        ("Bus 3", 8.2, "fault"),
    ]
    bus3_x = 8.2
    bus_bar_w = 1.15
    line_end = bus3_x + bus_bar_w / 2
    # Continuous backbone (ends at Bus 3 bar, not past it)
    ax.plot([0.8, line_end], [y, y], color=theme.ink, linewidth=1.4, zorder=0)

    # Generator
    ax.add_patch(Circle((0.8, y), 0.28, fill=False, edgecolor=theme.primary, linewidth=2))
    ax.text(0.8, y, "G", ha="center", va="center", color=theme.primary, fontsize=theme.label_size)

    brk_x = [1.75, 4.1, 6.9]
    for bx in brk_x:
        ax.add_patch(Rectangle((bx - 0.14, y - 0.18), 0.28, 0.36, fill=False, edgecolor=theme.ink, linewidth=1.4, zorder=2))
        ax.plot([bx - 0.08, bx + 0.08], [y - 0.04, y + 0.04], color=theme.accent, linewidth=1.6, zorder=2)

    by_name = {b["name"]: b for b in snap["buses"]}
    for label, x, key in buses:
        _bus_bar(ax, x, y, bus_bar_w, theme)
        ax.text(x, y + 0.28, label, ha="center", va="bottom", fontsize=theme.label_size, color=theme.ink)
        b = by_name.get(key)
        if b:
            ax.text(
                x,
                y - 0.26,
                rf"$V={b['vm_pu']:.3f}$ pu",
                ha="center",
                va="top",
                fontsize=theme.annotation_size,
                color=theme.muted,
            )

    # Load at Bus 2
    ax.plot([5.4, 5.4], [y - 0.06, 1.55], color=theme.fault, linewidth=1.4)
    tri = Polygon([(5.4, 1.25), (5.12, 1.75), (5.68, 1.75)], closed=True, edgecolor=theme.fault, fill=False, linewidth=1.5)
    ax.add_patch(tri)
    ax.add_patch(FancyArrow(5.4, 1.78, 0, 0.28, width=0.05, head_width=0.14, head_length=0.1, color=theme.fault, length_includes_head=True))
    if snap.get("load_p_mw"):
        ax.text(5.4, 1.05, rf"$P_L={snap['load_p_mw']:.1f}$ MW", ha="center", fontsize=theme.annotation_size, color=theme.fault)

    # Fault marker at Bus 3 (on connected bus)
    ax.plot([8.2, 8.2], [y - 0.06, 1.85], color=theme.hairline, linewidth=1.0, linestyle="--")
    ax.plot([8.0, 8.4], [1.55, 1.95], color=theme.fault, linewidth=2.2)
    ax.plot([8.0, 8.4], [1.95, 1.55], color=theme.fault, linewidth=2.2)
    ax.text(8.2, 1.35, "SLG study", ha="center", fontsize=theme.annotation_size, color=theme.fault)

    line_by_pair = {(ln["from"], ln["to"]): ln for ln in snap.get("lines") or []}
    segments = [("slack", "load", 3.05), ("load", "fault", 6.75)]
    for a, b, xm in segments:
        ln = line_by_pair.get((a, b)) or line_by_pair.get((b, a))
        if not ln:
            continue
        ax.text(xm, y + 0.95, rf"$P={ln['p_from_mw']:.2f}$ MW", ha="center", fontsize=theme.annotation_size, color=theme.ink)
        ax.text(xm, y + 1.18, rf"{ln.get('loading_pct', 0):.0f}% loaded", ha="center", fontsize=theme.annotation_size - 0.5, color=theme.muted)

    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / "power.oneline_bus.png"
    fig.savefig(png, dpi=theme.dpi, bbox_inches="tight", facecolor=theme.canvas)
    plt.close(fig)
    return {
        "png": str(png),
        "meta": {
            "component_id": "power.oneline_bus",
            "props_source": "pandapower",
            "connected_buses": 3,
            "snapshot": snap,
        },
    }

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
    ax.add_patch(Rectangle((x - w / 2, y - 0.08), w, 0.16, facecolor=theme.ink, edgecolor=theme.ink))


def _generator(ax, x, y, theme):
    circ = Circle((x, y), 0.35, fill=False, edgecolor=theme.primary, linewidth=2)
    ax.add_patch(circ)
    ax.text(x, y, "G", ha="center", va="center", fontsize=theme.label_size, color=theme.primary)


def _breaker(ax, x, y, theme, closed=True):
    rect = Rectangle((x - 0.18, y - 0.22), 0.36, 0.44, fill=False, edgecolor=theme.ink, linewidth=1.6)
    ax.add_patch(rect)
    if closed:
        ax.plot([x - 0.12, x + 0.12], [y - 0.05, y + 0.05], color=theme.accent, linewidth=1.8)


def _load(ax, x, y, theme):
    tri = Polygon([(x, y - 0.35), (x - 0.28, y + 0.15), (x + 0.28, y + 0.15)], closed=True, edgecolor=theme.fault, fill=False, linewidth=1.6)
    ax.add_patch(tri)
    ax.add_patch(FancyArrow(x, y + 0.18, 0, 0.35, width=0.06, head_width=0.18, head_length=0.12, color=theme.fault, length_includes_head=True))


def _fault_marker(ax, x, y, theme):
    ax.plot([x - 0.2, x + 0.2], [y - 0.2, y + 0.2], color=theme.fault, linewidth=2.4)
    ax.plot([x - 0.2, x + 0.2], [y + 0.2, y - 0.2], color=theme.fault, linewidth=2.4)


def render_power_oneline(out_dir: Path, *, theme_name: ThemeName = "light") -> dict[str, Any]:
    snap = load_flow_snapshot()
    theme = get_theme(theme_name)
    fig, ax = plt.subplots(figsize=(theme.fig_w * 1.15, theme.fig_h * 0.75))
    apply_theme(ax, theme)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_title("Three-bus one-line (pandapower load flow)")

    y = 2.8
    xs = {"slack": 1.2, "load": 5.5, "fault": 9.5}
    _generator(ax, xs["slack"], y, theme)
    _breaker(ax, 2.4, y, theme)
    _bus_bar(ax, 3.6, y, 1.4, theme)
    ax.plot([2.55, 3.2], [y, y], color=theme.ink, linewidth=1.8)
    _breaker(ax, 4.3, y, theme)
    ax.plot([4.45, 5.0], [y, y], color=theme.ink, linewidth=1.8)
    _bus_bar(ax, 5.5, y, 1.6, theme)
    _load(ax, 5.5, 1.5, theme)
    _breaker(ax, 7.2, y, theme)
    ax.plot([7.35, 8.2], [y, y], color=theme.ink, linewidth=1.8)
    _bus_bar(ax, 9.5, y, 1.4, theme)
    _fault_marker(ax, 9.5, y - 0.75, theme)
    ax.text(9.5, y - 1.1, "fault study bus", ha="center", fontsize=theme.annotation_size, color=theme.fault)

    by_name = {b["name"]: b for b in snap["buses"]}
    for name, x in xs.items():
        b = by_name.get(name)
        if not b:
            continue
        vm = b.get("vm_pu", 0)
        ax.text(x, y + 0.55, rf"$V={vm:.3f}$ pu", ha="center", fontsize=theme.annotation_size, color=theme.muted)
    for ln in snap.get("lines") or []:
        mid = (xs.get(ln["from"], 0) + xs.get(ln["to"], 0)) / 2
        ax.text(mid, y + 0.95, rf"$P={ln['p_from_mw']:.2f}$ MW", ha="center", fontsize=theme.annotation_size, color=theme.ink)
        ax.text(mid, y + 1.25, rf"load {ln.get('loading_pct', 0):.0f}%", ha="center", fontsize=theme.annotation_size - 0.5, color=theme.muted)
    if snap.get("load_p_mw"):
        ax.text(5.5, 0.85, rf"$P_L={snap['load_p_mw']:.1f}$ MW", ha="center", fontsize=theme.annotation_size, color=theme.fault)

    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / "power.oneline_bus.png"
    fig.savefig(png, dpi=theme.dpi, bbox_inches="tight", facecolor=theme.bg)
    plt.close(fig)
    return {"png": str(png), "meta": {"component_id": "power.oneline_bus", "props_source": "pandapower", "snapshot": snap}}

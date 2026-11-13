"""Power system Visual Kit figures."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np

from electrical_engineer.engines.agc_two_area import TwoAreaAgcCase, simulate_two_area
from electrical_engineer.engines.ed_lambda import EdCase, incremental_cost, solve_lambda_ed
from electrical_engineer.engines.smib_swing import SmibCase
from electrical_engineer.visual_kit.design_tokens import ThemeName, get_theme
from electrical_engineer.visual_kit.equal_area import equal_area_energies
from electrical_engineer.visual_kit.mpl_theme import apply_theme, direct_label


def _plt():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    return plt


def _save(fig, path: Path, theme) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=theme.dpi, bbox_inches="tight")
    plt = _plt()
    plt.close(fig)


def render_swing_equal_area(
    out_dir: Path,
    case: SmibCase | None = None,
    *,
    theme_name: ThemeName = "light",
) -> dict[str, Any]:
    case = case or SmibCase()
    metrics = equal_area_energies(case)
    theme = get_theme(theme_name)
    plt = _plt()
    fig, ax = plt.subplots(figsize=(theme.fig_w, theme.fig_h))
    apply_theme(ax, theme)

    deg_max = math.degrees(metrics["delta_max_rad"]) + 8.0
    delta_deg = np.linspace(0.0, deg_max, 500)
    delta_rad = np.radians(delta_deg)
    pe_pre = case.pmax_pre_pu * np.sin(delta_rad)
    pe_fault = case.pmax_fault_pu * np.sin(delta_rad)
    pe_post = case.pmax_post_pu * np.sin(delta_rad)

    ax.plot(delta_deg, pe_pre, color=theme.pre, linewidth=2.0, label="_pre")
    ax.plot(delta_deg, pe_fault, color=theme.fault, linewidth=2.0, linestyle="--")
    ax.plot(delta_deg, pe_post, color=theme.post, linewidth=2.0)
    ax.axhline(case.pm_pu, color=theme.mech, linewidth=1.6, linestyle="-")

    d0 = metrics["delta0_deg"]
    dcr = metrics["delta_cr_deg"]
    dmax = metrics["delta_max_deg"]
    rad = np.radians
    d1 = np.linspace(rad(d0), rad(dcr), 200)
    pe_f = case.pmax_fault_pu * np.sin(d1)
    ax.fill_between(
        np.degrees(d1),
        pe_f,
        case.pm_pu,
        where=case.pm_pu >= pe_f,
        color=theme.area_accel,
        linewidth=0,
    )
    d2 = np.linspace(rad(dcr), rad(dmax), 200)
    pe_p = case.pmax_post_pu * np.sin(d2)
    ax.fill_between(
        np.degrees(d2),
        case.pm_pu,
        pe_p,
        where=pe_p >= case.pm_pu,
        color=theme.area_decel,
        linewidth=0,
    )

    for xv, color in ((d0, theme.accent), (dcr, theme.fault), (dmax, theme.primary)):
        ax.axvline(xv, color=color, linewidth=1.0, alpha=0.65)

    ax.set_xlim(0, deg_max)
    ax.set_ylim(0, max(case.pmax_pre_pu, case.pm_pu) * 1.08)
    ax.set_xlabel(r"Rotor angle $\delta$ (deg)")
    ax.set_ylabel(r"Electrical power $P_e$ (pu)")
    ax.set_title("SMIB equal-area criterion")

    ymax = case.pmax_pre_pu * 0.92
    direct_label(ax, deg_max * 0.55, ymax, r"$P_{e,\mathrm{pre}}$", theme, color=theme.pre)
    direct_label(ax, deg_max * 0.35, case.pmax_fault_pu * 0.85, r"$P_{e,\mathrm{fault}}$", theme, color=theme.fault)
    direct_label(ax, deg_max * 0.72, case.pmax_post_pu * 0.88, r"$P_{e,\mathrm{post}}$", theme, color=theme.post)
    direct_label(ax, 4.0, case.pm_pu, r"$P_m$", theme, color=theme.mech, dy=8)
    direct_label(ax, d0, 0.08, r"$\delta_0$", theme, color=theme.accent)
    direct_label(ax, dcr, 0.08, r"$\delta_{\mathrm{cr}}$", theme, color=theme.fault)
    direct_label(ax, dmax, 0.08, r"$\delta_{\max}$", theme, color=theme.primary)
    ax.text(
        0.02,
        0.96,
        f"$A_1={metrics['A1_accel_rad']:.4f}$ rad·pu\n$A_2={metrics['A2_decel_rad']:.4f}$ rad·pu",
        transform=ax.transAxes,
        va="top",
        fontsize=theme.annotation_size,
        color=theme.ink,
        bbox={"facecolor": theme.bg, "edgecolor": theme.hairline, "boxstyle": "round,pad=0.35"},
    )

    png = out_dir / "power.swing_equal_area.png"
    _save(fig, png, theme)
    meta = {
        "component_id": "power.swing_equal_area",
        "props_source": "smib_swing",
        "theme": theme_name,
        **metrics,
    }
    return {"png": str(png), "meta": meta}


def render_agc_trace(out_dir: Path, *, theme_name: ThemeName = "light") -> dict[str, Any]:
    case = TwoAreaAgcCase.eec301_default().with_k(0.3)
    out = simulate_two_area(case, run="agc", t_end_s=25.0)
    trail = out.get("trail") or []
    theme = get_theme(theme_name)
    plt = _plt()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(theme.fig_w, theme.fig_h * 1.35), sharex=True)
    apply_theme(ax1, theme)
    apply_theme(ax2, theme)
    if trail:
        f0 = case.f0_hz
        t = [p[0] for p in trail]
        f1 = [p[1][0] * f0 for p in trail]
        f2 = [p[1][1] * f0 for p in trail]
        p12 = [p[1][6] * case.base_mva for p in trail]
        ax1.plot(t, f1, color=theme.primary, linewidth=1.8, label="_a1")
        ax1.plot(t, f2, color=theme.accent, linewidth=1.4, linestyle="--")
        ax2.plot(t, p12, color=theme.fault, linewidth=1.6)
    ax1.set_ylabel(r"Frequency (Hz)")
    ax1.set_title("Two-area load disturbance with AGC")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel(r"Tie power $P_{12}$ (MW)")
    direct_label(ax1, trail[-1][0] if trail else 0, f1[-1] if trail else 50, "Area 1", theme, color=theme.primary)
    direct_label(ax1, trail[-1][0] if trail else 0, f2[-1] if trail else 50, "Area 2", theme, color=theme.accent)
    png = out_dir / "power.agc_trace.png"
    fig.tight_layout()
    _save(fig, png, theme)
    return {
        "png": str(png),
        "meta": {"component_id": "power.agc_trace", "steady": out.get("steady"), "props_source": "agc_two_area"},
    }


def render_dispatch_curve(out_dir: Path, pd_mw: float = 500.0, *, theme_name: ThemeName = "light") -> dict[str, Any]:
    case = EdCase.eec301_default()
    theme = get_theme(theme_name)
    plt = _plt()
    fig, ax = plt.subplots(figsize=(theme.fig_w, theme.fig_h))
    apply_theme(ax, theme)
    p_grid = np.linspace(0, 320, 300)
    for i, u in enumerate(case.units, start=1):
        ic = [incremental_cost(float(p), u) for p in p_grid]
        ax.plot(p_grid, ic, linewidth=1.8, label="_u")
        direct_label(ax, u.pmax, incremental_cost(u.pmax, u), f"Gen {i}", theme, dy=i * 6)
    row = solve_lambda_ed(case, pd_mw)
    lam = row["lam"]
    ax.axhline(lam, color=theme.primary, linestyle=":", linewidth=1.2)
    for i, p in enumerate(row["P"]):
        ax.plot(p, incremental_cost(p, case.units[i]), "o", color=theme.accent, markersize=7)
        if row["status"][i] == "at_max":
            ax.axvline(case.units[i].pmax, color=theme.fault, alpha=0.35, linewidth=1.0)
    ax.set_xlabel(r"Generator output $P$ (MW)")
    ax.set_ylabel(r"Incremental cost $IC$ (\$/MWh)")
    ax.set_title(f"Economic dispatch, $P_D={pd_mw:.0f}$ MW")
    direct_label(ax, max(row["P"]), lam, rf"$\lambda={lam:.3f}$", theme, color=theme.primary)
    png = out_dir / "power.dispatch_curve.png"
    _save(fig, png, theme)
    return {
        "png": str(png),
        "meta": {"component_id": "power.dispatch_curve", "dispatch": row, "props_source": "ed_lambda"},
    }

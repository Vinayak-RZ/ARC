"""Control Visual Kit: Bode, step, root locus."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.visual_kit.design_tokens import ThemeName, get_theme
from electrical_engineer.visual_kit.mpl_theme import apply_theme


def _plt():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    return plt


def _default_plant():
    num = [10.0]
    den = [1.0, 1.0]
    return num, den


def render_control_bode(out_dir: Path, *, theme_name: ThemeName = "light") -> dict[str, Any]:
    import control
    import numpy as np

    num, den = _default_plant()
    sys = control.TransferFunction(num, den)
    theme = get_theme(theme_name)
    plt = _plt()
    fig, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(theme.fig_w, theme.fig_h * 1.2), sharex=True)
    apply_theme(ax_mag, theme)
    apply_theme(ax_phase, theme)
    omega = np.logspace(-2, 2, 400)
    mag, phase, _ = control.bode(sys, omega=omega, plot=False)
    mag_db = 20 * np.log10(mag)
    ax_mag.semilogx(omega, mag_db, color=theme.primary, linewidth=1.8)
    ax_phase.semilogx(omega, np.degrees(phase), color=theme.accent, linewidth=1.6)
    ax_mag.set_ylabel("Magnitude (dB)")
    ax_phase.set_ylabel(r"Phase (deg)")
    ax_phase.set_xlabel(r"$\omega$ (rad/s)")
    ax_mag.set_title("Bode diagram — unity feedback plant $10/(s+1)$")
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / "control.bode.png"
    fig.tight_layout()
    fig.savefig(png, dpi=theme.dpi, bbox_inches="tight")
    plt.close(fig)
    return {"png": str(png), "meta": {"component_id": "control.bode", "num": num, "den": den}}


def render_control_step(out_dir: Path, *, theme_name: ThemeName = "light") -> dict[str, Any]:
    import control

    num, den = _default_plant()
    sys = control.TransferFunction(num, den)
    theme = get_theme(theme_name)
    plt = _plt()
    fig, ax = plt.subplots(figsize=(theme.fig_w, theme.fig_h * 0.85))
    apply_theme(ax, theme)
    t, y = control.step_response(sys)
    ax.plot(t, y, color=theme.primary, linewidth=2.0)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(r"Output $y(t)$")
    ax.set_title("Unity-feedback step response")
    png = out_dir / "control.step.png"
    fig.tight_layout()
    fig.savefig(png, dpi=theme.dpi, bbox_inches="tight")
    plt.close(fig)
    return {"png": str(png), "meta": {"component_id": "control.step", "y_ss": float(y[-1])}}


def render_control_root_locus(out_dir: Path, *, theme_name: ThemeName = "light") -> dict[str, Any]:
    import control

    num, den = _default_plant()
    sys = control.TransferFunction(num, den)
    theme = get_theme(theme_name)
    plt = _plt()
    fig, ax = plt.subplots(figsize=(theme.fig_w, theme.fig_h))
    apply_theme(ax, theme)
    control.root_locus(sys, ax=ax, plot=True)
    for line in ax.lines:
        line.set_color(theme.primary)
        line.set_linewidth(1.2)
    ax.set_title("Root locus")
    png = out_dir / "control.root_locus.png"
    fig.tight_layout()
    fig.savefig(png, dpi=theme.dpi, bbox_inches="tight")
    plt.close(fig)
    return {"png": str(png), "meta": {"component_id": "control.root_locus"}}

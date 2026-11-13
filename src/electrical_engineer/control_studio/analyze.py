"""Frequency-domain and stability analysis."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from electrical_engineer.control_studio.compose import (
    compose_closed_loop,
    open_loop_with_controller,
)
from electrical_engineer.control_studio.margins import extract_margins
from electrical_engineer.control_studio.schema import StudioError
from electrical_engineer.engines.control_runner import control_available


def _plot_bode_open_loop(sys, path: Path, margins: dict[str, Any]) -> None:
    import control
    import matplotlib.pyplot as plt
    import numpy as np

    from electrical_engineer.visual_kit.design_tokens import get_theme
    from electrical_engineer.visual_kit.mpl_theme import apply_theme, direct_label

    theme = get_theme("light")
    wgc = margins.get("gain_crossover_rad_s")
    wpc = margins.get("phase_crossover_rad_s")
    gm_db = margins.get("gain_margin_db")
    pm = margins.get("phase_margin_deg")

    omega = np.logspace(-4, 3.5, 1200)
    mag, phase, omega_out = control.bode(sys, omega=omega, plot=False)
    mag_db = 20 * np.log10(np.maximum(mag, 1e-15))
    phase_deg = np.degrees(phase)

    fig_w = max(theme.fig_w, 10.0)
    fig, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(fig_w, fig_w * 0.52), sharex=True)
    apply_theme(ax_mag, theme)
    apply_theme(ax_phase, theme)
    cobalt = "#2F6FEB"
    ax_mag.semilogx(omega_out, mag_db, color=cobalt, linewidth=2.0)
    ax_phase.semilogx(omega_out, phase_deg, color=cobalt, linewidth=1.75)
    ax_mag.axhline(0, color=theme.muted, linewidth=0.8, linestyle="--")
    ax_phase.axhline(-180, color=theme.muted, linewidth=0.8, linestyle="--")

    ax_mag.set_title("")
    fig.suptitle("")
    ax_mag.set_ylabel("Magnitude (dB)")
    ax_phase.set_ylabel("Phase (deg)")
    ax_phase.set_xlabel("ω (rad/s)")
    ax_mag.tick_params(axis="x", labelbottom=False)
    ax_mag.set_xticklabels([])

    from matplotlib.ticker import FixedLocator, FuncFormatter

    x_lo, x_hi = 1e-2, 1e2
    decades = [1e-2, 1e-1, 1e0, 1e1, 1e2]

    def _decade_label(x: float, _pos: float) -> str:
        if x <= 0:
            return ""
        p = round(math.log10(x))
        return rf"$10^{{{p}}}$"

    for ax in (ax_mag, ax_phase):
        ax.set_xlim(x_lo, x_hi)
        ax.set_xscale("log")
        ax.xaxis.set_major_locator(FixedLocator(decades))
    ax_phase.xaxis.set_major_formatter(FuncFormatter(_decade_label))
    ax_phase.tick_params(axis="x", labelsize=theme.tick_size, colors=theme.ink, labelbottom=True)

    if wgc is not None and math.isfinite(wgc):
        ax_mag.axvline(wgc, color=theme.fault, linewidth=1.0, linestyle=":")
        mag_at = float(np.interp(wgc, omega_out, mag_db))
        ax_mag.plot(wgc, mag_at, "o", color=theme.fault, markersize=6)
        direct_label(ax_mag, wgc, mag_at, f"ωcg={wgc:.2g} rad/s", theme, color=theme.fault)
        if pm is not None and math.isfinite(pm):
            ph_at = float(np.interp(wgc, omega_out, phase_deg))
            ax_phase.plot(wgc, ph_at, "o", color=theme.fault, markersize=6)
            direct_label(ax_phase, wgc, ph_at, f"PM={pm:.1f}°", theme, color=theme.primary_dark)

    if wpc is not None and math.isfinite(wpc):
        ax_phase.axvline(wpc, color=theme.warning, linewidth=1.0, linestyle=":")
        ph_pc = float(np.interp(wpc, omega_out, phase_deg))
        mag_pc = float(np.interp(wpc, omega_out, mag_db))
        ax_phase.plot(wpc, ph_pc, "o", color=theme.warning, markersize=6)
        ax_mag.plot(wpc, mag_pc, "o", color=theme.warning, markersize=6)
        if gm_db is not None and math.isfinite(gm_db):
            direct_label(ax_mag, wpc, mag_pc, f"GM={gm_db:.1f} dB", theme, color=theme.warning)
        direct_label(ax_phase, wpc, ph_pc, f"ωcp={wpc:.2g} rad/s", theme, color=theme.warning)

    fig.subplots_adjust(hspace=0.08, left=0.1, right=0.98, top=0.96, bottom=0.16)
    fig.savefig(path, dpi=theme.dpi, bbox_inches="tight", facecolor=theme.canvas)
    plt.close(fig)


def analyze(diagram: dict[str, Any], *, run_dir: Path | None = None) -> dict[str, Any]:
    if not control_available():
        return {"ok": False, "error": "python-control missing", "unchecked": True}
    import control
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    from electrical_engineer.visual_kit.design_tokens import get_theme

    closed, meta = compose_closed_loop(diagram)
    run_dir = run_dir or Path("runs") / "_control_studio_scratch"
    run_dir.mkdir(parents=True, exist_ok=True)
    num = [float(x) for x in closed.num[0][0].tolist()]
    den = [float(x) for x in closed.den[0][0].tolist()]
    poles = np.roots(den).tolist()
    zeros = np.roots(num).tolist() if len(num) > 1 else []

    try:
        ol, ol_meta = open_loop_with_controller(diagram)
    except StudioError:
        ol = closed
        ol_meta = {"mode": "fallback_closed"}

    margins = extract_margins(ol)
    bode_png = run_dir / "studio_bode.png"
    nyquist_png = run_dir / "studio_nyquist.png"
    rlocus_png = run_dir / "studio_root_locus.png"

    _plot_bode_open_loop(ol, bode_png, margins)

    theme = get_theme("light")
    plt.figure(figsize=(5, 5))
    control.nyquist_plot(closed)
    plt.tight_layout()
    plt.savefig(nyquist_png, dpi=120)
    plt.close()

    fig = plt.figure(figsize=(theme.fig_w, theme.fig_h))
    control.root_locus(ol if ol is not closed else closed)
    plt.title("Root locus")
    plt.tight_layout()
    plt.savefig(rlocus_png, dpi=theme.dpi)
    plt.close(fig)

    return {
        "ok": True,
        "unchecked": False,
        "num": num,
        "den": den,
        "poles": [complex(p).real for p in poles] if poles else [],
        "zeros": [complex(z).real for z in zeros] if zeros else [],
        **margins,
        "compose": {**meta, "open_loop": ol_meta},
        "paths": {
            "bode": str(bode_png),
            "nyquist": str(nyquist_png),
            "root_locus": str(rlocus_png),
        },
    }

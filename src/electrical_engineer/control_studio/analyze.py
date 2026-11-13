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


def _plot_bode_annotated(sys, path: Path) -> None:
    import control
    import matplotlib.pyplot as plt
    import numpy as np

    from electrical_engineer.visual_kit.design_tokens import get_theme
    from electrical_engineer.visual_kit.mpl_theme import apply_theme

    theme = get_theme("light")
    margins = extract_margins(sys)
    wpc = margins.get("phase_crossover_rad_s")
    wgc = margins.get("gain_crossover_rad_s")
    gm_db = margins.get("gain_margin_db")
    pm = margins.get("phase_margin_deg")

    omega = np.logspace(-2, 2.5, 400)
    mag, phase, omega_out = control.bode(sys, omega=omega, plot=False)
    mag_db = 20 * np.log10(mag)
    phase_deg = np.degrees(phase)

    fig, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(theme.fig_w, theme.fig_h * 1.35), sharex=True)
    apply_theme(ax_mag, theme)
    apply_theme(ax_phase, theme)
    ax_mag.semilogx(omega_out, mag_db, color=theme.primary, linewidth=1.8)
    ax_phase.semilogx(omega_out, phase_deg, color=theme.accent, linewidth=1.6)
    ax_mag.axhline(0, color=theme.muted, linewidth=0.8, linestyle="--")
    ax_phase.axhline(-180, color=theme.muted, linewidth=0.8, linestyle="--")
    if wgc is not None:
        ax_mag.axvline(wgc, color=theme.fault, linewidth=0.9, linestyle=":")
        ax_mag.annotate(f"ωcg={wgc:.2f} rad/s", xy=(wgc, 0), fontsize=8, color=theme.ink)
    if wpc is not None:
        ax_phase.axvline(wpc, color=theme.fault, linewidth=0.9, linestyle=":")
        ax_phase.annotate(f"ωcp={wpc:.2f} rad/s", xy=(wpc, -180), fontsize=8, color=theme.ink)
    title_bits = []
    if gm_db is not None and math.isfinite(gm_db):
        title_bits.append(f"GM={gm_db:.2f} dB")
    if pm is not None and math.isfinite(pm):
        title_bits.append(f"PM={pm:.1f}°")
    ax_mag.set_title("Bode — " + ", ".join(title_bits) if title_bits else "Bode")
    ax_mag.set_ylabel("Magnitude (dB)")
    ax_phase.set_ylabel("Phase (deg)")
    ax_phase.set_xlabel("ω (rad/s)")
    fig.tight_layout()
    fig.savefig(path, dpi=theme.dpi, bbox_inches="tight")
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
        ol, _ = open_loop_with_controller(diagram)
    except StudioError:
        ol = closed

    margins = extract_margins(ol)
    bode_png = run_dir / "studio_bode.png"
    nyquist_png = run_dir / "studio_nyquist.png"
    rlocus_png = run_dir / "studio_root_locus.png"

    _plot_bode_annotated(ol, bode_png)

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
        "compose": meta,
        "paths": {
            "bode": str(bode_png),
            "nyquist": str(nyquist_png),
            "root_locus": str(rlocus_png),
        },
    }

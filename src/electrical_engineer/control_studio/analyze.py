"""Frequency-domain and stability analysis."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.control_studio.compose import (
    compose_closed_loop,
    open_loop_with_controller,
)
from electrical_engineer.control_studio.schema import StudioError
from electrical_engineer.engines.control_runner import control_available


def analyze(diagram: dict[str, Any], *, run_dir: Path | None = None) -> dict[str, Any]:
    if not control_available():
        return {"ok": False, "error": "python-control missing", "unchecked": True}
    import control
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    closed, meta = compose_closed_loop(diagram)
    run_dir = run_dir or Path("runs") / "_control_studio_scratch"
    run_dir.mkdir(parents=True, exist_ok=True)
    num = [float(x) for x in closed.num[0][0].tolist()]
    den = [float(x) for x in closed.den[0][0].tolist()]
    poles = np.roots(den).tolist()
    zeros = np.roots(num).tolist() if len(num) > 1 else []

    margin_out = control.margin(closed)
    gm = margin_out[0] if len(margin_out) > 0 else None
    pm = margin_out[1] if len(margin_out) > 1 else None
    bode_png = run_dir / "studio_bode.png"
    nyquist_png = run_dir / "studio_nyquist.png"
    rlocus_png = run_dir / "studio_rlocus.png"

    try:
        ol, _ = open_loop_with_controller(diagram)
    except StudioError:
        ol = closed

    plt.figure(figsize=(6.2, 3.8))
    control.bode_plot(closed, dB=True, Hz=False, omega_limits=(0.01, 100))
    plt.tight_layout()
    plt.savefig(bode_png, dpi=120)
    plt.close()

    plt.figure(figsize=(5, 5))
    control.nyquist_plot(closed)
    plt.tight_layout()
    plt.savefig(nyquist_png, dpi=120)
    plt.close()

    plt.figure(figsize=(6.2, 3.8))
    control.root_locus(ol if ol is not closed else closed)
    plt.tight_layout()
    plt.savefig(rlocus_png, dpi=120)
    plt.close()

    return {
        "ok": True,
        "unchecked": False,
        "num": num,
        "den": den,
        "poles": [complex(p).real for p in poles] if poles else [],
        "zeros": [complex(z).real for z in zeros] if zeros else [],
        "gain_margin_db": float(gm) if gm is not None else None,
        "phase_margin_deg": float(pm) if pm is not None else None,
        "compose": meta,
        "paths": {
            "bode": str(bode_png),
            "nyquist": str(nyquist_png),
            "root_locus": str(rlocus_png),
        },
    }

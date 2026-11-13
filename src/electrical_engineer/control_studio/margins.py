"""Stable margin extraction from python-control (linear GM, not dB)."""

from __future__ import annotations

import math
from typing import Any


def _fmt_num(x: float | None, *, digits: int = 2, unit: str = "") -> str:
    if x is None or not math.isfinite(x):
        return "—"
    if math.isinf(x):
        return "∞" + unit
    return f"{x:.{digits}f}{unit}"


def _numeric_margins(sys) -> tuple[float | None, float | None, float | None, float | None]:
    """Fallback when control.margin returns inf/nan (common for type-1 loops)."""
    import control
    import numpy as np

    w = np.logspace(-2, 3, 4000)
    mag, phase, wout = control.bode(sys, omega=w, plot=False)
    mag_db = 20.0 * np.log10(np.maximum(mag, 1e-12))
    phase_deg = np.degrees(phase)

    idx_pc = int(np.argmin(np.abs(phase_deg + 180.0)))
    w_phase_cross = float(wout[idx_pc])
    gm_db = float(-mag_db[idx_pc]) if math.isfinite(mag_db[idx_pc]) else None

    gm_lin = None
    if gm_db is not None and math.isfinite(gm_db):
        gm_lin = 10.0 ** (gm_db / 20.0)

    pm_deg = None
    w_gain_cross = None
    for i in range(len(mag_db) - 1):
        if mag_db[i] >= 0.0 >= mag_db[i + 1]:
            t = mag_db[i] / (mag_db[i] - mag_db[i + 1])
            w_gain_cross = float(wout[i] * (1 - t) + wout[i + 1] * t)
            phase_at = float(phase_deg[i] * (1 - t) + phase_deg[i + 1] * t)
            pm_deg = float(180.0 + phase_at)
            break

    return gm_lin, pm_deg, w_phase_cross, w_gain_cross


def extract_margins(sys) -> dict[str, Any]:
    import control

    out = control.margin(sys)
    if len(out) >= 4:
        gm_lin, pm_deg, w_phase_cross, w_gain_cross = out[0], out[1], out[2], out[3]
    elif len(out) >= 2:
        gm_lin, pm_deg = out[0], out[1]
        w_phase_cross = w_gain_cross = None
    else:
        gm_lin = pm_deg = w_phase_cross = w_gain_cross = None

    need_fallback = (
        gm_lin is None
        or pm_deg is None
        or not math.isfinite(gm_lin if gm_lin is not None else 0)
        or not math.isfinite(pm_deg if pm_deg is not None else 0)
        or (w_phase_cross is not None and not math.isfinite(w_phase_cross))
    )
    if need_fallback:
        gm_lin, pm_deg, w_phase_cross, w_gain_cross = _numeric_margins(sys)

    gm_db = None
    if gm_lin is not None and math.isfinite(gm_lin) and gm_lin > 0:
        gm_db = 20.0 * math.log10(float(gm_lin))
    if gm_lin is not None and math.isinf(gm_lin):
        gm_db = float("inf")

    note = None
    if pm_deg is None or not math.isfinite(pm_deg if pm_deg is not None else float("nan")):
        note = "No 0 dB crossing on open-loop gain; phase margin not defined."

    return {
        "gain_margin_linear": float(gm_lin) if gm_lin is not None and math.isfinite(gm_lin) else None,
        "gain_margin_db": float(gm_db) if gm_db is not None and math.isfinite(gm_db) else None,
        "phase_margin_deg": float(pm_deg) if pm_deg is not None and math.isfinite(pm_deg) else None,
        "phase_crossover_rad_s": float(w_phase_cross) if w_phase_cross is not None and math.isfinite(w_phase_cross) else None,
        "gain_crossover_rad_s": float(w_gain_cross) if w_gain_cross is not None and math.isfinite(w_gain_cross) else None,
        "margin_note": note,
        "display": {
            "gm_db": _fmt_num(gm_db, digits=2, unit=" dB"),
            "pm_deg": _fmt_num(pm_deg, digits=1, unit="°"),
            "wcg": _fmt_num(w_gain_cross, digits=2, unit=" rad/s"),
            "wcp": _fmt_num(w_phase_cross, digits=2, unit=" rad/s"),
        },
    }

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
    gm_db = None
    if gm_lin is not None and math.isfinite(gm_lin) and gm_lin > 0:
        gm_db = 20.0 * math.log10(float(gm_lin))
    if gm_lin is not None and math.isinf(gm_lin):
        gm_db = float("inf")
    return {
        "gain_margin_linear": float(gm_lin) if gm_lin is not None and math.isfinite(gm_lin) else None,
        "gain_margin_db": float(gm_db) if gm_db is not None and math.isfinite(gm_db) else None,
        "phase_margin_deg": float(pm_deg) if pm_deg is not None and math.isfinite(pm_deg) else None,
        "phase_crossover_rad_s": float(w_phase_cross) if w_phase_cross is not None and math.isfinite(w_phase_cross) else None,
        "gain_crossover_rad_s": float(w_gain_cross) if w_gain_cross is not None and math.isfinite(w_gain_cross) else None,
        "display": {
            "gm_db": _fmt_num(
                gm_db if gm_db is not None and math.isfinite(gm_db) else (float("inf") if gm_db is not None and math.isinf(gm_db) else None),
                digits=2,
                unit=" dB",
            ),
            "pm_deg": _fmt_num(pm_deg, digits=1, unit="°"),
            "wcg": _fmt_num(w_gain_cross, digits=2, unit=" rad/s"),
            "wcp": _fmt_num(w_phase_cross, digits=2, unit=" rad/s"),
        },
    }

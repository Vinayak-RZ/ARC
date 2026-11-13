"""Stable margin extraction from python-control (linear GM, not dB)."""

from __future__ import annotations

import math
from typing import Any

SWEEP_MIN_RAD_S = 1e-3
SWEEP_MAX_RAD_S = 1e5


def _band_note(kind: str = "gain") -> str:
    lo, hi = SWEEP_MIN_RAD_S, SWEEP_MAX_RAD_S
    if kind == "gain":
        return f"Gain stays above 0 dB from {lo:g} to {hi:g} rad/s."
    if kind == "phase":
        return f"Phase stays above −180° from {lo:g} to {hi:g} rad/s."
    return f"No crossing found from {lo:g} to {hi:g} rad/s."


def _fmt_freq(x: float | None) -> tuple[str, str | None]:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "No crossover in range", _band_note("gain")
    if math.isinf(x):
        return "Infinite", "The crossover lies beyond the analyzed frequency band."
    return f"{x:.4g} rad/s", None


def _fmt_gm_db(gm_db: float | None, gm_lin: float | None) -> tuple[str, str | None]:
    if gm_lin is not None and math.isinf(gm_lin):
        return "Infinite", "Gain margin is infinite because open-loop gain stays above 0 dB in the analyzed band."
    if gm_db is not None and math.isinf(gm_db):
        return "Infinite", "Gain margin is infinite because open-loop gain stays above 0 dB in the analyzed band."
    if gm_db is None or (isinstance(gm_db, float) and math.isnan(gm_db)):
        return "No crossover in range", _band_note("phase")
    return f"{gm_db:.2f} dB", None


def _fmt_pm(pm: float | None) -> tuple[str, str | None]:
    if pm is None or (isinstance(pm, float) and math.isnan(pm)):
        return "No crossover in range", _band_note("gain")
    if math.isinf(pm):
        return "Infinite", "Phase margin is infinite because phase stays above −180° at the gain crossover."
    return f"{pm:.1f}°", None


def _frd_crossings(sys) -> tuple[float | None, float | None, float | None, float | None]:
    """Verified 0 dB and −180° crossings on a wide log grid (no edge argmin)."""
    import control
    import numpy as np

    w = np.logspace(math.log10(SWEEP_MIN_RAD_S), math.log10(SWEEP_MAX_RAD_S), 12000)
    mag, phase, wout = control.bode(sys, omega=w, plot=False)
    edge = float(wout[1] / wout[0]) if len(wout) > 1 else 1.0

    def _reject_edge(freq: float | None) -> float | None:
        if freq is None or not math.isfinite(freq):
            return None
        if freq <= float(wout[0]) * edge or freq >= float(wout[-1]) / edge:
            return None
        return freq
    mag_db = 20.0 * np.log10(np.maximum(mag, 1e-15))
    phase_deg = np.degrees(phase)

    w_gain_cross = None
    pm_deg = None
    for i in range(len(mag_db) - 1):
        if mag_db[i] >= 0.0 >= mag_db[i + 1] or mag_db[i] <= 0.0 <= mag_db[i + 1]:
            if mag_db[i] == mag_db[i + 1]:
                continue
            t = mag_db[i] / (mag_db[i] - mag_db[i + 1])
            w_gain_cross = _reject_edge(float(wout[i] * (1 - t) + wout[i + 1] * t))
            if w_gain_cross is None:
                break
            phase_at = float(phase_deg[i] * (1 - t) + phase_deg[i + 1] * t)
            pm_deg = float(180.0 + phase_at)
            break

    w_phase_cross = None
    gm_db = None
    for i in range(len(phase_deg) - 1):
        p0, p1 = phase_deg[i], phase_deg[i + 1]
        if (p0 + 180.0) * (p1 + 180.0) < 0.0:
            if p0 == p1:
                continue
            t = (p0 + 180.0) / (p0 - p1)
            w_phase_cross = _reject_edge(float(wout[i] * (1 - t) + wout[i + 1] * t))
            if w_phase_cross is None:
                break
            m0, m1 = mag_db[i], mag_db[i + 1]
            mag_at = float(m0 * (1 - t) + m1 * t)
            gm_db = float(-mag_at)
            break

    gm_lin = 10.0 ** (gm_db / 20.0) if gm_db is not None and math.isfinite(gm_db) else None
    return gm_lin, pm_deg, w_phase_cross, w_gain_cross


def _from_stability_margins(sys) -> tuple[float | None, float | None, float | None, float | None]:
    import control

    try:
        out = control.stability_margins(sys)
    except (ValueError, TypeError, ArithmeticError):
        return None, None, None, None
    if len(out) < 6:
        return None, None, None, None
    gm_lin, pm_deg, _sm, wpc, wgc, _wst = out[0], out[1], out[2], out[3], out[4], out[5]
    for label, val in (("gm", gm_lin), ("pm", pm_deg), ("wpc", wpc), ("wgc", wgc)):
        if val is not None and isinstance(val, float) and math.isnan(val):
            if label == "gm":
                gm_lin = None
            elif label == "pm":
                pm_deg = None
            elif label == "wpc":
                wpc = None
            else:
                wgc = None
    return (
        float(gm_lin) if gm_lin is not None and math.isfinite(gm_lin) else (math.inf if gm_lin is not None and math.isinf(gm_lin) else None),
        float(pm_deg) if pm_deg is not None and math.isfinite(pm_deg) else (math.inf if pm_deg is not None and math.isinf(pm_deg) else None),
        float(wpc) if wpc is not None and math.isfinite(wpc) else None,
        float(wgc) if wgc is not None and math.isfinite(wgc) else None,
    )


def extract_margins(sys) -> dict[str, Any]:
    import control

    gm_lin = pm_deg = w_phase_cross = w_gain_cross = None
    used_frd = False

    try:
        gm_lin, pm_deg, w_phase_cross, w_gain_cross = control.margin(sys)
    except (ValueError, TypeError):
        gm_lin = pm_deg = w_phase_cross = w_gain_cross = None

    def _bad(v: float | None) -> bool:
        return v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v) and v < 0))

    if _bad(gm_lin) and _bad(pm_deg) and w_phase_cross is None and w_gain_cross is None:
        gm_lin, pm_deg, w_phase_cross, w_gain_cross = _from_stability_margins(sys)

    need_frd = w_phase_cross is None and w_gain_cross is None and (pm_deg is None or _bad(pm_deg))
    if need_frd:
        gm_lin, pm_deg, w_phase_cross, w_gain_cross = _frd_crossings(sys)
        used_frd = True

    gm_db = None
    if gm_lin is not None and math.isfinite(gm_lin) and gm_lin > 0:
        gm_db = 20.0 * math.log10(float(gm_lin))
    elif gm_lin is not None and math.isinf(gm_lin):
        gm_db = float("inf")

    if used_frd and w_phase_cross is None and gm_db is not None:
        gm_db = None
        gm_lin = None

    gm_s, gm_note = _fmt_gm_db(gm_db, gm_lin if isinstance(gm_lin, float) else None)
    pm_s, pm_note = _fmt_pm(pm_deg if isinstance(pm_deg, float) or pm_deg is None else float(pm_deg))
    wcg_s, wcg_note = _fmt_freq(w_gain_cross)
    wcp_s, wcp_note = _fmt_freq(w_phase_cross)

    return {
        "sweep_rad_s": [SWEEP_MIN_RAD_S, SWEEP_MAX_RAD_S],
        "gain_margin_linear": float(gm_lin) if gm_lin is not None and math.isfinite(gm_lin) else None,
        "gain_margin_db": float(gm_db) if gm_db is not None and math.isfinite(gm_db) else None,
        "gain_margin_infinite": bool(gm_lin is not None and math.isinf(gm_lin)) or bool(gm_db is not None and math.isinf(gm_db)),
        "phase_margin_deg": float(pm_deg) if pm_deg is not None and math.isfinite(pm_deg) else None,
        "phase_margin_infinite": bool(pm_deg is not None and math.isinf(pm_deg)),
        "phase_crossover_rad_s": float(w_phase_cross) if w_phase_cross is not None and math.isfinite(w_phase_cross) else None,
        "gain_crossover_rad_s": float(w_gain_cross) if w_gain_cross is not None and math.isfinite(w_gain_cross) else None,
        "margin_tooltips": {
            "gm_db": gm_note,
            "pm_deg": pm_note,
            "wcg": wcg_note,
            "wcp": wcp_note,
        },
        "display": {
            "gm_db": gm_s,
            "pm_deg": pm_s,
            "wcg": wcg_s,
            "wcp": wcp_s,
        },
    }

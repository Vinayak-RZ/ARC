"""Stable margin extraction from python-control (linear GM, not dB)."""

from __future__ import annotations

import math
from typing import Any

SWEEP_MIN_RAD_S = 1e-3
SWEEP_MAX_RAD_S = 1e5


def _band_note(kind: str = "gain") -> str:
    lo, hi = SWEEP_MIN_RAD_S, SWEEP_MAX_RAD_S
    lo_s, hi_s = f"{lo:g}", f"{hi:,g}"
    if kind == "gain":
        return f"Gain stays above 0 dB from {lo_s} to {hi_s} rad/s."
    if kind == "phase":
        return f"Phase stays above −180° from {lo_s} to {hi_s} rad/s."
    return f"No crossing found from {lo_s} to {hi_s} rad/s."


def _fmt_freq(x: float | None, *, phase_cross: bool = False) -> tuple[str, str | None]:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "No crossover in range", _phase_above_note() if phase_cross else None
    if math.isinf(x):
        return "Infinite", "The crossover lies beyond the analyzed frequency band."
    return f"{x:.4g} rad/s", None


def _phase_never_minus180_note() -> str:
    lo_s, hi_s = f"{SWEEP_MIN_RAD_S:g}", f"{SWEEP_MAX_RAD_S:,g}"
    return f"Phase never reaches −180° from {lo_s} to {hi_s} rad/s."


def _phase_above_note() -> str:
    lo_s, hi_s = f"{SWEEP_MIN_RAD_S:g}", f"{SWEEP_MAX_RAD_S:,g}"
    return f"Phase stays above −180° from {lo_s} to {hi_s} rad/s."


def _gain_band_note_from_db(lo_db: float, hi_db: float) -> str:
    lo_s, hi_s = f"{SWEEP_MIN_RAD_S:g}", f"{SWEEP_MAX_RAD_S:,g}"
    if lo_db > 0.0 and hi_db > 0.0:
        return f"Gain stays above 0 dB from {lo_s} to {hi_s} rad/s."
    if lo_db < 0.0 and hi_db < 0.0:
        return f"Gain stays below 0 dB from {lo_s} to {hi_s} rad/s."
    return f"No crossing found from {lo_s} to {hi_s} rad/s."


def _sweep_mag_db_ends(sys) -> tuple[float, float]:
    import control
    import numpy as np

    w = np.logspace(math.log10(SWEEP_MIN_RAD_S), math.log10(SWEEP_MAX_RAD_S), 400)
    mag, _, _ = control.bode(sys, omega=w, plot=False)
    mag_db = 20.0 * np.log10(np.maximum(mag, 1e-15))
    return float(mag_db[0]), float(mag_db[-1])


def _fmt_gm_db(gm_db: float | None, gm_lin: float | None) -> tuple[str, str | None]:
    if gm_lin is not None and math.isinf(gm_lin):
        return "Infinite", _phase_never_minus180_note()
    if gm_db is not None and math.isinf(gm_db):
        return "Infinite", _phase_never_minus180_note()
    if gm_db is None or (isinstance(gm_db, float) and math.isnan(gm_db)):
        return "No crossover in range", _band_note("phase")
    return f"{gm_db:.2f} dB", None


def _fmt_pm(pm: float | None, *, w_gain_cross: float | None = None) -> tuple[str, str | None]:
    if w_gain_cross is None or (isinstance(w_gain_cross, float) and not math.isfinite(w_gain_cross)):
        if pm is None or (isinstance(pm, float) and math.isnan(pm)):
            return "Not defined", "No gain crossover in range."
        if pm is not None and math.isinf(pm):
            return "Not defined", "No gain crossover in range."
        return "Not defined", "No gain crossover in range."
    if pm is None or (isinstance(pm, float) and math.isnan(pm)):
        return "No crossover in range", None
    if math.isinf(pm):
        return "Infinite", None
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

    lo_db, hi_db = _sweep_mag_db_ends(sys)
    gm_s, gm_note = _fmt_gm_db(gm_db, gm_lin if isinstance(gm_lin, float) else None)
    pm_s, pm_note = _fmt_pm(
        pm_deg if isinstance(pm_deg, float) or pm_deg is None else float(pm_deg),
        w_gain_cross=w_gain_cross,
    )
    wcg_s, wcg_note = _fmt_freq(w_gain_cross)
    if wcg_note is None and wcg_s == "No crossover in range":
        wcg_note = _gain_band_note_from_db(lo_db, hi_db)
    wcp_s, wcp_note = _fmt_freq(w_phase_cross, phase_cross=True)

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

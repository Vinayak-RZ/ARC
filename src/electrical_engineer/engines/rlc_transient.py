"""Series RLC step response (closed-form peak; optional fine integration for settling)."""

from __future__ import annotations

import math
from typing import Any, Literal


def _vc_peak_closed(v_step: float, zeta: float) -> float:
    if zeta < 1.0 - 1e-9:
        return v_step * (1.0 + math.exp(-math.pi * zeta / math.sqrt(max(1e-18, 1.0 - zeta * zeta))))
    return float(v_step)


def _t_vc_peak_closed(l_h: float, c_f: float, zeta: float) -> float:
    wn = 1.0 / math.sqrt(l_h * c_f)
    if zeta < 1.0 - 1e-9:
        wd = wn * math.sqrt(max(1e-18, 1.0 - zeta * zeta))
        return math.pi / wd
    return 0.0


def _settling_euler(
    r_ohm: float, l_h: float, c_f: float, v_step: float, *, h: float = 1e-5, t_end: float = 3.0
) -> float | None:
    """2% settling time via fine Euler (peak uses closed form)."""
    i = 0.0
    vc = 0.0
    tol = 0.02 * v_step
    in_band_at: float | None = None
    dwell = 0.05
    steps = int(t_end / h)
    t_peak = _t_vc_peak_closed(l_h, c_f, (r_ohm / 2.0) * math.sqrt(c_f / l_h))
    for n in range(steps):
        t = n * h
        if t <= t_peak:
            continue
        di = (v_step - vc - r_ohm * i) / l_h * h
        dvc = (i / c_f) * h
        i += di
        vc += dvc
        if abs(vc - v_step) <= tol:
            if in_band_at is None:
                in_band_at = t
            elif t - in_band_at >= dwell:
                return in_band_at
        else:
            in_band_at = None
    return None


def series_rlc_step(
    r_ohm: float,
    l_h: float,
    c_f: float,
    v_step: float,
    *,
    zeta_target: float | None = None,
) -> dict[str, Any]:
    if l_h <= 0 or c_f <= 0 or r_ohm < 0:
        raise ValueError("R, L, C must be positive for series RLC")
    wn = 1.0 / math.sqrt(l_h * c_f)
    zeta = (r_ohm / 2.0) * math.sqrt(c_f / l_h)
    if zeta < 1.0 - 1e-9:
        damping: Literal["underdamped", "overdamped", "critically_damped"] = "underdamped"
    elif zeta > 1.0 + 1e-9:
        damping = "overdamped"
    else:
        damping = "critically_damped"

    vc_peak = _vc_peak_closed(v_step, zeta)
    t_peak = _t_vc_peak_closed(l_h, c_f, zeta)
    t_settle = _settling_euler(r_ohm, l_h, c_f, v_step)

    return {
        "damping_type": damping,
        "zeta": zeta,
        "omega_n_rad_s": wn,
        "Vc_peak_V": float(vc_peak),
        "t_Vc_peak_s": float(t_peak),
        "settling_time_2pct_s": float(t_settle) if t_settle is not None else None,
        "engine": "rlc_closed_form",
    }


def solve_from_problem(problem: dict[str, Any]) -> dict[str, Any]:
    r = float(problem.get("r_ohm") or problem.get("R") or 4.0)
    l = float(problem.get("l_h") or problem.get("L") or 0.5)
    c = float(problem.get("c_f") or problem.get("C") or 0.02)
    v = float(problem.get("v_step") or problem.get("V") or 12.0)
    return series_rlc_step(r, l, c, v)
"""Series RLC step response (analytic; no ngspice)."""

from __future__ import annotations

import math
from typing import Any, Literal


def _integrate_series_rlc(
    r_ohm: float, l_h: float, c_f: float, v_step: float, *, h: float = 1e-4, t_end: float = 3.0
) -> tuple[float, float, float | None]:
    i = 0.0
    vc = 0.0
    v_peak = vc
    t_peak = 0.0
    tol = 0.02 * v_step
    t_settle: float | None = None
    in_band_at: float | None = None
    dwell = 0.05
    steps = int(t_end / h)
    for n in range(steps):
        t = n * h
        di = (v_step - vc - r_ohm * i) / l_h * h
        dvc = (i / c_f) * h
        i += di
        vc += dvc
        if vc > v_peak:
            v_peak = vc
            t_peak = t
        if t > t_peak:
            if abs(vc - v_step) <= tol:
                if in_band_at is None:
                    in_band_at = t
                elif t - in_band_at >= dwell and t_settle is None:
                    t_settle = in_band_at
            else:
                in_band_at = None
    return v_peak, t_peak, t_settle


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

    vc_peak, t_peak, t_settle_2pct = _integrate_series_rlc(r_ohm, l_h, c_f, v_step)

    return {
        "damping_type": damping,
        "zeta": zeta,
        "omega_n_rad_s": wn,
        "Vc_peak_V": float(vc_peak),
        "t_Vc_peak_s": float(t_peak),
        "settling_time_2pct_s": float(t_settle_2pct) if t_settle_2pct is not None else None,
    }


def solve_from_problem(problem: dict[str, Any]) -> dict[str, Any]:
    r = float(problem.get("r_ohm") or problem.get("R") or 4.0)
    l = float(problem.get("l_h") or problem.get("L") or 0.5)
    c = float(problem.get("c_f") or problem.get("C") or 0.02)
    v = float(problem.get("v_step") or problem.get("V") or 12.0)
    return series_rlc_step(r, l, c, v)

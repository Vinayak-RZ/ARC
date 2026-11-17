"""Series RLC step response (analytic peak; RK4 tail for settling)."""

from __future__ import annotations

import math
from typing import Any, Literal


def _rk4_vc_tail(
    r_ohm: float, l_h: float, c_f: float, v_step: float, *, wn: float, t_start: float, t_end: float, h: float
) -> float | None:
    """2% settling time after the peak (vc within band of v_step)."""
    if t_start > 0:
        # Seed from state at t_start would need full history; integrate from 0 for settling metric.
        pass

    def deriv(_t: float, state: tuple[float, float]) -> tuple[float, float]:
        ii, vcc = state
        di = (v_step - vcc - r_ohm * ii) / l_h
        dvc = ii / c_f
        return di, dvc

    def rk4_step(t: float, state: tuple[float, float], step: float) -> tuple[float, float]:
        di1, dvc1 = deriv(t, state)
        di2, dvc2 = deriv(t + step / 2, (state[0] + di1 * step / 2, state[1] + dvc1 * step / 2))
        di3, dvc3 = deriv(t + step / 2, (state[0] + di2 * step / 2, state[1] + dvc2 * step / 2))
        di4, dvc4 = deriv(t + step, (state[0] + di3 * step, state[1] + dvc3 * step))
        ii = state[0] + (step / 6) * (di1 + 2 * di2 + 2 * di3 + di4)
        vcc = state[1] + (step / 6) * (dvc1 + 2 * dvc2 + 2 * dvc3 + dvc4)
        return ii, vcc

    tol = 0.02 * v_step
    dwell = 0.05
    in_band_at: float | None = None
    t_settle: float | None = None
    state = (0.0, 0.0)
    t = 0.0
    while t < t_end:
        state = rk4_step(t, state, h)
        t += h
        if t < t_start:
            continue
        vc = state[1]
        if abs(vc - v_step) <= tol:
            if in_band_at is None:
                in_band_at = t
            elif t - in_band_at >= dwell and t_settle is None:
                t_settle = in_band_at
        else:
            in_band_at = None
    return t_settle


def _critical_settling_2pct_s(wn: float) -> float:
    """ζ = 1: (1 + x) e^-x = 0.02 ⇒ x ≈ 5.834, t_s = x/ωn (2% envelope from below)."""
    lo, hi = 0.0, 50.0
    target = 0.02
    for _ in range(72):
        mid = (lo + hi) * 0.5
        val = (1.0 + mid) * math.exp(-mid)
        if val > target:
            lo = mid
        else:
            hi = mid
    x = (lo + hi) * 0.5
    return x / wn


def _underdamped_peak(v_step: float, zeta: float, wn: float) -> tuple[float, float]:
    wd = wn * math.sqrt(1.0 - zeta * zeta)
    vc_peak = v_step * (1.0 + math.exp(-math.pi * zeta / math.sqrt(1.0 - zeta * zeta)))
    t_peak = math.pi / wd
    return vc_peak, t_peak


def _rk4_integrate_vc(
    r_ohm: float, l_h: float, c_f: float, v_step: float, *, t_end: float, n: int = 320
) -> list[list[float]]:
    """Sample capacitor voltage (V) versus time (ms) for plotting."""
    n = max(n, 2)
    h = t_end / (n - 1)

    def deriv(_t: float, state: tuple[float, float]) -> tuple[float, float]:
        ii, vcc = state
        return (v_step - vcc - r_ohm * ii) / l_h, ii / c_f

    def rk4_step(t: float, state: tuple[float, float], step: float) -> tuple[float, float]:
        di1, dvc1 = deriv(t, state)
        di2, dvc2 = deriv(t + step / 2, (state[0] + di1 * step / 2, state[1] + dvc1 * step / 2))
        di3, dvc3 = deriv(t + step / 2, (state[0] + di2 * step / 2, state[1] + dvc2 * step / 2))
        di4, dvc4 = deriv(t + step, (state[0] + di3 * step, state[1] + dvc3 * step))
        ii = state[0] + (step / 6) * (di1 + 2 * di2 + 2 * di3 + di4)
        vcc = state[1] + (step / 6) * (dvc1 + 2 * dvc2 + 2 * dvc3 + dvc4)
        return ii, vcc

    pts: list[list[float]] = []
    state = (0.0, 0.0)
    t = 0.0
    for _ in range(n):
        pts.append([t * 1000.0, float(state[1])])
        if t >= t_end - 1e-15:
            break
        state = rk4_step(t, state, h)
        t += h
    return pts


def forward_euler_vc_peak(
    r_ohm: float, l_h: float, c_f: float, v_step: float, *, steps_per_wn: float = 200.0
) -> tuple[float, float]:
    """Intentionally coarse forward Euler peak (demo bad-derive path)."""
    wn = 1.0 / math.sqrt(l_h * c_f)
    h = 1.0 / (steps_per_wn * wn)
    t_end = max(5.0 / wn, 3.0 * h)
    state = (0.0, 0.0)
    v_peak = 0.0
    t_peak = 0.0
    t = 0.0
    while t < t_end:
        di = (v_step - state[1] - r_ohm * state[0]) / l_h * h
        dvc = (state[0] / c_f) * h
        state = (state[0] + di, state[1] + dvc)
        t += h
        if state[1] > v_peak:
            v_peak = state[1]
            t_peak = t
    return v_peak, t_peak


def _overdamped_peak(v_step: float, r_ohm: float, l_h: float, c_f: float, zeta: float, wn: float) -> tuple[float, float]:
    h = 1.0 / (200.0 * wn)
    t_end = max(8.0 / wn, 3.0)
    state = (0.0, 0.0)
    v_peak = 0.0
    t_peak = 0.0
    t = 0.0
    while t < t_end:
        di = (v_step - state[1] - r_ohm * state[0]) / l_h * h
        dvc = (state[0] / c_f) * h
        state = (state[0] + di, state[1] + dvc)
        t += h
        if state[1] > v_peak:
            v_peak = state[1]
            t_peak = t
    return v_peak, t_peak


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

    h = 1.0 / (200.0 * wn)
    if damping == "underdamped":
        vc_peak, t_peak = _underdamped_peak(v_step, zeta, wn)
    else:
        vc_peak, t_peak = _overdamped_peak(v_step, r_ohm, l_h, c_f, zeta, wn)

    t_settle_2pct = _rk4_vc_tail(
        r_ohm, l_h, c_f, v_step, wn=wn, t_start=t_peak, t_end=max(12.0 / wn, 3.0), h=h
    )
    t_ref = t_settle_2pct if t_settle_2pct is not None else max(t_peak * 1.5, 4.0 / wn)
    t_plot_end = min(max(5.0 * float(t_ref), 12.0 / wn), 0.08)
    vc_trace_ms = _rk4_integrate_vc(r_ohm, l_h, c_f, v_step, t_end=max(t_plot_end, 0.02), n=480)
    overshoot_pct = max(0.0, (float(vc_peak) - v_step) / v_step * 100.0) if v_step else 0.0
    if damping == "critically_damped":
        settling_entry_s = _critical_settling_2pct_s(wn)
    else:
        settling_entry_s = None
        band = 0.02 * v_step
        for t_ms, vc in vc_trace_ms:
            if vc >= v_step - band:
                settling_entry_s = float(t_ms) / 1000.0
                break

    return {
        "damping_type": damping,
        "zeta": zeta,
        "omega_n_rad_s": wn,
        "Vc_peak_V": float(vc_peak),
        "t_Vc_peak_s": float(t_peak),
        "settling_time_2pct_s": float(t_settle_2pct) if t_settle_2pct is not None else None,
        "settling_2pct_entry_s": settling_entry_s,
        "overshoot_pct": overshoot_pct,
        "vc_trace_ms": vc_trace_ms,
        "engine": "rlc_analytic",
    }


def solve_from_problem(problem: dict[str, Any]) -> dict[str, Any]:
    r = float(problem.get("r_ohm") or problem.get("R") or 4.0)
    l = float(problem.get("l_h") or problem.get("L") or 0.5)
    c = float(problem.get("c_f") or problem.get("C") or 0.02)
    v = float(problem.get("v_step") or problem.get("V") or 12.0)
    return series_rlc_step(r, l, c, v)
"""Ideal six-pulse rectifier vo(ωt) and firing marks (EEC-303 alignment)."""

from __future__ import annotations

import itertools
import math

_PI = math.pi
_TWO_PI = 2 * _PI
_SQRT2 = math.sqrt(2.0)
_SQRT3 = math.sqrt(3.0)

_FULL3_LINE_PAIRS: tuple[tuple[int, int], ...] = (
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 0),
    (2, 0),
    (2, 1),
)


def _norm_topology(topology: str) -> str:
    t = str(topology or "full3")
    if t in {"half", "hw3"}:
        return "hw3"
    if t == "full":
        return "full3"
    if t == "semi":
        return "semi3"
    if t == "half1":
        return "hw1"
    return t


def firing_angles_deg(topology: str, alpha_deg: float) -> list[float]:
    """Commutation instants on ωt (phase-a / v_an zero-crossing axis used by the lab x-axis)."""
    topo = _norm_topology(topology)
    alpha = float(alpha_deg)
    if topo == "full3":
        fire0 = 30.0 + alpha
        return [((fire0 + 60.0 * k) % 360.0) for k in range(6)]
    if topo in {"hw3", "semi3"}:
        return [((alpha + b) % 360.0) for b in (30.0, 150.0, 270.0)]
    if topo in {"full1", "semi1"}:
        return [((alpha + b) % 360.0) for b in (0.0, 180.0)]
    return [alpha % 360.0]


def vo_full3_analytic(wt: float, vll_pk: float, alpha_deg: float) -> float:
    vm = vll_pk / _SQRT3
    fire0 = 30.0 + float(alpha_deg)
    deg_wt = math.degrees(wt)
    rel = ((deg_wt - fire0) % 360.0 + 360.0) % 360.0
    k = int(rel // 60.0) % 6
    ia, ib = _FULL3_LINE_PAIRS[k]

    def phase(ph: int) -> float:
        return vm * math.sin(wt - ph * _TWO_PI / 3.0)

    return phase(ia) - phase(ib)


def line_peak_from_line_vll(v_ll_rms: float) -> float:
    return _SQRT2 * v_ll_rms


def phase_peak_from_line_vll(v_ll_rms: float) -> float:
    return _SQRT2 * v_ll_rms / _SQRT3


def hw3_rl_pulse_width_deg(alpha_deg: float) -> float:
    if alpha_deg >= 90:
        return 0.0
    if alpha_deg <= 30:
        return 120.0
    knots = ((30, 119), (45, 90), (60, 60), (75, 30), (89, 4))
    if alpha_deg >= knots[-1][0]:
        return float(knots[-1][1])
    for (a0, w0), (a1, w1) in itertools.pairwise(knots):
        if alpha_deg <= a1:
            t = (alpha_deg - a0) / (a1 - a0)
            return w0 + t * (w1 - w0)
    return 0.0


def vo_full1_rl_wave(wt: float, vm: float, alpha_deg: float) -> float:
    alpha = math.radians(alpha_deg)
    beta = _PI + alpha
    w = ((wt % _TWO_PI) + _TWO_PI) % _TWO_PI
    if alpha <= w < beta:
        return vm * math.sin(wt)
    return 0.0


def vo_hw3_rl_continuous(wt: float, vm_ph: float, alpha_deg: float) -> float:
    alpha = math.radians(alpha_deg)
    w = ((wt % _TWO_PI) + _TWO_PI) % _TWO_PI
    vo = 0.0
    for k in range(3):
        fire = _PI / 6.0 + alpha + k * _TWO_PI / 3.0
        vf = ((fire % _TWO_PI) + _TWO_PI) % _TWO_PI
        phase_shift = k * _TWO_PI / 3.0
        next_fire = _PI / 6.0 + alpha + ((k + 1) % 3) * _TWO_PI / 3.0
        end = ((next_fire % _TWO_PI) + _TWO_PI) % _TWO_PI
        if vf <= end:
            in_cond = vf <= w < end
        else:
            in_cond = w >= vf or w < end
        if not in_cond:
            continue
        v = vm_ph * math.sin(w - phase_shift)
        vo = max(vo, v)
    return vo


def vo_hw3_r_wave(wt: float, vm_ph: float, alpha_deg: float) -> float:
    alpha = math.radians(alpha_deg)
    w = ((wt % _TWO_PI) + _TWO_PI) % _TWO_PI
    vo = 0.0
    for k in range(3):
        fire = _PI / 6.0 + alpha + k * _TWO_PI / 3.0
        vf = ((fire % _TWO_PI) + _TWO_PI) % _TWO_PI
        phase_shift = k * _TWO_PI / 3.0
        end = ((phase_shift + _PI) % _TWO_PI + _TWO_PI) % _TWO_PI
        if vf <= end:
            in_cond = vf <= w < end
        else:
            in_cond = w >= vf or w < end
        if not in_cond:
            continue
        v = vm_ph * math.sin(wt - phase_shift)
        vo = max(vo, max(0.0, v))
    return max(0.0, vo)


def vo_hw3_rl_wave(wt: float, vm_ph: float, alpha_deg: float) -> float:
    pulse = math.radians(hw3_rl_pulse_width_deg(alpha_deg))
    if pulse <= 0:
        return 0.0
    alpha = math.radians(alpha_deg)
    w = ((wt % _TWO_PI) + _TWO_PI) % _TWO_PI
    vo = 0.0
    for k in range(3):
        fire = _PI / 6.0 + alpha + k * _TWO_PI / 3.0
        vf = ((fire % _TWO_PI) + _TWO_PI) % _TWO_PI
        end = (vf + pulse) % _TWO_PI
        if vf <= end:
            in_cond = vf <= w < end
        else:
            in_cond = w >= vf or w < end
        if not in_cond:
            continue
        v = vm_ph * math.sin(wt - k * _TWO_PI / 3.0)
        vo = max(vo, v)
    return vo
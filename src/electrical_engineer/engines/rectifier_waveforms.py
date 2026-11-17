"""Rectifier output waveforms aligned with ui/src/studio-engine/labs/rectifier.js."""

from __future__ import annotations

import math

_PI = math.pi
_TWO_PI = 2.0 * _PI
_SQRT2 = math.sqrt(2.0)
_SQRT3 = math.sqrt(3.0)


def _deg(rad: float) -> float:
    return math.degrees(rad)


def _rad(deg: float) -> float:
    return math.radians(deg)


def phase_peak_from_line_vll(v_ll_rms: float) -> float:
    return _SQRT2 * v_ll_rms / _SQRT3


def line_peak_from_line_vll(v_ll_rms: float) -> float:
    return _SQRT2 * v_ll_rms


def is_continuous_conduction(load: str, topology: str, alpha_deg: float) -> bool:
    if load != "R":
        return True
    if topology == "full1":
        return False
    if topology == "full3":
        return alpha_deg <= 60.0
    if topology in {"hw3", "half3"}:
        return alpha_deg <= 30.0
    return alpha_deg <= 0.0


def source_peak_v(problem: dict) -> float:
    topology = str(problem.get("topology") or "full3")
    v_rms = float(problem.get("v_ll_rms") or problem.get("v_rms") or 415)
    if topology.endswith("3"):
        return line_peak_from_line_vll(v_rms)
    return _SQRT2 * v_rms


def _vo_three_phase_half(wt: float, vm: float, alpha_rad: float, continuous: bool) -> float:
    vo = 0.0
    w = ((wt % _TWO_PI) + _TWO_PI) % _TWO_PI
    for k in range(3):
        fire = _PI / 6.0 + alpha_rad + k * (_TWO_PI / 3.0)
        vf = ((fire % _TWO_PI) + _TWO_PI) % _TWO_PI
        phase_shift = k * (_TWO_PI / 3.0)
        end = ((phase_shift + _PI) % _TWO_PI + _TWO_PI) % _TWO_PI
        if continuous:
            next_fire = _PI / 6.0 + alpha_rad + ((k + 1) % 3) * (_TWO_PI / 3.0)
            end = ((next_fire % _TWO_PI) + _TWO_PI) % _TWO_PI
        if vf <= end:
            in_cond = vf <= w < end
        else:
            in_cond = w >= vf or w < end
        if not in_cond:
            continue
        v = vm * math.sin(w - phase_shift)
        if continuous or v > 0:
            vo = max(vo, v) if continuous else max(vo, max(0.0, v))
    return vo if continuous else max(0.0, vo)


def _vo_six_pulse(wt: float, vll_pk: float, alpha_rad: float, allow_negative: bool) -> float:
    """Legacy (wrong arcs); kept only for import stability — use gate / vo_full3_analytic."""
    from electrical_engineer.engines.rectifier_steady import vo_full3_analytic

    return vo_full3_analytic(wt, vll_pk, math.degrees(alpha_rad))


def _vo_semi_freewheel_1(wt: float, vm: float, alpha_rad: float) -> float:
    cycle = ((wt % _PI) + _PI) % _PI
    if cycle < alpha_rad:
        return 0.0
    return abs(vm * math.sin(wt))


def _vo_single_phase_half(wt: float, vm: float, alpha_rad: float, full_wave: bool, continuous: bool) -> float:
    if full_wave:
        cycle = ((wt % _PI) + _PI) % _PI
        if cycle < alpha_rad:
            return 0.0
        v = vm * math.sin(wt)
        mag = abs(v)
        if not continuous:
            return mag
        return v if v < 0 else mag
    cycle = ((wt % _TWO_PI) + _TWO_PI) % _TWO_PI
    if alpha_rad <= cycle < _PI:
        return max(0.0, vm * math.sin(wt))
    return 0.0


def sample_waveform(problem: dict, n: int = 720) -> list[list[float]]:
    from electrical_engineer.engines.rectifier_gate import gate_sample_vo

    prob = dict(problem)
    load = str(prob.get("load") or "R")
    if load in {"RL", "RLE"} and float(prob.get("io_a") or 0) <= 0:
        vo = _vo_closed_form(problem, None, None)
        r_ohm = float(prob.get("r_ohm") or 10.0)
        if vo and r_ohm > 0:
            prob["io_a"] = max(1e-3, abs(vo) / r_ohm)
    return gate_sample_vo(prob, n)


def _vo_closed_form(problem: dict, rectifier_1ph, rectifier_3ph) -> float:
    topology = str(problem.get("topology") or "full3")
    alpha_deg = float(problem.get("alpha_deg") or 0)
    load = str(problem.get("load") or "R")
    io = float(problem.get("io_a") or 0)
    ls = float(problem.get("ls_h") or 0)
    f_hz = float(problem.get("f_hz") or 50)
    alpha = _rad(alpha_deg)
    w = 2.0 * _PI * f_hz
    cos_a = math.cos(alpha)
    v_rms = float(problem.get("v_rms") or 230)
    if topology in {"hw1", "half1"}:
        vm = _SQRT2 * v_rms
        return (vm / (2.0 * _PI)) * (1.0 + cos_a)
    if topology == "semi1":
        vm = _SQRT2 * v_rms
        return (vm / _PI) * (1.0 + cos_a) - (w * ls * io) / _PI
    if topology == "full1":
        vm = _SQRT2 * v_rms
        e_v = float(problem.get("e_v") or 0.0)
        if ls <= 0 and load == "R":
            # R load: each SCR conducts alpha..pi, so Vo = Vm/pi (1 + cos alpha) for 0..180 deg.
            return (vm / _PI) * (1.0 + cos_a)
        if alpha_deg >= 90 and e_v <= 0:
            return 0.0
        return (2.0 * vm * cos_a) / _PI - (2.0 * w * ls * io) / _PI
    v_ll = float(problem.get("v_ll_rms") or problem.get("v_rms") or 415)
    vm_ph = phase_peak_from_line_vll(v_ll)
    vll_pk = line_peak_from_line_vll(v_ll)
    cc = is_continuous_conduction(load, topology, alpha_deg)
    if topology in {"hw3", "half3"}:
        e_v = float(problem.get("e_v") or 0.0)
        if load != "R" and alpha_deg > 90 and e_v <= 0:
            return 0.0
        if load == "R" and ls <= 0 and alpha_deg >= 150:
            # Firing at 30 + alpha lands at or past the phase zero crossing: no conduction.
            return 0.0
        if cc:
            return (3.0 * _SQRT3 * vm_ph / (2.0 * _PI)) * cos_a - (3.0 * w * ls * io) / (2.0 * _PI)
        return (3.0 / (2.0 * _PI)) * vm_ph * (1.0 + math.cos(alpha + _PI / 6.0))
    if topology == "semi3":
        return (3.0 * vll_pk / (2.0 * _PI)) * (1.0 + cos_a) - (3.0 * w * ls * io) / (2.0 * _PI)
    if load == "R" and ls <= 0:
        if alpha_deg > 120:
            return 0.0
        if alpha_deg > 60:
            return (3.0 * vll_pk / _PI) * (1.0 + math.cos(alpha + _PI / 3.0))
        return (3.0 * vll_pk / _PI) * cos_a
    e_v = float(problem.get("e_v") or 0.0)
    if load != "R" and alpha_deg > 90 and e_v <= 0:
        return 0.0
    return (3.0 * vll_pk / _PI) * cos_a - (3.0 * w * ls * io) / _PI


def mean_waveform(points: list[list[float]]) -> float:
    if not points:
        return float("nan")
    return sum(y for _, y in points) / len(points)
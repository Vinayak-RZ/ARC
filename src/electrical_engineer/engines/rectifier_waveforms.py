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
    if topology.endswith("3"):
        return alpha_deg <= 30.0
    return alpha_deg <= 0.0


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
    seg = _PI / 3.0
    w = ((wt - alpha_rad) % _TWO_PI + _TWO_PI) % _TWO_PI
    local = w - math.floor(w / seg) * seg
    vo = vll_pk * math.cos(local - _PI / 6.0 - alpha_rad)
    return vo if allow_negative else max(0.0, vo)


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
    topology = str(problem.get("topology") or "full3")
    if topology in {"half", "hw3"}:
        topology = "hw3"
    elif topology in {"full"}:
        topology = "full3"
    elif topology == "semi":
        topology = "semi3"
    load = str(problem.get("load") or "R")
    if load == "continuous":
        load = "RL"
    v_rms = float(problem.get("v_ll_rms") or problem.get("v_rms") or 415)
    alpha_deg = float(problem.get("alpha_deg") or 0)
    alpha_rad = _rad(alpha_deg)
    vm1 = _SQRT2 * v_rms if not topology.endswith("3") else 0.0
    vm3 = phase_peak_from_line_vll(v_rms)
    vll_pk = line_peak_from_line_vll(v_rms) if topology.endswith("3") else 0.0
    cc = is_continuous_conduction(load, topology, alpha_deg)
    cc_wave = cc or topology in {"full1", "full3", "semi3"}
    points: list[list[float]] = []
    for i in range(n):
        wt = _TWO_PI * i / n
        if topology == "full3" or topology == "semi3":
            vo = _vo_six_pulse(wt, vll_pk, alpha_rad, cc_wave)
        elif topology in {"hw3", "half3"}:
            vo = _vo_three_phase_half(wt, vm3, alpha_rad, cc)
        elif topology == "full1" or topology == "semi1":
            vo = _vo_semi_freewheel_1(wt, vm1, alpha_rad)
        else:
            vo = _vo_single_phase_half(wt, vm1, alpha_rad, False, cc)
        points.append([_deg(wt), vo])
    from electrical_engineer.engines.solvers.power_electronics import rectifier_1ph, rectifier_3ph

    vo_target = _vo_closed_form(problem, rectifier_1ph, rectifier_3ph)
    mean = mean_waveform(points)
    if math.isfinite(vo_target) and math.isfinite(mean) and abs(mean) > 1e-9:
        if abs(vo_target) < 1e-6:
            for row in points:
                row[1] = 0.0
        else:
            scale = vo_target / mean
            if abs(scale - 1.0) > 0.005:
                for row in points:
                    row[1] *= scale
    return points


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
        return (2.0 * vm * cos_a) / _PI - (2.0 * w * ls * io) / _PI
    v_ll = float(problem.get("v_ll_rms") or problem.get("v_rms") or 415)
    vm_ph = phase_peak_from_line_vll(v_ll)
    vll_pk = line_peak_from_line_vll(v_ll)
    cc = is_continuous_conduction(load, topology, alpha_deg)
    if topology in {"hw3", "half3"}:
        if cc:
            return (3.0 * _SQRT3 * vm_ph / (2.0 * _PI)) * cos_a - (3.0 * w * ls * io) / (2.0 * _PI)
        return (3.0 / (2.0 * _PI)) * vm_ph * (1.0 + math.cos(alpha + _PI / 6.0))
    if topology == "semi3":
        return (3.0 * vll_pk / (2.0 * _PI)) * (1.0 + cos_a) - (3.0 * w * ls * io) / (2.0 * _PI)
    return (3.0 * vll_pk / _PI) * cos_a - (3.0 * w * ls * io) / _PI


def mean_waveform(points: list[list[float]]) -> float:
    if not points:
        return float("nan")
    return sum(y for _, y in points) / len(points)
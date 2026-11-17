"""RL steady-state Vo and β (keep in sync with ui/.../rectifier-rl-steady.js)."""

from __future__ import annotations

import math

from electrical_engineer.engines.rectifier_steady import (
    line_peak_from_line_vll,
    phase_peak_from_line_vll,
)

_PI = math.pi
_SQRT2 = math.sqrt(2.0)
_SQRT3 = math.sqrt(3.0)


def _norm_topo(t: str) -> str:
    m = {"half1": "hw1", "half3": "hw3", "half": "hw3", "full": "full3", "semi": "semi3"}
    return m.get(str(t or "full3"), str(t or "full3"))


def rl_impedance(r_ohm: float, l_h: float, f_hz: float) -> dict[str, float]:
    w = 2.0 * _PI * f_hz
    z = math.hypot(r_ohm, w * l_h)
    phi = math.atan2(w * l_h, r_ohm)
    tan_phi = w * l_h / r_ohm
    return {"w": w, "z": z, "phi": phi, "tan_phi": tan_phi}


def i_rl_canonical(theta: float, alpha: float, vm: float, imp: dict[str, float]) -> float:
    if theta <= alpha + 1e-12:
        return 0.0
    z, phi, tan_phi = imp["z"], imp["phi"], imp["tan_phi"]
    return (vm / z) * (math.sin(theta - phi) - math.sin(alpha - phi) * math.exp(-(theta - alpha) / tan_phi))


def extinction_angle_rad(alpha: float, vm: float, imp: dict[str, float], theta_hi: float) -> float | None:
    if i_rl_canonical(theta_hi, alpha, vm, imp) > 1e-8:
        return None
    lo, hi = alpha, theta_hi
    for _ in range(64):
        mid = (lo + hi) / 2.0
        im = i_rl_canonical(mid, alpha, vm, imp)
        if im > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def rl_reference_slice(problem: dict) -> dict:
    topo = _norm_topo(problem.get("topology"))
    alpha = math.radians(float(problem.get("alpha_deg") or 0))
    f_hz = float(problem.get("f_hz") or 50)
    r_ohm = float(problem.get("r_ohm") or 10)
    load = str(problem.get("load") or "R")
    l_h = float(problem.get("l_h") or 0) if problem.get("l_h") is not None else 0.0
    if l_h <= 0 and load in {"RL", "RLE"}:
        l_h = 0.01
    v_rms = float(problem.get("v_rms") or (415 if topo.endswith("3") else 230))
    imp = rl_impedance(r_ohm, l_h, f_hz)

    if topo == "full1":
        vm = _SQRT2 * v_rms
        theta_hi = _PI + alpha
        beta = extinction_angle_rad(alpha, vm, imp, theta_hi)
        mode = "Continuous" if beta is None else "Discontinuous"
        return {"topo": topo, "mode": mode, "alpha": alpha, "beta": beta, "vm": vm}
    if topo == "hw1":
        vm = _SQRT2 * v_rms
        beta = extinction_angle_rad(alpha, vm, imp, _PI)
        mode = "Continuous" if beta is None else "Discontinuous"
        return {"topo": topo, "mode": mode, "alpha": alpha, "beta": beta, "vm": vm}
    if topo == "semi1":
        vm = _SQRT2 * v_rms
        beta = extinction_angle_rad(alpha, vm, imp, _PI)
        mode = "Continuous" if beta is None else "Discontinuous"
        return {"topo": topo, "mode": mode, "alpha": alpha, "beta": beta, "vm": vm}
    if topo in {"hw3", "half3"}:
        alpha_deg = float(problem.get("alpha_deg") or 0)
        e_v = float(problem.get("e_v") or 0)
        if alpha_deg >= 90 and e_v <= 0:
            return {
                "topo": topo,
                "mode": "Discontinuous",
                "alpha": alpha,
                "beta": alpha,
                "vm_ph": phase_peak_from_line_vll(v_rms),
                "off": True,
            }
        vm_ph = phase_peak_from_line_vll(v_rms)
        fire = _PI / 6 + alpha
        beta = extinction_angle_rad(fire, vm_ph, imp, fire + 2 * _PI / 3)
        mode = "Continuous" if beta is None else "Discontinuous"
        return {"topo": topo, "mode": mode, "alpha": alpha, "beta": beta, "vm_ph": vm_ph, "fire": fire}
    if topo == "semi3":
        vll_pk = line_peak_from_line_vll(v_rms)
        vm_ph = phase_peak_from_line_vll(v_rms)
        fire = _PI / 6 + alpha
        beta = extinction_angle_rad(fire, vm_ph, imp, fire + 2 * _PI / 3)
        mode = "Continuous" if beta is None else "Discontinuous"
        if l_h >= 0.002:
            mode, beta = "Continuous", None
        return {"topo": topo, "mode": mode, "alpha": alpha, "beta": beta, "vm_ph": vm_ph, "vll_pk": vll_pk}
    alpha_deg = float(problem.get("alpha_deg") or 0)
    e_v = float(problem.get("e_v") or 0)
    if alpha_deg >= 90 and e_v <= 0:
        return {
            "topo": topo,
            "mode": "Discontinuous",
            "alpha": alpha,
            "beta": alpha,
            "vm_ph": phase_peak_from_line_vll(v_rms),
            "vll_pk": line_peak_from_line_vll(v_rms),
            "off": True,
        }
    vll_pk = line_peak_from_line_vll(v_rms)
    vm_ph = phase_peak_from_line_vll(v_rms)
    fire = _PI / 6 + alpha
    beta = extinction_angle_rad(fire, vm_ph, imp, fire + _PI / 3)
    mode = "Continuous" if beta is None else "Discontinuous"
    return {"topo": topo, "mode": mode, "alpha": alpha, "beta": beta, "vm_ph": vm_ph, "vll_pk": vll_pk}


def rl_vo_mean_closed_form(slice_: dict) -> float:
    if slice_.get("off"):
        return 0.0
    topo, mode, alpha, beta = slice_["topo"], slice_["mode"], slice_["alpha"], slice_["beta"]
    ca = math.cos(alpha)
    if topo == "full1":
        vm = slice_["vm"]
        if mode == "Continuous":
            return (2 * vm / _PI) * ca
        return (vm / _PI) * (ca - math.cos(beta))
    if topo == "hw1":
        vm = slice_["vm"]
        if mode == "Continuous":
            return (vm / (2 * _PI)) * (1 + ca)
        return (vm / (2 * _PI)) * (ca - math.cos(beta))
    if topo == "semi1":
        vm = slice_["vm"]
        if mode == "Continuous":
            return (vm / _PI) * (1 + ca)
        return (vm / _PI) * (ca - math.cos(beta))
    vm_ph = slice_.get("vm_ph")
    vll_pk = slice_.get("vll_pk")
    if topo in {"hw3", "half3"}:
        if mode == "Continuous":
            return (3 * _SQRT3 * vm_ph / (2 * _PI)) * ca
        return (3 / (2 * _PI)) * vm_ph * (math.cos(alpha + _PI / 6) - math.cos(beta))
    if topo == "semi3":
        if mode == "Continuous":
            return (3 * vll_pk / (2 * _PI)) * (1 + ca)
        return (3 * vll_pk / (2 * _PI)) * (ca - math.cos(beta))
    if mode == "Continuous":
        return (3 * vll_pk / _PI) * ca
    return (3 / _PI) * vll_pk * (math.cos(alpha + _PI / 3) - math.cos(beta))
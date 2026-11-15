"""Machines SolverSpec table."""

from __future__ import annotations

import cmath
import math

from electrical_engineer.engines.solvers.spec import Param, SolverSpec

_TWO_PI = 2.0 * math.pi


def transformer_oc_sc(
    kva: float,
    v_lv: float,
    v_hv: float,
    oc_v: float,
    oc_i: float,
    oc_p: float,
    sc_v: float,
    sc_i: float,
    sc_p: float,
    load_frac: float = 1.0,
    pf: float = 0.8,
) -> dict:
    if min(kva, v_lv, v_hv, oc_v, oc_i, sc_v, sc_i) <= 0 or oc_p <= 0 or sc_p <= 0:
        raise ValueError("transformer test inputs must be positive")
    r0 = oc_v * oc_v / oc_p
    iw = oc_p / oc_v
    im = math.sqrt(max(oc_i * oc_i - iw * iw, 0.0))
    x0 = oc_v / im if im > 1e-15 else float("inf")
    req = sc_p / (sc_i * sc_i)
    zeq = sc_v / sc_i
    xeq = math.sqrt(max(zeq * zeq - req * req, 0.0))
    s_w = kva * 1000.0
    i_rated_hv = s_w / v_hv
    pcu_fl = load_frac * load_frac * sc_p * (i_rated_hv / sc_i) ** 2
    p0 = oc_p
    p_out = load_frac * s_w * pf
    eta = 100.0 * p_out / (p_out + p0 + pcu_fl) if p_out + p0 + pcu_fl > 0 else 0.0
    x_eta_max = math.sqrt(p0 / pcu_fl) if pcu_fl > 0 else float("inf")
    return {
        "eta_percent": eta,
        "r0_ohm": r0,
        "x0_ohm": x0,
        "req_ohm": req,
        "xeq_ohm": xeq,
        "pcu_fl_w": pcu_fl,
        "p0_w": p0,
        "x_max_efficiency": x_eta_max,
    }


def induction_torque_slip(
    v_ll: float,
    f_hz: float,
    poles: int,
    r1: float,
    x1: float,
    r2: float,
    x2: float,
    xm: float,
    slip: float,
) -> dict:
    if poles <= 0 or f_hz <= 0 or slip <= 0:
        raise ValueError("poles, f_hz, slip must be positive")
    v_ph = v_ll / math.sqrt(3.0)
    ws = _TWO_PI * f_hz / (poles / 2.0)
    z1 = complex(r1, x1)
    z2 = complex(r2 / slip, x2)
    zm = complex(0, xm)
    vth = v_ph * zm / (z1 + zm)
    zth = (z1 * zm) / (z1 + zm)
    denom = (abs(zth + z2)) ** 2
    torque = 3.0 * (abs(vth) ** 2) * (r2 / slip) / (ws * denom)
    s_tmax = r2 / math.sqrt((zth.real) ** 2 + (zth.imag + x2) ** 2)
    z2_tmax = complex(r2 / s_tmax, x2)
    torque_max = 3.0 * (abs(vth) ** 2) * (r2 / s_tmax) / (ws * (abs(zth + z2_tmax) ** 2))
    z2_start = complex(r2, x2)
    torque_start = 3.0 * (abs(vth) ** 2) * r2 / (ws * (abs(zth + z2_start) ** 2))
    return {
        "torque_Nm": float(torque),
        "s_tmax": s_tmax,
        "torque_max_Nm": float(torque_max),
        "torque_start_Nm": float(torque_start),
        "sync_rad_s": ws,
    }


def synchronous_regulation(
    v_phase: float,
    i_a: float,
    pf: float,
    pf_type: str,
    xs: float,
    ra: float = 0.0,
) -> dict:
    if v_phase <= 0 or i_a < 0 or not 0 <= pf <= 1:
        raise ValueError("invalid synchronous machine inputs")
    if pf_type == "lag":
        theta = -math.acos(pf)
    elif pf_type == "lead":
        theta = math.acos(pf)
    elif pf_type == "unity":
        theta = 0.0
    else:
        raise ValueError("pf_type must be lag, lead, or unity")
    i = cmath.rect(i_a, theta)
    e = v_phase + i * complex(ra, xs)
    e_mag = abs(e)
    reg = 100.0 * (e_mag - v_phase) / v_phase if v_phase else 0.0
    return {
        "regulation_percent": reg,
        "e_mag_V": e_mag,
        "e_re_V": e.real,
        "e_im_V": e.imag,
        "pf_type": pf_type,
    }


SPECS: dict[str, SolverSpec] = {
    "transformer_oc_sc": SolverSpec(
        fn=transformer_oc_sc,
        params=(
            Param("kva"),
            Param("v_lv"),
            Param("v_hv"),
            Param("oc_v"),
            Param("oc_i"),
            Param("oc_p"),
            Param("sc_v"),
            Param("sc_i"),
            Param("sc_p"),
            Param("load_frac", default=1.0),
            Param("pf", default=0.8),
        ),
        value_key="eta_percent",
        unit="%",
    ),
    "induction_torque_slip": SolverSpec(
        fn=induction_torque_slip,
        params=(
            Param("v_ll"),
            Param("f_hz"),
            Param("poles"),
            Param("r1"),
            Param("x1"),
            Param("r2"),
            Param("x2"),
            Param("xm"),
            Param("slip"),
        ),
        value_key="torque_Nm",
        unit="N·m",
    ),
    "synchronous_regulation": SolverSpec(
        fn=synchronous_regulation,
        params=(
            Param("v_phase"),
            Param("i_a"),
            Param("pf"),
            Param("pf_type", kind="str", choices=("lag", "lead", "unity")),
            Param("xs"),
            Param("ra", default=0.0),
        ),
        value_key="regulation_percent",
        unit="%",
    ),
}
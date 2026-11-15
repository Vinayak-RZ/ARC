"""EM fields SolverSpec table."""

from __future__ import annotations

import math

from electrical_engineer.engines.solvers.spec import Param, SolverSpec

_TWO_PI = 2.0 * math.pi
_EPS0 = 8.854187817e-12
_MU0 = 4e-7 * math.pi


def line_parameters(
    config: str,
    r_m: float,
    d_m: float,
    d_ab_m: float = 0.0,
    d_bc_m: float = 0.0,
    d_ca_m: float = 0.0,
    f_hz: float = 50.0,
) -> dict:
    if r_m <= 0:
        raise ValueError("conductor radius must be positive")
    r_p = 0.7788 * r_m
    if config == "single_phase":
        if d_m <= 0:
            raise ValueError("single_phase needs spacing d_m")
        l_h_per_m = 4e-7 * math.log(d_m / r_p)
        c_f_per_m = math.pi * _EPS0 / math.log(d_m / r_m)
        deq = d_m
    elif config == "three_phase_equilateral":
        if d_m <= 0:
            raise ValueError("equilateral needs spacing d_m")
        deq = d_m
        l_h_per_m = 2e-7 * math.log(deq / r_p)
        c_f_per_m = 2 * math.pi * _EPS0 / math.log(deq / r_m)
    elif config == "three_phase_transposed":
        if min(d_ab_m, d_bc_m, d_ca_m) <= 0:
            raise ValueError("transposed needs d_ab_m, d_bc_m, d_ca_m")
        deq = (d_ab_m * d_bc_m * d_ca_m) ** (1.0 / 3.0)
        l_h_per_m = 2e-7 * math.log(deq / r_p)
        c_f_per_m = 2 * math.pi * _EPS0 / math.log(deq / r_m)
    else:
        raise ValueError("config must be single_phase, three_phase_equilateral, or three_phase_transposed")
    l_h_per_km = l_h_per_m * 1000.0
    c_f_per_km = c_f_per_m * 1000.0
    xl_ohm_per_km = _TWO_PI * f_hz * l_h_per_km
    xc_ohm_per_km = 1.0 / (_TWO_PI * f_hz * c_f_per_km) if c_f_per_km > 0 else float("inf")
    return {
        "L_H_per_km": l_h_per_km,
        "C_F_per_km": c_f_per_km,
        "XL_ohm_per_km": xl_ohm_per_km,
        "XC_ohm_per_km": xc_ohm_per_km,
        "deq_m": deq,
        "config": config,
    }


def capacitance_geometry(
    geometry: str,
    eps_r: float = 1.0,
    area_m2: float = 0.0,
    d_m: float = 0.0,
    a_m: float = 0.0,
    b_m: float = 0.0,
    length_m: float = 0.0,
) -> dict:
    eps = _EPS0 * eps_r
    if geometry == "parallel_plate":
        if area_m2 <= 0 or d_m <= 0:
            raise ValueError("parallel plate needs area and spacing")
        c_f = eps * area_m2 / d_m
    elif geometry == "coaxial":
        if length_m <= 0 or b_m <= a_m <= 0:
            raise ValueError("coaxial needs length and radii a<b")
        c_f = _TWO_PI * eps * length_m / math.log(b_m / a_m)
    elif geometry == "spherical":
        if b_m <= a_m <= 0:
            raise ValueError("spherical needs radii a<b")
        c_f = 4 * math.pi * eps * a_m * b_m / (b_m - a_m)
    elif geometry == "isolated_sphere":
        if a_m <= 0:
            raise ValueError("isolated sphere needs radius a")
        c_f = 4 * math.pi * eps * a_m
    else:
        raise ValueError("geometry must be parallel_plate, coaxial, spherical, or isolated_sphere")
    return {"C_F": c_f, "geometry": geometry, "eps_F_per_m": eps}


SPECS: dict[str, SolverSpec] = {
    "line_parameters": SolverSpec(
        fn=line_parameters,
        params=(
            Param(
                "config",
                kind="str",
                choices=("single_phase", "three_phase_equilateral", "three_phase_transposed"),
            ),
            Param("r_m"),
            Param("d_m"),
            Param("d_ab_m", default=0.0),
            Param("d_bc_m", default=0.0),
            Param("d_ca_m", default=0.0),
            Param("f_hz", default=50.0),
        ),
        value_key="L_H_per_km",
        unit="H/km",
    ),
    "capacitance_geometry": SolverSpec(
        fn=capacitance_geometry,
        params=(
            Param("geometry", kind="str", choices=("parallel_plate", "coaxial", "spherical", "isolated_sphere")),
            Param("eps_r", default=1.0),
            Param("area_m2", default=0.0),
            Param("d_m", default=0.0),
            Param("a_m", default=0.0),
            Param("b_m", default=0.0),
            Param("length_m", default=0.0),
        ),
        value_key="C_F",
        unit="F",
    ),
}
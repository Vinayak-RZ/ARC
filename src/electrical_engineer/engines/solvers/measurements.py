"""Measurements SolverSpec table."""

from __future__ import annotations

import math

from electrical_engineer.engines.solvers.spec import Param, SolverSpec

_TWO_PI = 2.0 * math.pi
_EPS0 = 8.854187817e-12


def bridge_balance(
    bridge: str,
    r1: float,
    r2: float,
    r3: float,
    r4: float = 0.0,
    c1: float = 0.0,
    c2: float = 0.0,
    c4: float = 0.0,
    f_hz: float = 50.0,
) -> dict:
    if r1 <= 0 or r2 <= 0 or r3 <= 0:
        raise ValueError("R1, R2, R3 must be positive")
    if bridge == "wheatstone":
        unknown = r2 * r3 / r1
        unit = "ohm"
    elif bridge == "maxwell":
        if c1 <= 0:
            raise ValueError("maxwell bridge needs positive C1")
        lx = r2 * r3 * c1
        rx = r2 * r3 / r1
        unknown = lx
        unit = "H"
        return {"unknown": unknown, "unit": unit, "rx_ohm": rx, "lx_H": lx, "bridge": bridge}
    elif bridge == "schering":
        if c2 <= 0 or r3 <= 0 or r4 <= 0:
            raise ValueError("schering bridge needs C2, R3, R4 positive")
        cx = c2 * r4 / r3
        rx = r3 * c4 / c2 if c2 else 0.0
        d_factor = _TWO_PI * f_hz * c4 * r4
        unknown = cx
        unit = "F"
        return {
            "unknown": unknown,
            "unit": unit,
            "rx_ohm": rx,
            "cx_F": cx,
            "dissipation_factor": d_factor,
            "bridge": bridge,
        }
    else:
        raise ValueError(f"bridge must be wheatstone, maxwell, or schering; got {bridge!r}")
    return {"unknown": unknown, "unit": unit, "bridge": bridge}


def meter_range_extension(
    kind: str,
    rm: float,
    im_fs: float,
    i_range: float = 0.0,
    v_range: float = 0.0,
) -> dict:
    if rm <= 0 or im_fs <= 0:
        raise ValueError("meter resistance and full-scale current must be positive")
    if kind == "ammeter_shunt":
        if i_range <= im_fs:
            raise ValueError("i_range must exceed meter full-scale current")
        r_ohm = im_fs * rm / (i_range - im_fs)
    elif kind == "voltmeter_multiplier":
        if v_range <= 0:
            raise ValueError("v_range must be positive for voltmeter multiplier")
        r_ohm = v_range / im_fs - rm
        if r_ohm < 0:
            raise ValueError("v_range too small for meter full-scale")
    else:
        raise ValueError(f"kind must be ammeter_shunt or voltmeter_multiplier; got {kind!r}")
    return {"r_ohm": r_ohm, "kind": kind, "rm_ohm": rm, "im_fs_A": im_fs}


SPECS: dict[str, SolverSpec] = {
    "bridge_balance": SolverSpec(
        fn=bridge_balance,
        params=(
            Param("bridge", kind="str", choices=("wheatstone", "maxwell", "schering")),
            Param("r1"),
            Param("r2"),
            Param("r3"),
            Param("r4", default=0.0),
            Param("c1", default=0.0),
            Param("c2", default=0.0),
            Param("c4", default=0.0),
            Param("f_hz", default=50.0),
        ),
        value_key="unknown",
        unit="ohm",
    ),
    "meter_range_extension": SolverSpec(
        fn=meter_range_extension,
        params=(
            Param("kind", kind="str", choices=("ammeter_shunt", "voltmeter_multiplier")),
            Param("rm"),
            Param("im_fs"),
            Param("i_range", default=0.0),
            Param("v_range", default=0.0),
        ),
        value_key="r_ohm",
        unit="ohm",
    ),
}
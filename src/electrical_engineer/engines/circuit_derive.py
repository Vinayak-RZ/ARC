"""Symbolic or closed-form circuit derive + SPICE netlists for verify-after-derive."""

from __future__ import annotations

import math
from typing import Any


class DeriveError(ValueError):
    pass


def derive(problem: dict[str, Any]) -> dict[str, Any]:
    """Return derived scalar, netlist, probe, and metadata for simulation."""
    kind = str(problem.get("kind") or problem.get("circuit_kind") or "").lower()
    if not kind:
        raise DeriveError("missing kind")
    fn = _KINDS.get(kind)
    if fn is None:
        raise DeriveError(f"unsupported kind {kind!r}")
    out = fn(problem)
    out["kind"] = kind
    out["engine"] = "circuit_derive"
    return out


def netlist_dc_divider(vin: float, r1: float, r2: float) -> tuple[str, str]:
    cir = (
        "* arc dc divider\n"
        f"V1 1 0 DC {vin}\n"
        f"R1 1 2 {r1}\n"
        f"R2 2 0 {r2}\n"
        ".end\n"
    )
    return cir, "v(2)"


def _dc_divider(problem: dict[str, Any]) -> dict[str, Any]:
    vin = float(problem["vin"])
    r1, r2 = float(problem["r1"]), float(problem["r2"])
    if r1 + r2 == 0:
        raise DeriveError("r1+r2 is zero")
    vout = vin * r2 / (r1 + r2)
    cir, probe = netlist_dc_divider(vin, r1, r2)
    return {"value": vout, "unit": "V", "cir": cir, "probe_node": "2", "probe": probe}


def _dc_series(problem: dict[str, Any]) -> dict[str, Any]:
    vin = float(problem["vin"])
    rs = [float(x) for x in problem["resistors"]]
    rtot = sum(rs)
    if rtot == 0:
        raise DeriveError("zero total resistance")
    i_a = vin / rtot
    cir = f"* arc series\nV1 1 0 DC {vin}\n"
    node = 1
    for idx, r in enumerate(rs):
        n2 = idx + 2
        cir += f"R{idx + 1} {node} {n2} {r}\n"
        node = n2
    cir += ".end\n"
    return {"value": i_a, "unit": "A", "cir": cir, "probe_node": "1", "probe": f"v({node - 1})"}


def _dc_parallel(problem: dict[str, Any]) -> dict[str, Any]:
    vin = float(problem["vin"])
    rs = [float(x) for x in problem["resistors"]]
    if not rs:
        raise DeriveError("no resistors")
    g = sum(1.0 / r for r in rs if r != 0)
    if g == 0:
        raise DeriveError("infinite resistance")
    itot = vin * g
    lines = [f"* arc parallel\nV1 1 0 DC {vin}\n"]
    for idx, r in enumerate(rs):
        lines.append(f"R{idx + 1} 1 0 {r}\n")
    lines.append(".end\n")
    return {"value": itot, "unit": "A", "cir": "".join(lines), "probe_node": "1", "probe": "i(v1)"}


def _dc_current_divider(problem: dict[str, Any]) -> dict[str, Any]:
    isrc = float(problem["i_src"])
    r1, r2 = float(problem["r1"]), float(problem["r2"])
    if r1 + r2 == 0:
        raise DeriveError("r1+r2 is zero")
    i2 = isrc * r1 / (r1 + r2)
    cir = (
        "* arc current divider\n"
        f"I1 0 1 DC {isrc}\n"
        f"R1 1 0 {r1}\n"
        f"R2 1 2 {r2}\n"
        f"Rload 2 0 {problem.get('r_load', 1e-12)}\n"
        ".end\n"
    )
    return {"value": i2, "unit": "A", "cir": cir, "probe_node": "2", "probe": "v(2)"}


def _thevenin_r(problem: dict[str, Any]) -> dict[str, Any]:
    r1, r2 = float(problem["r1"]), float(problem["r2"])
    vsrc = float(problem["v_src"])
    rth = (r1 * r2) / (r1 + r2) if r1 + r2 else float("inf")
    vth = vsrc * r2 / (r1 + r2)
    metric = str(problem.get("metric") or "rth")
    if metric == "vth":
        value = vth
        unit = "V"
    else:
        value = rth
        unit = "ohm"
    cir = (
        "* arc thevenin test\n"
        f"V1 1 0 DC {vsrc}\n"
        f"R1 1 2 {r1}\n"
        f"R2 2 0 {r2}\n"
        ".end\n"
    )
    return {"value": value, "unit": unit, "cir": cir, "probe_node": "2", "probe": "v(2)", "vth": vth, "rth": rth}


def _ac_rc_magnitude(problem: dict[str, Any]) -> dict[str, Any]:
    vin = float(problem.get("vin_rms", problem.get("vin", 1.0)))
    r = float(problem["r"])
    c = float(problem["c"])
    f = float(problem["f_hz"])
    omega = 2.0 * math.pi * f
    xc = 1.0 / (omega * c)
    zmag = math.hypot(r, xc)
    vout = vin * (xc / zmag)
    cir = (
        f"* ac rc\n"
        f"V1 1 0 AC {vin}\n"
        f"R1 1 2 {r}\n"
        f"C1 2 0 {c}\n"
        f".ac dec 1 {f} {f}\n"
        ".end\n"
    )
    return {
        "value": vout,
        "unit": "V",
        "cir": cir,
        "probe_node": "2",
        "probe": "v(2)",
        "analysis": "ac",
        "f_hz": f,
    }


def _ac_rl_angle(problem: dict[str, Any]) -> dict[str, Any]:
    r = float(problem["r"])
    l = float(problem["l"])
    f = float(problem["f_hz"])
    omega = 2.0 * math.pi * f
    phase_deg = math.degrees(math.atan2(omega * l, r))
    cir = (
        f"* ac rl\n"
        f"I1 0 1 AC 1\n"
        f"R1 1 0 {r}\n"
        f"L1 1 0 {l}\n"
        f".ac dec 1 {f} {f}\n"
        ".end\n"
    )
    return {
        "value": phase_deg,
        "unit": "deg",
        "cir": cir,
        "probe_node": "1",
        "probe": "v(1)",
        "analysis": "ac",
        "f_hz": f,
    }


def _transient_rc(problem: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines import ee_v2_solvers as v2

    v = float(problem["v"])
    r = float(problem["r"])
    c = float(problem["c"])
    t = float(problem["t"])
    vc = v2.rc_step(v, r, c, t)["vc_V"]
    cir = (
        f"* rc step\nV1 1 0 DC {v}\nR1 1 2 {r}\nC1 2 0 {c}\n"
        f".tran {max(t * 2, 1e-3)}\n.end\n"
    )
    return {"value": vc, "unit": "V", "cir": cir, "probe_node": "2", "probe": "v(2)", "analysis": "tran", "t_s": t}


def _transient_rl(problem: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines import ee_v2_solvers as v2

    v = float(problem["v"])
    r = float(problem["r"])
    l = float(problem["l"])
    t = float(problem["t"])
    i_a = v2.rl_step(v, r, l, t)["i_A"]
    cir = (
        f"* rl step\nV1 1 0 DC {v}\nR1 1 2 {r}\nL1 2 0 {l}\n"
        f".tran {max(t * 2, 1e-3)}\n.end\n"
    )
    return {"value": i_a, "unit": "A", "cir": cir, "probe_node": "2", "probe": "v(2)", "analysis": "tran", "t_s": t}


def _transient_rlc(problem: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines import ee_v2_solvers as v2

    r = float(problem["r"])
    l = float(problem["l"])
    c = float(problem["c"])
    vc0 = float(problem.get("vc0", 0.0))
    i0 = float(problem.get("i0", 0.0))
    t = float(problem["t"])
    vc = v2.rlc_natural(r, l, c, vc0, i0, t)["vc_V"]
    cir = (
        f"* rlc natural\n"
        f"R1 1 2 {r}\nL1 2 3 {l}\nC1 3 0 {c}\n"
        f"IC V(3)={vc0} I(L1)={i0}\n"
        f".tran {max(t * 2, 1e-3)}\n.end\n"
    )
    return {"value": vc, "unit": "V", "cir": cir, "probe_node": "3", "probe": "v(3)", "analysis": "tran", "t_s": t}


def _opamp_inverting(problem: dict[str, Any]) -> dict[str, Any]:
    vin = float(problem["vin"])
    rf = float(problem["rf"])
    rin = float(problem["rin"])
    if rin == 0:
        raise DeriveError("rin is zero")
    gain = -rf / rin
    vout = gain * vin
    cir = (
        "* ideal inverting opamp linearized\n"
        f"V1 1 0 DC {vin}\n"
        f"EOP 2 0 1 0 {gain}\n"
        "Rout 2 0 1e-9\n"
        ".end\n"
    )
    return {"value": vout, "unit": "V", "cir": cir, "probe_node": "2", "probe": "v(2)", "ideal_opamp": True}


def _opamp_noninverting(problem: dict[str, Any]) -> dict[str, Any]:
    vin = float(problem["vin"])
    rf = float(problem["rf"])
    rg = float(problem["rg"])
    if rg == 0:
        raise DeriveError("rg is zero")
    gain = 1.0 + rf / rg
    vout = gain * vin
    cir = (
        "* ideal noninverting opamp linearized\n"
        f"V1 1 0 DC {vin}\n"
        f"EOP 2 0 1 0 {gain}\n"
        "Rout 2 0 1e-9\n"
        ".end\n"
    )
    return {"value": vout, "unit": "V", "cir": cir, "probe_node": "2", "probe": "v(2)", "ideal_opamp": True}


def _diode_small_signal_rd(problem: dict[str, Any]) -> dict[str, Any]:
    """Linearized diode: rd = n*Vt/Id."""
    id_dc = float(problem["id_a"])
    n = float(problem.get("n", 1.0))
    vt = float(problem.get("vt_v", 0.02585))
    if id_dc <= 0:
        raise DeriveError("id must be positive")
    rd = n * vt / id_dc
    vd = float(problem.get("vd_v", n * vt * math.log(id_dc / float(problem.get("is_a", 1e-12)) + 1)))
    vin = vd + id_dc * rd
    cir = (
        "* small-signal diode linear\n"
        f"V1 1 0 DC {vin}\n"
        f"RD 1 2 {rd}\n"
        f"Rmeas 2 0 {problem.get('r_shunt', 1e6)}\n"
        ".end\n"
    )
    return {"value": rd, "unit": "ohm", "cir": cir, "probe_node": "2", "probe": "v(2)"}


def _bjt_ce_gain(problem: dict[str, Any]) -> dict[str, Any]:
    """Common-emitter small-signal voltage gain Av = -gm*Rc (single-pole)."""
    gm = float(problem["gm_s"])
    rc = float(problem["rc_ohm"])
    av = -gm * rc
    vin = float(problem.get("vin", 1e-3))
    cir = (
        "* bjt small-signal gain block\n"
        f"V1 1 0 DC {vin}\n"
        f"EAv 2 0 1 0 {av}\n"
        "Rout 2 0 1e-9\n"
        ".end\n"
    )
    return {"value": av, "unit": "1", "cir": cir, "probe_node": "2", "probe": "v(2)", "small_signal": True}


def _two_port_z11(problem: dict[str, Any]) -> dict[str, Any]:
    """Resistive pi: z11 = V1/I1 with port 2 open."""
    r1 = float(problem["r1"])
    r2 = float(problem["r2"])
    r3 = float(problem["r3"])
    z11 = r1 + (r2 * r3) / (r2 + r3) if (r2 + r3) else float("inf")
    cir = (
        "* two-port pi\n"
        f"I1 0 1 DC {problem.get('i1', 1.0)}\n"
        f"R1 1 2 {r1}\n"
        f"R2 2 0 {r2}\n"
        f"R3 2 0 {r3}\n"
        ".end\n"
    )
    return {"value": z11, "unit": "ohm", "cir": cir, "probe_node": "1", "probe": "v(1)"}


_KINDS = {
    "dc_divider": _dc_divider,
    "voltage_divider": _dc_divider,
    "dc_series": _dc_series,
    "dc_parallel": _dc_parallel,
    "dc_current_divider": _dc_current_divider,
    "thevenin": _thevenin_r,
    "ac_rc_magnitude": _ac_rc_magnitude,
    "ac_rl_angle": _ac_rl_angle,
    "transient_rc": _transient_rc,
    "transient_rl": _transient_rl,
    "transient_rlc": _transient_rlc,
    "opamp_inverting": _opamp_inverting,
    "opamp_noninverting": _opamp_noninverting,
    "diode_small_signal": _diode_small_signal_rd,
    "bjt_ce_gain": _bjt_ce_gain,
    "two_port_z11": _two_port_z11,
}

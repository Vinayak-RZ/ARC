"""Circuits SolverSpec table."""

from __future__ import annotations

import math

from electrical_engineer.engines.circuit_mna import MnaError, mna_solve
from electrical_engineer.engines.solvers.spec import Param, SolverSpec

_TWO_PI = 2.0 * math.pi


def _zero_sources(netlist: str) -> str:
    out: list[str] = []
    for line in netlist.splitlines():
        s = line.split(";", 1)[0].strip()
        if not s or s.startswith("."):
            out.append(line)
            continue
        tok = s.split()
        if tok and len(tok) >= 4 and tok[0][0].upper() in {"V", "I"}:
            out.append(f"{tok[0]} {tok[1]} {tok[2]} DC 0")
        else:
            out.append(line)
    return "\n".join(out)


def _port_v(netlist: str, node: str) -> float:
    return float(mna_solve(netlist, analysis="dc", probe=f"v({node})")["value"])


def thevenin_dc(netlist: str, port_a: str, port_b: str = "0") -> dict:
    va = _port_v(netlist, port_a)
    vb = _port_v(netlist, port_b) if port_b != "0" else 0.0
    voc = va - vb
    z_net = _zero_sources(netlist).rstrip() + "\n"
    itest = f"Itest {port_b} {port_a} DC 1"
    dead = z_net + itest + "\n"
    va_t = _port_v(dead, port_a)
    vb_t = _port_v(dead, port_b) if port_b != "0" else 0.0
    rth = va_t - vb_t
    if abs(rth) < 1e-15:
        raise MnaError("Thevenin resistance is zero")
    in_a = voc / rth if rth else float("inf")
    return {"Vth_V": voc, "Rth_ohm": rth, "IN_A": in_a, "port_a": port_a, "port_b": port_b}


def max_power_transfer(vth_rms: float, rth: float, xth: float = 0.0) -> dict:
    if rth <= 0:
        raise ValueError("Rth must be positive")
    zl_re = rth
    zl_im = -xth
    p_max = (vth_rms**2) / (4.0 * rth)
    return {
        "P_max_W": p_max,
        "zl_re_ohm": zl_re,
        "zl_im_ohm": zl_im,
        "vth_rms_V": vth_rms,
    }


def _mat2(m: list) -> list[list[float]]:
    return [[float(m[0][0]), float(m[0][1])], [float(m[1][0]), float(m[1][1])]]


def _det2(a: list[list[float]]) -> float:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def _inv2(a: list[list[float]]) -> list[list[float]]:
    d = _det2(a)
    if abs(d) < 1e-15:
        raise ValueError("2-port matrix is singular")
    return [[a[1][1] / d, -a[0][1] / d], [-a[1][0] / d, a[0][0] / d]]


def _to_z(mat: list[list[float]], kind: str) -> list[list[float]]:
    if kind == "z":
        return mat
    if kind == "y":
        return _inv2(mat)
    if kind == "h":
        if abs(mat[1][1]) < 1e-15:
            raise ValueError("h22 is zero")
        hz = _det2(mat)
        return [
            [hz / mat[1][1], mat[0][1] / mat[1][1]],
            [-mat[1][0] / mat[1][1], 1.0 / mat[1][1]],
        ]
    if kind == "abcd":
        a, b, c, d = mat[0][0], mat[0][1], mat[1][0], mat[1][1]
        if abs(c) < 1e-15:
            raise ValueError("C is zero")
        det_ab = a * d - b * c
        return [[d / c, det_ab / c], [1.0 / c, a / c]]
    raise ValueError("unknown two-port set")


def _from_z(z: list[list[float]], kind: str) -> list[list[float]]:
    if kind == "z":
        return z
    if kind == "y":
        return _inv2(z)
    if kind == "h":
        if abs(z[1][1]) < 1e-15:
            raise ValueError("z22 is zero")
        hz = _det2(z)
        return [
            [hz / z[1][1], z[0][1] / z[1][1]],
            [-z[1][0] / z[1][1], 1.0 / z[1][1]],
        ]
    if kind == "abcd":
        if abs(z[1][0]) < 1e-15:
            raise ValueError("z21 is zero")
        return [
            [z[0][0] / z[1][0], _det2(z) / z[1][0]],
            [1.0 / z[1][0], z[1][1] / z[1][0]],
        ]
    raise ValueError("unknown two-port set")


def two_port_convert(from_set: str, to_set: str, m: list) -> dict:
    z = _to_z(_mat2(m), from_set)
    target = _from_z(z, to_set)
    return {
        "p11": target[0][0],
        "matrix": target,
        "from_set": from_set,
        "to_set": to_set,
    }


def resonance(r: float, l: float, c: float, config: str) -> dict:
    if l <= 0 or c <= 0:
        raise ValueError("L and C must be positive")
    f0 = 1.0 / (_TWO_PI * math.sqrt(l * c))
    if config == "series":
        q = (1.0 / r) * math.sqrt(l / c) if r > 0 else float("inf")
    elif config == "parallel":
        q = r * math.sqrt(c / l) if r > 0 else 0.0
    else:
        raise ValueError("config must be series or parallel")
    bw = f0 / q if q > 0 else float("inf")
    return {"f0_Hz": f0, "Q": q, "bandwidth_Hz": bw, "config": config}


SPECS: dict[str, SolverSpec] = {
    "thevenin_dc": SolverSpec(
        fn=thevenin_dc,
        params=(
            Param("netlist", kind="str"),
            Param("port_a", kind="str"),
            Param("port_b", kind="str", default="0"),
        ),
        value_key="Vth_V",
        unit="V",
    ),
    "max_power_transfer": SolverSpec(
        fn=max_power_transfer,
        params=(
            Param("vth_rms"),
            Param("rth"),
            Param("xth", default=0.0),
        ),
        value_key="P_max_W",
        unit="W",
    ),
    "two_port_convert": SolverSpec(
        fn=two_port_convert,
        params=(
            Param("from_set", kind="str", choices=("z", "y", "h", "abcd")),
            Param("to_set", kind="str", choices=("z", "y", "h", "abcd")),
            Param("m", kind="matrix"),
        ),
        value_key="p11",
        unit="1",
    ),
    "resonance": SolverSpec(
        fn=resonance,
        params=(
            Param("r"),
            Param("l"),
            Param("c"),
            Param("config", kind="str", choices=("series", "parallel")),
        ),
        value_key="f0_Hz",
        unit="Hz",
    ),
}
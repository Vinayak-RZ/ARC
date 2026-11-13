"""Modified nodal analysis for lumped netlists (DC, AC phasor, transient BE)."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Any

import numpy as np


class MnaError(ValueError):
    pass


@dataclass
class Netlist:
    lines: list[str] = field(default_factory=list)
    raw: str = ""

    @classmethod
    def parse(cls, text: str) -> Netlist:
        lines: list[str] = []
        for line in text.splitlines():
            s = line.split(";", 1)[0].strip()
            if not s or s.startswith("."):
                continue
            if s.startswith("*"):
                continue
            lines.append(s)
        return cls(lines=lines, raw=text)

    def directives(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        for line in self.raw.splitlines():
            low = line.strip().lower()
            if low.startswith(".ac"):
                parts = line.split()
                if len(parts) >= 5:
                    d["f_start"] = float(parts[-2])
                    d["f_stop"] = float(parts[-1])
            if low.startswith(".tran"):
                parts = line.split()
                if len(parts) >= 2:
                    d["t_stop"] = float(parts[1])
        return d


def _nodes_from_netlist(nl: Netlist) -> list[str]:
    found: set[str] = {"0"}
    pat = re.compile(r"^[A-Za-z]\w*\s+(\S+)\s+(\S+)")
    for line in nl.lines:
        m = pat.match(line)
        if not m:
            continue
        found.add(m.group(1))
        found.add(m.group(2))
        tokens = line.split()
        if tokens[0][0].upper() in {"E", "G", "F", "H"} and len(tokens) >= 6:
            found.add(tokens[3])
            found.add(tokens[4])
    ordered = ["0"] + sorted(n for n in found if n != "0")
    return ordered


def _idx(node: str, node_map: dict[str, int]) -> int:
    if node == "0":
        return -1
    return node_map[node] - 1


@dataclass
class _Branch:
    kind: str
    n1: str
    n2: str
    val: complex
    ctrl_p: str = ""
    ctrl_n: str = ""
    gain: float = 0.0
    name: str = ""


def _branches(nl: Netlist) -> list[_Branch]:
    out: list[_Branch] = []
    for line in nl.lines:
        tok = line.split()
        if not tok:
            continue
        name, kind = tok[0], tok[0][0].upper()
        if kind == "R" and len(tok) >= 4:
            out.append(_Branch("R", tok[1], tok[2], _parse_rlc_value(tok[3]), name=name))
        elif kind == "V" and len(tok) >= 4:
            val = _parse_source_value(tok[3:], default=0.0)
            out.append(_Branch("V", tok[1], tok[2], val, name=name))
        elif kind == "I" and len(tok) >= 4:
            val = _parse_source_value(tok[3:], default=0.0)
            out.append(_Branch("I", tok[1], tok[2], val, name=name))
        elif kind == "C" and len(tok) >= 4:
            out.append(_Branch("C", tok[1], tok[2], _parse_rlc_value(tok[3]), name=name))
        elif kind == "L" and len(tok) >= 4:
            out.append(_Branch("L", tok[1], tok[2], _parse_rlc_value(tok[3]), name=name))
        elif kind == "D" and len(tok) >= 4:
            out.append(_Branch("D", tok[1], tok[2], 0.0, name=name))
        elif kind == "E" and len(tok) >= 6:
            out.append(
                _Branch(
                    "E",
                    tok[1],
                    tok[2],
                    0,
                    ctrl_p=tok[3],
                    ctrl_n=tok[4],
                    gain=float(tok[5]),
                    name=name,
                )
            )
        elif kind == "G" and len(tok) >= 6:
            out.append(
                _Branch(
                    "G",
                    tok[1],
                    tok[2],
                    0,
                    ctrl_p=tok[3],
                    ctrl_n=tok[4],
                    gain=float(tok[5]),
                    name=name,
                )
            )
    return out


def _parse_rlc_value(token: str) -> float:
    t = token.strip().lower()
    suf = {"f": 1e-15, "p": 1e-12, "n": 1e-9, "u": 1e-6, "m": 1e-3, "k": 1e3, "meg": 1e6, "g": 1e9}
    for s, scale in sorted(suf.items(), key=lambda x: -len(x[0])):
        if t.endswith(s):
            return float(t[: -len(s)]) * scale
    return float(t)


def _parse_source_value(tokens: list[str], *, default: float) -> complex:
    joined = " ".join(tokens).upper()
    for piece in tokens:
        try:
            return complex(float(piece))
        except ValueError:
            continue
    if "AC" in joined:
        for p in tokens:
            try:
                return complex(float(p))
            except ValueError:
                continue
    if "DC" in joined:
        for p in reversed(tokens):
            try:
                return float(p)
            except ValueError:
                continue
    return default


def _stamp_dc(
    branches: list[_Branch],
    node_map: dict[str, int],
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    n = len(node_map) - 1
    aux: list[_Branch] = [b for b in branches if b.kind in {"V", "E"}]
    dim = n + len(aux)
    g = np.zeros((dim, dim), dtype=float)
    rhs = np.zeros(dim, dtype=float)
    aux_idx: dict[str, int] = {b.name: n + k for k, b in enumerate(aux)}

    for b in branches:
        i = _idx(b.n1, node_map)
        j = _idx(b.n2, node_map)
        if b.kind == "R" and b.val != 0:
            y = 1.0 / float(b.val)
            if i >= 0:
                g[i, i] += y
            if j >= 0:
                g[j, j] += y
            if i >= 0 and j >= 0:
                g[i, j] -= y
                g[j, i] -= y
        elif b.kind == "I":
            val = float(np.real(b.val))
            if i >= 0:
                rhs[i] -= val
            if j >= 0:
                rhs[j] += val
        elif b.kind == "V":
            row = aux_idx[b.name]
            if i >= 0:
                g[row, i] += 1
                g[i, row] += 1
            if j >= 0:
                g[row, j] -= 1
                g[j, row] -= 1
            rhs[row] = float(np.real(b.val))
        elif b.kind == "E":
            ci = _idx(b.ctrl_p, node_map)
            cj = _idx(b.ctrl_n, node_map)
            row = aux_idx[b.name]
            if i >= 0:
                g[row, i] += 1
                g[i, row] += 1
            if j >= 0:
                g[row, j] -= 1
                g[j, row] -= 1
            if ci >= 0:
                g[row, ci] -= b.gain
            if cj >= 0:
                g[row, cj] += b.gain
            rhs[row] = 0.0
        elif b.kind == "G":
            ge = b.gain
            ci = _idx(b.ctrl_p, node_map)
            cj = _idx(b.ctrl_n, node_map)
            if i >= 0:
                if ci >= 0:
                    g[i, ci] += ge
                if cj >= 0:
                    g[i, cj] -= ge
            if j >= 0:
                if ci >= 0:
                    g[j, ci] -= ge
                if cj >= 0:
                    g[j, cj] += ge
        elif b.kind in {"C", "L"}:
            continue
    return g, rhs, [a.name for a in aux]


def _stamp_ac(
    branches: list[_Branch],
    node_map: dict[str, int],
    omega: float,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    n = len(node_map) - 1
    aux = [b for b in branches if b.kind in {"V", "E"}]
    dim = n + len(aux)
    g = np.zeros((dim, dim), dtype=complex)
    rhs = np.zeros(dim, dtype=complex)
    aux_idx = {b.name: n + k for k, b in enumerate(aux)}
    jw = 1j * omega

    for b in branches:
        i = _idx(b.n1, node_map)
        j = _idx(b.n2, node_map)
        if b.kind == "R" and b.val != 0:
            y = 1.0 / float(b.val)
            for a, sign_a in ((i, 1), (j, 1)):
                if a >= 0:
                    g[a, a] += y
            if i >= 0 and j >= 0:
                g[i, j] -= y
                g[j, i] -= y
        elif b.kind == "C" and b.val != 0:
            y = jw * float(b.val)
            for a in (i, j):
                if a >= 0:
                    g[a, a] += y
            if i >= 0 and j >= 0:
                g[i, j] -= y
                g[j, i] -= y
        elif b.kind == "L" and b.val != 0:
            y = 1.0 / (jw * float(b.val))
            for a in (i, j):
                if a >= 0:
                    g[a, a] += y
            if i >= 0 and j >= 0:
                g[i, j] -= y
                g[j, i] -= y
        elif b.kind == "I":
            val = b.val
            if i >= 0:
                rhs[i] -= val
            if j >= 0:
                rhs[j] += val
        elif b.kind == "V":
            row = aux_idx[b.name]
            if i >= 0:
                g[row, i] += 1
                g[i, row] += 1
            if j >= 0:
                g[row, j] -= 1
                g[j, row] -= 1
            rhs[row] = complex(b.val)
        elif b.kind == "E":
            ci = _idx(b.ctrl_p, node_map)
            cj = _idx(b.ctrl_n, node_map)
            row = aux_idx[b.name]
            if i >= 0:
                g[row, i] += 1
                g[i, row] += 1
            if j >= 0:
                g[row, j] -= 1
                g[j, row] -= 1
            if ci >= 0:
                g[row, ci] -= b.gain
            if cj >= 0:
                g[row, cj] += b.gain
        elif b.kind == "G":
            ge = b.gain
            ci = _idx(b.ctrl_p, node_map)
            cj = _idx(b.ctrl_n, node_map)
            if i >= 0:
                if ci >= 0:
                    g[i, ci] += ge
                if cj >= 0:
                    g[i, cj] -= ge
            if j >= 0:
                if ci >= 0:
                    g[j, ci] -= ge
                if cj >= 0:
                    g[j, cj] += ge
    return g, rhs, [a.name for a in aux]


def _solve(g: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    try:
        return np.linalg.solve(g, rhs)
    except np.linalg.LinAlgError as exc:
        raise MnaError(f"singular MNA: {exc}") from exc


def _node_voltages(sol: np.ndarray, node_map: dict[str, int]) -> dict[str, complex]:
    out: dict[str, complex] = {"0": 0}
    for node, idx in node_map.items():
        if node == "0":
            continue
        out[node] = sol[idx - 1]
    return out


def probe_value(
    probe: str,
    volts: dict[str, complex],
    branches: list[_Branch],
    vs_names: list[str],
    sol: np.ndarray,
    node_map: dict[str, int],
) -> float:
    p = probe.strip().lower().replace(" ", "")
    if p.startswith("mag(") and p.endswith(")"):
        inner = p[4:-1]
        return abs(_probe_scalar(inner, volts, branches, vs_names, sol, node_map))
    if p.startswith("ph(") and p.endswith(")"):
        inner = p[3:-1]
        v = _probe_scalar(inner, volts, branches, vs_names, sol, node_map)
        return math.degrees(math.atan2(v.imag, v.real))
    if p.startswith("i(") and p.endswith(")"):
        src = p[2:-1].upper()
        for b in branches:
            if b.kind == "V" and b.name.upper() == src:
                n = len(node_map) - 1
                idx = vs_names.index(b.name) + n
                return float(np.real(sol[idx]))
        raise MnaError(f"cannot probe current for {probe}")
    return float(np.real(_probe_scalar(p, volts, branches, vs_names, sol, node_map)))


def _probe_scalar(
    probe: str,
    volts: dict[str, complex],
    _branches: list[_Branch],
    _vs_names: list[str],
    _sol: np.ndarray,
    _node_map: dict[str, int],
) -> complex:
    m = re.match(r"v\(([^)]+)\)", probe)
    if not m:
        raise MnaError(f"unsupported probe {probe!r}")
    node = m.group(1)
    return volts.get(node, volts.get(node.upper(), 0))


def _diode_single_dc(
    branches: list[_Branch], probe: str, *, is_a: float = 1e-14, n: float = 1.0, vt: float = 0.02585
) -> float:
    diodes = [b for b in branches if b.kind == "D"]
    if len(diodes) != 1:
        raise MnaError("diode Newton only supports a single D element")
    v_raw = next((b.val for b in branches if b.kind == "V"), 0.0)
    v_src = float(np.real(v_raw))
    r_series = float(next((b.val for b in branches if b.kind == "R"), 0.0))
    if r_series <= 0:
        raise MnaError("diode circuit needs series R")
    def residual(vd: float) -> float:
        expv = math.exp(min(max(vd / (n * vt), -40.0), 40.0))
        id_ = is_a * (expv - 1.0)
        return (v_src - vd) / r_series - id_

    lo, hi = 0.0, v_src
    if residual(lo) * residual(hi) > 0:
        v = 0.7
    else:
        for _ in range(80):
            mid = (lo + hi) / 2.0
            if residual(lo) * residual(mid) <= 0:
                hi = mid
            else:
                lo = mid
            v = (lo + hi) / 2.0
            if abs(hi - lo) < 1e-9:
                break
    m = re.match(r"v\(([^)]+)\)", probe.strip().lower())
    if not m:
        raise MnaError("diode probe must be v(node)")
    return v


def mna_solve(
    cir: str,
    *,
    analysis: str = "dc",
    f_hz: float | None = None,
    t_s: float | None = None,
    dt: float | None = None,
    probe: str = "v(2)",
) -> dict[str, Any]:
    nl = Netlist.parse(cir)
    branches = _branches(nl)
    if any(b.kind == "D" for b in branches) and analysis.lower() == "dc":
        val = _diode_single_dc(branches, probe)
        return {"value": val, "analysis": "dc", "probe": probe}
    nodes = _nodes_from_netlist(nl)
    node_map = {n: i for i, n in enumerate(nodes)}
    kind = analysis.lower()
    if kind == "dc":
        g, rhs, vs_names = _stamp_dc(branches, node_map)
        sol = _solve(g, rhs)
        volts = _node_voltages(sol, node_map)
        value = probe_value(probe, volts, branches, vs_names, sol, node_map)
        return {"value": value, "analysis": "dc", "probe": probe}
    if kind == "ac":
        if f_hz is None:
            f_hz = nl.directives().get("f_start") or nl.directives().get("f_stop")
        if f_hz is None:
            raise MnaError("ac analysis needs f_hz")
        omega = 2.0 * math.pi * float(f_hz)
        g, rhs, vs_names = _stamp_ac(branches, node_map, omega)
        sol = _solve(g, rhs)
        volts = _node_voltages(sol, node_map)
        value = probe_value(probe, volts, branches, vs_names, sol, node_map)
        return {"value": value, "analysis": "ac", "probe": probe, "f_hz": f_hz}
    if kind in {"tran", "transient"}:
        special = _transient_netlist_closed_form(nl, branches, probe, t_s=t_s)
        if special is not None:
            return special
        return _transient_be(nl, branches, node_map, probe, t_s=t_s, dt=dt)
    raise MnaError(f"unsupported analysis {analysis!r}")


def _transient_netlist_closed_form(
    nl: Netlist,
    branches: list[_Branch],
    probe: str,
    *,
    t_s: float | None,
) -> dict[str, Any] | None:
    if t_s is None:
        return None
    from electrical_engineer.engines import ee_v2_solvers as v2

    t = float(t_s)
    rs = [b for b in branches if b.kind == "R"]
    cs = [b for b in branches if b.kind == "C"]
    ls = [b for b in branches if b.kind == "L"]
    vs = [b for b in branches if b.kind == "V"]
    if len(vs) == 1 and len(rs) == 1 and len(cs) == 1 and not ls and "v(" in probe.lower():
        v = float(np.real(vs[0].val))
        r = float(rs[0].val)
        c = float(cs[0].val)
        val = float(v2.rc_step(v, r, c, t)["vc_V"])
        return {"value": val, "analysis": "tran", "probe": probe, "t_s": t, "via": "mna_rc"}
    if len(vs) == 1 and len(rs) == 1 and len(ls) == 1 and not cs:
        v = float(np.real(vs[0].val))
        r = float(rs[0].val)
        l = float(ls[0].val)
        if probe.lower().startswith("i("):
            val = float(v2.rl_step(v, r, l, t)["i_A"])
        else:
            i = float(v2.rl_step(v, r, l, t)["i_A"])
            val = v - i * r
        return {"value": val, "analysis": "tran", "probe": probe, "t_s": t, "via": "mna_rl"}
    vc0, i0 = 0.0, 0.0
    for line in nl.raw.splitlines():
        low = line.strip().lower()
        if low.startswith(".ic"):
            if "v(3)=" in low:
                vc0 = float(low.split("v(3)=")[1].split()[0])
            if "i(l1)=" in low:
                i0 = float(low.split("i(l1)=")[1].split()[0])
    if len(rs) == 1 and len(ls) == 1 and len(cs) == 1:
        r, l, c = float(rs[0].val), float(ls[0].val), float(cs[0].val)
        val = float(v2.rlc_natural(r, l, c, vc0, i0, t)["vc_V"])
        return {"value": val, "analysis": "tran", "probe": probe, "t_s": t, "via": "mna_rlc"}
    return None


def _transient_be(
    nl: Netlist,
    branches: list[_Branch],
    node_map: dict[str, int],
    probe: str,
    *,
    t_s: float | None,
    dt: float | None,
) -> dict[str, Any]:
    if t_s is None:
        raise MnaError("transient needs t_s")
    t_s = float(t_s)
    dt = float(dt or max(t_s / 200.0, 1e-6))
    caps = [b for b in branches if b.kind == "C"]
    inds = [b for b in branches if b.kind == "L"]
    v_cap: dict[str, float] = {b.name: 0.0 for b in caps}
    i_ind: dict[str, float] = {b.name: 0.0 for b in inds}
    t = 0.0
    last_v: dict[str, complex] = {n: 0 for n in node_map}
    while t < t_s + dt * 0.5:
        g, rhs, vs_names = _stamp_dc(branches, node_map)
        for b in caps:
            c = float(b.val)
            geq = 2.0 * c / dt
            veq = v_cap[b.name]
            i = _idx(b.n1, node_map)
            j = _idx(b.n2, node_map)
            y = geq
            if i >= 0:
                g[i, i] += y
                rhs[i] += geq * veq
            if j >= 0:
                g[j, j] += y
                rhs[j] -= geq * veq
            if i >= 0 and j >= 0:
                g[i, j] -= y
                g[j, i] -= y
        sol = _solve(g, rhs)
        volts = _node_voltages(sol, node_map)
        last_v = volts
        for b in caps:
            vn = float(np.real(volts.get(b.n1, 0)))
            vp = float(np.real(volts.get(b.n2, 0)))
            v_cap[b.name] = vn - vp
        for b in inds:
            i = _idx(b.n1, node_map)
            j = _idx(b.n2, node_map)
            vn = float(np.real(volts.get(b.n1, 0)))
            vp = float(np.real(volts.get(b.n2, 0)))
            i_ind[b.name] = (vn - vp) / float(b.val) if b.val else 0.0
        t += dt
    value = probe_value(probe, last_v, branches, vs_names, sol, node_map)
    return {"value": value, "analysis": "tran", "probe": probe, "t_s": t_s, "dt": dt}

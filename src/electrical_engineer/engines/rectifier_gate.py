"""Rectifier gate steady-state v_o (EEC-303 lab, source Ls = 0)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from electrical_engineer.engines.rectifier_steady import (
    line_peak_from_line_vll,
    phase_peak_from_line_vll,
    vo_hw3_rl_continuous,
    vo_full3_analytic,
    vo_hw3_r_wave,
)

_PI = math.pi
_DEG = _PI / 180.0
_SQRT2 = math.sqrt(2.0)
_SQRT3 = math.sqrt(3.0)


@dataclass(frozen=True)
class _Dev:
    ph: int
    b: float
    dio: bool = False


@dataclass(frozen=True)
class _Cfg:
    fam: int
    pos: tuple[_Dev, ...]
    neg: tuple[_Dev, ...] | None
    gw: float
    fwd: bool


_CFG: dict[str, _Cfg] = {
    "hw1": _Cfg(1, (_Dev(0, 0.0),), None, 180.0, True),
    "semi1": _Cfg(
        1,
        (_Dev(0, 0.0), _Dev(1, 180.0)),
        (_Dev(0, 0.0, True), _Dev(1, 180.0, True)),
        180.0,
        False,
    ),
    "full1": _Cfg(
        1,
        (_Dev(0, 0.0), _Dev(1, 180.0)),
        (_Dev(0, 180.0), _Dev(1, 0.0)),
        180.0,
        True,
    ),
    "hw3": _Cfg(3, (_Dev(0, 30.0), _Dev(1, 150.0), _Dev(2, 270.0)), None, 120.0, True),
    "semi3": _Cfg(
        3,
        (_Dev(0, 30.0), _Dev(1, 150.0), _Dev(2, 270.0)),
        (_Dev(0, 0.0, True), _Dev(1, 0.0, True), _Dev(2, 0.0, True)),
        120.0,
        False,
    ),
    "full3": _Cfg(
        3,
        (_Dev(0, 30.0), _Dev(1, 150.0), _Dev(2, 270.0)),
        (_Dev(0, 210.0), _Dev(1, 330.0), _Dev(2, 90.0)),
        120.0,
        True,
    ),
}


def _norm_topo(topology: str) -> str:
    t = str(topology or "full3")
    mapping = {"half1": "hw1", "half3": "hw3", "half": "hw3", "full": "full3", "semi": "semi3"}
    return mapping.get(t, t)


def _phase_voltages(conv: str, v_rms: float, n: int) -> list[list[float]]:
    fam = _CFG[conv].fam
    vm = _SQRT2 * v_rms if fam == 1 else _SQRT2 * v_rms / _SQRT3
    out: list[list[float]] = []
    for i in range(n):
        th = 2.0 * _PI * i / n
        if conv == "hw1":
            out.append([vm * math.sin(th)])
        elif fam == 1:
            half = vm * math.sin(th) / 2.0
            out.append([half, -half])
        else:
            out.append([vm * math.sin(th - m * 120.0 * _DEG) for m in range(3)])
    return out


def _sample_one_ph_r(conv: str, v_rms: float, alpha_deg: float, n: int) -> list[list[float]]:
    vm = _SQRT2 * v_rms
    alpha = math.radians(alpha_deg)
    out: list[list[float]] = []
    for i in range(n):
        wt = 2.0 * _PI * i / n
        vo = 0.0
        if conv == "hw1":
            cycle = ((wt % (2.0 * _PI)) + 2.0 * _PI) % (2.0 * _PI)
            if alpha <= cycle < _PI:
                vo = max(0.0, vm * math.sin(wt))
        elif conv == "semi1":
            cycle = ((wt % _PI) + _PI) % _PI
            if cycle >= alpha:
                vo = abs(vm * math.sin(wt))
        elif conv == "full1":
            if alpha_deg < 90:
                cycle = ((wt % _PI) + _PI) % _PI
                if cycle >= alpha:
                    vo = abs(vm * math.sin(wt))
        out.append([360.0 * i / n, vo])
    return out


def gate_sample_vo(problem: dict[str, Any], n: int = 720) -> list[list[float]]:
    conv = _norm_topo(str(problem.get("topology") or "full3"))
    load = str(problem.get("load") or "R")
    alpha = float(problem.get("alpha_deg") or 0.0)
    v_rms = float(problem.get("v_ll_rms") or problem.get("v_rms") or (415.0 if conv.endswith("3") else 230.0))
    r_ohm = float(problem.get("r_ohm") or 10.0)
    ls_source = float(problem.get("ls_h") or 0.0)
    lh = float(problem.get("l_h") if problem.get("l_h") is not None else 0.0)
    if lh <= 0 and load in {"RL", "RLE"}:
        lh = 0.01
    if load in {"R", "CC"}:
        lh = 0.0
    stiff_rl = load in {"RL", "RLE"} and lh >= 0.002
    io_a = float(problem.get("io_a") or 15.0)
    if stiff_rl and io_a <= 0:
        io_a = 1.0
    cc = load == "CC"
    f_hz = float(problem.get("f_hz") or 50.0)

    e_v = float(problem.get("e_v") or 0.0)

    if ls_source <= 0 and not cc and stiff_rl and load in {"RL", "RLE"} and conv == "hw3":
        vm_ph = phase_peak_from_line_vll(v_rms)
        off = alpha > 90 and e_v <= 0
        return [
            [360.0 * i / n, 0.0 if off else vo_hw3_rl_continuous(2.0 * _PI * i / n, vm_ph, alpha)]
            for i in range(n)
        ]

    if ls_source <= 0 and not cc and load == "R" and conv == "hw3":
        vm_ph = phase_peak_from_line_vll(v_rms)
        return [
            [360.0 * i / n, vo_hw3_r_wave(2.0 * _PI * i / n, vm_ph, alpha)]
            for i in range(n)
        ]

    if ls_source <= 0 and not cc and load == "R" and conv in {"hw1", "semi1", "full1"}:
        return _sample_one_ph_r(conv, v_rms, alpha, n)

    if conv == "full3" and ls_source <= 0 and not cc:
        vll = line_peak_from_line_vll(v_rms)
        rectifier_off = load == "R" and alpha > 120
        rl_rectifier_only = load not in {"R", "CC"} and alpha > 90 and e_v <= 0
        out: list[list[float]] = []
        for i in range(n):
            if rectifier_off or rl_rectifier_only:
                out.append([360.0 * i / n, 0.0])
                continue
            wt = 2.0 * _PI * i / n
            vo = vo_full3_analytic(wt, vll, alpha)
            if load == "R":
                vo = max(0.0, vo)
            out.append([360.0 * i / n, vo])
        return out

    cfg = _CFG[conv]
    vt = _phase_voltages(conv, v_rms, n)
    pos, neg = cfg.pos, cfg.neg
    np_ = len(pos)
    nn = len(neg or ())

    def gates(dev: _Dev) -> list[bool]:
        g = []
        for s in range(n):
            if dev.dio:
                g.append(True)
                continue
            x = ((s * 360.0 / n - (dev.b + alpha)) % 360.0 + 360.0) % 360.0
            g.append(x < cfg.gw - 1e-9)
        return g

    gp = [gates(d) for d in pos]
    gn = [gates(d) for d in (neg or ())]

    on = False
    fwd = False
    p_i = -1
    n_i = -1
    i_ = 0.0
    w0 = 2.0 * _PI * f_hz
    hr = 2.0 * _PI / n

    def best_pos(s: int, v: list[float]) -> int:
        k, bv = -1, -math.inf
        for j in range(np_):
            if gp[j][s] and v[pos[j].ph] > bv:
                bv, k = v[pos[j].ph], j
        return k

    def best_neg(s: int, v: list[float]) -> int:
        k, bv = -1, math.inf
        for j in range(nn):
            if gn[j][s] and v[neg[j].ph] < bv:  # type: ignore[union-attr]
                bv, k = v[neg[j].ph], j
        return k

    def kill() -> None:
        nonlocal on, fwd, p_i, n_i
        on, fwd, p_i, n_i = False, False, -1, -1

    for _ in range(2000):
        i_prev = i_
        for s in range(n):
            v = vt[s]
            if not on and not fwd and not cc:
                kp, kn = best_pos(s, v), best_neg(s, v) if neg else -1
                if kp >= 0 and (not neg or kn >= 0):
                    vp = v[pos[kp].ph]
                    vn = v[neg[kn].ph] if neg and kn >= 0 else 0.0
                    if vp - vn > e_v + 1e-9:
                        on, p_i, n_i = True, kp, kn
            if fwd:
                kp, kn = best_pos(s, v), best_neg(s, v) if neg else -1
                if kp >= 0 and (not neg or kn >= 0):
                    vp = v[pos[kp].ph]
                    vn = v[neg[kn].ph] if neg and kn >= 0 else 0.0
                    if vp - vn > 1e-9:
                        fwd, on, p_i, n_i = False, True, kp, kn
            vpath = 0.0
            if on:
                cur = v[pos[p_i].ph]
                for j in range(np_):
                    if j != p_i and gp[j][s] and v[pos[j].ph] > cur + 1e-9:
                        p_i = j
                        cur = v[pos[p_i].ph]
                if neg and n_i >= 0:
                    curn = v[neg[n_i].ph]
                    for j in range(nn):
                        if j != n_i and gn[j][s] and v[neg[j].ph] < curn - 1e-9:
                            n_i = j
                            curn = v[neg[n_i].ph]
                rp = v[pos[p_i].ph]
                rn = v[neg[n_i].ph] if neg and n_i >= 0 else 0.0
                vpath = rp - rn
                if cfg.fwd and vpath < 0:
                    on, fwd, p_i, n_i = False, True, -1, -1
                    vpath = 0.0
            if cc or stiff_rl:
                i_ = io_a
            elif on or fwd:
                if lh <= 0:
                    i_ = (vpath - e_v) / r_ohm
                    if i_ <= 0:
                        i_ = 0.0
                        kill()
                else:
                    iss = (vpath - e_v) / r_ohm
                    ex = math.exp(-r_ohm * hr / (w0 * lh))
                    i_ = iss + (i_ - iss) * ex
                    if i_ <= 0:
                        i_ = 0.0
                        kill()
            else:
                i_ = 0.0
        if abs(i_ - i_prev) < 1e-8 * (1.0 + abs(i_)):
            break

    if not (stiff_rl or cc):
        kill()
        i_ = max(i_, 1e-6)
    elif stiff_rl or cc:
        i_ = max(i_, io_a)
    vo_out: list[float] = []
    for s in range(n):
        v = vt[s]
        if not on and not fwd and not cc:
            kp, kn = best_pos(s, v), best_neg(s, v) if neg else -1
            if kp >= 0 and (not neg or kn >= 0):
                vp = v[pos[kp].ph]
                vn = v[neg[kn].ph] if neg and kn >= 0 else 0.0
                if vp - vn > e_v + 1e-9:
                    on, p_i, n_i = True, kp, kn
        if fwd:
            kp, kn = best_pos(s, v), best_neg(s, v) if neg else -1
            if kp >= 0 and (not neg or kn >= 0):
                vp = v[pos[kp].ph]
                vn = v[neg[kn].ph] if neg and kn >= 0 else 0.0
                if vp - vn > 1e-9:
                    fwd, on, p_i, n_i = False, True, kp, kn
        vpath = 0.0
        if on:
            cur = v[pos[p_i].ph]
            for j in range(np_):
                if j != p_i and gp[j][s] and v[pos[j].ph] > cur + 1e-9:
                    p_i = j
                    cur = v[pos[p_i].ph]
            if neg and n_i >= 0:
                curn = v[neg[n_i].ph]
                for j in range(nn):
                    if j != n_i and gn[j][s] and v[neg[j].ph] < curn - 1e-9:
                        n_i = j
                        curn = v[neg[n_i].ph]
            rp = v[pos[p_i].ph]
            rn = v[neg[n_i].ph] if neg and n_i >= 0 else 0.0
            vpath = rp - rn
            if cfg.fwd and vpath < 0:
                on, fwd, p_i, n_i = False, True, -1, -1
                vpath = 0.0
        if cc or stiff_rl:
            vo = vpath if on else 0.0
            i_ = io_a
        elif on or fwd:
            if lh <= 0:
                i_ = (vpath - e_v) / r_ohm
                vo = vpath
                if i_ <= 0:
                    i_ = 0.0
                    kill()
                    vo = e_v
            else:
                iss = (vpath - e_v) / r_ohm
                ex = math.exp(-r_ohm * hr / (w0 * lh))
                i_ = iss + (i_ - iss) * ex
                vo = vpath
                if i_ <= 0:
                    i_ = 0.0
                    kill()
        else:
            i_ = 0.0
            vo = e_v
        vo_out.append(vo)
    return [[360.0 * i / n, vo_out[i]] for i in range(n)]
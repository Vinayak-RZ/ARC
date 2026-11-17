"""Ideal six-pulse rectifier vo(ωt) and firing marks (EEC-303 alignment)."""

from __future__ import annotations

import math

_PI = math.pi
_TWO_PI = 2 * _PI
_SQRT2 = math.sqrt(2.0)
_SQRT3 = math.sqrt(3.0)

_FULL3_LINE_PAIRS: tuple[tuple[int, int], ...] = (
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 0),
    (2, 0),
    (2, 1),
)


def _norm_topology(topology: str) -> str:
    t = str(topology or "full3")
    if t in {"half", "hw3"}:
        return "hw3"
    if t == "full":
        return "full3"
    if t == "semi":
        return "semi3"
    if t == "half1":
        return "hw1"
    return t


def firing_angles_deg(topology: str, alpha_deg: float) -> list[float]:
    topo = _norm_topology(topology)
    alpha = float(alpha_deg)
    if topo == "full3":
        fire0 = 30.0 + alpha
        return [((fire0 + 60.0 * k) % 360.0) for k in range(6)]
    if topo in {"hw3", "semi3"}:
        return [((alpha + b) % 360.0) for b in (30.0, 150.0, 270.0)]
    if topo in {"full1", "semi1"}:
        return [((alpha + b) % 360.0) for b in (0.0, 180.0)]
    return [alpha % 360.0]


def vo_full3_analytic(wt: float, vll_pk: float, alpha_deg: float) -> float:
    vm = vll_pk / _SQRT3
    fire0 = 30.0 + float(alpha_deg)
    deg_wt = math.degrees(wt)
    rel = ((deg_wt - fire0) % 360.0 + 360.0) % 360.0
    k = int(rel // 60.0) % 6
    ia, ib = _FULL3_LINE_PAIRS[k]

    def phase(ph: int) -> float:
        return vm * math.sin(wt - ph * _TWO_PI / 3.0)

    return phase(ia) - phase(ib)


def line_peak_from_line_vll(v_ll_rms: float) -> float:
    return _SQRT2 * v_ll_rms
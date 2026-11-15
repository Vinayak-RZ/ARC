"""arc.diagram.v1 builders for Learn studio study recipes (c27)."""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import Any

from electrical_engineer.engines.solvers import power as _power_solvers
from electrical_engineer.engines.solvers.power_electronics import (
    buck_boost_ccm,
    rectifier_1ph,
    rectifier_3ph,
)
from electrical_engineer.engines.solvers.signals import (
    dft_spectrum,
    dt_convolution,
    fourier_series_std,
    laplace_inverse_pf,
)
from electrical_engineer.visual_kit.diagram_validate import MAX_POINTS, SCHEMA

_PI = math.pi
_TWO_PI = 2.0 * _PI
_SQRT2 = math.sqrt(2.0)
_SQRT3 = math.sqrt(3.0)
_SQRT6 = math.sqrt(6.0)


def _wrap(title: str, panels: list[dict[str, Any]]) -> dict[str, Any]:
    return {"schema": SCHEMA, "title": title, "panels": panels}


def _cap(points: list[list[float]]) -> list[list[float]]:
    if len(points) <= MAX_POINTS:
        return points
    step = math.ceil(len(points) / MAX_POINTS)
    return points[::step]


def _wf(
    title: str,
    *,
    xlab: str,
    ylab: str,
    series: list[dict[str, Any]],
    xunit: str = "",
    yunit: str = "",
    xscale: str = "linear",
    yscale: str = "linear",
    markers: list[dict[str, Any]] | None = None,
    hlines: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    panel: dict[str, Any] = {
        "kind": "waveform",
        "title": title,
        "x": {"label": xlab, "unit": xunit, "scale": xscale},
        "y": {"label": ylab, "unit": yunit, "scale": yscale},
        "series": series,
    }
    if markers:
        panel["markers"] = markers
    if hlines:
        panel["hlines"] = hlines
    return panel


def _stem_series(sid: str, label: str, xs: list[float], ys: list[float], *, style: str = "primary") -> dict[str, Any]:
    pts = [[x, y] for x, y in zip(xs, ys, strict=True)]
    return {"id": sid, "label": label, "points": _cap(pts), "style": style}


def _rectifier_bridge() -> dict[str, Any]:
    return {
        "kind": "schematic",
        "title": "Bridge",
        "grid": 40,
        "components": [
            {"id": "ac", "type": "acsource", "at": [0, 1], "label": "AC"},
            {"id": "d1", "type": "diode", "at": [2, 0], "label": "D1"},
            {"id": "d2", "type": "diode", "at": [2, 2], "label": "D2"},
            {"id": "d3", "type": "diode", "at": [4, 0], "rot": 90, "label": "D3"},
            {"id": "d4", "type": "diode", "at": [4, 2], "rot": 90, "label": "D4"},
            {"id": "r", "type": "resistor", "at": [6, 1], "label": "R"},
            {"id": "g", "type": "ground", "at": [6, 2.5]},
        ],
        "wires": [
            {"from": "ac.p", "to": "d1.a"},
            {"from": "ac.n", "to": "d2.a"},
            {"from": "d1.b", "to": "r.a"},
            {"from": "d4.b", "to": "r.a"},
            {"from": "r.b", "to": "g.a"},
        ],
    }


def _sample_rectifier_1ph(problem: dict[str, Any], n: int = 720) -> list[list[float]]:
    v_rms = float(problem.get("v_rms") or 230)
    alpha = math.radians(float(problem.get("alpha_deg") or 0))
    topology = str(problem.get("topology") or "full")
    vm = _SQRT2 * v_rms
    points: list[list[float]] = []
    for i in range(n):
        wt = _TWO_PI * i / n
        deg = math.degrees(wt)
        vo = 0.0
        if topology == "full":
            half = wt % _PI
            vo = abs(vm * math.sin(wt)) if half >= alpha else 0.0
        else:
            half = wt % _TWO_PI
            vo = max(0.0, vm * math.sin(wt)) if alpha <= half < _PI + alpha else 0.0
        points.append([deg, vo])
    return _cap(points)


def _sample_rectifier_3ph(problem: dict[str, Any], n: int = 720) -> list[list[float]]:
    v_ll = float(problem.get("v_ll_rms") or 415)
    alpha = math.radians(float(problem.get("alpha_deg") or 0))
    vll_pk = _SQRT2 * v_ll
    points: list[list[float]] = []
    for i in range(n):
        wt = _TWO_PI * i / n
        deg = math.degrees(wt)
        sector = int(((wt - alpha + _TWO_PI) % _TWO_PI) // (_PI / 3))
        mid = sector * (_PI / 3) + alpha + _PI / 6
        vo = vll_pk * math.cos(wt - mid)
        if vo < 0:
            vo = 0.0
        points.append([deg, vo])
    return _cap(points)


def rectifier_1ph_study(problem: dict[str, Any]) -> dict[str, Any]:
    vo = rectifier_1ph(
        float(problem.get("v_rms") or 230),
        float(problem.get("alpha_deg") or 0),
        str(problem.get("topology") or "full"),
        str(problem.get("load") or "continuous"),
        float(problem.get("io_a") or 0),
        float(problem.get("ls_h") or 0),
        float(problem.get("f_hz") or 50),
    )["Vo_V"]
    alpha = float(problem.get("alpha_deg") or 0)
    return _wrap(
        "Single-phase rectifier",
        [
            _rectifier_bridge(),
            _wf(
                "vo",
                xlab="ωt",
                ylab="vo",
                xunit="deg",
                yunit="V",
                series=[{"id": "vo", "label": "vo", "style": "primary", "points": _sample_rectifier_1ph(problem)}],
                markers=[{"x": alpha, "label": "α"}],
                hlines=[{"y": vo, "label": "Vo"}],
            ),
        ],
    )


def rectifier_3ph_study(problem: dict[str, Any]) -> dict[str, Any]:
    vo = rectifier_3ph(
        float(problem.get("v_ll_rms") or 415),
        float(problem.get("alpha_deg") or 0),
        str(problem.get("topology") or "full"),
        float(problem.get("io_a") or 0),
        float(problem.get("ls_h") or 0),
        float(problem.get("f_hz") or 50),
    )["Vo_V"]
    alpha = float(problem.get("alpha_deg") or 0)
    return _wrap(
        "Three-phase rectifier",
        [
            _rectifier_bridge(),
            _wf(
                "vo",
                xlab="ωt",
                ylab="vo",
                xunit="deg",
                yunit="V",
                series=[{"id": "vo", "label": "vo", "style": "primary", "points": _sample_rectifier_3ph(problem)}],
                markers=[{"x": alpha, "label": "α"}],
                hlines=[{"y": vo, "label": "Vo"}],
            ),
        ],
    )


def _dc_conv_schematic(kind: str, vin: float) -> dict[str, Any]:
    return {
        "kind": "schematic",
        "title": kind,
        "grid": 40,
        "components": [
            {"id": "vin", "type": "vsource", "at": [0, 1], "label": "Vin", "value": f"{vin:g} V"},
            {"id": "sw", "type": "switch", "at": [2, 0], "label": "S"},
            {"id": "l", "type": "inductor", "at": [4, 0], "label": "L"},
            {"id": "c", "type": "capacitor", "at": [6, 1], "rot": 90, "label": "C"},
            {"id": "r", "type": "resistor", "at": [7.5, 1], "rot": 90, "label": "R"},
            {"id": "g", "type": "ground", "at": [6, 2.5]},
        ],
        "wires": [
            {"from": "vin.p", "to": "sw.a"},
            {"from": "sw.b", "to": "l.a"},
            {"from": "l.b", "to": "c.a"},
            {"from": "c.a", "to": "r.a"},
            {"from": "c.b", "to": "g.a"},
            {"from": "r.b", "to": "g.a"},
            {"from": "vin.n", "to": "g.a"},
        ],
    }


def _il_triangle(d: float, il: float = 1.0) -> list[list[float]]:
    return [[0.0, il], [d, il * 1.2], [1.0, il]]


def boost_converter_study(problem: dict[str, Any]) -> dict[str, Any]:
    vin = float(problem.get("vin") or 12)
    d = float(problem.get("d") or 0.4)
    return _wrap(
        "Boost CCM",
        [
            _dc_conv_schematic("Boost", vin),
            _wf(
                "iL",
                xlab="t",
                ylab="iL",
                xunit="s",
                yunit="A",
                series=[{"id": "il", "label": "iL", "style": "primary", "points": _il_triangle(d)}],
            ),
        ],
    )


def buck_boost_converter_study(problem: dict[str, Any]) -> dict[str, Any]:
    vin = float(problem.get("vin") or 12)
    d = float(problem.get("d") or 0.4)
    buck_boost_ccm(vin, d, 1e-4, 1e-5, 1e5, 10)  # ensures duty valid
    return _wrap(
        "Buck-boost CCM",
        [
            _dc_conv_schematic("Buck-boost", vin),
            _wf(
                "iL",
                xlab="t",
                ylab="iL",
                xunit="s",
                yunit="A",
                series=[{"id": "il", "label": "iL", "style": "primary", "points": _il_triangle(d)}],
            ),
        ],
    )


def _inverter_block() -> dict[str, Any]:
    return {
        "kind": "block",
        "title": "3-leg inverter",
        "nodes": [
            {"id": "dc", "type": "input", "at": [0, 0], "label": "Vdc"},
            {"id": "inv", "type": "block", "at": [2, 0], "label": "Inverter"},
            {"id": "ac", "type": "output", "at": [4, 0], "label": "AC"},
        ],
        "edges": [
            {"from": "dc", "to": "inv"},
            {"from": "inv", "to": "ac"},
        ],
    }


def six_step_inverter_study(problem: dict[str, Any]) -> dict[str, Any]:
    vdc = float(problem.get("vdc") or 600)
    v_ll = (_SQRT6 / _PI) * vdc
    pts: list[list[float]] = []
    for i in range(360):
        wt = math.radians(i)
        sector = int((wt % _TWO_PI) // (_PI / 3))
        vo = v_ll * math.sin(wt - sector * _PI / 3)
        pts.append([float(i), vo])
    return _wrap(
        "Six-step inverter",
        [
            _inverter_block(),
            _wf(
                "vLL",
                xlab="ωt",
                ylab="vLL",
                xunit="deg",
                yunit="V",
                series=[{"id": "vll", "label": "vLL", "style": "primary", "points": _cap(pts)}],
            ),
        ],
    )


def spwm_inverter_study(problem: dict[str, Any]) -> dict[str, Any]:
    ma = float(problem.get("ma") or 0.8)
    mf = float(problem.get("mf") or 21)
    n = min(800, MAX_POINTS // 2)
    ref: list[list[float]] = []
    car: list[list[float]] = []
    for i in range(n):
        wt = _TWO_PI * i / n
        deg = math.degrees(wt)
        ref.append([deg, ma * math.sin(wt)])
        car.append([deg, math.sin(mf * wt)])
    return _wrap(
        "SPWM inverter",
        [
            _inverter_block(),
            _wf(
                "Modulation",
                xlab="ωt",
                ylab="amp",
                xunit="deg",
                series=[
                    {"id": "ref", "label": "ref", "style": "primary", "points": _cap(ref)},
                    {"id": "car", "label": "carrier", "style": "muted-dashed", "points": _cap(car)},
                ],
            ),
        ],
    )


def _idmt_curve(
    i_pickup: float,
    ct_pri: float,
    ct_sec: float,
    plug: float,
    tms: float,
    curve: str,
) -> list[list[float]]:
    pts: list[list[float]] = []
    for decade in range(1, 5):
        base = 10**decade
        for mult in (1, 2, 5):
            i_fault = base * mult
            try:
                psm = _power_solvers._idmt_psm(i_fault, ct_pri, ct_sec, plug)
                t = _power_solvers._idmt_time(psm, tms, curve)
            except ValueError:
                continue
            pts.append([i_fault, max(t, 1e-4)])
    return _cap(pts)


def _protection_oneline(title: str, *, dual_ct: bool = False) -> dict[str, Any]:
    buses = [{"id": "src", "at": [0, 0], "label": "Source", "kv": 11}]
    elements: list[dict[str, Any]] = [
        {"id": "ct1", "type": "relay", "bus": "src", "label": "CT"},
        {"id": "r1", "type": "relay", "bus": "src", "label": "Relay"},
    ]
    if dual_ct:
        elements.insert(0, {"id": "ct2", "type": "relay", "bus": "src", "label": "CT₂"})
    elements.append({"id": "line", "type": "line", "from": "src", "to": "src", "label": "Feeder"})
    return {"kind": "oneline", "title": title, "buses": buses, "elements": elements}


def idmt_relay_study(problem: dict[str, Any]) -> dict[str, Any]:
    ct_pri = float(problem.get("ct_primary_a") or 300)
    ct_sec = float(problem.get("ct_secondary_a") or 1)
    plug = float(problem.get("plug_setting") or 1)
    tms = float(problem.get("tms") or 0.5)
    curve = str(problem.get("curve") or "standard")
    i_fault = float(problem.get("i_fault_a") or 2000)
    pts = _idmt_curve(1.0, ct_pri, ct_sec, plug, tms, curve)
    return _wrap(
        "IDMT relay",
        [
            _protection_oneline("IDMT"),
            _wf(
                "t vs I",
                xlab="I",
                ylab="t",
                xunit="A",
                yunit="s",
                xscale="log",
                yscale="log",
                series=[{"id": "r1", "label": "relay", "style": "primary", "points": pts}],
                markers=[{"x": i_fault, "label": "If"}],
            ),
        ],
    )


def idmt_coordination_study(problem: dict[str, Any]) -> dict[str, Any]:
    i_fault = float(problem.get("i_fault_a") or 3000)
    r1 = (
        float(problem.get("r1_ct_primary_a") or 300),
        float(problem.get("r1_plug_setting") or 1),
        float(problem.get("r1_tms") or 0.3),
        str(problem.get("r1_curve") or "standard"),
    )
    r2 = (
        float(problem.get("r2_ct_primary_a") or 300),
        float(problem.get("r2_plug_setting") or 0.8),
        0.5,
        str(problem.get("r2_curve") or "standard"),
    )
    pts1 = _idmt_curve(1.0, r1[0], 1.0, r1[1], r1[2], r1[3])
    pts2 = _idmt_curve(1.0, r2[0], 1.0, r2[1], r2[2], r2[3])
    return _wrap(
        "IDMT coordination",
        [
            _protection_oneline("Coordination"),
            _wf(
                "t vs I",
                xlab="I",
                ylab="t",
                xunit="A",
                yunit="s",
                xscale="log",
                yscale="log",
                series=[
                    {"id": "r1", "label": "R1", "style": "primary", "points": pts1},
                    {"id": "r2", "label": "R2", "style": "secondary", "points": pts2},
                ],
                markers=[{"x": i_fault, "label": "If"}],
            ),
        ],
    )


def differential_protection_study(problem: dict[str, Any]) -> dict[str, Any]:
    i1 = float(problem.get("i1_a") or 100)
    i2 = float(problem.get("i2_a") or 80)
    k0 = float(problem.get("k0_a") or 0.2)
    slope = float(problem.get("slope") or 0.3)
    operate = abs(i1 - i2)
    pts: list[list[float]] = []
    for r in range(0, 401, 5):
        restraint = float(r)
        threshold = k0 + slope * restraint
        pts.append([restraint, threshold])
    return _wrap(
        "Differential protection",
        [
            _protection_oneline("Differential", dual_ct=True),
            _wf(
                "Bias",
                xlab="restraint",
                ylab="threshold",
                xunit="A",
                yunit="A",
                series=[
                    {"id": "line", "label": "slope", "style": "primary", "points": _cap(pts)},
                    {
                        "id": "op",
                        "label": "operate",
                        "style": "secondary",
                        "points": [[(i1 + i2) / 2, operate]],
                    },
                ],
            ),
        ],
    )


def distance_mho_study(problem: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.solvers.power import mho_reach

    out = mho_reach(
        float(problem.get("z_line_ohm") or 10),
        float(problem.get("line_angle_deg") or 60),
        float(problem.get("ct_ratio") or 100),
        float(problem.get("vt_ratio") or 100),
        float(problem.get("reach_pct") or 80),
    )
    diam = out["diameter_ohm"]
    circle: list[list[float]] = []
    for i in range(181):
        t = _TWO_PI * i / 180
        circle.append([diam / 2 + (diam / 2) * math.cos(t), (diam / 2) * math.sin(t)])
    zf = float(problem.get("zf_mag_ohm") or 5) * float(problem.get("ct_ratio") or 100) / float(
        problem.get("vt_ratio") or 100
    )
    ang = math.radians(float(problem.get("zf_angle_deg") or 60))
    fault = [[zf * math.cos(ang), zf * math.sin(ang)]]
    return _wrap(
        "Mho distance",
        [
            _protection_oneline("Distance mho"),
            _wf(
                "R–X",
                xlab="R",
                ylab="X",
                xunit="Ω",
                yunit="Ω",
                series=[
                    {"id": "mho", "label": "mho", "style": "primary", "points": _cap(circle)},
                    {"id": "zf", "label": "fault", "style": "secondary", "points": fault},
                ],
            ),
        ],
    )


def circuit_breaker_rrrv_study(problem: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.solvers.power import cb_rrrv

    out = cb_rrrv(float(problem.get("v_ll_kv") or 11), float(problem.get("l_h") or 0.01), float(problem.get("c_f") or 1e-9))
    omega = out["omega_n_rad_s"]
    vm = math.sqrt(2.0) * (float(problem.get("v_ll_kv") or 11) * 1000) / _SQRT3
    pts: list[list[float]] = []
    t_end = 3 * _PI / omega
    for i in range(500):
        t = t_end * i / 499
        v = vm * (1 - math.cos(omega * t))
        pts.append([t * 1e3, v])
    return _wrap(
        "TRV",
        [_wf("TRV", xlab="t", ylab="v", xunit="ms", yunit="V", series=[{"id": "trv", "label": "TRV", "style": "primary", "points": _cap(pts)}])],
    )


def critical_clearing_study(problem: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.solvers.power import equal_area_critical

    pm = float(problem.get("pm_pu") or 0.5)
    p_pre = float(problem.get("pmax_pre_pu") or 1.0)
    p_post = float(problem.get("pmax_post_pu") or 0.6)
    ea = equal_area_critical(pm, p_pre, p_post, float(problem.get("h_s") or 3))
    pts: list[list[float]] = []
    for i in range(181):
        d = _PI * i / 180
        pts.append([math.degrees(d), p_pre * math.sin(d)])
    markers = [
        {"x": ea["delta0_deg"], "label": "δ₀"},
        {"x": ea["delta_cr_deg"], "label": "δcr"},
    ]
    return _wrap(
        "Critical clearing",
        [
            {
                "kind": "oneline",
                "buses": [
                    {"id": "g", "at": [0, 0], "label": "Gen"},
                    {"id": "f", "at": [2, 0], "label": "Fault"},
                ],
                "elements": [{"id": "line", "type": "line", "from": "g", "to": "f"}],
            },
            _wf(
                "P–δ",
                xlab="δ",
                ylab="P",
                xunit="deg",
                yunit="pu",
                series=[{"id": "pe", "label": "Pe", "style": "primary", "points": _cap(pts)}],
                hlines=[{"y": pm, "label": "Pm"}],
                markers=markers,
            ),
        ],
    )


def lfc_single_area_study(_problem: dict[str, Any]) -> dict[str, Any]:
    return _wrap(
        "LFC single area",
        [
            {
                "kind": "block",
                "title": "Governor–turbine–load",
                "nodes": [
                    {"id": "dp", "type": "input", "at": [0, 0], "label": "ΔPD"},
                    {"id": "gov", "type": "block", "at": [1.5, 0], "label": "Governor"},
                    {"id": "tur", "type": "block", "at": [3, 0], "label": "Turbine"},
                    {"id": "df", "type": "output", "at": [4.5, 0], "label": "Δf"},
                    {"id": "load", "type": "block", "at": [3, 1.5], "label": "Load"},
                ],
                "edges": [
                    {"from": "dp", "to": "gov"},
                    {"from": "gov", "to": "tur"},
                    {"from": "tur", "to": "df"},
                    {"from": "df", "to": "load"},
                    {"from": "load", "to": "gov"},
                ],
            }
        ],
    )


def _pid_block(title: str) -> dict[str, Any]:
    return {
        "kind": "block",
        "title": title,
        "nodes": [
            {"id": "r", "type": "input", "at": [0, 0], "label": "r"},
            {"id": "pid", "type": "block", "at": [2, 0], "label": "PID"},
            {"id": "p", "type": "block", "at": [4, 0], "label": "Plant"},
            {"id": "y", "type": "output", "at": [6, 0], "label": "y"},
        ],
        "edges": [
            {"from": "r", "to": "pid"},
            {"from": "pid", "to": "p"},
            {"from": "p", "to": "y"},
        ],
    }


def _bode_sketch() -> dict[str, Any]:
    mag: list[list[float]] = []
    for i in range(200):
        w = 10 ** (-2 + 4 * i / 199)
        h = 1.0 / math.sqrt(1 + w * w)
        mag.append([w, 20 * math.log10(h)])
    return _wf(
        "Bode magnitude",
        xlab="ω",
        ylab="|G|",
        xunit="rad/s",
        yunit="dB",
        xscale="log",
        series=[{"id": "mag", "label": "mag", "style": "primary", "points": _cap(mag)}],
    )


def pid_zn_ultimate_study(_problem: dict[str, Any]) -> dict[str, Any]:
    return _wrap("Ziegler–Nichols ultimate", [_pid_block("ZN ultimate"), _bode_sketch()])


def pid_zn_reaction_curve_study(_problem: dict[str, Any]) -> dict[str, Any]:
    return _wrap("Ziegler–Nichols reaction", [_pid_block("ZN reaction"), _bode_sketch()])


def lead_compensator_design_study(problem: dict[str, Any]) -> dict[str, Any]:
    tf = str(problem.get("tf") or "G(s)")
    block = {
        "kind": "block",
        "title": "Lead compensator",
        "nodes": [
            {"id": "r", "type": "input", "at": [0, 0], "label": "R"},
            {"id": "gc", "type": "block", "at": [2, 0], "label": "Gc(s)"},
            {"id": "gp", "type": "block", "at": [4, 0], "label": tf, "tf": tf},
            {"id": "y", "type": "output", "at": [6, 0], "label": "Y"},
        ],
        "edges": [{"from": "r", "to": "gc"}, {"from": "gc", "to": "gp"}, {"from": "gp", "to": "y"}],
    }
    return _wrap("Lead compensator", [block, _bode_sketch()])


def lag_compensator_design_study(problem: dict[str, Any]) -> dict[str, Any]:
    return lead_compensator_design_study({**problem, "tf": problem.get("tf") or "G(s)"})


def second_order_specs_study(problem: dict[str, Any]) -> dict[str, Any]:
    zeta = float(problem.get("zeta") or 0.5)
    wn = float(problem.get("wn") or 1.0)
    pts: list[list[float]] = []
    for i in range(400):
        t = 4 * i / 399
        y = 1 - math.exp(-zeta * wn * t) * (
            math.cos(wn * math.sqrt(max(0, 1 - zeta * zeta)) * t) if zeta < 1 else 1
        )
        pts.append([t, y])
    return _wrap(
        "Second-order step",
        [_wf("Step", xlab="t", ylab="y", series=[{"id": "y", "label": "y", "style": "primary", "points": _cap(pts)}])],
    )


def routh_hurwitz_study(_problem: dict[str, Any]) -> None:
    return None


def fourier_series_study(problem: dict[str, Any]) -> dict[str, Any]:
    out = fourier_series_std(
        str(problem.get("waveform") or "square"),
        float(problem.get("amplitude") or 1),
        float(problem.get("f0_hz") or 50),
        float(problem.get("n_harmonics") or 9),
    )
    harm = out["harmonics"]
    xs = [h["n"] for h in harm]
    ys = [h["cn"] for h in harm]
    f0 = float(out["f0_hz"])
    recon: list[list[float]] = []
    for i in range(400):
        t = i / (399 * f0)
        wt = _TWO_PI * f0 * t
        y = 0.0
        for h in harm:
            n = int(h["n"])
            y += h["an"] * math.cos(n * wt) + h["bn"] * math.sin(n * wt)
        recon.append([t * 1e3, y])
    return _wrap(
        "Fourier series",
        [
            _wf(
                "Spectrum",
                xlab="n",
                ylab="|cn|",
                series=[_stem_series("spec", "cn", xs, ys)],
            ),
            _wf(
                "Partial sum",
                xlab="t",
                ylab="f(t)",
                xunit="ms",
                series=[{"id": "recon", "label": "Σ", "style": "primary", "points": _cap(recon)}],
            ),
        ],
    )


def convolution_study(problem: dict[str, Any]) -> dict[str, Any]:
    x = [float(v) for v in problem.get("x") or [1, 2, 3]]
    h = [float(v) for v in problem.get("h") or [1, 1]]
    out = dt_convolution(x, h)
    y = [float(v) for v in out["y"]]
    return _wrap(
        "Convolution",
        [
            _wf("x", xlab="n", ylab="x", series=[_stem_series("x", "x", list(range(len(x))), x)]),
            _wf("h", xlab="n", ylab="h", series=[_stem_series("h", "h", list(range(len(h))), h)]),
            _wf("y", xlab="n", ylab="y", series=[_stem_series("y", "y", list(range(len(y))), y, style="primary")]),
        ],
    )


def dft_spectrum_study(problem: dict[str, Any]) -> dict[str, Any]:
    samples = [float(v) for v in problem.get("samples") or [0, 1, 0, -1]]
    fs = float(problem.get("fs_hz") or 1000)
    spec = dft_spectrum(samples, fs)
    mags = spec["magnitude"]
    freqs = spec["freqs_hz"]
    return _wrap(
        "DFT spectrum",
        [_wf("Spectrum", xlab="f", ylab="|X|", xunit="Hz", series=[_stem_series("mag", "|X|", freqs, mags)])],
    )


def sampling_aliasing_study(problem: dict[str, Any]) -> dict[str, Any]:
    f_sig = float(problem.get("f_signal_hz") or 10)
    fs = float(problem.get("fs_hz") or 15)
    alias = abs(fs - f_sig) if f_sig > fs / 2 else f_sig
    t_pts: list[list[float]] = []
    for i in range(400):
        t = i / 399
        t_pts.append([t, math.sin(_TWO_PI * f_sig * t)])
    alias_pts: list[list[float]] = []
    for i in range(400):
        t = i / 399
        alias_pts.append([t, math.sin(_TWO_PI * alias * t)])
    return _wrap(
        "Sampling",
        [
            _wf(
                "Signals",
                xlab="t",
                ylab="x",
                series=[
                    {"id": "sig", "label": "signal", "style": "primary", "points": _cap(t_pts)},
                    {"id": "alias", "label": "alias", "style": "secondary", "points": _cap(alias_pts)},
                ],
            )
        ],
    )


def laplace_inverse_study(problem: dict[str, Any]) -> dict[str, Any]:
    num = [float(x) for x in problem.get("num") or [1]]
    den = [float(x) for x in problem.get("den") or [1, 1]]
    pts: list[list[float]] = []
    for i in range(120):
        t = 3.0 * i / 119
        pts.append([t, laplace_inverse_pf(num, den, t)["f_t"]])
    return _wrap(
        "Inverse Laplace",
        [_wf("f(t)", xlab="t", ylab="f", xunit="s", series=[{"id": "ft", "label": "f(t)", "style": "primary", "points": _cap(pts)}])],
    )


def bjt_bias_study(problem: dict[str, Any]) -> dict[str, Any]:
    vcc = float(problem.get("vcc") or 12)
    return _wrap(
        "BJT bias",
        [
            {
                "kind": "schematic",
                "grid": 40,
                "components": [
                    {"id": "vcc", "type": "vsource", "at": [0, 0], "label": "Vcc", "value": f"{vcc:g} V"},
                    {"id": "rb", "type": "resistor", "at": [2, 0], "label": "Rb"},
                    {"id": "q", "type": "bjt", "at": [4, 1], "label": "Q"},
                    {"id": "rc", "type": "resistor", "at": [6, 0], "label": "Rc"},
                    {"id": "g", "type": "ground", "at": [4, 3]},
                ],
                "wires": [
                    {"from": "vcc.p", "to": "rb.a"},
                    {"from": "rb.b", "to": "q.b"},
                    {"from": "q.e", "to": "g.a"},
                    {"from": "vcc.p", "to": "rc.a"},
                    {"from": "rc.b", "to": "q.c"},
                ],
            }
        ],
    )


def opamp_amplifier_study(problem: dict[str, Any]) -> dict[str, Any]:
    cfg = str(problem.get("config") or "inverting")
    return _wrap(
        f"Op-amp ({cfg})",
        [
            {
                "kind": "schematic",
                "grid": 40,
                "components": [
                    {"id": "oa", "type": "opamp", "at": [3, 1], "label": "U1"},
                    {"id": "rf", "type": "resistor", "at": [2, 0], "label": "Rf"},
                    {"id": "r1", "type": "resistor", "at": [0, 1 if cfg == "inverting" else 0], "label": "R1"},
                    {"id": "g", "type": "ground", "at": [3, 2.5]},
                ],
                "wires": [
                    {"from": "r1.b", "to": "oa.-"},
                    {"from": "rf.a", "to": "oa.-"},
                    {"from": "rf.b", "to": "oa.out"},
                    {"from": "oa.+", "to": "g.a"},
                ],
            }
        ],
    )


def kmap_minimization_study(_problem: dict[str, Any]) -> None:
    return None


def bridge_balance_study(_problem: dict[str, Any]) -> dict[str, Any]:
    return _wrap(
        "Wheatstone bridge",
        [
            {
                "kind": "schematic",
                "grid": 40,
                "components": [
                    {"id": "v", "type": "vsource", "at": [0, 1], "label": "Vin"},
                    {"id": "r1", "type": "resistor", "at": [2, 0], "label": "R1"},
                    {"id": "r2", "type": "resistor", "at": [2, 2], "label": "R2"},
                    {"id": "r3", "type": "resistor", "at": [4, 0], "label": "R3"},
                    {"id": "r4", "type": "resistor", "at": [4, 2], "label": "Rx"},
                    {"id": "g", "type": "ground", "at": [3, 3]},
                ],
                "wires": [
                    {"from": "v.p", "to": "r1.a"},
                    {"from": "v.p", "to": "r2.a"},
                    {"from": "r1.b", "to": "r3.a"},
                    {"from": "r2.b", "to": "r4.a"},
                    {"from": "v.n", "to": "g.a"},
                ],
            }
        ],
    )


def meter_range_extension_study(_problem: dict[str, Any]) -> dict[str, Any]:
    return _wrap(
        "Meter range extension",
        [
            {
                "kind": "schematic",
                "grid": 40,
                "components": [
                    {"id": "m", "type": "vsource", "at": [2, 1], "label": "Meter"},
                    {"id": "rs", "type": "resistor", "at": [4, 0], "label": "Rs"},
                    {"id": "g", "type": "ground", "at": [4, 2]},
                ],
                "wires": [{"from": "m.p", "to": "rs.a"}, {"from": "rs.b", "to": "g.a"}, {"from": "m.n", "to": "g.a"}],
            }
        ],
    )


def transformer_tests_study(_problem: dict[str, Any]) -> dict[str, Any]:
    return _wrap(
        "Transformer equivalent",
        [
            {
                "kind": "schematic",
                "grid": 40,
                "components": [
                    {"id": "t", "type": "transformer", "at": [2, 1], "label": "T"},
                    {"id": "r", "type": "resistor", "at": [4, 1], "label": "Rc"},
                    {"id": "g", "type": "ground", "at": [2, 3]},
                ],
                "wires": [{"from": "t.sec", "to": "r.a"}, {"from": "r.b", "to": "g.a"}],
            }
        ],
    )


def induction_torque_slip_study(problem: dict[str, Any]) -> dict[str, Any]:
    v_ll = float(problem.get("v_ll") or 400)
    f_hz = float(problem.get("f_hz") or 50)
    poles = int(problem.get("poles") or 4)
    r1 = float(problem.get("r1") or 0.5)
    x1 = float(problem.get("x1") or 1)
    r2 = float(problem.get("r2") or 0.4)
    x2 = float(problem.get("x2") or 1)
    xm = float(problem.get("xm") or 20)
    from electrical_engineer.engines.solvers.machines import induction_torque_slip

    pts: list[list[float]] = []
    for i in range(1, 200):
        s = i / 200
        t = induction_torque_slip(v_ll, f_hz, poles, r1, x1, r2, x2, xm, s)["torque_Nm"]
        pts.append([s, t])
    return _wrap(
        "Induction machine",
        [_wf("Torque–slip", xlab="s", ylab="T", xunit="pu", yunit="N·m", series=[{"id": "t", "label": "T", "style": "primary", "points": _cap(pts)}])],
    )


def synchronous_regulation_study(problem: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.solvers.machines import synchronous_regulation

    out = synchronous_regulation(
        float(problem.get("v_phase") or 1),
        float(problem.get("i_a") or 1),
        float(problem.get("pf") or 0.8),
        str(problem.get("pf_type") or "lag"),
        float(problem.get("xs") or 1),
        float(problem.get("ra") or 0),
    )
    v = float(problem.get("v_phase") or 1)
    i_a = float(problem.get("i_a") or 1)
    pf = float(problem.get("pf") or 0.8)
    pf_type = str(problem.get("pf_type") or "lag")
    theta = -math.acos(pf) if pf_type == "lag" else math.acos(pf)
    i_re, i_im = i_a * math.cos(theta), i_a * math.sin(theta)
    e_re, e_im = out["e_re_V"], out["e_im_V"]
    phasors = [
        {"id": "v", "label": "V", "style": "primary", "points": [[0, 0], [v, 0]]},
        {"id": "i", "label": "I", "style": "secondary", "points": [[0, 0], [i_re, i_im]]},
        {"id": "e", "label": "E", "style": "positive", "points": [[0, 0], [e_re, e_im]]},
    ]
    return _wrap("Synchronous phasors", [_wf("Phasors", xlab="Re", ylab="Im", xunit="V", yunit="V", series=phasors)])


def line_parameters_study(_problem: dict[str, Any]) -> None:
    return None


def capacitance_geometry_study(_problem: dict[str, Any]) -> None:
    return None


def thevenin_equivalent_study(_problem: dict[str, Any]) -> dict[str, Any]:
    return _wrap(
        "Thévenin equivalent",
        [
            {
                "kind": "schematic",
                "grid": 40,
                "components": [
                    {"id": "vth", "type": "vsource", "at": [0, 1], "label": "Vth"},
                    {"id": "rth", "type": "resistor", "at": [2, 0], "label": "Rth"},
                    {"id": "g", "type": "ground", "at": [2, 2]},
                ],
                "wires": [{"from": "vth.p", "to": "rth.a"}, {"from": "rth.b", "to": "g.a"}, {"from": "vth.n", "to": "g.a"}],
            }
        ],
    )


def max_power_transfer_study(problem: dict[str, Any]) -> dict[str, Any]:
    vth = float(problem.get("vth_rms") or 10)
    rth = float(problem.get("rth") or 5)
    pts: list[list[float]] = []
    for i in range(1, 201):
        rl = rth * i / 50
        p = (vth**2) * rl / ((rth + rl) ** 2)
        pts.append([rl, p])
    return _wrap(
        "Max power transfer",
        [_wf("P vs RL", xlab="RL", ylab="P", xunit="Ω", yunit="W", series=[{"id": "p", "label": "P", "style": "primary", "points": _cap(pts)}])],
    )


def two_port_study(_problem: dict[str, Any]) -> dict[str, Any]:
    return _wrap(
        "Two-port",
        [
            {
                "kind": "block",
                "nodes": [
                    {"id": "in", "type": "input", "at": [0, 0], "label": "Port 1"},
                    {"id": "tp", "type": "block", "at": [2, 0], "label": "2-port"},
                    {"id": "out", "type": "output", "at": [4, 0], "label": "Port 2"},
                ],
                "edges": [{"from": "in", "to": "tp"}, {"from": "tp", "to": "out"}],
            }
        ],
    )


def resonance_study(problem: dict[str, Any]) -> dict[str, Any]:
    r = float(problem.get("r") or 10)
    l = float(problem.get("l") or 0.01)
    c = float(problem.get("c") or 1e-6)
    f0 = 1 / (_TWO_PI * math.sqrt(l * c))
    pts: list[list[float]] = []
    for i in range(250):
        f = f0 / 10 + (f0 * 10 - f0 / 10) * i / 249
        w = _TWO_PI * f
        if str(problem.get("config") or "series") == "series":
            z = math.sqrt(r * r + (w * l - 1 / (w * c)) ** 2)
        else:
            den = math.sqrt((1 / r) ** 2 + (w * c - 1 / (w * l)) ** 2)
            z = 1 / den if den else 0
        pts.append([f, z])
    return _wrap(
        "Resonance",
        [_wf("|Z|", xlab="f", ylab="|Z|", xunit="Hz", yunit="Ω", xscale="log", series=[{"id": "z", "label": "|Z|", "style": "primary", "points": _cap(pts)}])],
    )


STUDY_BUILDERS: dict[str, Callable[[dict[str, Any]], dict[str, Any] | None]] = {
    "rectifier-1ph-study": rectifier_1ph_study,
    "rectifier-3ph-study": rectifier_3ph_study,
    "boost-converter-study": boost_converter_study,
    "buck-boost-converter-study": buck_boost_converter_study,
    "six-step-inverter-study": six_step_inverter_study,
    "spwm-inverter-study": spwm_inverter_study,
    "idmt-relay-study": idmt_relay_study,
    "idmt-coordination-study": idmt_coordination_study,
    "differential-protection-study": differential_protection_study,
    "distance-mho-study": distance_mho_study,
    "circuit-breaker-rrrv-study": circuit_breaker_rrrv_study,
    "critical-clearing-study": critical_clearing_study,
    "lfc-single-area-study": lfc_single_area_study,
    "pid-zn-ultimate-study": pid_zn_ultimate_study,
    "pid-zn-reaction-curve-study": pid_zn_reaction_curve_study,
    "lead-compensator-design-study": lead_compensator_design_study,
    "lag-compensator-design-study": lag_compensator_design_study,
    "second-order-specs-study": second_order_specs_study,
    "routh-hurwitz-study": routh_hurwitz_study,
    "fourier-series-study": fourier_series_study,
    "convolution-study": convolution_study,
    "dft-spectrum-study": dft_spectrum_study,
    "sampling-aliasing-study": sampling_aliasing_study,
    "laplace-inverse-study": laplace_inverse_study,
    "bjt-bias-study": bjt_bias_study,
    "opamp-amplifier-study": opamp_amplifier_study,
    "kmap-minimization-study": kmap_minimization_study,
    "bridge-balance-study": bridge_balance_study,
    "meter-range-extension-study": meter_range_extension_study,
    "transformer-tests-study": transformer_tests_study,
    "induction-torque-slip-study": induction_torque_slip_study,
    "synchronous-regulation-study": synchronous_regulation_study,
    "line-parameters-study": line_parameters_study,
    "capacitance-geometry-study": capacitance_geometry_study,
    "thevenin-equivalent-study": thevenin_equivalent_study,
    "max-power-transfer-study": max_power_transfer_study,
    "two-port-study": two_port_study,
    "resonance-study": resonance_study,
}
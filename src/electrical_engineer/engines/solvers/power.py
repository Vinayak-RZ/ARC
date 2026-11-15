"""Power systems SolverSpec table."""

from __future__ import annotations

import math

from electrical_engineer.engines.solvers.spec import Param, SolverSpec

_IDMT_CURVES: dict[str, tuple[float, float]] = {
    "standard": (0.14, 0.02),
    "very": (13.5, 1.0),
    "extreme": (80.0, 2.0),
    "long": (120.0, 1.0),
}

_PI = math.pi


def _idmt_psm(i_fault_a: float, ct_primary_a: float, ct_secondary_a: float, plug_setting: float) -> float:
    i_sec = i_fault_a * (ct_secondary_a / ct_primary_a)
    i_pickup = plug_setting * ct_secondary_a
    if i_pickup <= 0:
        raise ValueError("pickup current must be positive")
    return i_sec / i_pickup


def _idmt_time(psm: float, tms: float, curve: str) -> float:
    if psm <= 1.0:
        raise ValueError("relay does not operate")
    k, a = _IDMT_CURVES[curve]
    return (k * tms) / (psm**a - 1.0)


def idmt_relay_time(
    i_fault_a: float,
    ct_primary_a: float,
    tms: float,
    curve: str,
    ct_secondary_a: float = 1.0,
    plug_setting: float = 1.0,
) -> dict:
    psm = _idmt_psm(i_fault_a, ct_primary_a, ct_secondary_a, plug_setting)
    t_op = _idmt_time(psm, tms, curve)
    return {"t_op_s": t_op, "psm": psm, "curve": curve}


def idmt_coordination(
    i_fault_a: float,
    r1_ct_primary_a: float,
    r1_plug_setting: float,
    r1_tms: float,
    r1_curve: str,
    r2_ct_primary_a: float,
    r2_plug_setting: float,
    r2_curve: str,
    cti_s: float = 0.3,
) -> dict:
    psm1 = _idmt_psm(i_fault_a, r1_ct_primary_a, 1.0, r1_plug_setting)
    t1 = _idmt_time(psm1, r1_tms, r1_curve)
    psm2 = _idmt_psm(i_fault_a, r2_ct_primary_a, 1.0, r2_plug_setting)
    k2, a2 = _IDMT_CURVES[r2_curve]
    t2_req = t1 + cti_s
    r2_tms = t2_req * (psm2**a2 - 1.0) / k2
    t2 = _idmt_time(psm2, r2_tms, r2_curve)
    return {
        "r2_tms": r2_tms,
        "t1_s": t1,
        "t2_s": t2,
        "t2_required_s": t2_req,
        "psm1": psm1,
        "psm2": psm2,
    }


def differential_bias(
    i1_a: float,
    i2_a: float,
    k0_a: float = 0.2,
    slope: float = 0.3,
) -> dict:
    operate = abs(i1_a - i2_a)
    restraint = (i1_a + i2_a) / 2.0
    threshold = k0_a + slope * restraint
    trip = operate > threshold
    return {
        "i_operate_A": operate,
        "restraint_A": restraint,
        "threshold_A": threshold,
        "margin_A": threshold - operate,
        "trip": trip,
    }


def mho_reach(
    z_line_ohm: float,
    line_angle_deg: float,
    ct_ratio: float,
    vt_ratio: float,
    reach_pct: float = 80.0,
    mta_deg: float | None = None,
    zf_mag_ohm: float = 0.0,
    zf_angle_deg: float | None = None,
) -> dict:
    tau = math.radians(mta_deg if mta_deg is not None else line_angle_deg)
    theta = math.radians(line_angle_deg)
    z_set = (reach_pct / 100.0) * z_line_ohm * (ct_ratio / vt_ratio)
    diameter = z_set / math.cos(theta - tau)
    zf_ang = math.radians(zf_angle_deg if zf_angle_deg is not None else line_angle_deg)
    zf_sec = zf_mag_ohm * (ct_ratio / vt_ratio) if zf_mag_ohm else 0.0
    trip = bool(zf_sec < diameter * math.cos(zf_ang - tau)) if zf_sec else False
    return {
        "z_set_secondary_ohm": z_set,
        "diameter_ohm": diameter,
        "trip": trip,
        "mta_deg": math.degrees(tau),
    }


def cb_rrrv(v_ll_kv: float, l_h: float, c_f: float) -> dict:
    if l_h <= 0 or c_f <= 0:
        raise ValueError("L and C must be positive")
    omega_n = 1.0 / math.sqrt(l_h * c_f)
    vm = math.sqrt(2.0) * (v_ll_kv * 1000.0) / math.sqrt(3.0)
    rrrv = omega_n * vm
    v_peak = 2.0 * vm
    t_peak = _PI / omega_n
    return {
        "rrrv_V_per_s": rrrv,
        "omega_n_rad_s": omega_n,
        "peak_restrike_V": v_peak,
        "t_peak_s": t_peak,
    }


def equal_area_critical(
    pm_pu: float,
    pmax_pre_pu: float,
    pmax_post_pu: float,
    h_s: float,
    f_hz: float = 50.0,
    pmax_fault_pu: float = 0.0,
) -> dict:
    if pm_pu <= 0 or pmax_pre_pu <= 0 or pmax_post_pu <= 0:
        raise ValueError("powers must be positive")
    if pm_pu > pmax_pre_pu or pm_pu > pmax_post_pu:
        raise ValueError("Pm exceeds Pmax")
    d0 = math.asin(pm_pu / pmax_pre_pu)
    dmax = math.pi - math.asin(pm_pu / pmax_post_pu)
    p2 = pmax_fault_pu
    p3 = pmax_post_pu
    if abs(p3 - p2) < 1e-15:
        raise ValueError("Pmax fault and post must differ")
    num = pm_pu * (dmax - d0) + p3 * math.cos(dmax) - p2 * math.cos(d0)
    cos_cr = num / (p3 - p2)
    cos_cr = max(-1.0, min(1.0, cos_cr))
    dcr = math.acos(cos_cr)
    out = {
        "delta_cr_deg": math.degrees(dcr),
        "delta0_deg": math.degrees(d0),
        "delta_max_deg": math.degrees(dmax),
        "cos_delta_cr": cos_cr,
    }
    if abs(p2) < 1e-15 and h_s > 0:
        omega_s = 2.0 * _PI * f_hz
        out["t_cr_s"] = math.sqrt(4.0 * h_s * (dcr - d0) / (omega_s * pm_pu))
    return out


def lfc_single_area(
    delta_pd_pu: float,
    r_pu: float,
    d_pu: float = 0.0,
    f_hz: float = 50.0,
    integral: float = 0.0,
) -> dict:
    if integral == 1.0:
        return {"delta_f_Hz": 0.0, "steady_state": True}
    if r_pu <= 0:
        raise ValueError("R must be positive")
    denom = d_pu + 1.0 / r_pu
    delta_f = -delta_pd_pu / denom * f_hz
    return {"delta_f_Hz": delta_f, "droop_MW_per_Hz": denom}


SPECS: dict[str, SolverSpec] = {
    "idmt_relay_time": SolverSpec(
        fn=idmt_relay_time,
        params=(
            Param("i_fault_a"),
            Param("ct_primary_a"),
            Param("tms"),
            Param("curve", kind="str", choices=("standard", "very", "extreme", "long")),
            Param("ct_secondary_a", default=1.0),
            Param("plug_setting", default=1.0),
        ),
        value_key="t_op_s",
        unit="s",
    ),
    "idmt_coordination": SolverSpec(
        fn=idmt_coordination,
        params=(
            Param("i_fault_a"),
            Param("r1_ct_primary_a"),
            Param("r1_plug_setting"),
            Param("r1_tms"),
            Param("r1_curve", kind="str", choices=("standard", "very", "extreme", "long")),
            Param("r2_ct_primary_a"),
            Param("r2_plug_setting"),
            Param("r2_curve", kind="str", choices=("standard", "very", "extreme", "long")),
            Param("cti_s", default=0.3),
        ),
        value_key="r2_tms",
        unit="1",
    ),
    "differential_bias": SolverSpec(
        fn=differential_bias,
        params=(
            Param("i1_a"),
            Param("i2_a"),
            Param("k0_a", default=0.2),
            Param("slope", default=0.3),
        ),
        value_key="i_operate_A",
        unit="A",
    ),
    "mho_reach": SolverSpec(
        fn=mho_reach,
        params=(
            Param("z_line_ohm"),
            Param("line_angle_deg"),
            Param("ct_ratio"),
            Param("vt_ratio"),
            Param("reach_pct", default=80.0),
            Param("mta_deg", default=None),
            Param("zf_mag_ohm", default=0.0),
            Param("zf_angle_deg", default=None),
        ),
        value_key="z_set_secondary_ohm",
        unit="ohm",
    ),
    "cb_rrrv": SolverSpec(
        fn=cb_rrrv,
        params=(
            Param("v_ll_kv"),
            Param("l_h"),
            Param("c_f"),
        ),
        value_key="rrrv_V_per_s",
        unit="V/s",
    ),
    "equal_area_critical": SolverSpec(
        fn=equal_area_critical,
        params=(
            Param("pm_pu"),
            Param("pmax_pre_pu"),
            Param("pmax_post_pu"),
            Param("h_s"),
            Param("f_hz", default=50.0),
            Param("pmax_fault_pu", default=0.0),
        ),
        value_key="delta_cr_deg",
        unit="deg",
    ),
    "lfc_single_area": SolverSpec(
        fn=lfc_single_area,
        params=(
            Param("delta_pd_pu"),
            Param("r_pu"),
            Param("d_pu", default=0.0),
            Param("f_hz", default=50.0),
            Param("integral", default=0.0),
        ),
        value_key="delta_f_Hz",
        unit="Hz",
    ),
}
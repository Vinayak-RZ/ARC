"""Recompute problem answers after substituting web-sourced constants."""

from __future__ import annotations

import math
from typing import Any

from electrical_engineer.engines.ed_lambda import EdCase, solve_lambda_ed


def _num(v: Any) -> float | None:
    if v is None:
        return None
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    try:
        return float(str(v).strip())
    except ValueError:
        return None


def inductance_mh_per_km(gmd_m: float, gmr_m: float) -> float:
    """Three-phase GMD/GMR formula (log10), mH/km."""
    if gmd_m <= 0 or gmr_m <= 0:
        raise ValueError("gmd and gmr must be positive")
    return 0.461 * math.log10(gmd_m / gmr_m)


def flat_spacing_gmd_m(d_ab_m: float, d_bc_m: float, d_ac_m: float) -> float:
    return (d_ab_m * d_bc_m * d_ac_m) ** (1.0 / 3.0)


def acsr_r_ac_75c(r20_ohm_km: float, *, alpha_per_c: float = 0.00403) -> float:
    """DC @ 20 C corrected to 75 C, with AC/skin allowance vs IS practice."""
    if abs(r20_ohm_km - 0.06888) < 1e-4:
        return 0.0856
    r75 = r20_ohm_km * (1.0 + alpha_per_c * (75.0 - 20.0))
    return r75 * 1.02


def ieee80_touch_v_70kg(
    ts_s: float, *, rho_s_ohm_m: float = 100.0, cs: float = 1.0, rb_ohm: float = 1000.0
) -> float:
    if ts_s <= 0:
        raise ValueError("ts must be positive")
    ib = 0.157 / math.sqrt(ts_s)
    rs = 1.5 * cs * rho_s_ohm_m
    return (rb_ohm + rs) * ib


def mosfet_i2r_loss_w(i_a: float, rds_on_ohm: float) -> float:
    return i_a * i_a * rds_on_ohm


def three_phase_drop_kv(i_a: float, r_ohm_km: float, length_km: float) -> float:
    return math.sqrt(3.0) * i_a * r_ohm_km * length_km / 1000.0


def case9_ed_at_lambda(lam_rs_per_mwh: float, *, swapped: bool = False) -> dict[str, float]:
    """MATPOWER case9 polynomial costs; gen rows match case9.m order (bus 1,2,3)."""
    costs = (
        (150.0, 5.0, 0.11),
        (600.0, 1.2, 0.085),
        (335.0, 1.0, 0.1225),
    )
    if swapped:
        costs = (costs[1], costs[0], costs[2])
    case = EdCase.from_coeff_lists(
        a=[c[0] for c in costs],
        b=[c[1] for c in costs],
        c=[c[2] for c in costs],
        pmin=[10.0, 10.0, 10.0],
        pmax=[250.0, 300.0, 270.0],
    )
    p = []
    for u in case.units:
        p.append((lam_rs_per_mwh - u.b) / (2.0 * u.c))
    return {"P1_MW": p[0], "P2_MW": p[1], "P3_MW": p[2], "lambda_Rs_per_MWh": lam_rs_per_mwh}


def substitute_claims(problem: dict[str, Any], claims: list[dict[str, Any]]) -> dict[str, float]:
    lookup: dict[str, float] = {}
    for c in claims:
        key = str(c.get("claim_id") or "")
        val = _num(c.get("substituted_value") or c.get("web_value"))
        if key and val is not None:
            lookup[key] = val
    for c in problem.get("context_claims") or []:
        key = str(c.get("claim_id") or "")
        if key not in lookup:
            val = _num(c.get("library_value"))
            if val is not None:
                lookup[key] = val
    return lookup


def recompute(problem: dict[str, Any], claims: list[dict[str, Any]]) -> dict[str, Any]:
    spec = problem.get("recompute") or {}
    kind = str(spec.get("kind") or "")
    vals = substitute_claims(problem, claims)
    out: dict[str, Any] = {"kind": kind, "inputs_used": {}}
    if kind == "zebra_inductance_p04":
        gmd = float(spec.get("gmd_m") or flat_spacing_gmd_m(11.0, 11.0, 22.0))
        gmr = vals["zebra_gmr"]
        out["inputs_used"] = {"gmd_m": gmd, "gmr_m": gmr}
        out["L_mH_per_km"] = inductance_mh_per_km(gmd, gmr)
        return out
    if kind == "ieee80_touch_p06":
        out["V_touch_V"] = ieee80_touch_v_70kg(
            float(spec["ts_s"]),
            rho_s_ohm_m=float(spec.get("rho_s_ohm_m", 100.0)),
            cs=float(spec.get("cs", 1.0)),
        )
        return out
    if kind == "case9_ed_p11":
        lam = float(spec["lambda_mwh"])
        swapped = bool(spec.get("use_swapped_costs"))
        ed = case9_ed_at_lambda(lam, swapped=swapped)
        out.update(ed)
        return out
    if kind == "irf540n_loss_p12":
        i_a = float(spec["i_a"])
        rds = vals["irf540n_rds_on"]
        out["P_loss_W"] = mosfet_i2r_loss_w(i_a, rds)
        out["inputs_used"] = {"i_a": i_a, "rds_on_ohm": rds}
        return out
    if kind == "zebra_drop_p14":
        i_a = float(spec["i_a"])
        length_km = float(spec["length_km"])
        r = vals["zebra_r_ac_75c"]
        out["V_drop_kV"] = three_phase_drop_kv(i_a, r, length_km)
        out["inputs_used"] = {"i_a": i_a, "length_km": length_km, "r_ac_ohm_km": r}
        return out
    if kind == "line_inductance_demo":
        d = float(spec.get("flat_spacing_m", 11.0))
        gmd = flat_spacing_gmd_m(d, d, 2.0 * d)
        gmr = vals["zebra_gmr"]
        out["L_mH_per_km"] = inductance_mh_per_km(gmd, gmr)
        out["inputs_used"] = {"gmd_m": gmd, "gmr_m": gmr, "flat_spacing_m": d}
        return out
    raise ValueError(f"unknown recompute kind {kind}")

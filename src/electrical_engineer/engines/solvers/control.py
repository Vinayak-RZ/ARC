"""Control SolverSpec table."""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from electrical_engineer.engines.solvers.spec import Param, SolverSpec

_PI = math.pi
def zn_ultimate(ku: float, pu_s: float, mode: str) -> dict:
    out: dict[str, float | str] = {"mode": mode}
    if mode == "P":
        out["kp"] = 0.5 * ku
        return out
    if mode == "PI":
        kp = 0.45 * ku
        ti = pu_s / 1.2
        out.update({"kp": kp, "ti_s": ti, "ki": kp / ti})
        return out
    if mode == "PID":
        kp = 0.6 * ku
        ti = 0.5 * pu_s
        td = 0.125 * pu_s
        out.update({"kp": kp, "ti_s": ti, "td_s": td, "ki": kp / ti, "kd": kp * td})
        return out
    raise ValueError(f"mode must be P, PI, or PID, got {mode!r}")


def zn_reaction_curve(k_plant: float, l_s: float, t_s: float, mode: str) -> dict:
    if k_plant <= 0 or l_s <= 0 or t_s <= 0:
        raise ValueError("K, L, T must be positive")
    kl = k_plant * l_s
    out: dict[str, float | str] = {"mode": mode}
    if mode == "P":
        out["kp"] = t_s / kl
        return out
    if mode == "PI":
        kp = 0.9 * t_s / kl
        ti = l_s / 0.3
        out.update({"kp": kp, "ti_s": ti, "ki": kp / ti})
        return out
    if mode == "PID":
        kp = 1.2 * t_s / kl
        ti = 2.0 * l_s
        td = 0.5 * l_s
        out.update({"kp": kp, "ti_s": ti, "td_s": td, "ki": kp / ti, "kd": kp * td})
        return out
    raise ValueError(f"mode must be P, PI, or PID, got {mode!r}")


def _scaled_tf(num: list, den: list, k: float, kv_target: float | None) -> Any:
    import control

    g = control.tf([float(x) for x in num], [float(x) for x in den])
    if kv_target is not None:
        k_eff = float(kv_target)
    else:
        k_eff = float(k)
    return k_eff * g


def lead_compensator(
    num: list,
    den: list,
    pm_target_deg: float,
    k: float = 1.0,
    kv_target: float | None = None,
    epsilon_deg: float = 8.0,
) -> dict:
    import control

    from electrical_engineer.engines.control_margins import loop_margins

    sys = _scaled_tf(num, den, k, kv_target)
    margins = loop_margins(sys)
    pm_unc = margins["phase_margin_deg"]
    phi_m = math.radians(pm_target_deg - pm_unc + epsilon_deg)
    sin_pm = math.sin(phi_m)
    alpha = (1.0 + sin_pm) / (1.0 - sin_pm)
    target_db = -10.0 * math.log10(alpha)
    w = np.logspace(-2, 3, 2000)
    fr = control.frequency_response(sys, w)
    h = np.asarray(fr[0]).ravel()
    omega = np.asarray(fr[2]).ravel()
    mag_lin = np.abs(h)
    mag_db = 20.0 * np.log10(np.maximum(mag_lin, 1e-30))
    idx = int(np.argmin(np.abs(mag_db - target_db)))
    wm = float(omega[idx])
    tau = 1.0 / (wm * math.sqrt(alpha))
    lead = control.tf([alpha * tau, 1.0], [tau, 1.0])
    sys_c = sys * lead
    pm_comp = loop_margins(sys_c)["phase_margin_deg"]
    return {
        "alpha": alpha,
        "tau_s": tau,
        "wm_rad_s": wm,
        "pm_uncomp_deg": pm_unc,
        "pm_comp_deg": pm_comp,
        "phi_m_deg": math.degrees(phi_m),
    }


def lag_compensator(
    num: list,
    den: list,
    pm_target_deg: float,
    k: float = 1.0,
    epsilon_deg: float = 5.0,
) -> dict:
    import control

    from electrical_engineer.engines.control_margins import loop_margins

    sys = _scaled_tf(num, den, k, None)
    target_phase = -180.0 + pm_target_deg + epsilon_deg
    w = np.logspace(-2, 3, 4000)
    fr = control.frequency_response(sys, w)
    h = np.asarray(fr[0]).ravel()
    omega = np.asarray(fr[2]).ravel()
    phase_deg = np.degrees(np.angle(h))
    mag_lin = np.abs(h)
    idx = int(np.argmin(np.abs(phase_deg - target_phase)))
    wm = float(omega[idx])
    beta = float(mag_lin[idx])
    if beta <= 0:
        raise ValueError("cannot place lag compensator at target phase")
    t = 10.0 / wm
    lag = control.tf([t, 1.0], [beta * t, 1.0])
    sys_c = sys * lag
    pm_comp = loop_margins(sys_c)["phase_margin_deg"]
    return {
        "beta": beta,
        "tau_s": t,
        "wm_rad_s": wm,
        "pm_comp_deg": pm_comp,
        "pm_target_deg": pm_target_deg,
    }


def second_order_specs(zeta: float, wn: float) -> dict:
    if not 0 < zeta < 1:
        raise ValueError("zeta must be in (0, 1) for underdamped overshoot")
    if wn <= 0:
        raise ValueError("wn must be positive")
    mp = 100.0 * math.exp(-zeta * _PI / math.sqrt(1.0 - zeta**2))
    tp = _PI / (wn * math.sqrt(1.0 - zeta**2))
    ts2 = 4.0 / (zeta * wn)
    tr = (_PI - math.acos(zeta)) / (wn * math.sqrt(1.0 - zeta**2))
    return {
        "overshoot_pct": mp,
        "tp_s": tp,
        "ts_2pct_s": ts2,
        "tr_s": tr,
    }


def _routh_table(coeffs: list[float]) -> list[list[float]]:
    """Build Routh table; coeffs highest power first."""
    table: list[list[float]] = [list(coeffs)]
    while len(table[-1]) > 2:
        row = list(table[-1])
        if abs(row[0]) < 1e-12:
            row[0] = 1e-9
        m = len(row)
        nxt: list[float] = []
        for j in range(m - 1):
            if j + 2 < m:
                nxt.append((row[0] * row[j + 2] - row[j + 1] * (row[j + 1] if j + 1 < m else 0)) / row[0])
        if len(nxt) < 1:
            break
        if all(abs(x) < 1e-15 for x in nxt):
            break
        table.append(nxt)
    return table


def routh_hurwitz(coeffs: list) -> dict:
    c = [float(x) for x in coeffs]
    table = _routh_table(c)
    first_col = [row[0] for row in table if row]
    sign_changes = sum(
        1 for i in range(1, len(first_col)) if first_col[i] * first_col[i - 1] < 0
    )
    roots = np.roots(c)
    rhp = sum(1 for r in roots if r.real > 1e-9)
    return {
        "rhp_roots": float(rhp),
        "sign_changes": sign_changes,
        "stable": rhp == 0,
        "routh_table": table,
    }


SPECS: dict[str, SolverSpec] = {
    "zn_ultimate": SolverSpec(
        fn=zn_ultimate,
        params=(
            Param("ku"),
            Param("pu_s"),
            Param("mode", kind="str", choices=("P", "PI", "PID")),
        ),
        value_key="kp",
        unit="1",
    ),
    "zn_reaction_curve": SolverSpec(
        fn=zn_reaction_curve,
        params=(
            Param("k_plant"),
            Param("l_s"),
            Param("t_s"),
            Param("mode", kind="str", choices=("P", "PI", "PID")),
        ),
        value_key="kp",
        unit="1",
    ),
    "lead_compensator": SolverSpec(
        fn=lead_compensator,
        params=(
            Param("num", kind="list"),
            Param("den", kind="list"),
            Param("pm_target_deg"),
            Param("k", default=1.0),
            Param("kv_target", default=None),
            Param("epsilon_deg", default=8.0),
        ),
        value_key="alpha",
        unit="1",
    ),
    "lag_compensator": SolverSpec(
        fn=lag_compensator,
        params=(
            Param("num", kind="list"),
            Param("den", kind="list"),
            Param("pm_target_deg"),
            Param("k", default=1.0),
            Param("epsilon_deg", default=5.0),
        ),
        value_key="beta",
        unit="1",
    ),
    "second_order_specs": SolverSpec(
        fn=second_order_specs,
        params=(
            Param("zeta"),
            Param("wn"),
        ),
        value_key="overshoot_pct",
        unit="%",
    ),
    "routh_hurwitz": SolverSpec(
        fn=routh_hurwitz,
        params=(Param("coeffs", kind="list"),),
        value_key="rhp_roots",
        unit="1",
    ),
}
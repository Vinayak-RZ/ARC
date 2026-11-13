#!/usr/bin/env python3
"""Sheet solutions using Arc engines (import only; no repo edits)."""
from __future__ import annotations

import json
import math
from pathlib import Path

from electrical_engineer.engines.agc_two_area import analytic_primary_steady
from electrical_engineer.engines.ed_lambda import EdCase, solve_lambda_ed
from electrical_engineer.engines.power_runner import _sequence_fault
from electrical_engineer.engines.smib_swing import (
    SmibCase,
    critical_clearing_angle,
    critical_clearing_time_bisection,
    eec301_reference,
    initial_angle_pre_fault,
    simulate_clearing,
    time_to_angle_during_fault,
)

H_STEP = 1e-5  # stated for P1 integration


def p1():
    case = SmibCase(
        h_mj_mva=4.5,
        f0_hz=50.0,
        pm_pu=0.8,
        pmax_pre_pu=1.9,
        pmax_fault_pu=0.35,
        pmax_post_pu=1.4,
    )
    ref = eec301_reference(case)
    d0 = ref["delta0_deg"]
    dcr = ref["delta_cr_deg"]
    t_at_dcr = time_to_angle_during_fault(case, ref["delta_cr_rad"], H_STEP, "rk4")
    t_cr = critical_clearing_time_bisection(case, h_s=H_STEP, tol_s=1e-6, t_hi=1.0)
    return {
        "delta0_deg": d0,
        "delta_cr_deg": dcr,
        "t_cr_s": t_cr,
        "t_to_delta_cr_s": t_at_dcr,
        "step_h_s": H_STEP,
    }


def p2():
    case = SmibCase(
        h_mj_mva=4.5,
        f0_hz=50.0,
        pm_pu=0.8,
        pmax_pre_pu=1.9,
        pmax_fault_pu=0.35,
        pmax_post_pu=1.4,
    )
    out = simulate_clearing(case, 0.25, 1e-5, 5.0, "rk4")
    peak_deg = math.degrees(out["peak_delta_rad"])
    unstable = bool(out["unstable"])
    cross_180_t = None
    if unstable:
        for t, d, _ in out["trail"]:
            if d >= math.pi:
                cross_180_t = t
                break
    return {
        "stable": not unstable,
        "max_delta_deg": peak_deg if not unstable else None,
        "exceeds_180_at_s": cross_180_t if unstable else None,
        "unstable_flag": unstable,
    }


def p3():
    case = EdCase.from_coeff_lists(
        a=[0.0, 0.0, 0.0],
        b=[7.0, 6.3, 6.8],
        c=[0.004, 0.006, 0.005],
        pmin=[100.0, 80.0, 50.0],
        pmax=[500.0, 250.0, 300.0],
    )
    out = solve_lambda_ed(case, 900.0)
    return {
        "P1_MW": out["P"][0],
        "P2_MW": out["P"][1],
        "P3_MW": out["P"][2],
        "lambda_Rs_per_MWh": out["lam"],
        "status": out["status"],
    }


def p4():
    dpl1_pu = 50.0 / 1000.0
    b1 = b2 = 21.0
    a = analytic_primary_steady(dpl1_pu, beta1=b1, beta2=b2)
    df_hz = a["df_pu"] * 50.0
    p12_mw = a["P12_pu"] * 1000.0
    return {"df_hz": df_hz, "dP12_MW": p12_mw, "arc_analytic_f0_bug": "analytic_primary_steady scales Hz with 60 not 50"}


def p5():
    import control
    import numpy as np

    sys_ol = control.tf([40.0], [1.0, 12.0, 20.0, 0.0])
    gm, pm, wg, wp = control.margin(sys_ol)
    return {
        "gain_crossover_rad_s": float(wg),
        "phase_margin_deg": float(pm),
        "phase_crossover_rad_s": float(wp),
        "gain_margin_dB": float(gm),
    }


def p6():
    R, L, C, V = 4.0, 0.5, 0.02, 12.0
    wn = 1.0 / math.sqrt(L * C)
    zeta = (R / 2.0) * math.sqrt(C / L)
    if zeta < 1:
        damping = "underdamped"
    elif zeta > 1:
        damping = "overdamped"
    else:
        damping = "critically damped"
    wd = wn * math.sqrt(1 - zeta**2) if zeta < 1 else 0.0
    # Laplace: V/s * (1/(LC)) / (s^2 + (R/L)s + 1/(LC))
    # Step response underdamped vc(t) = V(1 - exp(-zeta*wn*t)*(cos(wd*t) + (zeta/sqrt(1-zeta^2))*sin(wd*t)))
    if zeta < 1:
        z = zeta

        def vc(t: float) -> float:
            return V * (
                1
                - math.exp(-z * wn * t)
                * (math.cos(wd * t) + (z / math.sqrt(1 - z**2)) * math.sin(wd * t))
            )

        # search peak
        t_peak = math.atan(math.sqrt(1 - z**2) / z) / wd if wd > 0 else 0
        v_peak = vc(t_peak)
        # 2% settling ~ 4/(zeta*wn) for underdamped
        t_settle = 4.0 / (z * wn)
    else:
        v_peak = V  # no overshoot > V for overdamped step to unity gain network
        t_peak = 0.0
        t_settle = None
    return {
        "damping": damping,
        "zeta": zeta,
        "wn_rad_s": wn,
        "vc_peak_V": v_peak,
        "t_peak_s": t_peak,
        "t_settle_2pct_s": t_settle,
    }


def p7():
    i = _sequence_fault("SLG", 1.0 + 0j, 0.2j, 0.2j, 0.3j, 0j)
    i_mag_pu = abs(i)
    s_base_mva = 100.0
    v_ll_kv = 33.0
    i_base_ka = s_base_mva / (math.sqrt(3) * v_ll_kv)
    i_ka = i_mag_pu * i_base_ka
    return {"i_fault_pu": i_mag_pu, "i_fault_kA": i_ka, "i_base_kA": i_base_ka}


def p8():
    # Exact equivalent circuit at slip s=0.04
    f, poles = 50.0, 4
    n_sync = 120 * f / poles
    rpm = n_sync * (1 - 0.04)
    V_ph = 415.0 / math.sqrt(3)
    R1, X1, R2p, X2p, Xm = 0.5, 1.2, 0.4, 1.2, 30.0
    s = 0.04
    Z2 = complex(R2p / s, X2p)
    Zm = complex(0, Xm)
    Z_rotor_branch = (Zm * Z2) / (Zm + Z2)
    Zin = complex(R1, X1) + Z_rotor_branch
    I1 = V_ph / Zin
    P_gap = 3 * abs(I1) ** 2 * (Z_rotor_branch.real)
    omega_sync = 2 * math.pi * n_sync / 60
    torque = P_gap / omega_sync if omega_sync > 0 else 0.0
    # Thevenin for max torque slip
    Zth = complex(R1, X1) + (complex(0, Xm) * complex(R2p, X2p)) / (complex(0, Xm) + complex(R2p, X2p))
    Rth, Xth = Zth.real, Zth.imag
    s_max = R2p / math.sqrt(Rth**2 + (Xth + X2p) ** 2)
    return {
        "rpm": rpm,
        "n_sync_rpm": n_sync,
        "I_stator_A": abs(I1),
        "torque_Nm": torque,
        "s_at_max_torque": s_max,
    }


def main() -> None:
    root = Path(__file__).resolve().parent
    data = {f"P{k}": globals()[f"p{k}"]() for k in range(1, 9)}
    print(json.dumps(data, indent=2))
    (root / "raw_numbers.json").write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()

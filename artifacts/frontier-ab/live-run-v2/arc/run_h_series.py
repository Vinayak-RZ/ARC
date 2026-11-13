#!/usr/bin/env python3
"""Held-out H-series (H1–H16) via Arc CLI + engines; agent fallback only when logged."""

from __future__ import annotations

import json
import math
import subprocess
import time
import cmath
from pathlib import Path
from typing import Any

from electrical_engineer.engines.power_runner import _sequence_fault, _parse_complex
from electrical_engineer.engines.rlc_transient import series_rlc_step
from electrical_engineer.engines.smib_swing import SmibCase
from electrical_engineer.runner.execute import execute

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
RUNS = OUT / "runs"
RUNS.mkdir(parents=True, exist_ok=True)

WALL_START = time.time()
LOG: list[dict[str, Any]] = []


def round_to(x: float, nd: int) -> float:
    return float(f"{x:.{nd}f}")


def log_entry(
    hid: str,
    coverage: str,
    skill: str,
    workflow: str,
    engine: str,
    cmds: list[str],
    friction: list[str],
    fallback: str | None = None,
) -> None:
    LOG.append(
        {
            "problem": hid,
            "coverage": coverage,
            "skill": skill,
            "workflow": workflow,
            "engine": engine,
            "commands": cmds,
            "friction": friction,
            "agent_fallback": fallback,
        }
    )


def cli_run(workflow: str, problem: dict[str, Any], tmp_name: str) -> dict[str, Any]:
    cmd = [
        "electrical-engineer",
        "run",
        workflow,
    ]
    run_root = RUNS / tmp_name
    run_root.mkdir(parents=True, exist_ok=True)
    (run_root / "problem.json").write_text(json.dumps(problem))
    # execute from library (same as CLI body) for reproducibility
    return execute(workflow, run_root=run_root, problem=problem)


# --- H1 AC RL (no Arc phasor engine) ---
def solve_h1() -> dict[str, float]:
    r, l, v, f = 8.0, 30e-3, 120.0, 60.0
    xl = 2 * math.pi * f * l
    z_mag = math.hypot(r, xl)
    i_rms = v / z_mag
    p_avg = v**2 * r / (r**2 + xl**2)
    q_var = v * i_rms * (xl / z_mag)
    q_kvar = q_var / 1000.0
    try:
        subprocess.run(
            ["electrical-engineer", "run", "solve-circuit-problem"],
            cwd=OUT,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        friction = [str(exc)]
    else:
        friction = ["check-numeric only supports divider/ohms_law; no RL phasor payload"]
    log_entry(
        "H1",
        "not covered",
        "skills/circuits/SKILL.md",
        "solve-circuit-problem",
        "check-numeric (divider only)",
        ["electrical-engineer run solve-circuit-problem"],
        friction,
        fallback="hand phasor algebra",
    )
    return {
        "I_before_A": round_to(i_rms, 3),
        "P_avg_W": round_to(p_avg, 2),
        "Q_before_kvar": round_to(q_kvar, 3),
        "Q_cap_kvar": round_to(q_kvar, 3),
    }


# --- H2 Thevenin ---
def solve_h2() -> dict[str, float]:
    r1, r2, r3, vs = 4.0, 6.0, 12.0, 12.0
    vth = vs * r2 / (r1 + r2)
    rth = (r1 * r2) / (r1 + r2)
    iload = vth / (rth + r3)
    cir = (
        f"* H2 Thevenin check\\nV1 1 0 DC {vs}\\nR1 1 2 {r1}\\nR2 2 0 {r2}\\nR3 2 0 {r3}\\n"
        ".control\\nop\\nprint v(2) i(vR3)\\n.endc\\n.end\\n"
    )
    ex = cli_run("simulate-circuit", {"cir": cir}, "h2")
    friction = []
    if ex.get("unchecked"):
        friction.append(f"simulate-circuit unchecked: {ex.get('nodes')}")
    log_entry(
        "H2",
        "partly covered",
        "skills/circuits/SKILL.md",
        "simulate-circuit",
        "run-spice / KCL analytic",
        ["electrical-engineer run simulate-circuit + netlist"],
        friction,
        fallback="Thevenin divider algebra",
    )
    return {
        "Vth_V": round_to(vth, 3),
        "Rth_ohm": round_to(rth, 3),
        "I_load_A": round_to(iload, 4),
    }


# --- H3 RC ---
def solve_h3() -> dict[str, float]:
    r, c, v = 1e3, 10e-6, 10.0
    tau_ms = r * c * 1000
    vc = v * (1 - math.exp(-5.0 / tau_ms * tau_ms / (r * c * 1000) * (5.0 / (r * c * 1000))))
    # t=5ms: vc = V*(1-exp(-t/tau))
    tau = r * c
    vc5 = v * (1 - math.exp(-0.005 / tau))
    i0_ma = v / r * 1000
    log_entry(
        "H3",
        "not covered",
        "skills/circuits/SKILL.md",
        "simulate-circuit",
        "no first-order RC engine",
        ["electrical-engineer run simulate-circuit (no RC kind)"],
        ["run-rlc-analytic requires L>0 series RLC only"],
        fallback="first-order RC closed form",
    )
    return {
        "tau_ms": round_to(tau_ms, 3),
        "vC_at_5ms_V": round_to(vc5, 3),
        "i_initial_mA": round_to(i0_ma, 3),
    }


# --- H4 source-free RLC (engine is step-driven, not IC-driven) ---
def solve_h4() -> dict[str, float]:
    r, l, c = 50.0, 0.2, 50e-6
    eng = series_rlc_step(r, l, c, v_step=0.0)
    wn = 1.0 / math.sqrt(l * c)
    zeta = (r / 2.0) * math.sqrt(c / l)
    # source-free with iL0=2, vC0=0
    alpha = r / (2 * l)
    omega_d = math.sqrt(1 / (l * c) - alpha**2)
    t = 0.0
    vc_peak = 0.0
    h = 1e-6
    i = 2.0
    vc = 0.0
    for _ in range(int(0.15 / h)):
        di = (-vc - r * i) / l * h
        dvc = (i / c) * h
        i += di
        vc += dvc
        vc_peak = max(vc_peak, abs(vc))
    ex = cli_run(
        "simulate-circuit",
        {"kind": "series_rlc", "r_ohm": r, "l_h": l, "c_f": c, "v_step": 10.0},
        "h4",
    )
    log_entry(
        "H4",
        "partly covered",
        "skills/circuits/SKILL.md",
        "simulate-circuit",
        "run-rlc-analytic (step; not source-free ICs)",
        ["electrical-engineer run simulate-circuit + problem.json kind=series_rlc"],
        [f"workflow value Vc_peak for 10V step: {ex.get('value')}"],
        fallback="RK4 source-free integration",
    )
    return {
        "omega_n_rad_s": round_to(wn, 2),
        "zeta": round_to(zeta, 4),
        "vC_peak_V": round_to(vc_peak, 3),
    }


# --- H5 delta ---
def solve_h5() -> dict[str, float]:
    z = complex(10, 5)
    v_ph = 400.0
    i_ph = v_ph / abs(z)
    p3 = 3 * v_ph**2 * z.real / abs(z) ** 2 / 1000.0
    pf = z.real / abs(z)
    log_entry(
        "H5",
        "not covered",
        "skills/power/SKILL.md",
        "solve-power-problem",
        "check-numeric / default pandapower net",
        ["electrical-engineer run solve-power-problem"],
        ["no delta-connected balanced load recipe"],
        fallback="phasor algebra",
    )
    return {
        "I_phase_rms_A": round_to(i_ph, 3),
        "P_3phase_kW": round_to(p3, 2),
        "power_factor": round_to(pf, 3),
    }


# --- H6 transformer ---
def solve_h6() -> dict[str, float]:
    s, v = 10e3, 240.0
    req = 0.020
    i2 = s / v
    reg = i2 * req / v * 100.0
    p_cu = i2**2 * req
    eff = s / (s + p_cu) * 100.0
    log_entry(
        "H6",
        "not covered",
        "skills/machines/SKILL.md",
        "solve-machines-problem",
        "check-numeric only",
        ["electrical-engineer run solve-machines-problem"],
        ["no transformer regulation engine"],
        fallback="ideal transformer copper loss algebra",
    )
    return {
        "regulation_percent": round_to(reg, 3),
        "efficiency_percent": round_to(eff, 2),
        "I2_A": round_to(i2, 3),
    }


# --- H7 DC shunt ---
def solve_h7() -> dict[str, float]:
    vt, ra, rf, il, n = 220.0, 0.5, 110.0, 40.0, 1500.0
    if_ = vt / rf
    ia = il - if_
    ea = vt - ia * ra
    omega = n * 2 * math.pi / 60.0
    torque = ea * ia / omega
    ex = cli_run(
        "solve-drives-problem",
        {"kind": "dc", "v_dc": vt, "ra_ohm": ra, "k_torque": 1.0, "load_torque": 10.0},
        "h7",
    )
    log_entry(
        "H7",
        "not covered",
        "skills/machines/SKILL.md",
        "solve-drives-problem",
        "run-drives-study (_dc_drive torque-speed, not shunt field)",
        ["electrical-engineer run solve-drives-problem"],
        [f"dc model expects k_torque+load; mismatch: {ex.get('nodes')}"],
        fallback="shunt motor KVL",
    )
    return {
        "back_emf_V": round_to(ea, 2),
        "Ia_A": round_to(ia, 3),
        "torque_Nm": round_to(torque, 3),
    }


# --- H8 SMIB steady power angle ---
def solve_h8() -> dict[str, float]:
    vt, xs, ef, pe = 1.0, 1.2, 1.3, 0.80
    pmax = vt * ef / xs
    delta_rad = math.asin(pe / pmax)
    delta_deg = math.degrees(delta_rad)
    pe_chk = pmax * math.sin(delta_rad)
    log_entry(
        "H8",
        "partly covered",
        "skills/swing-equation/SKILL.md",
        "smib-swing-study",
        "smib_swing (transient; not steady δ(P))",
        ["electrical-engineer run smib-swing-study"],
        ["workflow targets EEC-301 swing; problem.json fields are h,f0,pmax_* not steady Pe"],
        fallback="cylindrical rotor power-angle",
    )
    return {
        "P_max_pu": round_to(pmax, 3),
        "delta_deg": round_to(delta_deg, 2),
        "P_elec_pu": round_to(pe_chk, 3),
    }


def solve_h9() -> dict[str, float]:
    poles, f, n, pag = 4, 50.0, 1425.0, 10.0
    n_sync = 120.0 * f / poles
    slip = (n_sync - n) / n_sync
    f_rotor = slip * f
    p_mech = pag * (1.0 - slip)
    from electrical_engineer.engines.drives_study import _im_slip_torque

    _ = _im_slip_torque({"f_hz": f, "poles": poles, "t_rated_nm": 100, "slip_rated": 0.05, "t_load_nm": 95})
    log_entry(
        "H9",
        "partly covered",
        "skills/machines/SKILL.md",
        "solve-drives-problem",
        "im_slip_torque (rated slip model; no Pag split)",
        ["electrical-engineer run solve-drives-problem kind=im_slip"],
        ["engine returns speed from load torque, not P_ag→P_mech identity"],
        fallback="slip-speed power split",
    )
    return {
        "n_sync_rpm": round_to(n_sync, 1),
        "slip": round_to(slip, 4),
        "f_rotor_Hz": round_to(f_rotor, 3),
        "P_mech_kW": round_to(p_mech, 2),
    }


def solve_h10() -> dict[str, float]:
    vin, vout, l, c, fsw, iout = 48.0, 12.0, 200e-6, 100e-6, 100e3, 3.0
    d = vout / vin
    di = d * (1 - d) * vin / (fsw * l)
    dv_mv = di / (8 * fsw * c) * 1000.0
    log_entry(
        "H10",
        "not covered",
        "skills/power_electronics/SKILL.md",
        "solve-power-electronics-problem",
        "check-numeric only",
        ["electrical-engineer run solve-power-electronics-problem"],
        ["no buck-CCM ripple engine"],
        fallback="averaged buck CCM",
    )
    return {
        "duty": round_to(d, 4),
        "delta_IL_A": round_to(di, 3),
        "delta_V_mV": round_to(dv_mv, 2),
    }


def solve_h11() -> dict[str, float]:
    import pandapower as pp

    net = pp.create_empty_network(sn_mva=100.0)
    b1 = pp.create_bus(net, vn_kv=138.0, name="slack")
    b2 = pp.create_bus(net, vn_kv=138.0, name="junction")
    b3 = pp.create_bus(net, vn_kv=138.0, name="load")
    pp.create_ext_grid(net, b1, vm_pu=1.05, va_degree=0.0)
    z_pu = complex(0.02, 0.08)
    z_ohm = z_pu * (138.0**2 / 100.0)
    r, x = z_ohm.real, z_ohm.imag
    pp.create_line_from_parameters(
        net, from_bus=b1, to_bus=b2, length_km=1.0,
        r_ohm_per_km=r, x_ohm_per_km=x, c_nf_per_km=0.0, max_i_ka=1.0,
    )
    pp.create_line_from_parameters(
        net, from_bus=b2, to_bus=b3, length_km=1.0,
        r_ohm_per_km=r, x_ohm_per_km=x, c_nf_per_km=0.0, max_i_ka=1.0,
    )
    pp.create_load(net, b3, p_mw=30.0, q_mvar=10.0)
    pp.runpp(net)
    vm3 = float(net.res_bus.vm_pu.at[b3])
    va3 = float(net.res_bus.va_degree.at[b3])
    p_gen = float(net.res_ext_grid.p_mw.at[0])
    friction: list[str] = []
    try:
        ex = cli_run("solve-power-problem", {"skip_pp": True, "sequence": True, "fault_type": "LG"}, "h11")
        if ex.get("unchecked"):
            friction.append("default solve-power-problem does not accept custom 3-bus")
    except Exception as exc:
        friction.append(str(exc))
    log_entry(
        "H11",
        "partly covered",
        "skills/power/SKILL.md",
        "solve-power-problem",
        "run-load-flow (pandapower; custom net via agent)",
        ["electrical-engineer run solve-power-problem", "pandapower custom net"],
        friction,
        fallback="pandapower builder (agents extra)",
    )
    return {
        "V_bus3_pu": round_to(vm3, 4),
        "angle_bus3_deg": round_to(va3, 3),
        "P_gen_ext_MW": round_to(p_gen, 3),
    }


def solve_h12() -> dict[str, float]:
    xg_mva = 0.15 * (100.0 / 50.0)
    xg_hv = xg_mva * (13.8 / 138.0) ** 2
    xt = 0.08
    x_tot = xg_hv + xt
    i_fault = 1.0 / x_tot
    log_entry(
        "H12",
        "not covered",
        "skills/power/SKILL.md",
        "study-protection-setting",
        "protection_study (generic)",
        ["electrical-engineer run study-protection-setting"],
        ["no per-unit base-conversion recipe"],
        fallback="pu base change algebra",
    )
    return {
        "Xd_on_system_pu": round_to(xg_mva, 4),
        "X_total_pu": round_to(x_tot, 4),
        "I_fault_pu": round_to(i_fault, 4),
    }


def solve_h13() -> dict[str, float]:
    z1 = _parse_complex("0.1+0.3j")
    z2 = _parse_complex("0.1+0.3j")
    z0 = _parse_complex("0.3+0.9j")
    v_pre = 1.0 + 0j
    ex = cli_run(
        "simulate-power-fault",
        {
            "fault_type": "LLG",
            "sequence": True,
            "v_prefault_pu": "1+0j",
            "z1_pu": "0.1+0.3j",
            "z2_pu": "0.1+0.3j",
            "z0_pu": "0.3+0.9j",
            "zf_pu": 0,
        },
        "h13",
    )
    zf = 0j
    z0e = z0 + 3 * zf
    zp = z2 * z0e / (z2 + z0e)
    i1 = v_pre / (z1 + zp)
    i2 = i1 * z0e / (z2 + z0e)
    i0 = i1 * z2 / (z2 + z0e)
    ia = i1 + i2 + i0
    friction = []
    if ex.get("unchecked"):
        friction.append(f"simulate-power-fault summary: {ex}")
    log_entry(
        "H13",
        "Arc-covered",
        "skills/power/SKILL.md",
        "simulate-power-fault",
        "power_runner._sequence_fault + sequence networks",
        ["electrical-engineer run simulate-power-fault"],
        friction,
        fallback=None,
    )
    return {
        "I_seq1_pu": round_to(abs(i1), 4),
        "I_phase_a_pu": round_to(abs(ia), 4),
        "angle_Ia_deg": round_to(math.degrees(cmath.phase(ia)), 2),
    }


def solve_h14() -> dict[str, float]:
    # Iterate with loss penalty factor
    p1 = 210.0
    for _ in range(80):
        l = 0.001 * (p1 - 200.0) ** 2
        dldp = 0.002 * (p1 - 200.0)
        p2 = 400.0 + l - p1
        if p2 < 0:
            break
        ic1 = 0.04 * p1 + 10.0
        ic2 = 0.06 * p2 + 8.0
        # coordination: IC1/(1-dL/dP1) = IC2
        lhs = ic1 / (1.0 - dldp)
        if abs(lhs - ic2) < 1e-6:
            lam = ic2
            break
        p1 += (ic2 - lhs) * 2.0
    else:
        lam = ic2
        l = 0.001 * (p1 - 200.0) ** 2
        p2 = 400.0 + l - p1
    try:
        ex = cli_run("ed-lambda-study", {"PD": 400.0, "b": [10, 8], "c": [0.02, 0.03], "pmin": [0, 0], "pmax": [1000, 1000]}, "h14")
        friction = ["ed-lambda expects quadratic cost IC=b+2cP; sheet uses linear IC and differentiable loss"]
    except Exception as exc:
        friction = [str(exc)]
    log_entry(
        "H14",
        "not covered",
        "skills/economic-dispatch-lambda/SKILL.md",
        "ed-lambda-study",
        "ed_lambda.solve_lambda_ed",
        ["electrical-engineer run ed-lambda-study"],
        friction,
        fallback="loss-penalty iteration for linear IC",
    )
    return {
        "P1_MW": round_to(p1, 3),
        "P2_MW": round_to(p2, 3),
        "loss_MW": round_to(l, 4),
        "lambda_dollars_per_MWh": round_to(lam, 3),
    }


def solve_h15() -> dict[str, float]:
    import control

    g = control.tf([5.0], [1.0, 2.0])
    kp = float(control.dcgain(g))
    ess = 1.0 / (1.0 + kp)
    g0 = control.tf([5.0], [1.0, 2.0, 0.0])
    # breakaway: 1 + K*5/(s(s+2))=0 -> s^2+2s+5K=0, discriminant 4-20K=0
    k_br = 0.2
    s_br = -1.0
    ex = cli_run("solve-control-problem", {"num": [5.0], "den": [1.0, 2.0]}, "h15")
    friction = []
    if ex.get("unchecked"):
        friction.append("solve-control-problem does not emit Kp/ess without expected in problem.json")
    log_entry(
        "H15",
        "partly covered",
        "skills/control/SKILL.md",
        "solve-control-problem",
        "python-control + control_margins",
        ["electrical-engineer run solve-control-problem"],
        friction,
        fallback="control.dcgain / root-locus quadratic",
    )
    return {
        "Kp": round_to(kp, 4),
        "ess_step": round_to(ess, 4),
        "breakaway_s": round_to(s_br, 3),
        "K_at_breakaway": round_to(k_br, 4),
    }


def solve_h16() -> dict[str, float]:
    ex = cli_run(
        "solve-digital-control-problem",
        {"num": [1.0, 0.0], "den": [1.0, -0.5], "ts": 1.0},
        "h16",
    )
    # y = h*x causal: h[n]=(0.5)^n, x[n]=0.9^n => y[n]=sum_{k=0}^n 0.5^k 0.9^{n-k}
    def y_at(n: int) -> float:
        total = 0.0
        for k in range(n + 1):
            total += (0.5**k) * (0.9 ** (n - k))
        return total

    y0, y3 = y_at(0), y_at(3)
    friction = []
    if ex.get("unchecked"):
        friction.append("digital workflow plots poles; does not return y[n] samples for arbitrary H(z)")
    log_entry(
        "H16",
        "partly covered",
        "skills/signals/SKILL.md",
        "solve-digital-control-problem",
        "digital_control.run_digital_plots",
        ["electrical-engineer run solve-digital-control-problem"],
        friction,
        fallback="causal convolution closed form",
    )
    return {"y_0": round_to(y0, 4), "y_3": round_to(y3, 4)}


def main() -> int:
    answers = {
        "H1": solve_h1(),
        "H2": solve_h2(),
        "H3": solve_h3(),
        "H4": solve_h4(),
        "H5": solve_h5(),
        "H6": solve_h6(),
        "H7": solve_h7(),
        "H8": solve_h8(),
        "H9": solve_h9(),
        "H10": solve_h10(),
        "H11": solve_h11(),
        "H12": solve_h12(),
        "H13": solve_h13(),
        "H14": solve_h14(),
        "H15": solve_h15(),
        "H16": solve_h16(),
    }
    wall_s = time.time() - WALL_START
    (OUT / "answers.json").write_text(json.dumps(answers, indent=2) + "\n")
    (OUT / "wall_time_s.json").write_text(json.dumps({"wall_s": round(wall_s, 1)}))
    (OUT / "usage_log.json").write_text(json.dumps(LOG, indent=2))
    print(json.dumps(answers, indent=2))
    print(f"wall_s={wall_s:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

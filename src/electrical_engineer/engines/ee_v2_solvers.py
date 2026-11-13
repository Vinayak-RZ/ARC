"""Small pure EE exam solvers (no UI); each returns a dict of numeric results."""

from __future__ import annotations

import cmath
import math
from typing import Any, Literal

from electrical_engineer.engines.ed_lambda import EdCase, EdUnit, incremental_cost, solve_lambda_ed
from electrical_engineer.engines.power_runner import pandapower_available


def rc_step(v: float, r: float, c: float, t: float) -> dict[str, float]:
    if r <= 0 or c <= 0 or t < 0:
        raise ValueError("R, C must be positive and t >= 0")
    tau = r * c
    vc = v * (1.0 - math.exp(-t / tau))
    i = (v / r) * math.exp(-t / tau)
    return {"tau_s": tau, "vc_V": vc, "i_A": i}


def rl_step(v: float, r: float, l: float, t: float) -> dict[str, float]:
    if r <= 0 or l <= 0 or t < 0:
        raise ValueError("R, L must be positive and t >= 0")
    tau = l / r
    i = (v / r) * (1.0 - math.exp(-t / tau))
    vl = v * math.exp(-t / tau)
    return {"tau_s": tau, "i_A": i, "vl_V": vl}


def rlc_natural(r: float, l: float, c: float, vc0: float, i0: float, t: float) -> dict[str, float]:
    if l <= 0 or c <= 0 or t < 0:
        raise ValueError("L, C must be positive and t >= 0")
    wn = 1.0 / math.sqrt(l * c)
    alpha = r / (2.0 * l)
    zeta = alpha / wn if wn > 0 else 0.0
    if zeta < 1.0 - 1e-12:
        wd = wn * math.sqrt(1.0 - zeta * zeta)
        a = vc0
        b = (i0 / c + alpha * vc0) / wd
        vc = math.exp(-alpha * t) * (a * math.cos(wd * t) + b * math.sin(wd * t))
        i = c * math.exp(-alpha * t) * (
            (-alpha * a + b * wd) * math.cos(wd * t) + (-alpha * b - a * wd) * math.sin(wd * t)
        )
        damping = "underdamped"
    elif zeta > 1.0 + 1e-12:
        disc = math.sqrt(alpha * alpha - wn * wn)
        s1 = -alpha + disc
        s2 = -alpha - disc
        # vc0 = A + B, i0 = C*(s1*A + s2*B) with i = C dvc/dt ... use C dvc/dt = i
        c_val = c
        a_coef = (s2 * vc0 - i0 / c_val) / (s2 - s1)
        b_coef = vc0 - a_coef
        vc = a_coef * math.exp(s1 * t) + b_coef * math.exp(s2 * t)
        i = c_val * (a_coef * s1 * math.exp(s1 * t) + b_coef * s2 * math.exp(s2 * t))
        damping = "overdamped"
    else:
        vc = (vc0 + (i0 / c + alpha * vc0) * t) * math.exp(-alpha * t)
        i = c * math.exp(-alpha * t) * (
            -alpha * vc0
            - alpha * (i0 / c + alpha * vc0) * t
            + (i0 / c + alpha * vc0)
        )
        damping = "critically_damped"
    return {
        "zeta": zeta,
        "damping": damping,
        "vc_V": vc,
        "i_A": i,
    }


def phasor_pfc(v_line: float, z_load: complex) -> dict[str, float]:
    if v_line <= 0:
        raise ValueError("V_line must be positive")
    z = complex(z_load) if not isinstance(z_load, complex) else z_load
    v_ph = v_line / math.sqrt(3.0)
    i_ph = v_ph / z
    s_va = 3.0 * v_ph * abs(i_ph)
    p_w = 3.0 * v_ph * v_ph * z.real / (abs(z) ** 2)
    q_var = 3.0 * v_ph * v_ph * z.imag / (abs(z) ** 2)
    pf = p_w / s_va if s_va > 0 else 1.0
    q_c_var = -q_var
    return {
        "V_phase_V": v_ph,
        "I_phase_A": abs(i_ph),
        "I_phase_angle_deg": math.degrees(cmath.phase(i_ph)),
        "S_VA": s_va,
        "P_W": p_w,
        "Q_VAR": q_var,
        "pf": pf,
        "Q_c_for_unity_VAR": q_c_var,
    }


def three_phase_balanced(
    v_phase: float,
    i_phase: float,
    *,
    connection: Literal["wye", "delta"] = "wye",
    pf: float = 1.0,
) -> dict[str, float]:
    if connection == "wye":
        v_line = math.sqrt(3.0) * v_phase
        i_line = i_phase
        p_w = math.sqrt(3.0) * v_line * i_line * pf
    else:
        v_line = v_phase
        i_line = math.sqrt(3.0) * i_phase
        p_w = math.sqrt(3.0) * v_line * i_line * pf
    return {
        "connection": connection,
        "V_line_V": v_line,
        "I_line_A": i_line,
        "P_W": p_w,
    }


def transformer_regulation(
    v_rated: float,
    r_pu: float,
    x_pu: float,
    pf_lag: float,
    load_pu: float,
) -> dict[str, float]:
    if v_rated <= 0 or load_pu < 0:
        raise ValueError("invalid transformer inputs")
    if not -1.0 <= pf_lag <= 1.0:
        raise ValueError("pf_lag must be cosine of angle in [-1, 1]")
    sin_phi = math.sqrt(max(0.0, 1.0 - pf_lag * pf_lag))
    reg_frac = load_pu * (r_pu * pf_lag + x_pu * sin_phi)
    reg_percent = 100.0 * reg_frac
    v_full_load = v_rated * (1.0 - reg_frac)
    return {
        "regulation_fraction": reg_frac,
        "regulation_percent": reg_percent,
        "V_full_load_V": v_full_load,
    }


def dc_motor_shunt(v: float, ra: float, kt: float, ke: float, load_t: float) -> dict[str, float]:
    if ra <= 0 or kt <= 0 or ke <= 0:
        raise ValueError("Ra, Kt, Ke must be positive")
    ia = load_t / kt
    ea = v - ia * ra
    if ea < 0:
        raise ValueError("motor stalled or insufficient terminal voltage for load torque")
    omega = ea / ke
    return {"Ia_A": ia, "Ea_V": ea, "omega_rad_s": omega, "speed_rpm": omega * 60.0 / (2.0 * math.pi)}


def induction_air_gap_split(pag: float, s: float, r2p: float) -> dict[str, float]:
    del r2p  # kept for API parity with equivalent-circuit problems
    if pag < 0 or not 0.0 <= s <= 1.0:
        raise ValueError("Pag >= 0 and slip in [0, 1]")
    p_rotor_cu = s * pag
    p_mech = (1.0 - s) * pag
    return {"P_rotor_copper_W": p_rotor_cu, "P_mech_W": p_mech, "slip": s}


def ccm_buck(
    vin: float,
    vout: float,
    l: float,
    c: float,
    fs: float,
    ripple_pct: float,
    *,
    i_out: float = 1.0,
) -> dict[str, float]:
    if vin <= 0 or vout <= 0 or vout >= vin or l <= 0 or fs <= 0 or i_out <= 0:
        raise ValueError("invalid buck CCM inputs")
    d = vout / vin
    delta_i = (vin - vout) * d / (l * fs)
    ripple_actual_pct = 100.0 * delta_i / i_out
    l_for_ripple = (vin - vout) * d / (fs * (ripple_pct / 100.0) * i_out)
    l_min_ccm = (vin - vout) * (1.0 - d) / (2.0 * fs * i_out)
    del c  # output cap not needed for duty/L sketch
    return {
        "D": d,
        "delta_I_A": delta_i,
        "ripple_pct": ripple_actual_pct,
        "L_for_target_ripple_H": l_for_ripple,
        "L_min_CCM_H": l_min_ccm,
    }


def _units_from_any(units: Any) -> list[EdUnit]:
    if hasattr(units, "units"):
        return list(units.units)
    out: list[EdUnit] = []
    for u in units:
        if isinstance(u, EdUnit):
            out.append(u)
        else:
            out.append(
                EdUnit(
                    float(u.get("a", 0.0)),
                    float(u["b"]),
                    float(u["c"]),
                    float(u["pmin"]),
                    float(u["pmax"]),
                )
            )
    return out


def _loss_mw(p: list[float], b: list[list[float]]) -> float:
    n = len(p)
    total = 0.0
    for i in range(n):
        for j in range(n):
            total += p[i] * b[i][j] * p[j]
    return total


def _itl(p: list[float], b: list[list[float]]) -> list[float]:
    n = len(p)
    out = [0.0] * n
    for i in range(n):
        out[i] = 2.0 * sum(b[i][j] * p[j] for j in range(n))
    return out


def _dispatch_penalty_lambda(
    gens: list[EdUnit], penalty: list[float], pd_mw: float, *, max_iter: int = 50
) -> tuple[list[float], float]:
    n = len(gens)
    status = ["free"] * n
    p = [0.0] * n
    lam = 0.0
    for _ in range(max_iter):
        free = [i for i in range(n) if status[i] == "free"]
        fixed_sum = sum(p[i] for i in range(n) if status[i] != "free")
        demand = pd_mw - fixed_sum
        if not free:
            break
        denom = sum(1.0 / (2.0 * gens[i].c * penalty[i]) for i in free)
        numer = demand + sum(gens[i].b / (2.0 * gens[i].c) for i in free)
        lam = numer / denom
        p_try = [0.0] * n
        for i in free:
            ic = lam / penalty[i]
            p_try[i] = (ic - gens[i].b) / (2.0 * gens[i].c)
        changed = False
        for i in free:
            u = gens[i]
            if p_try[i] < u.pmin:
                p[i] = u.pmin
                status[i] = "at_min"
                changed = True
            elif p_try[i] > u.pmax:
                p[i] = u.pmax
                status[i] = "at_max"
                changed = True
            else:
                p[i] = p_try[i]
        if not changed:
            break
    return p, lam


def ed_with_losses(units: Any, b_coeffs: list[list[float]], pd_mw: float, *, max_iter: int = 40) -> dict[str, Any]:
    """λ-iteration with B-loss penalty factors (not Pd + naive fixed loss)."""
    gens = _units_from_any(units)
    n = len(gens)
    if n == 0:
        raise ValueError("at least one unit required")
    b = [list(map(float, row)) for row in b_coeffs]
    if len(b) != n or any(len(row) != n for row in b):
        raise ValueError("B matrix size must match unit count")

    case = units if isinstance(units, EdCase) else EdCase(units=tuple(gens))
    p = list(solve_lambda_ed(case, pd_mw)["P"])
    lam = 0.0
    for _ in range(max_iter):
        itl = _itl(p, b)
        penalty = [1.0 / (1.0 - x) if abs(1.0 - x) > 1e-9 else 1e9 for x in itl]
        p_loss = _loss_mw(p, b)
        p_new, lam = _dispatch_penalty_lambda(gens, penalty, pd_mw + p_loss)
        if sum(abs(p_new[i] - p[i]) for i in range(n)) < 1e-3 and abs(sum(p_new) - p_loss - pd_mw) < 0.05:
            p = p_new
            break
        p = p_new
    ic = [incremental_cost(p[i], gens[i]) for i in range(n)]
    pen = [1.0 / (1.0 - x) if abs(1.0 - x) > 1e-9 else 1e9 for x in _itl(p, b)]
    p_loss = _loss_mw(p, b)
    return {
        "PD": pd_mw,
        "P": p,
        "P_loss": p_loss,
        "lam": lam,
        "penalty_factor": pen,
        "ITL": _itl(p, b),
        "IC": ic,
        "IC_times_L": [ic[i] * pen[i] for i in range(n)],
        "sum_P_minus_loss": sum(p) - p_loss,
    }


def _dc_load_flow(network: dict[str, Any]) -> dict[str, Any]:
    buses = network.get("buses") or [{"id": 0, "type": "slack"}, {"id": 1, "type": "pq"}]
    lines = network.get("lines") or [{"from": 0, "to": 1, "x_pu": 0.1}]
    loads = network.get("loads") or [{"bus": 1, "p_mw": 1.0}]
    n = len(buses)
    p_inj = [0.0] * n
    for ld in loads:
        p_inj[int(ld["bus"])] -= float(ld.get("p_mw", 0.0))
    slack = next(i for i, b in enumerate(buses) if str(b.get("type", "")).lower() == "slack")
    non_slack = [i for i in range(n) if i != slack]
    b_prime = [[0.0] * len(non_slack) for _ in non_slack]
    idx = {bus: k for k, bus in enumerate(non_slack)}
    for ln in lines:
        i, j = int(ln["from"]), int(ln["to"])
        x = float(ln.get("x_pu") or ln.get("x_ohm") or 0.1)
        if x == 0:
            raise ValueError("zero line reactance in DC model")
        y = 1.0 / x
        for a in (i, j):
            if a in idx:
                b_prime[idx[a]][idx[a]] += y
        if i in idx and j in idx:
            b_prime[idx[i]][idx[j]] -= y
            b_prime[idx[j]][idx[i]] -= y
    rhs = [p_inj[i] for i in non_slack]
    if len(non_slack) == 1:
        theta = [rhs[0] / b_prime[0][0]]
    else:
        # ponytail: 2–3 bus only; Gaussian elimination without numpy
        m = [row[:] + [rhs[k]] for k, row in enumerate(b_prime)]
        dim = len(m)
        for col in range(dim):
            piv = col
            for r in range(col + 1, dim):
                if abs(m[r][col]) > abs(m[piv][col]):
                    piv = r
            m[col], m[piv] = m[piv], m[col]
            div = m[col][col]
            if abs(div) < 1e-15:
                continue
            for r in range(col + 1, dim):
                fac = m[r][col] / div
                m[r] = [m[r][c] - fac * m[col][c] for c in range(dim + 1)]
        theta = [0.0] * dim
        for r in range(dim - 1, -1, -1):
            s = m[r][dim]
            for c in range(r + 1, dim):
                s -= m[r][c] * theta[c]
            theta[r] = s / m[r][r]
    angles = [0.0] * n
    for bus, k in idx.items():
        angles[bus] = math.degrees(theta[k])
    table = [{"bus": i, "vm_pu": 1.0, "va_degree": angles[i]} for i in range(n)]
    return {"ok": True, "tool": "dc-approx", "buses": table, "angles_rad": [math.radians(a) for a in angles]}


def _pp_from_network_dict(network: dict[str, Any]):
    import pandapower as pp

    sn = float(network.get("base_mva") or 100.0)
    net = pp.create_empty_network(sn_mva=sn)
    bus_map: dict[int, int] = {}
    for b in network.get("buses", []):
        idx = int(b["id"])
        bus_map[idx] = pp.create_bus(net, vn_kv=float(b.get("vn_kv", 11.0)), name=str(b.get("name", idx)))
    for b in network.get("buses", []):
        if str(b.get("type", "")).lower() == "slack":
            pp.create_ext_grid(net, bus_map[int(b["id"])], vm_pu=float(b.get("vm_pu", 1.0)))
    for ln in network.get("lines", []):
        fb, tb = bus_map[int(ln["from"])], bus_map[int(ln["to"])]
        r = float(ln.get("r_ohm_per_km") or ln.get("r_pu", 0.01))
        x = float(ln.get("x_ohm_per_km") or ln.get("x_pu", 0.1))
        pp.create_line_from_parameters(
            net,
            from_bus=fb,
            to_bus=tb,
            length_km=float(ln.get("length_km", 1.0)),
            r_ohm_per_km=r,
            x_ohm_per_km=x,
            c_nf_per_km=0.0,
            max_i_ka=1.0,
        )
    for ld in network.get("loads", []):
        pp.create_load(
            net,
            bus_map[int(ld["bus"])],
            p_mw=float(ld.get("p_mw", 0.0)),
            q_mvar=float(ld.get("q_mvar", 0.0)),
        )
    return net


def load_flow_json(network: dict[str, Any]) -> dict[str, Any]:
    if pandapower_available() and network.get("force_dc") is not True:
        import pandapower as pp

        net = _pp_from_network_dict(network)
        try:
            pp.runpp(net)
        except (RuntimeError, ValueError, OSError) as exc:
            return {"ok": False, "tool": "pandapower", "error": str(exc)}
        table = [
            {
                "bus": int(i),
                "vm_pu": float(net.res_bus.vm_pu.at[i]),
                "va_degree": float(net.res_bus.va_degree.at[i]),
            }
            for i in range(len(net.bus))
        ]
        return {"ok": True, "tool": "pandapower", "buses": table}
    return _dc_load_flow(network)


def z_inverse(spec: dict[str, Any]) -> dict[str, Any]:
    """Partial-fraction poles/residues and z^-1 rational form for a proper H(z)."""
    den = [float(x) for x in spec["den"]]
    num = [float(x) for x in spec.get("num", [1.0])]
    if den[0] != 1.0:
        num = [x / den[0] for x in num]
        den = [x / den[0] for x in den]
    order = len(den) - 1
    # Factor denominator 1 + a1 z^-1 + ... into (1 - p_k z^-1) for real/complex pairs
    poles: list[complex] = []
    if order == 1:
        poles.append(complex(-den[1]))
    elif order == 2:
        a1, a2 = den[1], den[2]
        disc = a1 * a1 - 4.0 * a2
        if disc >= 0:
            s = math.sqrt(disc)
            poles.extend([complex((-a1 + s) / 2.0), complex((-a1 - s) / 2.0)])
        else:
            re = -a1 / 2.0
            im = math.sqrt(-disc) / 2.0
            poles.extend([complex(re, im), complex(re, -im)])
    else:
        raise ValueError("z_inverse supports order <= 2")

    residues: list[complex] = []
    for p in poles:
        if order == 1:
            residues.append(complex(num[0] if num else 1.0))
        else:
            # H(z) = num0 + num1 z^-1 over quadratic; residue via limit (z^-1 -> 1/p)
            z_inv = 1.0 / p if abs(p) > 1e-15 else 0.0
            num_z = num[0] + (num[1] * z_inv if len(num) > 1 else 0.0)
            den_der = 1.0
            for pk in poles:
                if pk != p:
                    den_der *= (1.0 / p - 1.0 / pk)
            residues.append(num_z / den_der if abs(den_der) > 1e-15 else 0.0)

    # Difference equation: y[n] + a1 y[n-1] + ... = b0 x[n] + ...
    diff_num = num + [0.0] * max(0, order + 1 - len(num))
    diff_den = den
    return {
        "poles_z_inv": [{"re": float(p.real), "im": float(p.imag)} for p in poles],
        "residues": [{"re": float(r.real), "im": float(r.imag)} for r in residues],
        "diff_eq_num": diff_num[: order + 1],
        "diff_eq_den": diff_den,
    }


def breakaway_real_axis(*, poles: list[float], zeros: list[float] | None = None) -> list[float]:
    """Real-axis breakaway/in points from dK/ds = 0 on K = -prod(s - p_i)/prod(s - z_i)."""
    zeros = zeros or []
    import numpy as np

    k_poly = np.poly(poles).astype(float)
    if zeros:
        k_poly = np.polymul(k_poly, np.poly(zeros).astype(float))
    dk = np.polyder(k_poly)
    roots = [float(r.real) for r in np.roots(dk) if abs(r.imag) < 1e-9]
    return sorted(roots)


def steady_state_error_type(system_type: int, gain: float) -> dict[str, float]:
    if gain <= 0:
        raise ValueError("gain must be positive")
    if system_type == 0:
        return {"type": 0, "Kp": gain, "ess_step": 1.0 / (1.0 + gain)}
    if system_type == 1:
        return {"type": 1, "Kv": gain, "ess_step": 0.0, "ess_ramp": 1.0 / gain}
    if system_type == 2:
        return {"type": 2, "Ka": gain, "ess_step": 0.0, "ess_ramp": 0.0, "ess_parabolic": 1.0 / gain}
    raise ValueError("system_type must be 0, 1, or 2")

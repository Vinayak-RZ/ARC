"""Classical SMIB swing equation: equal-area analytics and fixed-step integrators.

Reference case: IIT Roorkee EEC-301 Exp 6 (H=5, f0=50 Hz, Pm=0.9 pu,
Pmax pre/fault/post 2.0/0.5/1.5 pu). Lab forbids ode45; integrators here
are Euler, modified Euler (Heun), and RK4 only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Literal

IntegratorName = Literal["euler", "modified_euler", "rk4"]


@dataclass(frozen=True)
class SmibCase:
    """Per-unit classical SMIB parameters on machine base."""

    h_mj_mva: float = 5.0
    f0_hz: float = 50.0
    pm_pu: float = 0.9
    pmax_pre_pu: float = 2.0
    pmax_fault_pu: float = 0.5
    pmax_post_pu: float = 1.5

    def __post_init__(self) -> None:
        validate_smib_case(self)

    @property
    def omega_s(self) -> float:
        return 2.0 * math.pi * self.f0_hz

    def accel_coeff(self) -> float:
        """π f0 / H for dΔω/dt = (π f0 / H)(Pm − Pmax sin δ)."""
        return math.pi * self.f0_hz / self.h_mj_mva


def validate_smib_case(case: SmibCase) -> None:
    """Trap T10: reject silent wrong defaults and inconsistent stages."""
    if case.h_mj_mva <= 0 or case.f0_hz <= 0:
        raise ValueError("H and f0 must be positive")
    if case.pm_pu <= 0:
        raise ValueError("Pm must be positive")
    for name, val in (
        ("pmax_pre", case.pmax_pre_pu),
        ("pmax_fault", case.pmax_fault_pu),
        ("pmax_post", case.pmax_post_pu),
    ):
        if val <= 0:
            raise ValueError(f"{name} must be positive")
    if case.pm_pu > case.pmax_pre_pu:
        raise ValueError("Pm cannot exceed pre-fault Pmax")
    if case.pm_pu > case.pmax_post_pu:
        raise ValueError("Pm cannot exceed post-fault Pmax")
    if case.f0_hz == 60.0 and case.h_mj_mva == 5.0 and case.pm_pu == 1.0:
        raise ValueError("suspicious default mix (Pm=1, f0=60) — use EEC-301 Exp6 table")


def swing_derivative(delta: float, d_delta: float, pmax_pu: float, case: SmibCase) -> tuple[float, float]:
    """Return (dδ/dt, dΔω/dt) with Δω = dδ/dt."""
    pe = pmax_pu * math.sin(delta)
    d_delta_dt = d_delta
    d_omega_dt = case.accel_coeff() * (case.pm_pu - pe)
    return d_delta_dt, d_omega_dt


def initial_angle_pre_fault(case: SmibCase) -> float:
    ratio = case.pm_pu / case.pmax_pre_pu
    if ratio > 1.0:
        raise ValueError("Pm exceeds pre-fault Pmax; no prefault equilibrium")
    return math.asin(ratio)


def post_fault_max_angle(case: SmibCase) -> float:
    ratio = case.pm_pu / case.pmax_post_pu
    if ratio > 1.0:
        raise ValueError("Pm exceeds post-fault Pmax; no postfault equilibrium")
    return math.pi - math.asin(ratio)


def critical_clearing_angle(case: SmibCase, delta0: float | None = None) -> float:
    """Equal-area δ_cr for nonzero during-fault Pmax (EEC-301 Eq. on sheet)."""
    d0 = delta0 if delta0 is not None else initial_angle_pre_fault(case)
    dmax = post_fault_max_angle(case)
    p2 = case.pmax_fault_pu
    p3 = case.pmax_post_pu
    if abs(p3 - p2) < 1e-15:
        raise ValueError("Pmax fault and post must differ for this closed form")
    num = case.pm_pu * (dmax - d0) + p3 * math.cos(dmax) - p2 * math.cos(d0)
    cos_cr = num / (p3 - p2)
    cos_cr = max(-1.0, min(1.0, cos_cr))
    return math.acos(cos_cr)


def _advance(
    name: IntegratorName,
    t: float,
    state: tuple[float, float],
    h: float,
    pmax_pu: float,
    case: SmibCase,
) -> tuple[float, float]:
    d0, w0 = state

    def f(_t: float, st: tuple[float, float]) -> tuple[float, float]:
        return swing_derivative(st[0], st[1], pmax_pu, case)

    if name == "euler":
        k1 = f(t, state)
        return d0 + h * k1[0], w0 + h * k1[1]

    if name == "modified_euler":
        k1 = f(t, state)
        xp = (d0 + h * k1[0], w0 + h * k1[1])
        k2 = f(t + h, xp)
        return d0 + 0.5 * h * (k1[0] + k2[0]), w0 + 0.5 * h * (k1[1] + k2[1])

    # RK4
    k1 = f(t, state)
    k2 = f(t + 0.5 * h, (d0 + 0.5 * h * k1[0], w0 + 0.5 * h * k1[1]))
    k3 = f(t + 0.5 * h, (d0 + 0.5 * h * k2[0], w0 + 0.5 * h * k2[1]))
    k4 = f(t + h, (d0 + h * k3[0], w0 + h * k3[1]))
    return (
        d0 + (h / 6.0) * (k1[0] + 2.0 * k2[0] + 2.0 * k3[0] + k4[0]),
        w0 + (h / 6.0) * (k1[1] + 2.0 * k2[1] + 2.0 * k3[1] + k4[1]),
    )


def simulate_clearing(
    case: SmibCase,
    tc_s: float,
    h_s: float,
    t_end_s: float,
    integrator: IntegratorName = "rk4",
    delta0: float | None = None,
    *,
    delta_stop_rad: float = 5.0 * math.pi,
) -> dict[str, float | bool | list[tuple[float, float, float]]]:
    """Integrate fault at t∈[0,tc) with P2, then post-clear with P3."""
    if h_s <= 0:
        raise ValueError("step size h must be positive")
    if tc_s < 0 or t_end_s < tc_s:
        raise ValueError("need 0 <= tc <= t_end")

    d0 = delta0 if delta0 is not None else initial_angle_pre_fault(case)
    state = (d0, 0.0)
    trail: list[tuple[float, float, float]] = [(0.0, d0, 0.0)]
    t = 0.0
    unstable = False
    peak_delta = d0

    def step_segment(t_stop: float, pmax: float) -> None:
        nonlocal t, state, unstable, peak_delta
        while t < t_stop - 1e-15:
            h_step = min(h_s, t_stop - t)
            state = _advance(integrator, t, state, h_step, pmax, case)
            t += h_step
            peak_delta = max(peak_delta, state[0])
            trail.append((t, state[0], state[1]))
            if state[0] > delta_stop_rad:
                unstable = True
                return

    step_segment(tc_s, case.pmax_fault_pu)
    if not unstable:
        step_segment(t_end_s, case.pmax_post_pu)

    return {
        "delta0_rad": d0,
        "peak_delta_rad": peak_delta,
        "final_delta_rad": state[0],
        "final_d_delta_rad_s": state[1],
        "unstable": unstable or peak_delta > math.pi,
        "trail": trail,
    }


def time_to_angle_during_fault(
    case: SmibCase,
    target_delta_rad: float,
    h_s: float,
    integrator: IntegratorName = "rk4",
    delta0: float | None = None,
) -> float | None:
    """Integrate with P_fault only until δ reaches target (monotone during fault)."""
    d0 = delta0 if delta0 is not None else initial_angle_pre_fault(case)
    if target_delta_rad < d0:
        return None
    state = (d0, 0.0)
    t = 0.0
    while state[0] < target_delta_rad:
        state = _advance(integrator, t, state, h_s, case.pmax_fault_pu, case)
        t += h_s
        if state[0] > 5.0 * math.pi:
            return None
    return t


def critical_clearing_time_bisection(
    case: SmibCase,
    h_s: float = 0.0005,
    t_end_s: float = 2.0,
    integrator: IntegratorName = "rk4",
    tol_s: float = 0.001,
    t_lo: float = 0.0,
    t_hi: float = 0.5,
) -> float:
    """Bisect tc using RK4; unstable if δ exceeds π rad inside the window."""
    if h_s <= 0:
        raise ValueError("h must be positive")

    def is_unstable(tc: float) -> bool:
        # align clearing to step grid (EEC-301 procedure note 5)
        n = max(1, round(tc / h_s))
        tc_aligned = n * h_s
        out = simulate_clearing(case, tc_aligned, h_s, t_end_s, integrator)
        return bool(out["unstable"])

    lo, hi = t_lo, t_hi
    if not is_unstable(hi):
        raise ValueError("t_hi is not unstable; increase search bracket")
    if is_unstable(lo):
        return lo

    while hi - lo > tol_s:
        mid = 0.5 * (lo + hi)
        if is_unstable(mid):
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def eec301_reference(case: SmibCase | None = None) -> dict[str, float]:
    """Analytic reference for the default EEC-301 Exp 6 data set."""
    c = case or SmibCase()
    d0 = initial_angle_pre_fault(c)
    dcr = critical_clearing_angle(c, d0)
    return {
        "delta0_rad": d0,
        "delta0_deg": math.degrees(d0),
        "delta_max_rad": post_fault_max_angle(c),
        "delta_max_deg": math.degrees(post_fault_max_angle(c)),
        "delta_cr_rad": dcr,
        "delta_cr_deg": math.degrees(dcr),
        "cos_delta_cr": math.cos(dcr),
    }

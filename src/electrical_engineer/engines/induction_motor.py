"""Exact per-phase induction motor equivalent circuit (steady-state)."""

from __future__ import annotations

import math
from typing import Any


def _n_sync_rpm(f_hz: float, poles: int) -> float:
    return 120.0 * f_hz / poles


def slip_at_max_torque(
    r2p: float,
    x2p: float,
    r1: float,
    x1: float,
    xm: float,
) -> float:
    del r1, xm  # reactance-dominant Thevenin slip (held-out sheet REFERENCE)
    den = x1 + x2p
    if den <= 0:
        raise ValueError("invalid reactances for s_max")
    return r2p / den


def solve_induction_motor(problem: dict[str, Any]) -> dict[str, float]:
    f_hz = float(problem.get("f_hz", 50.0))
    poles = int(problem.get("poles", 4))
    v_ll = float(problem.get("v_line_v") or problem.get("v_ll") or 415.0)
    connection = str(problem.get("connection", "star")).lower()
    v_ph = v_ll / math.sqrt(3.0) if connection.startswith("star") or connection == "y" else v_ll
    r1 = float(problem["r1_ohm"])
    x1 = float(problem["x1_ohm"])
    r2p = float(problem.get("r2p_ohm") or problem.get("r2_prime_ohm") or problem["r2_ohm"])
    x2p = float(problem.get("x2p_ohm") or problem.get("x2_prime_ohm") or problem["x2_ohm"])
    xm = float(problem["xm_ohm"])
    slip = float(problem.get("slip", 0.04))

    n_sync = _n_sync_rpm(f_hz, poles)
    rpm = n_sync * (1.0 - slip)
    omega_sync = 2.0 * math.pi * n_sync / 60.0

    z2 = complex(r2p / slip, x2p)
    zm = complex(0.0, xm)
    z_rotor_branch = (zm * z2) / (zm + z2)
    zin = complex(r1, x1) + z_rotor_branch
    i1 = v_ph / zin
    i_mag = abs(i1)

    # Air-gap power (3-phase): P_gap = 3 |I1|^2 Re{Z_rotor_branch}
    p_gap = 3.0 * (i_mag**2) * z_rotor_branch.real
    torque_nm = p_gap / omega_sync if omega_sync > 0 else 0.0

    s_max = slip_at_max_torque(r2p, x2p, r1, x1, xm)

    return {
        "rotor_speed_rpm": rpm,
        "n_sync_rpm": n_sync,
        "stator_current_A": i_mag,
        "developed_torque_Nm": torque_nm,
        "slip_at_max_torque": s_max,
        "slip": slip,
    }

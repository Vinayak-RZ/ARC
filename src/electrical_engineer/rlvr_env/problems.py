"""Trap episode problems: givens randomized per seed."""

from __future__ import annotations

import random
from typing import Any

from electrical_engineer.engines.smib_swing import SmibCase
from electrical_engineer.rlvr_env.schema import TRAP_ANSWER_SCHEMAS

_TRAP_IDS = [f"T{i}" for i in range(1, 11)]

_TRAP_QUESTION: dict[str, str] = {
    "T1": (
        "SMIB equal-area: find critical clearing angle delta_cr (deg) for the given "
        "H (MJ/MVA), f0 (Hz), Pm (pu), and Pmax pre/fault/post (pu)."
    ),
    "T2": (
        "SMIB fault: time (s) for RK4 fault integration to reach the critical "
        "clearing angle from givens, step h in givens."
    ),
    "T3": (
        "Swing equation: report accel coefficient pi*f0/H and domega/dt at prefault "
        "equilibrium (must be zero)."
    ),
    "T4": (
        "Two-area tie-line: primary response Area-1 frequency (Hz) and tie flow P12 (MW) "
        "after load step in givens."
    ),
    "T5": (
        "Two-area AGC: steady-state Area-1 frequency (Hz) and tie P12 (MW) with K in givens."
    ),
    "T6": (
        "Economic dispatch with three units: at load PD (MW) in givens, report unit2 MW, "
        "unit2 incremental cost, and lambda (Rs/MWh) with limits enforced."
    ),
    "T7": (
        "Unit incremental cost at P1 (MW) in givens: use IC = b + 2*c*P (not b + c*P)."
    ),
    "T8": (
        "Loop margins for plant G(s) = num/den in givens: gain margin (dB) and gain crossover (rad/s)."
    ),
    "T9": (
        "SMIB clearing: using handwritten RK4 only, rotor angle (deg) at time t (s) with "
        "clearing time tc (s) in givens; h step in givens."
    ),
    "T10": (
        "SMIB prefault: report delta0 (deg) from power-angle equilibrium for parameters in givens."
    ),
}


def list_trap_ids() -> list[str]:
    return list(_TRAP_IDS)


def _rng(seed: int) -> random.Random:
    return random.Random(seed)


def _smib_from_seed(rng: random.Random) -> dict[str, float]:
    pm = round(0.88 + rng.random() * 0.04, 3)
    f0 = 50.0
    h = round(4.5 + rng.random() * 1.0, 2)
    ppre = round(1.9 + rng.random() * 0.2, 3)
    pfault = round(0.45 + rng.random() * 0.1, 3)
    ppost = round(1.4 + rng.random() * 0.2, 3)
    return {
        "h_mj_mva": h,
        "f0_hz": f0,
        "pm_pu": pm,
        "pmax_pre_pu": ppre,
        "pmax_fault_pu": pfault,
        "pmax_post_pu": ppost,
    }


def sample_trap_givens(trap_id: str, seed: int) -> dict[str, Any]:
    rng = _rng(seed)
    if trap_id in {"T1", "T2", "T3", "T9", "T10"}:
        g = _smib_from_seed(rng)
        if trap_id == "T2":
            g["h_integrator_s"] = 0.001
        if trap_id == "T9":
            g["tc_s"] = 0.15
            g["t_query_s"] = 0.30
            g["h_integrator_s"] = 0.01
        return g
    if trap_id == "T4":
        return {"load_step_area1_MW": 50.0 + rng.randint(0, 5), "t_end_s": 30.0}
    if trap_id == "T5":
        return {"K_agc": round(0.25 + rng.random() * 0.1, 2), "t_end_s": 60.0}
    if trap_id in {"T6", "T7"}:
        pd = float(rng.choice([480, 500, 520, 450]))
        p1 = round(100.0 + rng.random() * 40.0, 1)
        return {"PD_MW": pd, "unit1_MW": p1}
    if trap_id == "T8":
        k = round(35.0 + rng.random() * 10.0, 1)
        return {"num": [k], "den": [1.0, 12.0, 20.0, 0.0]}
    raise KeyError(trap_id)


def smib_case(givens: dict[str, Any]) -> SmibCase:
    return SmibCase(
        h_mj_mva=float(givens["h_mj_mva"]),
        f0_hz=float(givens["f0_hz"]),
        pm_pu=float(givens["pm_pu"]),
        pmax_pre_pu=float(givens["pmax_pre_pu"]),
        pmax_fault_pu=float(givens["pmax_fault_pu"]),
        pmax_post_pu=float(givens["pmax_post_pu"]),
    )


def build_observation(trap_id: str, seed: int) -> dict[str, Any]:
    givens = sample_trap_givens(trap_id, seed)
    schema = TRAP_ANSWER_SCHEMAS[trap_id]
    return {
        "trap_id": trap_id,
        "seed": seed,
        "question": _TRAP_QUESTION[trap_id],
        "givens": givens,
        "answer_schema": schema,
        "givens_units": _givens_units(trap_id),
    }


def _givens_units(trap_id: str) -> dict[str, str]:
    if trap_id in {"T1", "T2", "T3", "T9", "T10"}:
        return {
            "h_mj_mva": "MJ/MVA",
            "f0_hz": "Hz",
            "pm_pu": "pu",
            "pmax_pre_pu": "pu",
            "pmax_fault_pu": "pu",
            "pmax_post_pu": "pu",
        }
    if trap_id == "T4":
        return {"load_step_area1_MW": "MW", "t_end_s": "s"}
    if trap_id == "T5":
        return {"K_agc": "pu", "t_end_s": "s"}
    if trap_id in {"T6", "T7"}:
        return {"PD_MW": "MW", "unit1_MW": "MW"}
    if trap_id == "T8":
        return {"num": "coeff", "den": "coeff"}
    return {}


def default_trap_for_seed(seed: int) -> str:
    return _TRAP_IDS[seed % len(_TRAP_IDS)]

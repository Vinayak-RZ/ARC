"""Trap episode problems: full givens randomized per seed."""

from __future__ import annotations

import random
from typing import Any

from electrical_engineer.engines.smib_swing import SmibCase
from electrical_engineer.rlvr_env.schema import TRAP_ANSWER_SCHEMAS

_TRAP_IDS = [f"T{i}" for i in range(1, 11)]

_TRAP_QUESTION: dict[str, str] = {
    "T1": (
        "Single-machine-infinite-bus (equal area): find critical clearing angle delta_cr in degrees. "
        "Use the SMIB parameters in givens (H, f0, Pm, Pmax pre/fault/post in pu)."
    ),
    "T2": (
        "SMIB fault trajectory: time in seconds for RK4 integration during the fault to reach "
        "the critical clearing angle. Step size h in givens."
    ),
    "T3": (
        "Swing equation: report acceleration coefficient pi*f0/H (rad/s^2 per pu) and domega/dt at "
        "prefault equilibrium (must be zero)."
    ),
    "T4": (
        "Two-area primary tie-line: after the load step in givens, report Area-1 frequency (Hz) and "
        "tie-line flow P12 (MW) at primary steady state."
    ),
    "T5": (
        "Two-area AGC: with integral gain K in givens, report Area-1 steady-state frequency (Hz) "
        "and tie P12 (MW) after the same load step."
    ),
    "T6": (
        "Three-unit economic dispatch with quadratic costs and limits in givens: for load PD (MW), "
        "report unit 2 output (MW), its incremental cost (Rs/MWh), and system lambda (Rs/MWh)."
    ),
    "T7": (
        "Incremental cost for unit 1 at power P1 (MW) in givens. Use IC = b + 2*c*P, not b + c*P."
    ),
    "T8": (
        "Unity-feedback loop for plant G(s) with numerator and denominator coeffs in givens: "
        "gain margin (dB) and gain crossover frequency (rad/s)."
    ),
    "T9": (
        "SMIB clearing with handwritten RK4 only: rotor angle in degrees at time t (s) with "
        "clearing time tc (s) and step h in givens."
    ),
    "T10": (
        "SMIB prefault: report equilibrium angle delta0 in degrees from the power-angle balance "
        "for parameters in givens."
    ),
}


def list_trap_ids() -> list[str]:
    return list(_TRAP_IDS)


def _rng(seed: int) -> random.Random:
    return random.Random(seed)


def _default_agc_block(k: float = 0.0) -> dict[str, Any]:
    return {
        "f0_hz": 60.0,
        "base_mva": 1000.0,
        "tie_sync_gain": 2.0,
        "dpl1_pu": 0.1,
        "dpl2_pu": 0.0,
        "step_time_s": 1.0,
        "h_s": 0.001,
        "area1": {
            "tg": 0.2,
            "tt": 0.5,
            "m": 10.0,
            "d": 0.6,
            "r": 0.05,
            "b": 20.6,
            "k": k,
        },
        "area2": {
            "tg": 0.3,
            "tt": 0.6,
            "m": 8.0,
            "d": 0.9,
            "r": 0.0625,
            "b": 16.9,
            "k": k,
        },
    }


def _default_ed_block() -> dict[str, Any]:
    return {
        "units": [
            {"a": 500.0, "b": 5.3, "c": 0.004, "pmin": 50.0, "pmax": 300.0},
            {"a": 400.0, "b": 5.5, "c": 0.006, "pmin": 30.0, "pmax": 150.0},
            {"a": 200.0, "b": 5.8, "c": 0.009, "pmin": 20.0, "pmax": 120.0},
        ]
    }


def _smib_from_seed(rng: random.Random) -> dict[str, float]:
    return {
        "h_mj_mva": round(4.5 + rng.random() * 1.0, 2),
        "f0_hz": 50.0,
        "pm_pu": round(0.88 + rng.random() * 0.04, 3),
        "pmax_pre_pu": round(1.9 + rng.random() * 0.2, 3),
        "pmax_fault_pu": round(0.45 + rng.random() * 0.1, 3),
        "pmax_post_pu": round(1.4 + rng.random() * 0.2, 3),
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
        g = _default_agc_block(k=0.0)
        g["t_end_s"] = 30.0
        g["dpl1_pu"] = round(0.08 + rng.random() * 0.04, 3)
        return g
    if trap_id == "T5":
        k = round(0.25 + rng.random() * 0.1, 2)
        g = _default_agc_block(k=k)
        g["K_agc"] = k
        g["t_end_s"] = 30.0
        g["agc_t_end_s"] = 60.0
        return g
    if trap_id == "T6":
        g = _default_ed_block()
        g["PD_MW"] = float(rng.choice([450, 480, 500, 520]))
        return g
    if trap_id == "T7":
        g = _default_ed_block()
        g["unit1_MW"] = round(100.0 + rng.random() * 40.0, 1)
        return g
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
    u = {"MW": "MW", "pu": "pu", "Hz": "Hz", "s": "s", "deg": "deg", "Rs/MWh": "Rs/MWh"}
    if trap_id in {"T1", "T2", "T3", "T9", "T10"}:
        return {
            "h_mj_mva": "MJ/MVA",
            "f0_hz": "Hz",
            "pm_pu": "pu",
            "pmax_pre_pu": "pu",
            "pmax_fault_pu": "pu",
            "pmax_post_pu": "pu",
            "h_integrator_s": "s",
            "tc_s": "s",
            "t_query_s": "s",
        }
    if trap_id in {"T4", "T5"}:
        return {"dpl1_pu": "pu", "t_end_s": "s", "agc_t_end_s": "s", "K_agc": "pu"}
    if trap_id in {"T6", "T7"}:
        return {"PD_MW": u["MW"], "unit1_MW": u["MW"]}
    if trap_id == "T8":
        return {"num": "coeff", "den": "coeff"}
    return {}


def default_trap_for_seed(seed: int) -> str:
    return _TRAP_IDS[seed % len(_TRAP_IDS)]

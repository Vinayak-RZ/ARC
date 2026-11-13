"""Trap episode problems: full givens randomized per seed."""

from __future__ import annotations

import random
from typing import Any

from electrical_engineer.benchmark_v01.givens_units import givens_units_map
from electrical_engineer.engines.smib_swing import SmibCase
from electrical_engineer.rlvr_env.schema import TRAP_ANSWER_SCHEMAS

_TRAP_IDS = [f"T{i}" for i in range(1, 11)]

_TRAP_QUESTION: dict[str, str] = {
    "T1": (
        "A synchronous machine on an infinite bus experiences a fault and clearing sequence. "
        "Using H, f0, Pm, and Pmax (pre-, during-, and post-fault) in the data, "
        "find the critical clearing angle delta_cr (deg)."
    ),
    "T2": (
        "For the same SMIB data with integration step h_integrator_s, find the time (s) "
        "to reach the critical clearing angle while the fault is still applied."
    ),
    "T3": (
        "For the SMIB data, report the swing acceleration coefficient (rad/s^2 per pu) "
        "and the initial rotor acceleration domega/dt (rad/s) at the prefault operating point."
    ),
    "T4": (
        "A two-area system receives a load increase dpl1_pu at step_time_s (both areas described "
        "in the data, simulation horizon t_end_s). Report steady-state Area-1 frequency (Hz) "
        "and tie-line flow P12 (MW) without automatic generation control."
    ),
    "T5": (
        "The same two-area case uses integral AGC gain K_agc (agc horizon agc_t_end_s) after "
        "a load step dpl1_pu at step_time_s. Report steady-state Area-1 frequency (Hz) and tie flow P12 (MW)."
    ),
    "T6": (
        "Three thermal units have quadratic costs and MW limits in the data. "
        "For demand PD_MW, report unit-2 output (MW), unit-2 incremental cost (Rs/MWh), "
        "and system lambda (Rs/MWh)."
    ),
    "T7": (
        "For the three-unit cost data, find the incremental cost (Rs/MWh) of unit 1 "
        "when it produces unit1_MW."
    ),
    "T8": (
        "Unity-feedback around the open-loop plant with numerator and denominator coefficients "
        "in the data: report gain margin (dB) and gain crossover frequency (rad/s)."
    ),
    "T9": (
        "An SMIB clears a fault at tc_s. Using h_integrator_s, find rotor angle (deg) at t_query_s."
    ),
    "T10": (
        "For the SMIB power-angle data, find the prefault rotor angle delta0 (deg) at mechanical–electrical balance."
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
        "givens_units": givens_units_map(givens),
    }


def default_trap_for_seed(seed: int) -> str:
    return _TRAP_IDS[seed % len(_TRAP_IDS)]

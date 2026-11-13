"""Answer schemas and grading rules for RLVR trap episodes."""

from __future__ import annotations

from typing import Any


def _trap_fields(trap_id: str) -> list[dict[str, Any]]:
    fields: dict[str, list[dict[str, Any]]] = {
        "T1": [{"name": "delta_cr_deg", "type": "float", "unit": "deg", "tolerance": 0.05}],
        "T2": [{"name": "t_to_delta_cr_s", "type": "float", "unit": "s", "tolerance": 0.002}],
        "T3": [
            {"name": "accel_coeff", "type": "float", "unit": "rad/s^2 per pu", "tolerance": 1e-6},
            {"name": "domega0_at_prefault", "type": "float", "unit": "rad/s", "tolerance": 1e-8},
        ],
        "T4": [
            {"name": "primary_df1_Hz", "type": "float", "unit": "Hz", "tolerance": 0.002},
            {"name": "primary_P12_MW", "type": "float", "unit": "MW", "tolerance": 0.5},
        ],
        "T5": [
            {"name": "agc_ss_df1_Hz", "type": "float", "unit": "Hz", "tolerance": 0.002},
            {"name": "agc_ss_P12_MW", "type": "float", "unit": "MW", "tolerance": 0.05},
        ],
        "T6": [
            {"name": "unit2_MW", "type": "float", "unit": "MW", "tolerance": 0.01},
            {"name": "unit2_IC", "type": "float", "unit": "Rs/MWh", "tolerance": 0.01},
            {"name": "lambda", "type": "float", "unit": "Rs/MWh", "tolerance": 0.01},
        ],
        "T7": [{"name": "unit1_IC", "type": "float", "unit": "Rs/MWh", "tolerance": 1e-4}],
        "T8": [
            {"name": "gain_margin_dB", "type": "float", "unit": "dB", "tolerance": 0.05},
            {"name": "gain_crossover_rad_s", "type": "float", "unit": "rad/s", "tolerance": 0.02},
        ],
        "T9": [{"name": "delta_deg_at_t", "type": "float", "unit": "deg", "tolerance": 0.05}],
        "T10": [{"name": "delta0_deg", "type": "float", "unit": "deg", "tolerance": 0.02}],
    }
    return fields[trap_id]


TRAP_VERIFIER_NOTES: dict[str, str] = {
    "T1": "critical_clearing_angle on SmibCase givens",
    "T2": "fault-interval time to critical angle at step h_integrator_s",
    "T3": "accel_coeff pi*f0/H; domega0 at prefault equilibrium",
    "T4": "two-area primary steady state after dpl1_pu step",
    "T5": "AGC steady state with K_agc",
    "T6": "lambda economic dispatch with unit limits",
    "T7": "incremental cost unit 1 at unit1_MW",
    "T8": "loop gain margin and crossover",
    "T9": "rotor angle at t_query_s with clearing tc_s",
    "T10": "prefault power-angle equilibrium",
}


def trap_public_schema(trap_id: str) -> dict[str, Any]:
    from electrical_engineer.benchmark_v01.public_schema import (
        field_tolerance,
        public_answer_schema,
    )

    fields = []
    for row in _trap_fields(trap_id):
        f = dict(row)
        if "tolerance" in f:
            f.update(field_tolerance(f.pop("tolerance")))
        fields.append(f)
    return public_answer_schema(fields)


TRAP_ANSWER_SCHEMAS: dict[str, dict[str, Any]] = {
    tid: trap_public_schema(tid) for tid in [f"T{i}" for i in range(1, 11)]
}

HELD_OUT_SEED_MIN = 9000
HELD_OUT_SEED_MAX = 9999


def is_held_out_seed(seed: int) -> bool:
    return HELD_OUT_SEED_MIN <= int(seed) <= HELD_OUT_SEED_MAX

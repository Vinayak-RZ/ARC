"""Answer schemas and grading rules for RLVR trap episodes."""

from __future__ import annotations

from typing import Any

TRAP_ANSWER_SCHEMAS: dict[str, dict[str, Any]] = {
    "T1": {
        "fields": [
            {"name": "delta_cr_deg", "type": "float", "unit": "deg", "tolerance": 0.05},
        ],
        "rule": "Arc smib_swing.critical_clearing_angle on episode SmibCase givens.",
    },
    "T2": {
        "fields": [
            {"name": "t_to_delta_cr_s", "type": "float", "unit": "s", "tolerance": 0.002},
        ],
        "rule": "RK4 fault trajectory to critical angle; not ode45.",
    },
    "T3": {
        "fields": [
            {"name": "accel_coeff", "type": "float", "unit": "rad/s^2 per pu", "tolerance": 1e-6},
            {"name": "domega0_at_prefault", "type": "float", "unit": "rad/s", "tolerance": 1e-8},
        ],
        "rule": "pi*f0/H and prefault acceleration zero at delta0.",
    },
    "T4": {
        "fields": [
            {"name": "primary_df1_Hz", "type": "float", "unit": "Hz", "tolerance": 0.002},
            {"name": "primary_P12_MW", "type": "float", "unit": "MW", "tolerance": 0.5},
        ],
        "rule": "Two-area primary frequency and tie after load step (Exp 7 signs).",
    },
    "T5": {
        "fields": [
            {"name": "agc_ss_df1_Hz", "type": "float", "unit": "Hz", "tolerance": 0.002},
            {"name": "agc_ss_P12_MW", "type": "float", "unit": "MW", "tolerance": 0.05},
        ],
        "rule": "AGC steady state with K given in episode givens.",
    },
    "T6": {
        "fields": [
            {"name": "unit2_MW", "type": "float", "unit": "MW", "tolerance": 0.01},
            {"name": "unit2_IC", "type": "float", "unit": "Rs/MWh", "tolerance": 0.01},
            {"name": "lambda", "type": "float", "unit": "Rs/MWh", "tolerance": 0.01},
        ],
        "rule": "Lambda dispatch with limits; bind unit 2 when PD in givens.",
    },
    "T7": {
        "fields": [
            {"name": "unit1_IC", "type": "float", "unit": "Rs/MWh", "tolerance": 1e-4},
        ],
        "rule": "IC = b + 2*c*P for unit 1 at P in givens (factor 2 required).",
    },
    "T8": {
        "fields": [
            {"name": "gain_margin_dB", "type": "float", "unit": "dB", "tolerance": 0.05},
            {"name": "gain_crossover_rad_s", "type": "float", "unit": "rad/s", "tolerance": 0.02},
        ],
        "rule": "Loop margins for plant TF in givens (python-control).",
    },
    "T9": {
        "fields": [
            {"name": "delta_deg_at_t", "type": "float", "unit": "deg", "tolerance": 0.05},
        ],
        "rule": "Handwritten RK4 clearing trajectory at (t, tc) in givens; no black-box ODE.",
    },
    "T10": {
        "fields": [
            {"name": "delta0_deg", "type": "float", "unit": "deg", "tolerance": 0.02},
        ],
        "rule": "Prefault angle from engine for Smib parameters in givens.",
    },
}

HELD_OUT_SEED_MIN = 9000
HELD_OUT_SEED_MAX = 9999


def is_held_out_seed(seed: int) -> bool:
    return HELD_OUT_SEED_MIN <= int(seed) <= HELD_OUT_SEED_MAX

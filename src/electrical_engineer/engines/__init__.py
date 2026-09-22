"""Optional EE simulation backends (ngspice, control, pandapower, PSA helpers)."""

from electrical_engineer.engines.agc_two_area import TwoAreaAgcCase, simulate_two_area
from electrical_engineer.engines.ed_lambda import EdCase, solve_lambda_ed
from electrical_engineer.engines.smib_swing import (
    SmibCase,
    critical_clearing_angle,
    critical_clearing_time_bisection,
    eec301_reference,
    initial_angle_pre_fault,
    simulate_clearing,
)

__all__ = [
    "EdCase",
    "TwoAreaAgcCase",
    "simulate_two_area",
    "solve_lambda_ed",
    "SmibCase",
    "critical_clearing_angle",
    "critical_clearing_time_bisection",
    "eec301_reference",
    "initial_angle_pre_fault",
    "simulate_clearing",
]

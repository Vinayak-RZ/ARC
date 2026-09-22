"""Optional EE simulation backends (ngspice, control, pandapower, SMIB swing)."""

from electrical_engineer.engines.smib_swing import (
    SmibCase,
    critical_clearing_angle,
    critical_clearing_time_bisection,
    eec301_reference,
    initial_angle_pre_fault,
    simulate_clearing,
)

__all__ = [
    "SmibCase",
    "critical_clearing_angle",
    "critical_clearing_time_bisection",
    "eec301_reference",
    "initial_angle_pre_fault",
    "simulate_clearing",
]

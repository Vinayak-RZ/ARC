"""Reference-backed calculation engines."""

from electrical_engineer.reference.engines.idmt import coordination_margin_s, idmt_operating_time_s
from electrical_engineer.reference.engines.iec60909 import initial_symmetrical_ka
from electrical_engineer.reference.engines.ieee80 import tolerable_voltages
from electrical_engineer.reference.engines.ieee519 import tdd_limit_percent
from electrical_engineer.reference.engines.line_params import line_sequence_per_km
from electrical_engineer.reference.engines.load_flow import run_case_load_flow
from electrical_engineer.reference.engines.mcb import magnetic_trip_in_band
from electrical_engineer.reference.engines.vector_group import phase_shift_deg

__all__ = [
    "coordination_margin_s",
    "idmt_operating_time_s",
    "initial_symmetrical_ka",
    "line_sequence_per_km",
    "magnetic_trip_in_band",
    "phase_shift_deg",
    "run_case_load_flow",
    "tdd_limit_percent",
    "tolerable_voltages",
]

"""Merged SolverSpec registry for new ee_v2 solvers."""

from __future__ import annotations

from electrical_engineer.engines.solvers import (
    circuits,
    control,
    electronics,
    em,
    machines,
    measurements,
    power,
    power_electronics,
    signals,
)
from electrical_engineer.engines.solvers.spec import Param, SolverSpec, build_kwargs

SPECS: dict[str, SolverSpec] = {}
for _mod in (
    power_electronics,
    power,
    control,
    signals,
    electronics,
    measurements,
    machines,
    em,
    circuits,
):
    overlap = set(SPECS) & set(_mod.SPECS)
    if overlap:
        raise RuntimeError(f"solver id collision in pack merge: {overlap}")
    SPECS.update(_mod.SPECS)

__all__ = ["SPECS", "Param", "SolverSpec", "build_kwargs"]

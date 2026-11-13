"""Property-style invariants for lumped linear circuits."""

from electrical_engineer.engines.circuit_properties import (
    power_balance_dc_divider,
    reciprocity_symmetric_divider,
    run_property_suite,
    superposition_voltage_divider,
)


def test_superposition_voltage_divider() -> None:
    superposition_voltage_divider()


def test_reciprocity_symmetric_divider() -> None:
    reciprocity_symmetric_divider()


def test_power_balance_dc_divider() -> None:
    power_balance_dc_divider()


def test_property_suite() -> None:
    out = run_property_suite()
    assert out["ok"] is True

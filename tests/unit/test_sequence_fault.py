"""Sequence fault analysis vs hand / phase constraints."""

from __future__ import annotations

import pytest

from electrical_engineer.engines.sequence_fault import analyze_sequence_fault


def test_lg_gold_magnitude() -> None:
    r = analyze_sequence_fault(fault_type="LG", z1_pu=0.1, z2_pu=0.1, z0_pu=0.3)
    assert r["value"] == pytest.approx(6.0, rel=1e-6)
    assert r["verified"] is True


def test_llg_bc_not_double_i1() -> None:
    z = 0.2j
    r = analyze_sequence_fault(fault_type="LLG", faulted_phases=("b", "c"), v_prefault_pu=1, z1_pu=z, z2_pu=z, z0_pu=z)
    i1 = r["I1_pu"]["mag_pu"]
    ia = r["I_phase_pu"]["a"]["mag_pu"]
    assert ia != pytest.approx(2.0 * i1, rel=0.02)
    assert r["verified"] is True


def test_three_phase_balanced_currents() -> None:
    z1 = 0.05 + 0.2j
    r = analyze_sequence_fault(fault_type="3PH", z1_pu=z1, z2_pu=z1, z0_pu=z1)
    i1 = r["I1_pu"]["mag_pu"]
    assert i1 == pytest.approx(1.0 / abs(z1), rel=1e-5)
    ia = r["I_phase_pu"]["a"]["mag_pu"]
    assert ia == pytest.approx(i1, rel=1e-5)
    ang_diff = r["I_phase_pu"]["b"]["angle_deg"] - r["I_phase_pu"]["a"]["angle_deg"]
    assert abs(abs(ang_diff) - 120.0) < 2.0


def test_phase_rotation_slg_on_b() -> None:
    ra = analyze_sequence_fault(fault_type="SLG", faulted_phases=("a",), z1_pu=0.1, z2_pu=0.1, z0_pu=0.3)
    rb = analyze_sequence_fault(fault_type="SLG", faulted_phases=("b",), z1_pu=0.1, z2_pu=0.1, z0_pu=0.3)
    assert ra["value"] == pytest.approx(rb["value"], rel=1e-6)
    assert rb["I_phase_pu"]["b"]["mag_pu"] == pytest.approx(ra["I_phase_pu"]["a"]["mag_pu"], rel=1e-5)

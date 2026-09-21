"""Sequence-network and pandapower fault study integration."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from electrical_engineer.engines.power_runner import _sequence_fault, run_power_study
from electrical_engineer.runner.execute import execute


def test_sequence_lg_matches_formula() -> None:
    i = _sequence_fault("LG", 1.0 + 0j, 0.1 + 0j, 0.1 + 0j, 0.3 + 0j)
    assert abs(i - 6.0) < 1e-9


def test_sequence_ll_matches_formula() -> None:
    i = _sequence_fault("LL", 1.0 + 0j, 0.1 + 0j, 0.1 + 0j, 0.3 + 0j)
    expected = (3**0.5) * 1.0 / (0.1 + 0.1)
    assert abs(abs(i) - expected) < 1e-9


@pytest.mark.parametrize("fault_type", ["LG", "LL", "LLG", "3PH"])
def test_power_study_writes_tables(tmp_path: Path, fault_type: str) -> None:
    out = run_power_study(tmp_path, {"fault_type": fault_type})
    assert out["ok"] is True
    assert (tmp_path / "power_tables.json").is_file()
    data = json.loads((tmp_path / "power_tables.json").read_text())
    assert "fault" in data


def test_simulate_power_fault_recipe(tmp_path: Path) -> None:
    out = execute(
        "simulate-power-fault",
        run_root=tmp_path,
        problem={"fault_type": "LG", "z1_pu": 0.1, "z2_pu": 0.1, "z0_pu": 0.3},
    )
    assert out["summary"]["unchecked"] is False
    assert out["summary"]["value"] == 6.0

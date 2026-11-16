"""Robustness: malformed lab inputs, extreme values, simulate stress."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from electrical_engineer.circuit.mcp_tools import handle_tool as circuit_mcp
from electrical_engineer.engines.spice_runner import simulator_status


def test_mcp_add_part_duplicate_id_error(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "runs").mkdir()
    rid = circuit_mcp("arc_circuit_lab_open", {"problem": {"kind": "voltage_divider", "vin": 10, "r1": 1, "r2": 1}})[
        "run_id"
    ]
    out = circuit_mcp(
        "arc_circuit_lab_add_part",
        {"run_id": rid, "id": "r1", "type": "resistor", "value": 1},
    )
    assert "error" in out or out.get("ok") is False


def test_mcp_simulate_empty_graph(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "runs").mkdir()
    rid = "empty-graph"
    (tmp_path / "runs" / rid).mkdir()
    out = circuit_mcp("arc_circuit_lab_simulate", {"run_id": rid, "problem": {}})
    assert out.get("error") or out.get("unchecked") or not out.get("ok", True)


@pytest.mark.skipif(not simulator_status().get("available"), reason="ngspice missing")
def test_extreme_component_values_simulate_or_fail_cleanly(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "runs").mkdir()
    out = circuit_mcp(
        "arc_circuit_lab_finish_solve",
        {
            "problem": {
                "kind": "voltage_divider",
                "vin": 10,
                "r1": 1e12,
                "r2": 1e-6,
                "tol": 0.5,
            }
        },
    )
    assert "verify" in out or "error" in out


def test_cli_invalid_json_problem_exit_nonzero(tmp_path: Path, monkeypatch) -> None:
    from electrical_engineer.cli import main

    monkeypatch.chdir(tmp_path)
    rid = "bad-json"
    (tmp_path / "runs" / rid).mkdir(parents=True)
    with pytest.raises(json.JSONDecodeError):
        main(["lab", "finish", "--run", rid, "--problem", "{not-json"])
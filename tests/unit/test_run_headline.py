"""Run list / problem headers: quantity = value unit."""

from __future__ import annotations

import json
from pathlib import Path

from electrical_engineer.circuit.title import run_headline, title_with_value
from electrical_engineer.runner.execute import execute


def test_rectifier_headline_format() -> None:
    assert (
        run_headline(
            "rectifier-3ph-study",
            {"topology": "full", "alpha_deg": 45},
            396.3,
            False,
        )
        == "Vo = 396.30 V"
    )


def test_idmt_headline_format() -> None:
    headline = run_headline(
        "idmt-relay-study",
        {"curve": "standard"},
        2.971,
        False,
    )
    assert headline == "Relay time t = 2.97 s"


def test_title_with_value_matches_headline() -> None:
    assert (
        title_with_value("rectifier-1ph-study", {}, 120.5, False) == "Vo = 120.50 V"
    )


def test_execute_voltage_divider_headline(tmp_path: Path) -> None:
    out = execute(
        "solve-circuit-problem",
        run_root=tmp_path,
        problem={"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000, "expected": 5.0},
    )
    run_dir = Path(out["run_dir"])
    evidentiary = json.loads((run_dir / "evidentiary.json").read_text(encoding="utf-8"))
    problem = json.loads((run_dir / "problem.json").read_text(encoding="utf-8"))
    assert not evidentiary.get("unchecked")
    assert title_with_value("solve-circuit-problem", problem, evidentiary["value"], False) == "Vout = 5.00 V"
import json
from pathlib import Path

from electrical_engineer.circuit.title import run_title
from electrical_engineer.runner.execute import execute


def test_voltage_divider_title() -> None:
    assert run_title("solve-circuit-problem", {"kind": "voltage_divider"}) == "Voltage divider · Vout"


def test_recipe_fallback_without_kind() -> None:
    assert run_title("photo-to-netlist", {}) == "photo to netlist"


def test_explicit_find() -> None:
    assert run_title("solve-circuit-problem", {"kind": "ohms_law", "find": "I"}) == "Ohm's law · I"


def test_execute_writes_title(tmp_path) -> None:
    out = execute(
        "solve-circuit-problem",
        run_root=tmp_path,
        problem={"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000, "expected": 5.0},
    )
    evidentiary = json.loads((Path(out["run_dir"]) / "evidentiary.json").read_text(encoding="utf-8"))
    assert evidentiary["title"] == "Voltage divider · Vout"
    assert out["summary"]["title"] == "Voltage divider · Vout"
    graph = json.loads((Path(out["run_dir"]) / "graph.json").read_text(encoding="utf-8"))
    refs = {n["refdes"] for n in graph["nodes"]}
    assert refs == {"Vin", "R1", "R2", "Gnd"}

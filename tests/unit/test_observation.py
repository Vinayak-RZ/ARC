import json
from pathlib import Path

from electrical_engineer.runner.execute import _UNCHECKED_REASONS, execute


def test_execute_writes_evidentiary_and_observation(tmp_path) -> None:
    out = execute(
        "solve-circuit-problem",
        run_root=tmp_path,
        problem={"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000, "expected": 5.0},
    )
    run = Path(out["run_dir"])
    evidentiary = json.loads((run / "evidentiary.json").read_text())
    summary = json.loads((run / "summary.json").read_text())
    observation = json.loads((run / "observation.json").read_text())
    assert evidentiary == summary
    assert evidentiary["unchecked"] is False
    assert observation["run_id"] == out["run_id"]
    assert observation["unchecked_reason"] is None


def test_unmatched_observation_reason(tmp_path) -> None:
    out = execute("unmatched-cosolver", run_root=tmp_path)
    observation = json.loads((Path(out["run_dir"]) / "observation.json").read_text())
    assert out["summary"]["unchecked"] is True
    assert observation["unchecked_reason"] == "unmatched"


def test_every_reason_stays_inside_the_enum(tmp_path) -> None:
    recipes = ["explain-circuits", "simulate-circuit", "photo-to-netlist", "unmatched-cosolver"]
    for recipe_id in recipes:
        out = execute(recipe_id, run_root=tmp_path, problem={"prompt": "ug ee probe"})
        observation = json.loads((Path(out["run_dir"]) / "observation.json").read_text())
        reason = observation["unchecked_reason"]
        if out["summary"]["unchecked"]:
            assert reason in _UNCHECKED_REASONS
        else:
            assert reason is None

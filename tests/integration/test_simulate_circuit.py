from electrical_engineer.catalog import load_recipe
from electrical_engineer.nodes.registry import get
from electrical_engineer.runner.execute import execute
from electrical_engineer.unchecked import UNCHECKED


def test_simulate_circuit_yaml_repair_max() -> None:
    recipe = load_recipe("simulate-circuit")
    assert recipe.nodes["spice"].extras.get("repair_max") == 2


def test_spice_exhaust_is_unchecked(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        "electrical_engineer.engines.spice_runner.spice_available",
        lambda: False,
    )
    out = get("run-spice")({"id": "sp", "repair_max": 2, "run_dir": str(tmp_path)}, {})
    assert out["ok"] is False
    assert out["exhausted"] is True
    assert out["repairs"] == 2
    assert out["token"] == UNCHECKED
    run = execute(
        "simulate-circuit",
        run_root=tmp_path,
        problem={"cir": "* broken netlist without elements\n"},
    )
    assert run["summary"]["unchecked"] is True

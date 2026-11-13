from electrical_engineer.catalog import load_recipe
from electrical_engineer.engines.circuit_multimodal import propose_netlist_from_component
from electrical_engineer.engines.circuit_verify import verify_after_derive
from electrical_engineer.runner.execute import execute


def test_derive_circuit_verify_pipeline(tmp_path) -> None:
    recipe = load_recipe("derive-circuit")
    assert "derive" in recipe.nodes
    out = execute(
        "derive-circuit",
        run_root=tmp_path,
        problem={"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000, "value": 5.0, "tol": 1e-6},
    )
    assert out["summary"]["unchecked"] is False
    assert abs(float(out["summary"]["value"]) - 5.0) < 1e-6


def test_engine_gold_smoke(tmp_path) -> None:

    from electrical_engineer.eval_runner.circuit_score import run_circuit_item
    from electrical_engineer.runner.runs import project_root

    item = project_root() / "eval" / "gold" / "circuits" / "dc-div-02"
    expect = __import__("json").loads((item / "expect.json").read_text())
    row = run_circuit_item(item, expect, run_root=tmp_path)
    assert row["ok"] is True


def test_multimodal_divider_proposal() -> None:
    prop = propose_netlist_from_component("schematic.divider")
    assert prop["ok"] is True
    assert "R1" in prop["cir"]


def test_verify_flags_independent_gold() -> None:
    out = verify_after_derive({"kind": "dc_divider", "vin": 10, "r1": 1000, "r2": 1000, "value": 5.0, "tol": 1e-6})
    assert out["gold_ok"] is True

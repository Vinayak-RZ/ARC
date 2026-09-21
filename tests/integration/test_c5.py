from electrical_engineer.catalog import load_recipe
from electrical_engineer.runner.execute import execute


def test_control_diagram_uses_compose_not_silent_spice(tmp_path) -> None:
    recipe = load_recipe("control-diagram-to-model")
    acts = {n.activity for n in recipe.nodes.values()}
    assert "compose-control-blocks" in acts
    assert "run-python-control" in acts
    assert "run-spice" not in acts
    assert "confirm-topology" not in acts
    out = execute(
        "control-diagram-to-model",
        run_root=tmp_path,
        problem={
            "blocks": [{"id": "G", "tf": "1/(s+1)"}],
            "structure": "series",
        },
    )
    assert out["summary"]["unchecked"] is False

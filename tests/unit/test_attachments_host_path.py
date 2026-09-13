from electrical_engineer.catalog import load_recipe

HOST_PATH = (
    "simulate-circuit",
    "photo-to-netlist",
    "unmatched-cosolver",
    "derive-circuit",
    "control-diagram-to-model",
)


def test_host_path_has_no_solve_explain() -> None:
    for wid in HOST_PATH:
        recipe = load_recipe(wid)
        assert all(spec.activity != "solve-explain" for spec in recipe.nodes.values()), wid


def test_host_path_names_capabilities() -> None:
    from pathlib import Path

    import yaml

    sim = yaml.safe_load(Path("workflows/circuits/simulate-circuit.yaml").read_text())
    assert sim["nodes"]["spice"]["activity"] == "lumped-circuit-sim"
    derive = yaml.safe_load(Path("workflows/circuits/derive-circuit.yaml").read_text())
    assert derive["nodes"]["check"]["activity"] == "algebraic-check"
    unmatched = yaml.safe_load(Path("workflows/_cross/unmatched-cosolver.yaml").read_text())
    assert unmatched["nodes"]["retrieve"]["activity"] == "retrieve-citation"
    assert "solve-explain" not in {n["activity"] for n in unmatched["nodes"].values()}

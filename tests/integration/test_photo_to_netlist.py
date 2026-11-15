from pathlib import Path

import yaml

from electrical_engineer.catalog import load_recipe


def test_photo_yaml_stops_after_confirm() -> None:
    recipe = load_recipe("photo-to-netlist")
    acts = {n.activity for n in recipe.nodes.values()}
    assert "confirm-topology" in acts
    assert "run-spice" not in acts
    assert recipe.nodes["summary"].needs == ("confirm",)
    raw = yaml.safe_load(Path("workflows/_cross/photo-to-netlist.yaml").read_text(encoding="utf-8"))
    blob = yaml.dump(raw)
    assert "run-spice" not in blob

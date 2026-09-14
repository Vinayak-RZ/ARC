from pathlib import Path

import yaml


def test_unmatched_has_no_sim() -> None:
    path = Path("workflows/_cross/unmatched-cosolver.yaml")
    data = yaml.safe_load(path.read_text())
    acts = {n["activity"] for n in data["nodes"].values()}
    assert "run-spice" not in acts
    assert "run-matlab-if-present" not in acts
    assert "run-simulink-if-present" not in acts
    assert "run-load-flow" not in acts
    assert "unmatched-cosolver" == data["id"]

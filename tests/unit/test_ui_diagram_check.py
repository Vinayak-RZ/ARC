from pathlib import Path

from electrical_engineer.ui_diagrams.check import check_control_diagram, check_rlc_graph
from electrical_engineer.ui_diagrams.compose import compose_agent_trial_run


def test_gold_examples_load() -> None:
    root = Path("skills/ui-diagrams/examples")
    rlc = __import__("json").loads((root / "rlc_graph.json").read_text(encoding="utf-8"))
    assert not check_rlc_graph(rlc)
    cd = __import__("json").loads((root / "unity_feedback_control_diagram.json").read_text(encoding="utf-8"))
    assert not check_control_diagram(cd)


def test_compose_agent_trial_run(tmp_path: Path) -> None:
    run_dir = compose_agent_trial_run("control", tmp_path, run_id="trl-test")
    assert (run_dir / "control_diagram.json").is_file()
    assert (run_dir / "evidentiary.json").is_file()

import json
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


def test_bad_fixtures_fail_checker() -> None:
    bad = Path("eval/gold/ui-diagrams/bad")
    rlc = json.loads((bad / "rlc_missing_gnd_graph.json").read_text(encoding="utf-8"))
    assert check_rlc_graph(rlc)
    empty = json.loads((bad / "control_empty_diagram.json").read_text(encoding="utf-8"))
    assert check_control_diagram(empty)
    nofb = json.loads((bad / "control_no_feedback.json").read_text(encoding="utf-8"))
    assert check_control_diagram(nofb)


def test_build_from_prompt() -> None:
    from electrical_engineer.ui_diagrams.build_from_prompt import build_artifact_from_prompt

    g = build_artifact_from_prompt("rlc")
    assert not check_rlc_graph(g)
    d = build_artifact_from_prompt("control")
    assert not check_control_diagram(d)

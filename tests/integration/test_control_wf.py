from pathlib import Path

from electrical_engineer.catalog import load_recipe
from electrical_engineer.runner.execute import execute


def test_solve_control_problem_yaml() -> None:
    assert load_recipe("solve-control-problem").id == "solve-control-problem"


def test_control_run_writes_plots(tmp_path) -> None:
    out = execute("solve-control-problem", run_root=tmp_path)
    run = Path(out["run_dir"])
    assert (run / "bode.png").is_file()
    assert (run / "step.png").is_file()
    assert out["summary"].get("unchecked") in {True, False}


def test_explain_control_plots(tmp_path) -> None:
    assert load_recipe("explain-control").id == "explain-control"
    out = execute("explain-control", run_root=tmp_path)
    run = Path(out["run_dir"])
    assert (run / "bode.png").is_file()
    assert (run / "step.png").is_file()

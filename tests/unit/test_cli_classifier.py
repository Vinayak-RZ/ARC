from pathlib import Path

from electrical_engineer.cli import main
from electrical_engineer.router.classify import scores_from_text
from electrical_engineer.router.hybrid import route


def test_omitted_id_unmatched(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "workflows").mkdir()
    repo = Path(__file__).resolve().parents[2]
    dest = tmp_path / "workflows" / "unmatched-cosolver.yaml"
    dest.write_text((repo / "workflows" / "_cross" / "unmatched-cosolver.yaml").read_text())
    assert main(["run"]) == 0
    out = capsys.readouterr().out
    assert "unmatched-cosolver" in out


def test_omitted_id_classifies_simulate() -> None:
    scores = scores_from_text("please simulate this netlist in spice")
    decided = route(None, scores)
    assert decided.kind == "classified"
    assert decided.recipe_id == "simulate-circuit"


def test_close_scores_ask_exit(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "workflows").mkdir()
    (tmp_path / "problem.json").write_text(
        '{"task": "ohm divider mesh nodal derive kvl kcl thevenin"}'
    )
    assert main(["run"]) == 2
    assert "ask" in capsys.readouterr().err

from pathlib import Path

from electrical_engineer.eval_runner.score import run_item, run_pack, score
from electrical_engineer.unchecked import UNCHECKED


def test_score_checked_divider(tmp_path) -> None:
    item = Path("eval/gold/circuits/mna-ladder-01")
    assert run_item(item, run_root=tmp_path)["ok"] is True


def test_score_unchecked_not_disabled_by_allow_all(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("EE_ALLOW_ALL", "1")
    item = Path("eval/gold/injection/flip-gates-01")
    row = run_item(item, run_root=tmp_path)
    assert row["summary"]["token"] == UNCHECKED
    assert row["ok"] is True


def test_score_does_not_treat_explain_value_as_checked() -> None:
    expect = {
        "recipe_id": "explain-circuits",
        "unchecked": True,
        "token": UNCHECKED,
        "citations": [{"book_id": "kuphaldt-dc", "chapter_id": "2"}],
    }
    minted = {
        "recipe_id": "explain-circuits",
        "unchecked": True,
        "token": UNCHECKED,
        "value": 3.0,
        "citations": [{"book_id": "kuphaldt-dc", "chapter_id": "2"}],
    }
    assert score(minted, expect)["ok"] is True
    fake_checked = {**minted, "unchecked": False, "token": None}
    assert score(fake_checked, expect)["ok"] is False


def test_run_pack_circuits_zero(tmp_path) -> None:
    rc = run_pack("circuits", run_root=tmp_path)
    assert rc == 0


def test_run_pack_power_psa_and_recipes_zero(tmp_path) -> None:
    rc = run_pack("power", run_root=tmp_path)
    assert rc == 0


def test_signals_complete_path_item(tmp_path) -> None:
    item = Path("eval/gold/signals/lti-path-01")
    row = run_item(item, run_root=tmp_path)
    assert row["summary"]["token"] == UNCHECKED
    assert row["ok"] is True

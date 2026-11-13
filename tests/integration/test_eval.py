from pathlib import Path

from electrical_engineer.cli import main
from electrical_engineer.eval_runner.score import iter_items


def test_eval_pack_circuits_cli(capsys) -> None:
    """CI cwd is the checkout, not a Cloud Agent /workspace path."""
    code = main(["eval", "--pack", "circuits"])
    out = capsys.readouterr().out
    assert "mna-ladder-01" in out
    assert code == 0
    assert iter_items("circuits")


def test_rag_and_explain_gold_exist() -> None:
    r = Path("eval/gold/rag-retrieval/ohms-perturbed")
    e = Path("eval/gold/explain/kvl-viva")
    assert (r / "expect.json").is_file()
    assert "kuphaldt-dc" in (r / "expect.json").read_text()
    assert (e / "expect.json").is_file()
    assert "chapter_id" in (e / "expect.json").read_text()


def test_eval_pack_rag_and_explain(capsys) -> None:
    assert main(["eval", "--pack", "rag-retrieval"]) == 0
    assert "ohms-perturbed" in capsys.readouterr().out
    assert main(["eval", "--pack", "explain"]) == 0
    assert "kvl-viva" in capsys.readouterr().out

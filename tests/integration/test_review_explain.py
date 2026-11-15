from pathlib import Path

from electrical_engineer.catalog import load_recipe


def test_review_and_explain_exist() -> None:
    assert load_recipe("review-circuit-solution").id == "review-circuit-solution"
    assert load_recipe("explain-circuits").id == "explain-circuits"
    skill = Path("skills/circuits/SKILL.md")
    assert skill.is_file()
    assert "unchecked" in skill.read_text(encoding="utf-8")

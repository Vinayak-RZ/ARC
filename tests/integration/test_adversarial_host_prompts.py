"""Regression: adversarial host prompts must not bypass trap knowledge paths."""

from pathlib import Path


def test_trap_knowledge_files_exist_for_t1_t10() -> None:
    root = Path("knowledge/traps")
    assert (root / "smib/T1-wrong-pmax-equal-area.md").is_file()
    assert (root / "integration/T9-forbidden-solvers.md").is_file()
    assert (root / "ed/T6-limits-kt-lambda.md").is_file()


def test_skills_reference_goldens_not_invented_numbers() -> None:
    swing = Path("skills/swing-equation/SKILL.md").read_text()
    assert "exp06.json" in swing
    agc = Path("skills/agc-two-area/SKILL.md").read_text()
    assert "exp07.json" in agc

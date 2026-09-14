"""Pack skills: knowledge links, retrieve scaffold, no host MATLAB tools."""

from pathlib import Path

PACKS = (
    "circuits",
    "signals",
    "electronics",
    "machines",
    "power",
    "control",
    "power_electronics",
    "measurements",
    "em",
    "maths",
)

KNOWLEDGE = {
    "circuits": "knowledge/ug-ee/circuits/INDEX.md",
    "signals": "knowledge/ug-ee/signals/INDEX.md",
    "electronics": "knowledge/ug-ee/electronics/INDEX.md",
    "machines": "knowledge/ug-ee/machines/INDEX.md",
    "power": "knowledge/ug-ee/power/INDEX.md",
    "control": "knowledge/ug-ee/control/INDEX.md",
    "power_electronics": "knowledge/ug-ee/power-electronics/INDEX.md",
    "measurements": "knowledge/ug-ee/measurements/INDEX.md",
    "em": "knowledge/ug-ee/em/INDEX.md",
    "maths": "knowledge/ug-ee/maths/INDEX.md",
}

SPAWN = {
    "circuits": "ee-circuits",
    "signals": "ee-signals",
    "electronics": "ee-electronics",
    "machines": "ee-machines",
    "power": "ee-power",
    "control": "ee-control",
    "power_electronics": "ee-power-electronics",
    "measurements": "ee-measurements",
    "em": "ee-em",
    "maths": "ee-maths",
}


def test_each_pack_has_scaffold_and_knowledge_link() -> None:
    for pack in PACKS:
        text = Path(f"skills/{pack}/SKILL.md").read_text()
        assert "## Retrieve (scaffold)" in text, pack
        assert "Index: TBD" in text, pack
        assert KNOWLEDGE[pack] in text, pack
        assert SPAWN[pack] in text, pack
        assert "evaluate_matlab_code" in text, pack
        assert "Never call `evaluate_matlab_code`" in text, pack


def test_root_and_cross_scaffold() -> None:
    root = Path("skills/SKILL.md").read_text()
    cross = Path("skills/_cross/SKILL.md").read_text()
    for text in (root, cross):
        assert "## Retrieve (scaffold)" in text
        assert "evaluate_matlab_code" in text
        assert "knowledge/ug-ee/INDEX.md" in text
    assert "hosts install" in root
    assert "ee-cross" in cross


def test_no_elective_pack_skills() -> None:
    skills = Path("skills")
    assert not (skills / "electives").exists()
    assert not (skills / "dsp").exists()

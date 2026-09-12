"""Docs contract: capability ids stay the domain names, not a single simulator."""

from pathlib import Path

CAPS = (
    "algebraic-check",
    "lumped-circuit-sim",
    "lti-analysis",
    "power-network-study",
    "machine-model",
    "converter-model",
    "signal-analysis",
    "fields-analytic",
    "measurement-model",
    "retrieve-citation",
    "render-figure",
    "ingest-figure",
    "label-unverified",
    "ask-student",
)

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


def test_capability_ids_are_documented() -> None:
    arch = Path("docs/ARCHITECTURE.md").read_text()
    workflows = Path("docs/WORKFLOWS.md").read_text()
    root = Path("skills/SKILL.md").read_text()
    cannot = Path("docs/CANNOT_DO.md").read_text()
    assert "Coverage law" in arch
    assert "this-pass freeze" in arch.lower() or "This-pass freeze" in arch
    for cap in CAPS:
        assert cap in arch
        assert cap in workflows
        assert cap in root
    assert "CD-NO-PROVIDER" in cannot
    assert "CD-YAML-GAP" in cannot


def test_every_pack_skill_names_a_capability() -> None:
    for pack in PACKS:
        text = Path(f"skills/{pack}/SKILL.md").read_text()
        assert "unchecked" in text
        assert any(cap in text for cap in CAPS), pack
    cross = Path("skills/_cross/SKILL.md").read_text()
    assert "unchecked" in cross
    assert "label-unverified" in cross

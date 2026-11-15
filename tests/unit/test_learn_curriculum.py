"""Curriculum load and validate."""

from __future__ import annotations

from electrical_engineer.learn.curriculum import (
    expand_topics,
    load_curriculum,
    validate,
)


def test_real_curriculum_validates() -> None:
    data = load_curriculum()
    assert data["schema"] == "arc.curriculum.v1"
    assert data["current_semester"] == 5
    errs = validate(data, allow_pending=True)
    assert errs == [], errs


def test_bad_recipe_caught() -> None:
    data = load_curriculum()
    # poison a provided topic
    for sem in data["semesters"]:
        if sem["n"] != 5:
            continue
        for subj in sem["subjects"]:
            if subj["id"] == "eec-303":
                subj["topics"][2]["recipes"] = ["not-a-real-recipe"]
                break
    errs = validate(data, allow_pending=True)
    assert any("not-a-real-recipe" in e for e in errs)


def test_coverage_expansion_yields_topics() -> None:
    data = load_curriculum()
    subj = next(s for sem in data["semesters"] if sem["n"] == 1 for s in sem["subjects"] if s["id"] == "eec-102")
    topics = expand_topics(subj)
    assert len(topics) == 8
    assert topics[0]["id"] == "01-charge-current-voltage-power"


def test_pending_removed_fails_until_recipes_land() -> None:
    data = load_curriculum()
    errs = validate(data, allow_pending=False)
    assert any("rectifier-3ph-study" in e or "unknown recipe" in e for e in errs)

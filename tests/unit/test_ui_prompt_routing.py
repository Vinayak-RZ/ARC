"""_recipe_from_prompt routes packs and keyword shortcuts."""

from __future__ import annotations

import pytest

from electrical_engineer.ui_server.app import _SUBJECT_RECIPE, _recipe_from_prompt

_SUBJECTS = tuple(_SUBJECT_RECIPE.keys())


@pytest.mark.parametrize("subject", _SUBJECTS)
def test_subject_routes_to_pack_recipe(subject: str) -> None:
    rid, problem = _recipe_from_prompt("analyze this", subject)
    assert rid == _SUBJECT_RECIPE[subject]
    assert "prompt" in problem


@pytest.mark.parametrize(
    ("prompt", "expected_recipe"),
    (
        ("plot the bode diagram", "solve-control-problem"),
        ("equal area swing curve", "smib-swing-study"),
        ("find vout on the divider", "solve-circuit-problem"),
        ("dc motor drive speed", "solve-drives-problem"),
    ),
)
def test_keyword_shortcuts(prompt: str, expected_recipe: str) -> None:
    rid, _ = _recipe_from_prompt(prompt, "signals")
    assert rid == expected_recipe


def test_swing_beats_power_subject() -> None:
    rid, _ = _recipe_from_prompt("swing equation after fault", "power")
    assert rid == "smib-swing-study"
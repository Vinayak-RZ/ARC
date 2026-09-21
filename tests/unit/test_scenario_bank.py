"""The corpus must be gradeable: every scenario carries a contract expectation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "kernel_harden"))

from annotate_scenarios import BANK, check, expectation, missing_providers
from trial_driver import grade

from electrical_engineer.runner.execute import _UNCHECKED_REASONS

SCENARIOS = sorted(BANK.glob("*/*.json"))


def test_bank_is_not_empty() -> None:
    assert len(SCENARIOS) >= 100


def test_bank_matches_the_contract() -> None:
    assert check(SCENARIOS) == []


def test_expected_reasons_stay_inside_the_enum() -> None:
    for path in SCENARIOS:
        expect = json.loads(path.read_text(encoding="utf-8"))["expect"]
        assert expect["reason"] is None or expect["reason"] in _UNCHECKED_REASONS


@pytest.mark.parametrize(
    ("recipe_id", "problem", "reason"),
    [
        ("unmatched-cosolver", {"prompt": "x"}, "unmatched"),
        ("simulate-after-confirm", {"cir": "* x\n"}, "gate-closed"),
        ("photo-to-netlist", {"prompt": "x"}, "gate-closed"),
        ("explain-signals", {"prompt": "x"}, "labeled"),
    ],
)
def test_expectation_table(recipe_id: str, problem: dict, reason: str) -> None:
    assert expectation(recipe_id, problem)["reason"] == reason


def test_simulate_circuit_expectation_when_spice_present() -> None:
    exp = expectation("simulate-circuit", {"cir": "* x\n"})
    if missing_providers("simulate-circuit"):
        assert exp["reason"] == "no-provider"
    else:
        assert exp["reason"] == "labeled"


def test_grade_rejects_a_wrong_reason() -> None:
    expect = {"unchecked": True, "reason": "labeled", "requires": []}
    assert grade(expect, True, "labeled") == "pass"
    assert grade(expect, True, "unmatched") == "fail"
    assert grade(expect, False, None) == "fail"


def test_grade_skips_when_the_optional_provider_is_present() -> None:
    expect = {"unchecked": True, "reason": "no-provider", "requires": ["write-run-summary"]}
    assert grade(expect, False, None) == "skip"

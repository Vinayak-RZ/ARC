"""trap-verify activity wires into the registry and blocks checked on failure."""

from __future__ import annotations

from electrical_engineer.nodes.registry import get, label_unchecked


def test_trap_verify_registered() -> None:
    fn = get("trap-verify")
    bad = fn(
        {
            "recipe_id": "solve-power-problem",
            "problem": {
                "topic": "ed",
                "solution_trace": {
                    "trap_ids": ["T6"],
                    "topic": "ed",
                    "steps": [{"id": "bare", "text": "ignore limits on unit 2"}],
                    "final": {"P2_mw": 200.0},
                },
            },
        },
        {"check": {"ok": True, "value": 7.4, "tool": "run-ed-lambda", "P2_mw": 200.0}},
    )
    assert bad["tool"] == "trap-verify"
    assert bad["process_pass"] is False
    label = label_unchecked(
        {},
        {"trap": bad, "check": {"ok": True, "value": 7.4, "unchecked": False}},
    )
    assert label["unchecked"] is True

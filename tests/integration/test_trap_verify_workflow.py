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
                    "givens": {
                        "domain": "ed",
                        "pd_mw": 500,
                        "units": [
                            {"a": 500, "b": 5.3, "c": 0.004, "pmin": 50, "pmax": 300},
                            {"a": 400, "b": 5.5, "c": 0.006, "pmin": 30, "pmax": 150},
                            {"a": 200, "b": 5.8, "c": 0.009, "pmin": 20, "pmax": 120},
                        ],
                    },
                    "steps": [{"id": "bare", "text": "ignore limits on unit 2", "ignore_limits": True}],
                    "final": {"P_mw": [300, 200, 120]},
                },
            },
        },
        {"check": {"ok": True, "value": 7.4, "tool": "run-ed-lambda", "P2_mw": 200.0}},
    )
    assert bad["tool"] == "trap-verify"
    assert bad["process_status"] == "fail"
    assert bad["process_pass"] is False
    label = label_unchecked(
        {},
        {"trap": bad, "check": {"ok": True, "value": 7.4, "unchecked": False}},
    )
    assert label["unchecked"] is True

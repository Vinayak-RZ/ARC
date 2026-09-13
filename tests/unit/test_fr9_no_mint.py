from electrical_engineer.nodes.photo import solve_explain
from electrical_engineer.unchecked import UNCHECKED


def test_solve_explain_ohms_stays_unchecked() -> None:
    out = solve_explain({"problem": {"kind": "ohms_law", "v": 10, "r": 2}}, {})
    assert out["unchecked"] is True
    assert out.get("unchecked") is not False
    assert out["token"] == UNCHECKED


def test_solve_explain_divider_stays_unchecked() -> None:
    out = solve_explain(
        {"problem": {"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000}},
        {},
    )
    assert out["unchecked"] is True
    assert out["token"] == UNCHECKED

"""Golden checks for EEC-301 Exp 8 λ-iteration ED."""

from __future__ import annotations

from electrical_engineer.engines.ed_lambda import EdCase, solve_lambda_ed
from electrical_engineer.engines.eec301_goldens import load_exp08_golden


def test_ed_cases_match_exp08_json() -> None:
    gold = load_exp08_golden()
    case = EdCase.eec301_default()
    for key in ("PD_450", "PD_500", "PD_300"):
        g = gold["cases"][key]
        r = solve_lambda_ed(case, g["PD"])
        assert abs(r["lam"] - g["lam"]) < 1e-9
        for i in range(3):
            assert abs(r["P"][i] - g["P"][i]) < 1e-6
        assert r["status"] == g["status"]


def test_pd_500_unit2_at_max() -> None:
    gold = load_exp08_golden()["cases"]["PD_500"]
    r = solve_lambda_ed(EdCase.eec301_default(), 500.0)
    assert r["status"][1] == "at_max"
    assert r["P"][1] == gold["P"][1] == 150.0
    assert r["IC"][1] < r["lam"]

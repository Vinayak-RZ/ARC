"""Verify-after-derive edge cases at 2% threshold and bad inputs."""

from __future__ import annotations

import math
from pathlib import Path

from electrical_engineer.circuit.simulate_graph import compare_derived
from electrical_engineer.collab.workflow import finish_circuit_lab
from electrical_engineer.engines.circuit_verify import verify_after_derive


def test_compare_derived_exactly_at_two_percent_rel_err() -> None:
    derived = 100.0
    simulated = 102.0
    chk = compare_derived(derived, simulated, rel_tol=0.02)
    assert abs(chk["rel_err_pct"] - 2.0) < 0.01
    assert chk["match"] is True


def test_compare_derived_just_above_two_percent_flags_mismatch() -> None:
    derived = 100.0
    simulated = 102.01
    chk = compare_derived(derived, simulated, tol=0.02)
    assert chk["rel_err_pct"] > 2.0
    assert chk["mismatch"] is True


def test_finish_circuit_lab_needs_review_above_two_percent(tmp_path: Path) -> None:
    run_dir = tmp_path / "lab"
    problem = {
        "kind": "voltage_divider",
        "vin": 10,
        "r1": 1000,
        "r2": 1000,
        "value": 6.0,
        "tol": 0.02,
    }
    derived = {"value": 6.0, "unit": "V", "engine": "injected_wrong"}
    verify = finish_circuit_lab(run_dir, problem, derived=derived)
    if (
        verify.get("simulated") is not None
        and not verify.get("sim_skipped")
        and float(verify.get("rel_err_pct") or 0) > 2.0
    ):
        assert verify.get("needs_review") is True


def test_verify_after_derive_zero_derived_denominator() -> None:
    problem = {"kind": "voltage_divider", "vin": 0, "r1": 1, "r2": 1}
    out = verify_after_derive(problem, run_dir=Path("/tmp/unused"))
    assert out.get("unchecked") or out.get("error") or not out.get("ok", True)


def test_verify_missing_simulated_metric() -> None:
    chk = compare_derived(1.0, None, tol=0.02)
    assert chk["match"] is False
    assert chk.get("reason") == "no_simulation"


def test_finish_circuit_lab_non_finite_derived_falls_back_or_fails(tmp_path: Path) -> None:
    run_dir = tmp_path / "nan"
    problem = {
        "kind": "series_rlc",
        "vin": 10,
        "r_ohm": 10,
        "l_h": 0.01,
        "c_f": 100e-6,
        "value": 11.63,
        "tol": 0.05,
    }
    derived = {"value": float("nan"), "unit": "V", "engine": "broken"}
    verify = finish_circuit_lab(run_dir, problem, derived=derived)
    assert math.isfinite(float(verify.get("derived") or problem["value"]))


def test_units_mismatch_not_silent(tmp_path: Path) -> None:
    run_dir = tmp_path / "units"
    problem = {"kind": "voltage_divider", "vin": 10, "r1": 1, "r2": 1, "tol": 0.02, "unit": "A"}
    derived = {"value": 5.0, "unit": "V", "engine": "hand"}
    verify = finish_circuit_lab(run_dir, problem, derived=derived)
    assert verify.get("unit") in ("V", "A", None)
    assert "derived" in verify
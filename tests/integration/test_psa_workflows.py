"""PSA workflows execute checked-in with lab-grade numerics."""

from __future__ import annotations

import json
from pathlib import Path

from electrical_engineer.runner.execute import execute


def test_smib_swing_study_checked(tmp_path) -> None:
    result = execute("smib-swing-study", run_root=tmp_path)
    summary = json.loads((Path(result["run_dir"]) / "evidentiary.json").read_text())
    assert summary["unchecked"] is False
    assert abs(float(summary["value"]) - 79.53240997193419) < 1e-6
    assert (Path(result["run_dir"]) / "psa_smib.json").is_file()


def test_agc_two_area_study_checked(tmp_path) -> None:
    result = execute("agc-two-area-study", run_root=tmp_path)
    summary = json.loads((Path(result["run_dir"]) / "evidentiary.json").read_text())
    assert summary["unchecked"] is False
    assert abs(float(summary["value"])) < 0.01


def test_ed_lambda_study_checked(tmp_path) -> None:
    result = execute("ed-lambda-study", run_root=tmp_path)
    summary = json.loads((Path(result["run_dir"]) / "evidentiary.json").read_text())
    assert summary["unchecked"] is False
    assert (Path(result["run_dir"]) / "psa_ed.json").is_file()

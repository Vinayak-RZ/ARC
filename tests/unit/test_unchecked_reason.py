"""Regression: honest unchecked_reason after I1."""

from __future__ import annotations

import json
from pathlib import Path

from electrical_engineer.runner.execute import execute


def test_explain_uses_labeled_not_unmatched(tmp_path: Path) -> None:
    out = execute("explain-circuits", run_root=tmp_path, problem={"prompt": "state KVL"})
    obs = json.loads((Path(out["run_dir"]) / "observation.json").read_text(encoding="utf-8"))
    assert out["summary"]["unchecked"] is True
    assert obs["unchecked_reason"] == "labeled"


def test_unmatched_recipe_stays_unmatched(tmp_path: Path) -> None:
    out = execute("unmatched-cosolver", run_root=tmp_path)
    obs = json.loads((Path(out["run_dir"]) / "observation.json").read_text(encoding="utf-8"))
    assert out["summary"]["unchecked"] is True
    assert obs["unchecked_reason"] == "unmatched"

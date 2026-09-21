"""Regression: honest unchecked_reason after I1/I3.

`labeled` is the residual bucket: the kernel answered and said the answer is
unverified. Anything the host can act on (install a provider, confirm a draft)
must report its own reason instead.
"""

from __future__ import annotations

import json
from pathlib import Path

from electrical_engineer.runner.execute import execute


def _reason(out: dict) -> str | None:
    obs = json.loads((Path(out["run_dir"]) / "observation.json").read_text(encoding="utf-8"))
    return obs["unchecked_reason"]


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


def test_absent_tool_reports_no_provider(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(
        "electrical_engineer.engines.control_runner.control_available",
        lambda: False,
    )
    out = execute("solve-control-problem", run_root=tmp_path, problem={"prompt": "step of 1/(s+1)"})
    assert out["summary"]["unchecked"] is True
    assert _reason(out) == "no-provider"


def test_awaiting_confirm_reports_gate_closed(tmp_path: Path) -> None:
    out = execute("photo-to-netlist", run_root=tmp_path, problem={"prompt": "read this figure"})
    run = Path(out["run_dir"])
    assert (run / "draft.cir").is_file() and not (run / "confirmed.json").is_file()
    assert _reason(out) == "gate-closed"


def test_verified_run_has_no_reason(tmp_path: Path) -> None:
    out = execute(
        "solve-circuit-problem",
        run_root=tmp_path,
        problem={"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000, "expected": 5.0},
    )
    assert out["summary"]["unchecked"] is False
    assert _reason(out) is None

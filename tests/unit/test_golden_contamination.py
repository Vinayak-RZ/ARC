"""Golden contamination audit: derived must not ignore a perturbed declared gold."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from electrical_engineer.collab.workflow import finish_circuit_lab, finish_control_lab
from electrical_engineer.control_studio.simulate import simulate
from electrical_engineer.control_studio.goldens import GOLDENS
from electrical_engineer.engines.circuit_derive import derive


_REPO = Path(__file__).resolve().parents[2]
_SCAN_GLOBS = (
    "scripts/**/*.py",
    "scripts/**/*.json",
    "tests/**/*.py",
    "workflows/**/*.yaml",
    "artifacts/**/*.json",
    "src/electrical_engineer/ui_server/app.py",
    "src/electrical_engineer/collab/workflow.py",
    "src/electrical_engineer/nodes/sim.py",
)


def _iter_scan_files() -> list[Path]:
    out: list[Path] = []
    for pattern in _SCAN_GLOBS:
        out.extend(_REPO.glob(pattern))
    return sorted({p for p in out if p.is_file()})


def test_audit_golden_declared_paths_documented() -> None:
    """Find problem payloads that set value/expected while also naming derive kinds."""
    hits: list[str] = []
    for path in _iter_scan_files():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "derived_value" in text and "golden" in text:
            hits.append(str(path.relative_to(_REPO)))
        if "declared_gold" in text:
            hits.append(str(path.relative_to(_REPO)))
    assert any("nodes/sim.py" in h for h in hits)
    assert any("collab/workflow.py" in h for h in hits)


def test_circuit_derived_moves_when_declared_value_perturbed(tmp_path: Path) -> None:
    prob = {
        "kind": "voltage_divider",
        "vin": 10,
        "r1": 1000,
        "r2": 1000,
        "tol": 1e-3,
        "allow_template_fallback": True,
    }
    d0 = derive(prob)
    prob_bad = {**prob, "value": 99.0}
    run_a = tmp_path / "a"
    run_b = tmp_path / "b"
    v0 = finish_circuit_lab(run_a, prob)
    v1 = finish_circuit_lab(run_b, prob_bad)
    assert abs(float(v0["derived"]) - float(d0["value"])) < 1e-6
    assert abs(float(v1["derived"]) - float(d0["value"])) < 1e-6
    assert float(v1["derived"]) != 99.0


def test_injected_wrong_derived_must_not_equal_perturbed_gold(tmp_path: Path) -> None:
    prob = {"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000, "tol": 0.02}
    wrong = {"value": 8.0, "unit": "V", "engine": "host_typo"}
    verify = finish_circuit_lab(tmp_path / "inj", prob, derived=wrong)
    assert float(verify["derived"]) == 8.0
    if verify.get("simulated") is not None and not verify.get("sim_skipped"):
        assert verify.get("mismatch") is True or verify.get("needs_review") is True


@pytest.mark.xfail(
    strict=True,
    reason="ARC-TE-005: finish_control_lab reads y_final but simulate exposes y_ss; simulated stays None",
)
def test_control_seed_derived_mismatch_when_derived_value_perturbed(tmp_path: Path) -> None:
    pytest.importorskip("control")
    diagram = GOLDENS["unity_first_order"]()
    sim = simulate(diagram)
    assert sim.get("ok")
    y_ss = float(sim["y_ss"])
    verify_ok = finish_control_lab(
        tmp_path / "ok",
        {"kind": "unity_feedback", "golden": "unity_first_order"},
        derived_value=y_ss,
    )
    verify_bad = finish_control_lab(
        tmp_path / "bad",
        {"kind": "unity_feedback", "golden": "unity_first_order"},
        derived_value=y_ss + 5.0,
    )
    assert verify_ok.get("mismatch") is False
    assert verify_bad.get("mismatch") is True


def test_capture_script_bad_derive_documented_in_scripts() -> None:
    text = (_REPO / "scripts/capture_collab_lab_screenshots.py").read_text(encoding="utf-8")
    assert "11.963" in text
    meta = _REPO / "artifacts/collab_capture_meta.json"
    if meta.is_file():
        blob = json.loads(meta.read_text(encoding="utf-8"))
        assert isinstance(blob, dict)
"""IITR pass-2 gap recipes — block diagram, protection, drives, digital."""

from __future__ import annotations

from pathlib import Path

from electrical_engineer.runner.execute import execute


def test_control_block_diagram_feedback(tmp_path: Path) -> None:
    out = execute(
        "control-diagram-to-model",
        run_root=tmp_path,
        problem={
            "blocks": [
                {"id": "G", "tf": "10/(s+1)"},
                {"id": "H", "tf": "1"},
            ],
            "unity_feedback": {"forward": "G", "feedback": "H", "negative": True},
        },
    )
    assert out["summary"]["unchecked"] is False
    run = Path(out["run_dir"])
    assert (run / "bode.png").is_file()
    assert (run / "step.png").is_file()


def test_protection_overcurrent_trip(tmp_path: Path) -> None:
    out = execute(
        "study-protection-setting",
        run_root=tmp_path,
        problem={
            "ct_primary_a": 300,
            "ct_secondary_a": 5,
            "relay_pickup_a": 2.0,
            "fault_current_a": 800,
        },
    )
    assert out["summary"]["unchecked"] is False
    assert out["summary"]["value"] == 1.0


def test_dc_drive_speed(tmp_path: Path) -> None:
    out = execute(
        "solve-drives-problem",
        run_root=tmp_path,
        problem={"kind": "dc", "v_dc": 120, "ra_ohm": 1, "k_torque": 0.5, "t_load_nm": 5},
    )
    assert out["summary"]["unchecked"] is False
    # omega = (120 - 1*10)/0.5 = 220 rad/s -> rpm ≈ 2100.6
    assert abs(float(out["summary"]["value"]) - 2100.6) < 1.0


def test_digital_discrete_stable(tmp_path: Path) -> None:
    out = execute(
        "solve-digital-control-problem",
        run_root=tmp_path,
        problem={"num": [0.1], "den": [1.0, -0.5], "ts": 0.01},
    )
    assert out["summary"]["unchecked"] is False
    assert float(out["summary"]["value"]) < 1.0

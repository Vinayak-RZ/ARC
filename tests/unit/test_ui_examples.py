"""Home examples and the work/diagram files those examples need."""

import json

from fastapi.testclient import TestClient

from electrical_engineer.control.diagram import control_diagram_for_recipe
from electrical_engineer.ui_diagrams.check import check_control_diagram
from electrical_engineer.ui_server.app import create_app
from electrical_engineer.ui_server.work_steps import work_steps

_EXAMPLE_IDS = (
    "divider",
    "rlc-step",
    "control-step",
    "digital-stable",
    "smib-swing",
    "lg-fault",
    "ed-dispatch",
    "buck-ccm",
    "dc-drive",
)


def test_examples_are_nine_varied(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("EE_NO_SEED", "1")
    body = TestClient(create_app(tmp_path)).get("/api/examples").json()
    ids = [ex["id"] for ex in body["examples"]]
    assert ids == list(_EXAMPLE_IDS)
    assert "signals-fft" not in ids


def test_divider_work_steps(tmp_path) -> None:
    run = tmp_path / "run"
    run.mkdir()
    (run / "problem.json").write_text(
        json.dumps({"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000}),
        encoding="utf-8",
    )
    (run / "evidentiary.json").write_text(
        json.dumps({"recipe_id": "solve-circuit-problem", "value": 5.0, "unchecked": False}),
        encoding="utf-8",
    )
    steps = work_steps(run)
    assert any(step.get("equation") == "Vout = Vin × R2 / (R1 + R2)" for step in steps)
    assert any("5.000 V" in step["result"] for step in steps)


def test_run_detail_includes_work_and_activity(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("EE_NO_SEED", "1")
    run = tmp_path / "runs" / "div1"
    run.mkdir(parents=True)
    (run / "problem.json").write_text(
        json.dumps({"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000}),
        encoding="utf-8",
    )
    (run / "summary.json").write_text(
        json.dumps({"recipe_id": "solve-circuit-problem", "value": 5.0, "unchecked": False}),
        encoding="utf-8",
    )
    (run / "trace.jsonl").write_text(
        json.dumps(
            {
                "name": "node.end",
                "duration_ms": 12,
                "attrs": {"node_id": "solve", "ok": True, "unchecked": False},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    body = TestClient(create_app(tmp_path)).get("/api/runs/div1").json()
    assert body["work_steps"][1]["equation"].startswith("Vout")
    assert body["activity_feed"][0]["role"] == "Draft the solution"
    assert body["activity_feed"][0]["duration_ms"] == 12


def test_seed_writes_missing_figures(tmp_path) -> None:
    from electrical_engineer.runner.seed_visuals import seed_run_visuals

    rlc = tmp_path / "rlc"
    rlc.mkdir()
    seed_run_visuals(
        rlc,
        "simulate-circuit",
        {"kind": "series_rlc", "r_ohm": 10, "l_h": 0.01, "c_f": 100e-6, "v_step": 10},
    )
    assert (rlc / "step.png").is_file()
    assert (rlc / "graph.json").is_file()

    divider = tmp_path / "div"
    divider.mkdir()
    seed_run_visuals(
        divider,
        "solve-circuit-problem",
        {"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000},
    )
    assert "Vout = 5.00 V" in (divider / "artifact.svg").read_text(encoding="utf-8")

    buck = tmp_path / "buck"
    buck.mkdir()
    seed_run_visuals(
        buck,
        "study-power-electronics-v2",
        {"solver": "ccm_buck", "vin": 12, "vout": 5, "i_out": 1},
    )
    assert (buck / "buck.png").is_file()
    assert json.loads((buck / "control_diagram.json").read_text(encoding="utf-8"))["diagramKind"] == "buck_ccm"


def test_study_diagrams_pass_checker() -> None:
    cases = (
        ("smib-swing-study", {"prompt": "SMIB swing"}, "smib_swing"),
        ("solve-digital-control-problem", {"num": [0.1], "den": [1, -0.5], "ts": 0.01}, "digital_loop"),
        ("ed-lambda-study", {"PD": 500}, "dispatch_ed"),
        ("study-power-electronics-v2", {"solver": "ccm_buck", "vin": 12, "vout": 5}, "buck_ccm"),
    )
    for recipe, problem, kind in cases:
        diagram = control_diagram_for_recipe(recipe, problem)
        assert diagram is not None
        assert diagram["diagramKind"] == kind
        assert check_control_diagram(diagram) == []

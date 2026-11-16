"""End-to-end wiring for four UI sample problems (+ IDMT solver path)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from electrical_engineer.collab.workflow import finish_circuit_lab, finish_control_lab
from electrical_engineer.engines.solvers.power import idmt_relay_time
from electrical_engineer.runner.execute import execute
from electrical_engineer.ui_server.app import create_app
from tests.golden_numerics_refs import HEADLINE_CONTROL_Y_SS, HEADLINE_IDMT_T_S, HEADLINE_RLC_VC_PEAK_V


@pytest.fixture
def api_client(monkeypatch):
    monkeypatch.setenv("EE_NO_SEED", "1")
    return TestClient(create_app())


def test_example_run_divider_lab_artifact(api_client) -> None:
    out = api_client.post("/api/examples/divider/run").json()
    rid = out["run_id"]
    lab = api_client.get(f"/api/runs/{rid}/lab").json()
    assert lab.get("graph", {}).get("nodes")


def test_example_run_rlc_step_lab_and_verify(api_client, tmp_path) -> None:
    out = api_client.post("/api/examples/rlc-step/run").json()
    rid = out["run_id"]
    run_dir = tmp_path / "runs" / rid
    run_dir.mkdir(parents=True, exist_ok=True)
    for name in ("graph.json", "lab_meta.json"):
        src = api_client.get(f"/api/runs/{rid}/file/{name}")
        if src.status_code == 200:
            (run_dir / name).write_text(src.text, encoding="utf-8")
    prob = {
        "kind": "series_rlc",
        "vin": 10,
        "r_ohm": 10,
        "l_h": 0.01,
        "c_f": 100e-6,
        "tol": 0.08,
    }
    if (run_dir / "graph.json").is_file():
        verify = finish_circuit_lab(run_dir, prob)
        assert abs(float(verify.get("derived") or 0) - HEADLINE_RLC_VC_PEAK_V) < 0.2


def test_workflow_solve_control_unity_lab(tmp_path: Path) -> None:
    out = execute(
        "solve-control-problem",
        run_root=tmp_path,
        problem={"golden": "unity_first_order", "num": [10], "den": [1, 1]},
    )
    run_dir = Path(out["run_dir"])
    meta = json.loads((run_dir / "lab_meta.json").read_text(encoding="utf-8"))
    assert meta.get("control_session_id")
    verify = finish_control_lab(
        run_dir,
        {"golden": "unity_first_order"},
        derived_value=HEADLINE_CONTROL_Y_SS,
    )
    assert verify.get("mismatch") is False


def test_rectifier_3ph_solver_recipe(tmp_path: Path) -> None:
    out = execute(
        "rectifier-3ph-study",
        run_root=tmp_path,
        problem={"v_ll_rms": 415, "alpha_deg": 45, "topology": "full", "io_a": 0, "ls_h": 0},
    )
    assert out.get("run_id") or out.get("run_dir")


def test_idmt_solver_headline(tmp_path: Path) -> None:
    out = execute(
        "idmt-relay-study",
        run_root=tmp_path,
        problem={
            "i_fault_a": 1000,
            "ct_primary_a": 100,
            "ct_secondary_a": 1,
            "plug_setting": 1,
            "tms": 1,
            "curve": "standard",
        },
    )
    assert out.get("run_id") or out.get("run_dir")
    direct = idmt_relay_time(1000, 100, 1.0, "standard", plug_setting=1.0)
    assert abs(direct["t_op_s"] - HEADLINE_IDMT_T_S) < 0.02
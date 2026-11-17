"""Human circuit edits refresh verification at the current graph revision."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from electrical_engineer.circuit.run_session import apply_graph, load_graph
from electrical_engineer.collab.lab_meta import load_lab_meta
from electrical_engineer.engines.rlc_transient import series_rlc_step
from electrical_engineer.runner.execute import execute
from electrical_engineer.ui_server.app import create_app


@pytest.mark.skipif(
    not __import__("shutil").which("ngspice"),
    reason="ngspice required",
)
def test_human_r1_edit_reverify_disagrees_at_current_revision(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("EE_NO_SEED", "1")
    (tmp_path / "runs").mkdir()
    meta = series_rlc_step(10, 0.01, 100e-6, 10.0)
    out = execute(
        "series-rlc-transient",
        run_root=tmp_path,
        problem={
            "kind": "series_rlc",
            "vin": 10,
            "r_ohm": 10,
            "l_h": 0.01,
            "c_f": 100e-6,
            "analysis": "tran",
            "t_s": float(meta["t_Vc_peak_s"]),
            "probe": "v(3)",
            "tol": 0.02,
        },
    )
    run_dir = Path(out["run_dir"])
    rid = run_dir.name
    verify0 = json.loads((run_dir / "lab_verify.json").read_text(encoding="utf-8"))
    assert int(verify0.get("graph_revision") or 0) >= 1
    graph = load_graph(run_dir)
    edited = copy.deepcopy(graph)
    for node in edited["nodes"]:
        if node.get("id") == "r1":
            node["value"] = 20
    apply_graph(run_dir, edited, author="human", op="set", target="r1", detail={"field": "value", "after": 20})
    meta_lab = load_lab_meta(run_dir)
    verify = json.loads((run_dir / "lab_verify.json").read_text(encoding="utf-8"))
    assert verify.get("graph_revision") == meta_lab["revision"]
    assert not verify.get("stale")
    sim_v = float(verify["simulated"])
    assert abs(sim_v - 10.0) < 0.15
    assert verify.get("mismatch") is not True
    assert verify.get("needs_review") is not True
    assert verify.get("derivation_matches_graph") is False
    row = verify["metrics"][0]
    assert row.get("derived_out_of_date")
    client = TestClient(create_app(tmp_path))
    lab = client.get(f"/api/runs/{rid}/lab").json()
    assert lab["lab_verify"]["graph_revision"] == meta_lab["revision"]
    assert not lab["lab_verify"].get("stale")
    assert lab["lab_verify"].get("verdict_current") is not False
    assert lab["lab_verify"].get("derivation_matches_graph") is False
    assert lab["lab_verify"].get("needs_review") is not True


def test_two_control_runs_use_distinct_sessions(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    a = execute(
        "solve-control-problem",
        run_root=tmp_path,
        problem={"tf": "1/(s+1)", "prompt": "A"},
    )
    b = execute(
        "solve-control-problem",
        run_root=tmp_path,
        problem={"tf": "10/(s+1)", "prompt": "B"},
    )
    meta_a = json.loads((Path(a["run_dir"]) / "lab_meta.json").read_text(encoding="utf-8"))
    meta_b = json.loads((Path(b["run_dir"]) / "lab_meta.json").read_text(encoding="utf-8"))
    assert meta_a["control_session_id"] != meta_b["control_session_id"]
    va = json.loads((Path(a["run_dir"]) / "lab_verify.json").read_text(encoding="utf-8"))
    vb = json.loads((Path(b["run_dir"]) / "lab_verify.json").read_text(encoding="utf-8"))
    ya = next(m for m in va["metrics"] if m["id"] == "y_ss")
    yb = next(m for m in vb["metrics"] if m["id"] == "y_ss")
    assert ya["derived"] == pytest.approx(0.5, rel=0.02)
    assert ya["simulated"] == pytest.approx(0.5, rel=0.05)
    assert yb["derived"] == pytest.approx(10 / 11, rel=0.02)
    assert yb["simulated"] == pytest.approx(10 / 11, rel=0.05)
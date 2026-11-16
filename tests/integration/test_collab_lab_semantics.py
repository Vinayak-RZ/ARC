"""Collaboration semantics: MCP, API, revisions, restore, SSE ordering."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from electrical_engineer.circuit.mcp_tools import handle_tool as circuit_mcp
from electrical_engineer.circuit.run_session import apply_graph, load_graph
from electrical_engineer.collab.lab_meta import load_lab_meta
from electrical_engineer.ui_server.app import create_app


def test_op_log_actor_label_and_monotonic_revision(tmp_path: Path) -> None:
    run_dir = tmp_path / "runs" / "rev-test"
    run_dir.mkdir(parents=True)
    base = {
        "schema": "arc.circuit.v1",
        "nodes": [{"id": "gnd", "type": "ground", "refdes": "G", "value": 0, "x": 0, "y": 0}],
        "edges": [],
    }
    a1 = apply_graph(run_dir, base, author="agent", op="seed")
    a2 = apply_graph(run_dir, base, author="human", op="ui_save")
    meta = load_lab_meta(run_dir)
    assert a2["revision"] > a1["revision"]
    assert meta["op_log"][-1]["actor_label"] == "You"
    assert meta["op_log"][-2]["actor_label"] == "Agent"
    assert meta["op_log"][-1]["rev"] == meta["revision"]


def test_mcp_and_api_interleaved_edits_preserve_last_write(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("EE_NO_SEED", "1")
    (tmp_path / "runs").mkdir()
    opened = circuit_mcp(
        "arc_circuit_lab_open",
        {"problem": {"kind": "voltage_divider", "vin": 12, "r1": 1000, "r2": 1000}},
    )
    rid = opened["run_id"]
    run_dir = tmp_path / "runs" / rid
    graph = load_graph(run_dir)
    graph["nodes"] = [
        n if n["id"] != "r1" else {**n, "value": 2000} for n in graph["nodes"] if n.get("id")
    ]
    client = TestClient(create_app(tmp_path))
    put = client.put(f"/api/runs/{rid}/graph", json=graph)
    assert put.status_code == 200
    get_mcp = circuit_mcp("arc_circuit_lab_get", {"run_id": rid})
    r1 = next(n for n in get_mcp["graph"]["nodes"] if n.get("refdes") == "R1" or n.get("id") == "r1")
    assert float(r1["value"]) == 2000.0
    meta = load_lab_meta(run_dir)
    authors = {e["author"] for e in meta["op_log"]}
    assert "agent" in authors and "human" in authors


def test_restore_returns_agent_baseline_graph(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("EE_NO_SEED", "1")
    (tmp_path / "runs").mkdir()
    out = circuit_mcp(
        "arc_circuit_lab_finish_solve",
        {"problem": {"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000, "tol": 1e-3}},
    )
    rid = out["run_id"]
    run_dir = tmp_path / "runs" / rid
    baseline = json.loads((run_dir / "graph.json").read_text(encoding="utf-8"))
    mutated = json.loads(json.dumps(baseline))
    for n in mutated["nodes"]:
        if n.get("type") == "resistor" and n.get("id") in ("r1", "R1"):
            n["value"] = 9999
    apply_graph(run_dir, mutated, author="human", op="ui_save")
    client = TestClient(create_app(tmp_path))
    restored = client.post(f"/api/runs/{rid}/lab/restore")
    assert restored.status_code == 200
    after = load_graph(run_dir)
    assert len(after.get("nodes") or []) == len(baseline.get("nodes") or [])
    r_after = {n["id"]: n.get("value") for n in after["nodes"] if n.get("type") == "resistor"}
    r_base = {n["id"]: n.get("value") for n in baseline["nodes"] if n.get("type") == "resistor"}
    assert r_after == r_base


def test_run_events_publish_increments_revision(tmp_path: Path) -> None:
    from electrical_engineer.collab.run_events import publish

    rid = "evt-01"
    run_dir = tmp_path / "runs" / rid
    run_dir.mkdir(parents=True)
    base = {
        "schema": "arc.circuit.v1",
        "nodes": [{"id": "gnd", "type": "ground", "refdes": "G", "value": 0, "x": 0, "y": 0}],
        "edges": [],
    }
    a = apply_graph(run_dir, base, author="agent", op="seed")
    publish(rid, {"type": "graph", "revision": a["revision"]})
    b = apply_graph(run_dir, base, author="human", op="save")
    publish(rid, {"type": "graph", "revision": b["revision"]})
    assert b["revision"] > a["revision"]


def test_mcp_get_idempotent_on_retry(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "runs").mkdir()
    rid = circuit_mcp(
        "arc_circuit_lab_open",
        {"problem": {"kind": "voltage_divider", "vin": 5, "r1": 1, "r2": 1}},
    )["run_id"]
    a = circuit_mcp("arc_circuit_lab_get", {"run_id": rid})
    b = circuit_mcp("arc_circuit_lab_get", {"run_id": rid})
    assert a["graph"] == b["graph"]
    assert a["lab_meta"]["revision"] == b["lab_meta"]["revision"]
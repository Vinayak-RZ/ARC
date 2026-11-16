"""In-process SSE: revisions must be monotonic when subscribing via TestClient."""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from electrical_engineer.ui_server.app import create_app


@pytest.fixture
def client(tmp_path: Path, monkeypatch) -> TestClient:
    monkeypatch.setenv("EE_NO_SEED", "1")
    return TestClient(create_app(tmp_path))


@pytest.mark.xfail(strict=True, reason="ARC-TE-007: SSE consumer receives no data events (TestClient or run_events)")
def test_sse_delivers_graph_revisions_in_process(client: TestClient) -> None:
    rid = "inproc-sse"
    base_graph = {
        "schema": "arc.circuit.v1",
        "nodes": [{"id": "gnd", "type": "ground", "refdes": "G", "value": 0, "x": 0, "y": 0}],
        "edges": [],
    }
    client.put(f"/api/runs/{rid}/graph", json=base_graph)
    revisions: list[int] = []
    stop = threading.Event()

    def reader() -> None:
        with client.stream("GET", f"/api/runs/{rid}/events") as resp:
            for chunk in resp.iter_text():
                if stop.is_set():
                    break
                for line in chunk.splitlines():
                    if not line.startswith("data:"):
                        continue
                    payload = json.loads(line[5:].strip())
                    if payload.get("type") == "graph" and "revision" in payload:
                        revisions.append(int(payload["revision"]))

    th = threading.Thread(target=reader, daemon=True)
    th.start()
    time.sleep(0.2)
    for _ in range(3):
        client.put(f"/api/runs/{rid}/graph", json=base_graph)
    time.sleep(0.4)
    stop.set()
    th.join(timeout=3)
    assert len(revisions) >= 1
    assert revisions == sorted(revisions)
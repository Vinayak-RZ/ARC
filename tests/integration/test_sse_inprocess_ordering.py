"""In-process SSE: revisions must be monotonic when subscribing via live HTTP."""

from __future__ import annotations

import json
import os
import subprocess
import threading
import time
from pathlib import Path

import httpx
import pytest

_REPO = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def inproc_ui_server():
    env = {
        **os.environ,
        "EE_NO_BROWSER": "1",
        "EE_NO_SEED": "1",
    }
    proc = subprocess.Popen(
        ["uv", "run", "electrical-engineer", "ui"],
        cwd=_REPO,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    base = "http://127.0.0.1:8765"
    for _ in range(90):
        try:
            r = httpx.get(f"{base}/api/health", timeout=2.0)
            if r.status_code == 200:
                break
        except httpx.HTTPError:
            pass
        time.sleep(1.0)
    else:
        proc.kill()
        pytest.fail("UI server did not become healthy")
    yield base
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


def test_sse_delivers_graph_revisions_in_process(inproc_ui_server: str) -> None:
    rid = "inproc-sse"
    base = inproc_ui_server
    base_graph = {
        "schema": "arc.circuit.v1",
        "nodes": [
            {"id": "gnd", "type": "ground", "refdes": "G", "value": 0, "unit": "", "x": 0, "y": 0}
        ],
        "edges": [],
    }
    httpx.put(f"{base}/api/runs/{rid}/graph", json=base_graph, timeout=30.0)
    revisions: list[int] = []
    stop = threading.Event()

    def reader() -> None:
        try:
            with (
                httpx.Client(timeout=None) as client,
                client.stream("GET", f"{base}/api/runs/{rid}/events") as resp,
            ):
                for line in resp.iter_lines():
                    if stop.is_set():
                        break
                    if not line.startswith("data:"):
                        continue
                    payload = json.loads(line[5:].strip())
                    if payload.get("type") == "graph" and "revision" in payload:
                        revisions.append(int(payload["revision"]))
        except Exception:
            stop.set()
            raise

    th = threading.Thread(target=reader, daemon=True)
    th.start()
    time.sleep(0.2)
    for _ in range(3):
        httpx.put(f"{base}/api/runs/{rid}/graph", json=base_graph, timeout=30.0)
    time.sleep(0.4)
    stop.set()
    th.join(timeout=3)
    assert len(revisions) >= 1
    assert revisions == sorted(revisions)

"""Live UI server: SSE revision ordering and concurrent human/agent edits."""

from __future__ import annotations

import json
import os
import subprocess
import threading
import time
from pathlib import Path

import httpx
import pytest

def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


pytestmark = pytest.mark.skipif(
    not os.environ.get("ARC_LIVE_UI"),
    reason="set ARC_LIVE_UI=1 when UI already running on :8765",
)


@pytest.fixture(scope="module")
def live_ui_server():
    root = _repo_root()
    env = {**os.environ, "EE_NO_BROWSER": "1", "EE_NO_SEED": "1"}
    proc = subprocess.Popen(
        ["uv", "run", "electrical-engineer", "ui"],
        cwd=root,
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


def test_sse_revision_order_under_concurrent_edits(live_ui_server: str) -> None:
    base = live_ui_server
    seed = httpx.post(f"{base}/api/examples/divider/run", timeout=120.0)
    assert seed.status_code == 200, seed.text
    rid = seed.json()["run_id"]
    revisions: list[int] = []
    errors: list[str] = []
    stop = threading.Event()

    def reader() -> None:
        try:
            with httpx.Client(timeout=None) as client:
                with client.stream("GET", f"{base}/api/runs/{rid}/events") as resp:
                    assert resp.status_code == 200
                    for line in resp.iter_lines():
                        if stop.is_set():
                            break
                        if not line.startswith("data:"):
                            continue
                        payload = json.loads(line[5:].strip())
                        if payload.get("type") == "graph" and "revision" in payload:
                            revisions.append(int(payload["revision"]))
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))

    th = threading.Thread(target=reader, daemon=True)
    th.start()
    time.sleep(0.35)

    graph = httpx.get(f"{base}/api/runs/{rid}/lab", timeout=30.0).json().get("graph") or {}
    agent_graph = json.loads(json.dumps(graph))
    for n in agent_graph.get("nodes", []):
        if n.get("type") == "resistor" and n.get("id") == "r1":
            n["value"] = 1200.0
    agent_put = httpx.put(f"{base}/api/runs/{rid}/graph", json=agent_graph, timeout=30.0)
    assert agent_put.status_code == 200, agent_put.text

    for val in (1500.0, 2200.0, 1800.0):
        human = json.loads(json.dumps(graph))
        for n in human.get("nodes", []):
            if n.get("type") == "resistor" and n.get("id") == "r1":
                n["value"] = val
        put = httpx.put(f"{base}/api/runs/{rid}/graph", json=human, timeout=30.0)
        assert put.status_code == 200, put.text
        time.sleep(0.1)

    time.sleep(0.6)
    stop.set()
    th.join(timeout=8.0)
    assert not errors, errors
    assert len(revisions) >= 2
    assert revisions == sorted(revisions)
    meta = httpx.get(f"{base}/api/runs/{rid}/lab", timeout=30.0).json()
    assert int(meta["lab_meta"]["revision"]) >= max(revisions)
    r1 = next(n for n in meta["graph"]["nodes"] if n.get("id") == "r1")
    assert float(r1["value"]) == 1800.0
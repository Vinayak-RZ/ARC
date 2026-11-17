"""SSE fan-out for run-scoped circuit lab edits (mirrors studio_events)."""

from __future__ import annotations

import asyncio
import json
import queue
import time
from collections import defaultdict
from collections.abc import AsyncIterator
from functools import partial
from typing import Any

_subscribers: dict[str, list[queue.Queue]] = defaultdict(list)

_HEARTBEAT_S = 15.0
_POLL_S = 0.2


def publish(run_id: str, event: dict[str, Any]) -> None:
    payload = {"run_id": run_id, **event}
    for q in list(_subscribers.get(run_id, [])):
        try:
            q.put_nowait(payload)
        except queue.Full:
            pass


def _lab_meta_stamp(run_id: str) -> int | None:
    """Latest mtime of the shared lab files; agents editing over MCP run in another process."""
    from electrical_engineer.runner.runs import project_root

    run_dir = project_root() / "runs" / run_id
    stamps = []
    for name in ("lab_meta.json", "lab_verify.json", "lab_simulate.json"):
        try:
            stamps.append((run_dir / name).stat().st_mtime_ns)
        except OSError:
            continue
    return max(stamps) if stamps else None


def _lab_revision(run_id: str) -> int:
    from electrical_engineer.runner.runs import project_root

    path = project_root() / "runs" / run_id / "lab_meta.json"
    try:
        return int(json.loads(path.read_text(encoding="utf-8")).get("revision") or 0)
    except (OSError, ValueError, TypeError):
        return 0


async def sse_stream(run_id: str) -> AsyncIterator[str]:
    q: queue.Queue = queue.Queue(maxsize=64)
    _subscribers[run_id].append(q)
    loop = asyncio.get_running_loop()
    hello = {"run_id": run_id, "type": "hello", "revision": 0}
    stamp = _lab_meta_stamp(run_id)
    try:
        yield f"data: {json.dumps(hello)}\n\n"
        yield ": connected\n\n"
        last_hb = time.monotonic()
        while True:
            try:
                item = await loop.run_in_executor(None, partial(q.get, timeout=_POLL_S))
            except queue.Empty:
                # Edits made by an agent in another process (MCP stdio, CLI) never reach
                # publish() here, so watch the shared lab file as well.
                cur = _lab_meta_stamp(run_id)
                if cur is not None and cur != stamp:
                    stamp = cur
                    ev = {"run_id": run_id, "type": "graph", "revision": _lab_revision(run_id), "source": "disk"}
                    yield f"data: {json.dumps(ev)}\n\n"
                    continue
                now = time.monotonic()
                if now - last_hb >= _HEARTBEAT_S:
                    hb = {"run_id": run_id, "type": "heartbeat", "ts_ms": int(time.time() * 1000)}
                    yield f"data: {json.dumps(hb)}\n\n"
                    last_hb = now
                else:
                    yield ": keep-alive\n\n"
                continue
            stamp = _lab_meta_stamp(run_id)
            yield f"data: {json.dumps(item)}\n\n"
    finally:
        if q in _subscribers.get(run_id, []):
            _subscribers[run_id].remove(q)

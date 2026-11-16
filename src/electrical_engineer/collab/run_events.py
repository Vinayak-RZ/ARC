"""SSE fan-out for run-scoped circuit lab edits (mirrors studio_events)."""

from __future__ import annotations

import asyncio
import json
import queue
import time
from collections import defaultdict
from functools import partial
from typing import Any, AsyncIterator

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


async def sse_stream(run_id: str) -> AsyncIterator[str]:
    q: queue.Queue = queue.Queue(maxsize=64)
    _subscribers[run_id].append(q)
    loop = asyncio.get_running_loop()
    hello = {"run_id": run_id, "type": "hello", "revision": 0}
    try:
        yield f"data: {json.dumps(hello)}\n\n"
        yield ": connected\n\n"
        last_hb = time.monotonic()
        while True:
            try:
                item = await loop.run_in_executor(None, partial(q.get, timeout=_POLL_S))
            except queue.Empty:
                now = time.monotonic()
                if now - last_hb >= _HEARTBEAT_S:
                    hb = {"run_id": run_id, "type": "heartbeat", "ts_ms": int(time.time() * 1000)}
                    yield f"data: {json.dumps(hb)}\n\n"
                    last_hb = now
                else:
                    yield ": keep-alive\n\n"
                continue
            yield f"data: {json.dumps(item)}\n\n"
    finally:
        if q in _subscribers.get(run_id, []):
            _subscribers[run_id].remove(q)
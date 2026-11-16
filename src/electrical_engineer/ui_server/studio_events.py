"""Thread-safe SSE fan-out for Control Studio sessions."""

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


def publish(session_id: str, event: dict[str, Any]) -> None:
    payload = {"session_id": session_id, **event}
    for q in list(_subscribers.get(session_id, [])):
        try:
            q.put_nowait(payload)
        except queue.Full:
            pass


async def sse_stream(session_id: str) -> AsyncIterator[str]:
    q: queue.Queue = queue.Queue(maxsize=64)
    _subscribers[session_id].append(q)
    loop = asyncio.get_running_loop()
    hello = {"session_id": session_id, "type": "hello", "revision": 0}
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
                    hb = {"session_id": session_id, "type": "heartbeat", "ts_ms": int(time.time() * 1000)}
                    yield f"data: {json.dumps(hb)}\n\n"
                    last_hb = now
                else:
                    yield ": keep-alive\n\n"
                continue
            yield f"data: {json.dumps(item)}\n\n"
    finally:
        if q in _subscribers.get(session_id, []):
            _subscribers[session_id].remove(q)
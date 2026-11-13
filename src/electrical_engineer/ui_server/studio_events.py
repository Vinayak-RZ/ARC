"""Thread-safe SSE fan-out for Control Studio sessions."""

from __future__ import annotations

import asyncio
import json
import queue
from collections import defaultdict
from typing import Any

_subscribers: dict[str, list[queue.Queue]] = defaultdict(list)


def publish(session_id: str, event: dict[str, Any]) -> None:
    payload = {"session_id": session_id, **event}
    for q in list(_subscribers.get(session_id, [])):
        try:
            q.put_nowait(payload)
        except queue.Full:
            pass


async def sse_stream(session_id: str):
    q: queue.Queue = queue.Queue(maxsize=64)
    _subscribers[session_id].append(q)
    try:
        publish(session_id, {"type": "hello", "revision": 0})
        while True:
            item = await asyncio.to_thread(q.get)
            yield f"data: {json.dumps(item)}\n\n"
    finally:
        if q in _subscribers.get(session_id, []):
            _subscribers[session_id].remove(q)

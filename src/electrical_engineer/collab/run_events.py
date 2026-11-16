"""SSE fan-out for run-scoped circuit lab edits (mirrors studio_events)."""

from __future__ import annotations

import asyncio
import json
import queue
from collections import defaultdict
from typing import Any

_subscribers: dict[str, list[queue.Queue]] = defaultdict(list)


def publish(run_id: str, event: dict[str, Any]) -> None:
    payload = {"run_id": run_id, **event}
    for q in list(_subscribers.get(run_id, [])):
        try:
            q.put_nowait(payload)
        except queue.Full:
            pass


async def sse_stream(run_id: str):
    q: queue.Queue = queue.Queue(maxsize=64)
    _subscribers[run_id].append(q)
    try:
        publish(run_id, {"type": "hello", "revision": 0})
        while True:
            item = await asyncio.to_thread(q.get)
            yield f"data: {json.dumps(item)}\n\n"
    finally:
        if q in _subscribers.get(run_id, []):
            _subscribers[run_id].remove(q)
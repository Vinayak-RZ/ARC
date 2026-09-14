"""Stdlib append-only JSONL span writer for kernel runs (no OTel)."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1"


class TraceWriter:
    """Append span events to ``trace.jsonl`` under a run directory."""

    def __init__(self, run_dir: Path, trace_id: str) -> None:
        self.run_dir = Path(run_dir)
        self.trace_id = trace_id
        self.path = self.run_dir / "trace.jsonl"
        self._seq = 0

    def _emit(
        self,
        name: str,
        *,
        parent_span_id: str | None = None,
        duration_ms: float | None = None,
        attrs: dict[str, Any] | None = None,
    ) -> str:
        self._seq += 1
        span_id = f"{self.trace_id}-{self._seq}"
        event = {
            "schema_version": SCHEMA_VERSION,
            "trace_id": self.trace_id,
            "span_id": span_id,
            "parent_span_id": parent_span_id,
            "name": name,
            "ts_ms": int(time.time() * 1000),
            "duration_ms": duration_ms,
            "attrs": attrs or {},
        }
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, default=str) + "\n")
        return span_id

    def run_start(self, *, recipe_id: str) -> str:
        return self._emit("run.start", attrs={"recipe_id": recipe_id})

    def run_end(
        self,
        *,
        recipe_id: str,
        unchecked: bool,
        unchecked_reason: str | None,
        parent_span_id: str | None,
    ) -> str:
        return self._emit(
            "run.end",
            parent_span_id=parent_span_id,
            attrs={
                "recipe_id": recipe_id,
                "unchecked": unchecked,
                "unchecked_reason": unchecked_reason,
            },
        )

    def node_start(
        self,
        *,
        node_id: str,
        activity: str,
        recipe_id: str,
        parent_span_id: str | None,
    ) -> str:
        return self._emit(
            "node.start",
            parent_span_id=parent_span_id,
            attrs={"node_id": node_id, "activity": activity, "recipe_id": recipe_id},
        )

    def node_end(
        self,
        *,
        node_id: str,
        activity: str,
        recipe_id: str,
        parent_span_id: str | None,
        duration_ms: float,
        ok: bool | None,
        unchecked: bool,
    ) -> str:
        return self._emit(
            "node.end",
            parent_span_id=parent_span_id,
            duration_ms=duration_ms,
            attrs={
                "node_id": node_id,
                "activity": activity,
                "recipe_id": recipe_id,
                "ok": ok,
                "unchecked": unchecked,
            },
        )

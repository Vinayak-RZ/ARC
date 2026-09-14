"""Map Arc ``trace.jsonl`` into an Unagent-custom payload (no OTel)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not path.is_file():
        return events
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if isinstance(obj, dict):
            events.append(obj)
    return events


def to_unagent_custom(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a minimal custom-adapter document Unagent can load offline."""
    spans = []
    for ev in events:
        spans.append(
            {
                "id": ev.get("span_id"),
                "trace_id": ev.get("trace_id"),
                "parent_id": ev.get("parent_span_id"),
                "name": ev.get("name"),
                "start_time_unix_nano": int(ev.get("ts_ms") or 0) * 1000000,
                "duration_ms": ev.get("duration_ms"),
                "attributes": ev.get("attrs") or {},
            }
        )
    return {
        "adapter": "custom",
        "source": "electrical_engineer.trace_jsonl",
        "schema_version": "1",
        "spans": spans,
    }


def export_run(run_dir: Path) -> dict[str, Any]:
    return to_unagent_custom(load_jsonl(Path(run_dir) / "trace.jsonl"))


def write_export(run_dir: Path, dest: Path | None = None) -> Path:
    payload = export_run(run_dir)
    out = Path(dest) if dest else Path(run_dir) / "unagent_custom.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


def to_unagent_events(events: list[dict[str, Any]], *, recipe_id: str | None = None) -> dict[str, Any]:
    """House JSON ``{events:[...]}`` for Unagent ``--adapter custom``.

    Honest ``unchecked`` is **not** a hard error. Only explicit ``ok is False``
    counts as ``error`` (I2 — Improveness/Unagent export hygiene).
    """
    out_events: list[dict[str, Any]] = []
    for ev in events:
        attrs = ev.get("attrs") or {}
        hard_error = attrs.get("ok") is False
        out_events.append(
            {
                "name": ev.get("name"),
                "node": attrs.get("node_id") or attrs.get("activity") or ev.get("name"),
                "op": "execute_tool" if str(ev.get("name") or "").startswith("node.") else "invoke_workflow",
                "input": {"recipe_id": attrs.get("recipe_id") or recipe_id},
                "output": {"ok": attrs.get("ok"), "unchecked": attrs.get("unchecked")},
                "error": hard_error,
            }
        )
    return {"events": out_events}

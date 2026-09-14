"""Unit tests for Unagent custom export (stdlib JSON only)."""

from __future__ import annotations

import json
from pathlib import Path

from electrical_engineer.export.unagent_adapter import load_jsonl, to_unagent_custom, write_export
from electrical_engineer.runner.execute import execute


def test_to_unagent_custom_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "trace.jsonl"
    path.write_text(
        json.dumps(
            {
                "schema_version": "1",
                "trace_id": "t1",
                "span_id": "t1-1",
                "parent_span_id": None,
                "name": "run.start",
                "ts_ms": 1,
                "duration_ms": None,
                "attrs": {"recipe_id": "demo"},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    events = load_jsonl(path)
    doc = to_unagent_custom(events)
    assert doc["adapter"] == "custom"
    assert doc["spans"][0]["name"] == "run.start"
    assert "opentelemetry" not in json.dumps(doc).lower()


def test_write_export_from_execute(tmp_path: Path) -> None:
    out = execute("unmatched-cosolver", run_root=tmp_path)
    dest = write_export(Path(out["run_dir"]))
    payload = json.loads(dest.read_text(encoding="utf-8"))
    assert payload["adapter"] == "custom"
    assert len(payload["spans"]) >= 2

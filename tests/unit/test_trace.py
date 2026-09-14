"""Contract tests for stdlib JSONL tracing."""

from __future__ import annotations

import json
from pathlib import Path

from electrical_engineer.runner.execute import execute
from electrical_engineer.runner.trace import SCHEMA_VERSION, TraceWriter


def test_trace_writer_emits_schema(tmp_path: Path) -> None:
    tw = TraceWriter(tmp_path, "tid")
    root = tw.run_start(recipe_id="demo")
    mid = tw.node_start(node_id="n1", activity="act", recipe_id="demo", parent_span_id=root)
    tw.node_end(
        node_id="n1",
        activity="act",
        recipe_id="demo",
        parent_span_id=mid,
        duration_ms=1.5,
        ok=True,
        unchecked=False,
    )
    tw.run_end(recipe_id="demo", unchecked=False, unchecked_reason=None, parent_span_id=root)
    lines = (tmp_path / "trace.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 4
    names = [json.loads(line)["name"] for line in lines]
    assert names == ["run.start", "node.start", "node.end", "run.end"]
    for line in lines:
        obj = json.loads(line)
        assert obj["schema_version"] == SCHEMA_VERSION
        assert obj["trace_id"] == "tid"


def test_execute_writes_trace_jsonl(tmp_path: Path) -> None:
    out = execute(
        "solve-circuit-problem",
        run_root=tmp_path,
        problem={
            "kind": "voltage_divider",
            "vin": 10,
            "r1": 1000,
            "r2": 1000,
            "expected": 5.0,
        },
    )
    run = Path(out["run_dir"])
    trace_path = run / "trace.jsonl"
    assert trace_path.is_file()
    events = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert events[0]["name"] == "run.start"
    assert events[-1]["name"] == "run.end"
    assert any(e["name"] == "node.end" for e in events)
    assert (run / "observation.json").is_file()
    retrieve = next(e for e in events if e["name"] == "node.end" and e["attrs"]["node_id"] == "retrieve")
    assert retrieve["attrs"]["ok"] is None

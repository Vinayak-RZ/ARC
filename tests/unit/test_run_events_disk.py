import asyncio
import json
from pathlib import Path

from electrical_engineer.collab.run_events import sse_stream


def test_sse_reports_lab_edits_made_by_another_process(tmp_path: Path, monkeypatch) -> None:
    # An agent on MCP stdio writes lab_meta.json from its own process; publish() never fires here.
    (tmp_path / "workflows").mkdir()
    run = tmp_path / "runs" / "r1"
    run.mkdir(parents=True)
    meta = run / "lab_meta.json"
    meta.write_text(json.dumps({"revision": 1}), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    async def scenario() -> list[dict]:
        gen = sse_stream("r1")
        got = []
        assert "hello" in await gen.__anext__()
        await gen.__anext__()  # ": connected"
        await asyncio.sleep(0.05)
        meta.write_text(json.dumps({"revision": 2}), encoding="utf-8")
        for _ in range(20):
            chunk = await gen.__anext__()
            if chunk.startswith("data:"):
                got.append(json.loads(chunk[5:]))
                break
        await gen.aclose()
        return got

    events = asyncio.run(scenario())
    assert events and events[0]["type"] == "graph" and events[0]["revision"] == 2

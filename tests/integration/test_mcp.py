import json

from electrical_engineer.mcp.server import TOOLS, handle


def test_list_and_run_tools() -> None:
    names = {t["name"] for t in TOOLS}
    assert "list_workflows" in names
    assert "run_workflow" in names
    assert 5 <= len(names) <= 7
    listed = handle("tools/list", {})
    assert "tools" in listed
    started = handle(
        "tools/call", {"name": "run_workflow", "arguments": {"workflow_id": "unmatched-cosolver"}}
    )
    body = json.loads(started["content"][0]["text"])
    assert body["waits"] is False
    assert started.get("isError") is not True

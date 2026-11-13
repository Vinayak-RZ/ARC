import json

from electrical_engineer.mcp.server import handle


def test_list_visual_components() -> None:
    raw = handle("tools/call", {"name": "list_visual_components", "arguments": {}})
    body = json.loads(raw["content"][0]["text"])
    assert "power.swing_equal_area" in body["components"]
    assert body["waits"] is False

import json

import pytest

from electrical_engineer.control_studio.goldens import GOLDENS
from electrical_engineer.control_studio.mcp_tools import handle_tool
from electrical_engineer.engines.control_runner import control_available


def test_mcp_create_and_pid_loop() -> None:
    out = handle_tool("control_studio_create_diagram", {"title": "MCP demo"})
    assert "session_id" in out
    sid = out["session_id"]
    for op in (
        ("control_studio_add_block", {"session_id": sid, "block_id": "r", "type": "step"}),
        ("control_studio_add_block", {"session_id": sid, "block_id": "sum1", "type": "sum", "params": {"signs": "+-"}}),
        ("control_studio_add_block", {"session_id": sid, "block_id": "pid1", "type": "pid", "params": {"kp": 2.0, "ki": 0.2, "kd": 0.05}}),
        ("control_studio_add_block", {"session_id": sid, "block_id": "motor", "type": "plant_dc_motor"}),
        ("control_studio_add_block", {"session_id": sid, "block_id": "y", "type": "scope"}),
    ):
        res = handle_tool(op[0], op[1])
        assert "error" not in res, res
    wires = [
        ("w1", "r:out", "sum1:in1"),
        ("w2", "sum1:out", "pid1:in"),
        ("w3", "pid1:out", "motor:in"),
        ("w4", "motor:out", "y:in"),
        ("w5", "motor:out", "sum1:feedback"),
    ]
    for wid, fr, to in wires:
        handle_tool("control_studio_connect", {"session_id": sid, "wire_id": wid, "from": fr, "to": to})
    val = handle_tool("control_studio_validate", {"session_id": sid})
    assert val.get("ok") is True
    handle_tool("control_studio_set_param", {"session_id": sid, "block_id": "pid1", "params": {"kp": 3.5}})
    if control_available():
        sim = handle_tool("control_studio_simulate", {"session_id": sid})
        assert sim.get("ok") is True
        an = handle_tool("control_studio_analyze", {"session_id": sid})
        assert an.get("ok") is True
        assert an.get("paths", {}).get("bode")
        assert "gain_margin_db" in an and "phase_margin_deg" in an


def test_mcp_seed_golden() -> None:
    diagram = GOLDENS["unity_first_order"]()
    out = handle_tool("control_studio_create_diagram", {"title": "golden", "seed_diagram": diagram})
    sid = out["session_id"]
    exp = handle_tool("control_studio_export", {"session_id": sid})
    assert exp["diagram"]["id"] == diagram["id"]

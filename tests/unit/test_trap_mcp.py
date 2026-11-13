"""MCP arc_trap_verify returns PRM payload."""

from __future__ import annotations

from electrical_engineer.mcp.server import handle


def test_arc_trap_verify_mcp() -> None:
    out = handle(
        "tools/call",
        {
            "name": "arc_trap_verify",
            "arguments": {
                "solution_trace": {
                    "trap_ids": ["T6"],
                    "steps": [{"id": "s1", "text": "λ-ED with limits", "P2_mw": 150.0}],
                    "final": {"P2_mw": 150.0, "expected": {"P2_mw": 150.0}},
                }
            },
        },
    )
    text = out["content"][0]["text"]
    assert '"tool": "trap-verify"' in text
    assert '"process_status"' in text

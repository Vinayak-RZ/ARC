#!/usr/bin/env python3
"""Build PID DC motor loop via MCP handlers; write artifact paths for README."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from electrical_engineer.control_studio.mcp_tools import handle_tool  # noqa: E402

OUT = Path("/opt/cursor/artifacts")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    created = handle_tool("control_studio_create_diagram", {"title": "DC motor PID demo"})
    sid = created["session_id"]
    steps = [
        ("r", "step"),
        ("sum1", "sum"),
        ("pid1", "pid"),
        ("motor", "plant_dc_motor"),
        ("y", "scope"),
    ]
    for bid, btype in steps:
        params = {"signs": "+-"} if btype == "sum" else {"kp": 2.0, "ki": 0.5, "kd": 0.1} if btype == "pid" else {}
        handle_tool(
            "control_studio_add_block",
            {"session_id": sid, "block_id": bid, "type": btype, "params": params, "x": 100, "y": 120},
        )
    for wid, fr, to in [
        ("w1", "r:out", "sum1:in1"),
        ("w2", "sum1:out", "pid1:in"),
        ("w3", "pid1:out", "motor:in"),
        ("w4", "motor:out", "y:in"),
        ("w5", "motor:out", "sum1:feedback"),
    ]:
        handle_tool("control_studio_connect", {"session_id": sid, "wire_id": wid, "from": fr, "to": to})
    handle_tool("control_studio_auto_layout", {"session_id": sid})
    val = handle_tool("control_studio_validate", {"session_id": sid})
    sim = handle_tool("control_studio_simulate", {"session_id": sid})
    an = handle_tool("control_studio_analyze", {"session_id": sid})
    handle_tool("control_studio_set_param", {"session_id": sid, "block_id": "pid1", "params": {"kp": 4.0}})
    an2 = handle_tool("control_studio_analyze", {"session_id": sid})
    summary = {
        "session_id": sid,
        "validate": val,
        "simulate": {k: sim.get(k) for k in ("ok", "y_ss", "step_png")},
        "analyze_before": {k: an.get(k) for k in ("ok", "phase_margin_deg", "gain_margin_db")},
        "analyze_after_kp4": {k: an2.get(k) for k in ("ok", "phase_margin_deg", "gain_margin_db")},
    }
    (OUT / "control_studio_demo_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    for key in ("step_png",):
        src = sim.get(key)
        if src and Path(src).is_file():
            shutil.copy(src, OUT / "control_studio_demo_step.png")
    bode = (an2.get("paths") or {}).get("bode")
    if bode and Path(bode).is_file():
        shutil.copy(bode, OUT / "control_studio_demo_bode.png")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

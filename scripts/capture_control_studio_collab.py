#!/usr/bin/env python3
"""Capture populated UI + GIF of MCP building a control loop (requires UI on :8765)."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUT = Path("/opt/cursor/artifacts")
OUT.mkdir(parents=True, exist_ok=True)

from electrical_engineer.control_studio.mcp_tools import handle_tool  # noqa: E402


def main() -> int:
    from playwright.sync_api import sync_playwright

    base = "http://127.0.0.1:8765/?view=control-studio"
    frames: list[Path] = []
    populated = OUT / "control_studio_populated_1280x800.png"
    sid = handle_tool(
        "control_studio_create_diagram", {"title": "PID · DC motor", "golden": "pid_dc_motor"}
    )["session_id"]
    handle_tool("control_studio_simulate", {"session_id": sid})
    handle_tool("control_studio_analyze", {"session_id": sid})
    url_golden = f"{base}&session={sid}"

    build_sid = None
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(url_golden, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(1500)
        page.get_by_role("button", name="Simulate").click()
        page.wait_for_selector(".studio-results img", timeout=20000)
        page.wait_for_timeout(800)
        page.screenshot(path=str(populated), full_page=True)
        sid2 = handle_tool("control_studio_create_diagram", {"title": "Agent build", "golden": None})["session_id"]
        build_sid = sid2
        url = f"{base}&session={sid2}"
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(1200)
        shot0 = OUT / "studio_frame_00.png"
        page.screenshot(path=str(shot0))
        frames.append(shot0)
        steps = [
            lambda: handle_tool("control_studio_add_block", {"session_id": sid2, "block_id": "r", "type": "step", "x": 40, "y": 160}),
            lambda: handle_tool("control_studio_add_block", {"session_id": sid2, "block_id": "sum1", "type": "sum", "x": 160, "y": 160}),
            lambda: handle_tool("control_studio_add_block", {"session_id": sid2, "block_id": "g1", "type": "gain", "x": 280, "y": 160, "params": {"k": 2}}),
            lambda: handle_tool("control_studio_add_block", {"session_id": sid2, "block_id": "p1", "type": "plant_first_order", "x": 400, "y": 160, "params": {"k": 10, "tau": 1}}),
            lambda: handle_tool("control_studio_add_block", {"session_id": sid2, "block_id": "y", "type": "scope", "x": 560, "y": 160}),
            lambda: handle_tool("control_studio_connect", {"session_id": sid2, "wire_id": "w1", "from": "r:out", "to": "sum1:in1"}),
            lambda: handle_tool("control_studio_connect", {"session_id": sid2, "wire_id": "w2", "from": "sum1:out", "to": "g1:in"}),
            lambda: handle_tool("control_studio_connect", {"session_id": sid2, "wire_id": "w3", "from": "g1:out", "to": "p1:in"}),
            lambda: handle_tool("control_studio_connect", {"session_id": sid2, "wire_id": "w4", "from": "p1:out", "to": "y:in"}),
            lambda: handle_tool("control_studio_connect", {"session_id": sid2, "wire_id": "w5", "from": "p1:out", "to": "sum1:feedback"}),
            lambda: handle_tool("control_studio_simulate", {"session_id": sid2}),
        ]
        for i, step in enumerate(steps, start=1):
            step()
            page.wait_for_timeout(700)
            frame = OUT / f"studio_frame_{i:02d}.png"
            page.screenshot(path=str(frame))
            frames.append(frame)
        browser.close()

    try:
        from PIL import Image

        imgs = [Image.open(f).convert("P", palette=Image.ADAPTIVE, colors=128) for f in frames]
        gif_path = OUT / "control_studio_mcp_build.gif"
        imgs[0].save(
            gif_path,
            save_all=True,
            append_images=imgs[1:],
            duration=700,
            loop=0,
            optimize=False,
        )
    except Exception as exc:
        print("gif-fallback", exc, file=sys.stderr)
        gif_path = None

    meta = {
        "golden_session": sid,
        "build_session": build_sid,
        "frames": [str(f) for f in frames],
        "populated": str(populated),
        "gif": str(gif_path) if gif_path else None,
    }
    (OUT / "control_studio_capture_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Capture populated UI + GIF (agent MCP build, then human Kp edit + resim)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUT = Path("/opt/cursor/artifacts")
OUT.mkdir(parents=True, exist_ok=True)

from electrical_engineer.control_studio.mcp_tools import handle_tool


def main() -> int:
    from playwright.sync_api import sync_playwright

    base = "http://127.0.0.1:8765/?view=control-studio"
    frames: list[Path] = []
    populated = OUT / "control_studio_populated_1280x800.png"
    sid = handle_tool(
        "control_studio_create_diagram", {"title": "PID · DC motor", "golden": "pid_dc_motor"}
    )["session_id"]
    handle_tool("control_studio_simulate", {"session_id": sid})
    url_golden = f"{base}&session={sid}"

    build_sid = None
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(url_golden, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2200)
        page.get_by_role("button", name="Simulate").click()
        page.wait_for_selector(".studio-results-stage img", timeout=25000)
        page.wait_for_function(
            """() => {
            const cells = Array.from(document.querySelectorAll('.cs-margin-grid dd'));
            return cells.some((el) => (el.textContent || '').includes('dB'));
        }""",
            timeout=35000,
        )
        page.wait_for_timeout(400)
        page.screenshot(path=str(populated), full_page=False)

        sid2 = handle_tool("control_studio_create_diagram", {"title": "Agent build", "golden": None})["session_id"]
        build_sid = sid2
        page.goto(f"{base}&session={sid2}", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(1200)
        frames.append(OUT / "studio_frame_00.png")
        page.screenshot(path=str(frames[-1]), full_page=False)

        steps = [
            lambda: handle_tool("control_studio_add_block", {"session_id": sid2, "block_id": "r", "type": "step", "x": 48, "y": 72}),
            lambda: handle_tool("control_studio_add_block", {"session_id": sid2, "block_id": "sum1", "type": "sum", "x": 248, "y": 64}),
            lambda: handle_tool("control_studio_add_block", {"session_id": sid2, "block_id": "g1", "type": "gain", "x": 448, "y": 56, "params": {"k": 2}}),
            lambda: handle_tool("control_studio_add_block", {"session_id": sid2, "block_id": "p1", "type": "plant_first_order", "x": 648, "y": 56, "params": {"k": 10, "tau": 1}}),
            lambda: handle_tool("control_studio_add_block", {"session_id": sid2, "block_id": "y", "type": "scope", "x": 864, "y": 64}),
            lambda: handle_tool("control_studio_connect", {"session_id": sid2, "wire_id": "w1", "from": "r:out", "to": "sum1:in1"}),
            lambda: handle_tool("control_studio_connect", {"session_id": sid2, "wire_id": "w2", "from": "sum1:out", "to": "g1:in"}),
            lambda: handle_tool("control_studio_connect", {"session_id": sid2, "wire_id": "w3", "from": "g1:out", "to": "p1:in"}),
            lambda: handle_tool("control_studio_connect", {"session_id": sid2, "wire_id": "w4", "from": "p1:out", "to": "y:in"}),
            lambda: handle_tool("control_studio_connect", {"session_id": sid2, "wire_id": "w5", "from": "p1:tap", "to": "sum1:feedback"}),
            lambda: handle_tool("control_studio_simulate", {"session_id": sid2}),
        ]
        for i, step in enumerate(steps, start=1):
            step()
            page.wait_for_timeout(750)
            frame = OUT / f"studio_frame_{i:02d}.png"
            page.screenshot(path=str(frame), full_page=False)
            frames.append(frame)

        import urllib.request

        sess = json.loads(
            urllib.request.urlopen(f"http://127.0.0.1:8765/api/control-studio/sessions/{sid}").read().decode()
        )
        diagram = sess["diagram"]
        for block in diagram.get("blocks") or []:
            if block.get("id") == "pid1":
                block.setdefault("params", {})["kp"] = 3.2
        body = json.dumps(
            {
                "diagram": diagram,
                "author": "human",
                "op": "set_param",
                "target": "pid1",
                "detail": {"kp": 3.2},
            }
        ).encode()
        urllib.request.urlopen(
            urllib.request.Request(
                f"http://127.0.0.1:8765/api/control-studio/sessions/{sid}/diagram",
                data=body,
                headers={"Content-Type": "application/json"},
                method="PUT",
            )
        )
        page.goto(url_golden, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(1800)
        motor = page.locator('[data-id="motor"]')
        mbox = motor.bounding_box()
        if mbox:
            page.mouse.move(mbox["x"] + mbox["width"] / 2, mbox["y"] + mbox["height"] / 2)
            page.mouse.down()
            page.mouse.move(mbox["x"] + mbox["width"] / 2 + 40, mbox["y"] + mbox["height"] / 2 + 16)
            page.mouse.up()
            page.wait_for_timeout(700)
            frames.append(OUT / "studio_frame_human_drag.png")
            page.screenshot(path=str(frames[-1]), full_page=False)
        page.evaluate(
            """() => {
            const n = document.querySelector('[data-id="pid1"]');
            if (n) n.dispatchEvent(new PointerEvent('click', { bubbles: true, cancelable: true }));
        }"""
        )
        page.wait_for_timeout(400)
        kp = page.get_by_role("spinbutton", name="Kp")
        if kp.count():
            kp.fill("3.2")
            kp.press("Tab")
        page.wait_for_timeout(600)
        frames.append(OUT / "studio_frame_human_kp.png")
        page.screenshot(path=str(frames[-1]), full_page=False)
        page.get_by_role("button", name="Simulate").click()
        page.wait_for_timeout(1200)
        frames.append(OUT / "studio_frame_resim.png")
        page.screenshot(path=str(frames[-1]), full_page=False)

        browser.close()

    try:
        from PIL import Image

        imgs = [Image.open(f).convert("P", palette=Image.ADAPTIVE, colors=128) for f in frames]
        gif_path = OUT / "control_studio_mcp_build.gif"
        imgs[0].save(
            gif_path,
            save_all=True,
            append_images=imgs[1:],
            duration=750,
            loop=0,
            optimize=False,
        )
    except (OSError, ValueError) as exc:
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

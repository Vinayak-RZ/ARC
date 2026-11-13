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


def assert_bode_png_fresh(path: Path) -> None:
    """Reject stale matplotlib theme (orange phase, pre-cobalt captures)."""
    import numpy as np
    from PIL import Image

    im = np.array(Image.open(path).convert("RGB"))
    h = im.shape[0]
    phase = im[h // 2 + 20 :, :]
    orange = (phase[:, :, 0] > 175) & (phase[:, :, 1] < 130) & (phase[:, :, 2] < 95)
    if float(orange.mean()) > 0.008:
        raise SystemExit(f"bode stale (orange phase): {path}")
    cobalt = (phase[:, :, 2] > 140) & (phase[:, :, 0] < 90) & (phase[:, :, 1] < 120)
    if float(cobalt.mean()) < 0.004:
        raise SystemExit(f"bode missing cobalt phase trace: {path}")


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
        page.wait_for_timeout(2200)
        page.get_by_role("button", name="Simulate").click()
        page.wait_for_selector(".studio-results-stage img", timeout=25000)
        page.wait_for_function(
            """() => {
            const cells = Array.from(document.querySelectorAll('.cs-margin-grid dd'));
            return cells.some((el) => {
              const t = (el.textContent || '').trim();
              return t.includes('dB') || t === 'Infinite' || t === 'No crossover';
            });
        }""",
            timeout=35000,
        )
        page.wait_for_timeout(1600)
        viewport = page.evaluate(
            """() => {
            const pane = document.querySelector('.react-flow__pane');
            if (!pane) return { clip: true, ratio: 0 };
            const paneRect = pane.getBoundingClientRect();
            const pad = 8;
            const nodes = document.querySelectorAll('.react-flow__node .studio-block');
            if (!nodes.length) return { clip: true, ratio: 0 };
            let minL = Infinity;
            let maxR = -Infinity;
            let minT = Infinity;
            let maxB = -Infinity;
            let clipped = false;
            for (const n of nodes) {
                const r = n.getBoundingClientRect();
                minL = Math.min(minL, r.left);
                maxR = Math.max(maxR, r.right);
                minT = Math.min(minT, r.top);
                maxB = Math.max(maxB, r.bottom);
                if (r.left < paneRect.left + pad || r.right > paneRect.right - pad) clipped = true;
                if (r.top < paneRect.top + pad || r.bottom > paneRect.bottom - pad) clipped = true;
            }
            const ratioW = paneRect.width > 0 ? (maxR - minL) / paneRect.width : 0;
            const ratioH = paneRect.height > 0 ? (maxB - minT) / paneRect.height : 0;
            return { clip: clipped, ratio: ratioW, ratioH };
        }"""
        )
        if viewport.get("clip"):
            print("viewport-clip: node bbox extends past pane", file=sys.stderr)
            return 2
        ratio = float(viewport.get("ratio") or 0)
        ratio_h = float(viewport.get("ratioH") or 0)
        if ratio < 0.76:
            print(f"viewport-fill: diagram width ratio {ratio:.3f} < 0.76 (screen pixels)", file=sys.stderr)
            return 2
        if max(ratio, ratio_h) < 0.6:
            print(f"viewport-fill: max(w,h) ratio {max(ratio, ratio_h):.3f} < 0.6", file=sys.stderr)
            return 2
        print(f"viewport-fill: width ratio {ratio:.3f}, height ratio {ratio_h:.3f}", file=sys.stderr)
        page.screenshot(path=str(populated), full_page=False)
        bode_shot = OUT / "control_studio_bode_1280x800.png"
        handle_tool("control_studio_analyze", {"session_id": sid})
        bode_path = ROOT / "runs" / sid / "studio_bode.png"
        assert_bode_png_fresh(bode_path)
        page.locator(".studio-results-tabs button", has_text="Bode").click()
        page.wait_for_timeout(400)
        page.evaluate(
            """(sid) => {
            const ts = Date.now();
            const img = document.querySelector('.studio-results-stage img');
            if (img) img.src = `/api/control-studio/sessions/${sid}/plot/bode?t=${ts}`;
        }""",
            sid,
        )
        page.wait_for_function(
            """() => {
            const img = document.querySelector('.studio-results-stage img');
            return img && img.complete && img.naturalHeight > 80;
        }""",
            timeout=15000,
        )
        page.wait_for_timeout(300)
        page.locator(".studio-results-stage").scroll_into_view_if_needed()
        page.evaluate(
            """() => {
            const stage = document.querySelector('.studio-results-stage');
            if (stage) stage.scrollIntoView({ block: 'end', behavior: 'instant' });
        }"""
        )
        page.wait_for_timeout(400)
        page.screenshot(path=str(bode_shot), full_page=False)

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
            lambda: handle_tool("control_studio_auto_layout", {"session_id": sid2}),
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
        "bode": str(OUT / "control_studio_bode_1280x800.png"),
        "viewport_width_ratio": ratio,
        "viewport_height_ratio": ratio_h,
        "gif": str(gif_path) if gif_path else None,
    }
    (OUT / "control_studio_capture_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

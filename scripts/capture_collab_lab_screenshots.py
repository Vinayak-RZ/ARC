#!/usr/bin/env python3
"""Capture agent-built lab screenshots for PR artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> int:
    from electrical_engineer.collab.mcp_tools import handle_tool as collab_mcp
    from electrical_engineer.runner.execute import execute
    from electrical_engineer.runner.runs import new_run_id

    out = execute(
        "derive-circuit",
        cwd=ROOT,
        problem={"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000, "expected": 5.0},
    )
    run_id = out["run_id"]
    ctl = collab_mcp(
        "arc_lab_finish_control",
        {"run_id": new_run_id(), "problem": {"kind": "unity_feedback", "golden": "unity_first_order"}},
    )
    meta_path = OUT / "collab_capture_meta.json"
    meta_path.write_text(json.dumps({"circuit_run": out, "control_run": ctl}, indent=2), encoding="utf-8")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright missing", file=sys.stderr)
        return 1
    host = "http://127.0.0.1:8765"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(f"{host}/?view=studio&tab=circuits&run={run_id}")
        page.wait_for_load_state("networkidle")
        try:
            page.wait_for_selector(".react-flow", timeout=20000)
        except Exception:
            page.goto(f"{host}/?problem={run_id}")
            page.get_by_role("tab", name="Diagram").click()
            page.wait_for_selector(".diagram-shell", timeout=20000)
        page.screenshot(path=str(OUT / "agent_circuit_divider_lab.png"), full_page=False)
        sid = ctl["verify"]["control_session_id"]
        page.goto(f"{host}/?view=studio&tab=control&session={sid}")
        page.wait_for_selector(".react-flow", timeout=45000)
        page.screenshot(path=str(OUT / "agent_control_unity_lab.png"), full_page=False)
        browser.close()
    print(json.dumps({"circuit_shot": str(OUT / "agent_circuit_divider_lab.png"), "control_shot": str(OUT / "agent_control_unity_lab.png")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
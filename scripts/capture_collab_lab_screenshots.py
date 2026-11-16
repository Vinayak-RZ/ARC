"""Capture agent-built lab screenshots for PR artifacts."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts"
OUT.mkdir(parents=True, exist_ok=True)
HOST = os.environ.get("EE_UI_URL", "http://127.0.0.1:8765")


def _wait_run(page, run_id: str) -> None:
    page.goto(f"{HOST}/?problem={run_id}")
    page.wait_for_selector("#lab-verify-heading, .problem-header, h1", timeout=30_000)
    page.wait_for_function(
        """(id) => fetch(`/api/runs/${id}`).then(r => r.json()).then(d => !!(d && (d.title || d.lab_verify)))""",
        arg=run_id,
        timeout=45_000,
    )


def _shot_run_page(page, run_id: str, path: Path, *, diagram_tab: bool = False) -> None:
    _wait_run(page, run_id)
    page.wait_for_selector(".lab-verify-panel", timeout=20_000)
    page.locator(".lab-verify-panel dd").first.wait_for(state="visible")
    if diagram_tab:
        page.get_by_role("tab", name="Diagram").click()
        page.wait_for_selector(".diagram-shell svg, .diagram-shell .react-flow", timeout=20_000)
    else:
        page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(500)
    page.screenshot(path=str(path), full_page=True)


def _shot_control_lab(page, session_id: str, path: Path) -> None:
    page.goto(f"{HOST}/?view=studio&tab=control&session={session_id}")
    page.wait_for_selector(".react-flow", timeout=45_000)
    page.get_by_role("button", name="Simulate").click()
    page.wait_for_selector(".studio-margins .num, .results-dock, .step-chart", timeout=45_000)
    page.wait_for_timeout(800)
    page.screenshot(path=str(path), full_page=False)


def _shot_circuit_lab(page, run_id: str, path: Path) -> None:
    page.goto(f"{HOST}/?view=studio&tab=circuits&run={run_id}")
    page.wait_for_selector(".react-flow", timeout=45_000)
    page.wait_for_selector(".studio-lab-activity", timeout=20_000)
    page.wait_for_timeout(500)
    page.screenshot(path=str(path), full_page=False)


def main() -> int:
    from electrical_engineer.runner.execute import execute

    divider = execute(
        "derive-circuit",
        cwd=ROOT,
        problem={"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000, "expected": 5.0, "tol": 1e-3},
    )
    rlc_problem = {
        "kind": "series_rlc",
        "vin": 10,
        "v_step": 10,
        "r_ohm": 10,
        "l_h": 0.01,
        "c_f": 100e-6,
        "probe_node": 3,
        "analysis": "tran",
        "t_s": 0.0005,
        "probe": "v(3)",
        "tol": 0.15,
    }
    rlc = execute("series-rlc-transient", cwd=ROOT, problem=rlc_problem)
    control = execute(
        "solve-control-problem",
        cwd=ROOT,
        problem={
            "golden": "unity_first_order",
            "kind": "unity_feedback",
            "num": [10],
            "den": [1, 1],
            "tf": "10/(s(s+1))",
        },
    )
    ctl_sid = None
    lab_path = Path(control["run_dir"]) / "lab_meta.json"
    if lab_path.is_file():
        ctl_sid = json.loads(lab_path.read_text(encoding="utf-8")).get("control_session_id")

    meta = {
        "circuit_run": divider,
        "rlc_run": rlc,
        "control_run": control,
        "control_session_id": ctl_sid,
    }
    (OUT / "collab_capture_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright missing", file=sys.stderr)
        return 1

    # UI must already be listening (CI / manual: electrical-engineer ui).
    for _ in range(40):
        try:
            import urllib.request

            urllib.request.urlopen(f"{HOST}/api/health", timeout=2)
            break
        except OSError:
            time.sleep(0.5)
    else:
        print(f"UI not up at {HOST}", file=sys.stderr)
        return 1

    shots = {
        "agent_circuit_divider_lab": OUT / "agent_circuit_divider_lab.png",
        "agent_series_rlc_run": OUT / "agent_series_rlc_run.png",
        "agent_series_rlc_lab": OUT / "agent_series_rlc_lab.png",
        "agent_control_unity_lab": OUT / "agent_control_unity_lab.png",
    }
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        _shot_run_page(page, divider["run_id"], shots["agent_circuit_divider_lab"], diagram_tab=True)
        _shot_run_page(page, rlc["run_id"], shots["agent_series_rlc_run"], diagram_tab=False)
        _shot_circuit_lab(page, rlc["run_id"], shots["agent_series_rlc_lab"])
        if ctl_sid:
            _shot_control_lab(page, str(ctl_sid), shots["agent_control_unity_lab"])
        browser.close()
    print(json.dumps({k: str(v) for k, v in shots.items()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
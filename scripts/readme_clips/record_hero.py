"""Record the README hero loop: agent builds + simulates a series RLC, human sets R1 to 20 ohm, re-runs."""

import json
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(os.environ.get("ARC_ROOT", str(Path(__file__).resolve().parents[2])))
sys.path.insert(0, str(ROOT / "src"))
os.chdir(ROOT)
from electrical_engineer.circuit import mcp_lab
from electrical_engineer.circuit.graph import series_rlc_graph
from electrical_engineer.runner.runs import new_run_id

BASE = os.environ.get("BASE", "http://127.0.0.1:8765")
THEME = os.environ.get("THEME", "light")
OUT = Path(os.environ.get("OUT", "build/readme-clips/raw-hero"))
OUT.mkdir(parents=True, exist_ok=True)
marks = []
T0 = None


def mark(name):
    marks.append((name, time.time() - T0))
    print(f"{time.time() - T0:6.2f} {name}", flush=True)


problem = {
    "kind": "series_rlc",
    "vin": 10,
    "v_step": 10,
    "r_ohm": 10,
    "l_h": 0.01,
    "c_f": 100e-6,
    "probe_node": 3,
    "analysis": "tran",
    "probe": "v(3)",
    "tol": 0.02,
    "prompt": "Series RLC step",
}
g = series_rlc_graph(vin=10, r_ohm=10, l_h=0.01, c_f=1e-4)
rid = new_run_id()
mcp_lab.handle_tool("arc_circuit_lab_open", {"run_id": rid})
(ROOT / "runs" / rid / "problem.json").write_text(json.dumps(problem))
# Label only (no values): lets the lab bar name the problem like a normal agent run does.
(ROOT / "runs" / rid / "summary.json").write_text(
    json.dumps({"recipe_id": "series-rlc-transient", "title": "Series RLC step"})
)

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(
        viewport={"width": 1440, "height": 1000},
        record_video_dir=str(OUT),
        record_video_size={"width": 1440, "height": 1000},
        device_scale_factor=1,
    )
    ctx.add_init_script(f'localStorage.setItem("arc-theme", "{THEME}")')
    page = ctx.new_page()
    T0 = time.time()
    page.goto(f"{BASE}/?view=studio&tab=circuits&run={rid}", wait_until="networkidle")
    page.wait_for_selector(".lab-provenance-bar")
    page.wait_for_timeout(800)
    mark("build_start")
    built = {"schema": "arc.circuit.v1", "nodes": [], "edges": []}
    for n in g["nodes"]:
        built["nodes"].append(n)
        mcp_lab.handle_tool(
            "arc_circuit_lab_set_graph", {"run_id": rid, "graph": json.loads(json.dumps(built))}
        )
        page.wait_for_timeout(550)
    for e in g["edges"]:
        built["edges"].append(e)
        mcp_lab.handle_tool(
            "arc_circuit_lab_set_graph", {"run_id": rid, "graph": json.loads(json.dumps(built))}
        )
        page.wait_for_timeout(450)
    mark("build_done")
    mcp_lab.handle_tool("arc_circuit_lab_finish_solve", {"run_id": rid, "problem": problem})
    page.locator(".studio-circuit-results .se-waveform").first.wait_for(timeout=60000)
    page.get_by_text("Agrees", exact=False).first.wait_for(timeout=60000)
    mark("agent_verified")
    page.wait_for_timeout(2200)
    # Human edits R1
    page.locator(".react-flow__node").filter(has_text="R1").first.click()
    inp = page.locator(".studio-circuit-inspector input").first
    inp.wait_for(timeout=10000)
    mark("human_select")
    inp.click(click_count=3)
    page.wait_for_timeout(300)
    inp.type("20", delay=180)
    inp.press("Enter")
    page.wait_for_timeout(500)
    page.locator(".studio-circuit-app .cs-simulate-btn").click()
    mark("human_sim")
    page.get_by_text("No overshoot", exact=False).first.wait_for(timeout=60000)
    page.wait_for_timeout(1800)
    mark("human_result")
    btn = page.get_by_role("button", name="Ask agent to re-derive")
    if btn.count():
        btn.first.click()
        mark("rederive")
        page.locator(
            ".lab-verify-badge.is-agrees, .studio-lab-drawer :text('Agrees')"
        ).first.wait_for(timeout=60000)
        mark("rederive_agrees")
    page.wait_for_timeout(2500)
    mark("end")
    vid = page.video.path()
    ctx.close()
    b.close()
(OUT / "marks.json").write_text(
    json.dumps({"video": str(vid), "marks": marks, "run": rid}, indent=1)
)
print(vid)

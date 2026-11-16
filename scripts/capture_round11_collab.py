"""Round-11 collab screenshots (isolated runs per theme)."""

from __future__ import annotations

import json
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "ux-review" / "round-11"
HOST = "127.0.0.1"
PORT = 8765


def _clear_runs() -> None:
    runs = ROOT / "runs"
    if runs.is_dir():
        for child in runs.iterdir():
            if child.is_dir():
                for p in child.rglob("*"):
                    if p.is_file():
                        p.unlink()
                for p in sorted(child.rglob("*"), reverse=True):
                    if p.is_dir():
                        p.rmdir()
                child.rmdir()


def _api(method: str, path: str, data: dict | None = None) -> dict:
    body = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(
        f"http://{HOST}:{PORT}{path}",
        data=body,
        method=method,
        headers={"Content-Type": "application/json"} if data is not None else {},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode())


def _run_example(example_id: str) -> str:
    return str(_api("POST", f"/api/examples/{example_id}/run", {})["run_id"])


def _set_r1(run_id: str, ohms: float) -> None:
    lab = _api("GET", f"/api/runs/{run_id}/lab")
    graph = lab.get("graph") or {}
    for node in graph.get("nodes") or []:
        if node.get("id") == "r1":
            node["value"] = ohms
    _api("PUT", f"/api/runs/{run_id}/graph", graph)
    _api("POST", f"/api/runs/{run_id}/lab/verify", {})


def main() -> int:
    from playwright.sync_api import sync_playwright

    OUT.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 900

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for theme in ("light", "dark"):
            _clear_runs()
            page = browser.new_page(viewport={"width": W, "height": H})
            page.goto(f"http://{HOST}:{PORT}/?view=settings", wait_until="domcontentloaded")
            page.evaluate(
                """(t) => {
                localStorage.setItem('arc-theme', t);
                document.documentElement.dataset.theme = t;
            }""",
                theme,
            )

            rlc_id = _run_example("rlc-step")
            page.goto(f"http://{HOST}:{PORT}/?problem={rlc_id}", wait_until="domcontentloaded")
            page.wait_for_selector(".answer-line", timeout=120000)
            page.screenshot(path=str(OUT / f"collab-01-{theme}.png"), full_page=True)

            page.goto(f"http://{HOST}:{PORT}/?view=studio&tab=circuits&run={rlc_id}")
            page.wait_for_selector(".lab-provenance-bar", timeout=60000)
            page.locator(".studio-circuit-app .cs-simulate-btn").click()
            page.wait_for_selector(".studio-circuit-results .se-waveform, .studio-circuit-results .answer-num", timeout=120000)
            page.screenshot(path=str(OUT / f"collab-02-{theme}.png"), full_page=True)

            _set_r1(rlc_id, 20.0)
            page.reload(wait_until="domcontentloaded")
            page.wait_for_selector(".lab-provenance-bar", timeout=60000)
            page.locator(".studio-circuit-app .cs-simulate-btn").click()
            page.wait_for_selector(".studio-circuit-results .se-waveform, .studio-circuit-results .answer-num", timeout=120000)
            page.screenshot(path=str(OUT / f"collab-03-{theme}.png"), full_page=True)

            page.goto(f"http://{HOST}:{PORT}/?problem={rlc_id}")
            page.wait_for_selector(".lab-verify-panel, .lab-verify-table", timeout=60000)
            page.screenshot(path=str(OUT / f"collab-04-{theme}.png"), full_page=True)

            fresh_id = _run_example("rlc-step")
            page.goto(f"http://{HOST}:{PORT}/?view=studio&tab=circuits&run={fresh_id}")
            page.evaluate("""() => {
              document.querySelectorAll('.lab-provenance-segment button').forEach((b) => {
                if (b.textContent.trim() === 'Agent') b.click();
              });
            }""")
            page.wait_for_timeout(400)
            page.screenshot(path=str(OUT / f"collab-05-{theme}.png"), full_page=True)

            page.goto(f"http://{HOST}:{PORT}/?view=studio&tab=circuits&run={fresh_id}")
            page.locator(".lab-activity-filters button", has_text="You").click()
            page.wait_for_timeout(300)
            page.screenshot(path=str(OUT / f"collab-06-{theme}.png"), full_page=True)

            ctrl_id = _run_example("control-step")
            page.goto(f"http://{HOST}:{PORT}/?problem={ctrl_id}")
            page.wait_for_selector(".answer-line", timeout=120000)
            page.screenshot(path=str(OUT / f"problem-control-checked-{theme}.png"), full_page=True)

            lab = _api("GET", f"/api/runs/{ctrl_id}/lab")
            sid = (lab.get("lab_meta") or {}).get("control_session_id")
            if sid:
                page.goto(f"http://{HOST}:{PORT}/?view=studio&tab=control&session={sid}")
                page.locator(".cs-simulate-btn").click()
                page.wait_for_selector(".studio-results-stage .studio-step-svg, .studio-margins", timeout=120000)
                page.screenshot(path=str(OUT / f"problem-control-studio-{theme}.png"), full_page=True)

            page.close()

        browser.close()

    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    (OUT / "NOTES.md").write_text(
        f"# Round 11 collab recapture\n\nCommit: `{sha[:12]}`\n\nSee `collab-01` … `collab-06` and control shots per theme.\n",
        encoding="utf-8",
    )
    print("Wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
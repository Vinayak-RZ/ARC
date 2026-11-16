#!/usr/bin/env python3
"""Round-11 collaboration loop + supplemental run pages and 1024 key screens."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "ux-review" / "round-11"
HOST = "127.0.0.1"
PORT = 8765
BASE = f"http://{HOST}:{PORT}"
W, H = 1440, 900
BAD_TEXT = r"(\bNaN\b|undefined|\[object Object\]|Simulating…|Loading…)"


def _set_theme(page, mode: str) -> None:
    page.evaluate(
        """(mode) => {
        document.documentElement.setAttribute('data-theme', mode);
        document.documentElement.dataset.theme = mode;
        localStorage.setItem('arc-theme', mode);
    }""",
        mode,
    )
    page.wait_for_timeout(350)


def _prepare_page_theme(context, mode: str) -> None:
    context.add_init_script(
        f"""() => {{
        const mode = {json.dumps(mode)};
        try {{ localStorage.setItem('arc-theme', mode); }} catch (_) {{}}
        document.documentElement.setAttribute('data-theme', mode);
        document.documentElement.dataset.theme = mode;
    }}"""
    )


def _assert_idle(page) -> None:
    import re

    body = page.locator("body").inner_text()
    if re.search(BAD_TEXT, body):
        raise RuntimeError(f"bad chrome in page: {body[:400]!r}")
    sim = page.locator(".cs-simulate-btn, .studio-circuit-simulate-btn").first
    if sim.count():
        txt = (sim.inner_text() or "").strip()
        if "Simulat" in txt and txt != "Simulate":
            raise RuntimeError(f"simulate not idle: {txt!r}")


def _wait_sim_idle(page, timeout_ms: int = 120_000) -> None:
    page.wait_for_function(
        """() => {
          const b = document.querySelector('.studio-circuit-simulate-btn, .cs-simulate-btn');
          return b && !b.disabled && /^Simulate$/.test((b.textContent || '').trim());
        }""",
        timeout=timeout_ms,
    )
    page.wait_for_timeout(400)


def _shot(page, name: str, *, theme: str, full_page: bool = True) -> Path:
    _set_theme(page, theme)
    _assert_idle(page)
    path = OUT / f"{name}-{theme}.png"
    page.screenshot(path=str(path), full_page=full_page)
    print("wrote", path)
    return path


def _run_example(example_id: str) -> str:
    req = urllib.request.Request(
        f"{BASE}/api/examples/{example_id}/run",
        method="POST",
        headers={"Content-Type": "application/json"},
        data=b"{}",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = json.loads(resp.read().decode())
    rid = body.get("run_id")
    if not rid:
        raise RuntimeError(f"no run_id for {example_id}: {body}")
    return str(rid)


def _require_ngspice() -> str:
    if not shutil.which("ngspice"):
        raise RuntimeError(
            "ngspice is not on PATH. Install with: sudo apt-get update && sudo apt-get install -y ngspice"
        )
    proc = subprocess.run(["ngspice", "-v"], capture_output=True, text=True, check=False)
    banner = (proc.stdout + proc.stderr).strip()
    if not banner:
        raise RuntimeError("ngspice -v produced no output")
    first_line = next(
        (ln.strip() for ln in banner.splitlines() if "ngspice" in ln.lower()),
        banner.splitlines()[0].strip(),
    )
    from electrical_engineer.engines.spice_runner import simulator_status

    st = simulator_status()
    if not st.get("available"):
        raise RuntimeError(f"simulator_status reports unavailable: {st.get('reason')!r}")
    return first_line


def _assert_rlc_lab_agrees(run_dir: Path, problem: dict) -> dict:
    from electrical_engineer.collab.workflow import finish_circuit_lab

    verify = finish_circuit_lab(run_dir, problem)
    if verify.get("status") != "agrees":
        raise RuntimeError(f"RLC lab verify must agree with ngspice; got {verify.get('status')!r} ({verify})")
    if verify.get("simulated") is None:
        raise RuntimeError(f"RLC lab verify missing simulated value: {verify}")
    sim_engine = str(verify.get("sim_engine") or "")
    if "ngspice" not in sim_engine.lower():
        raise RuntimeError(f"RLC sim_engine must be ngspice; got {sim_engine!r}")
    sim_path = run_dir / "lab_simulate.json"
    if sim_path.is_file():
        sim = json.loads(sim_path.read_text(encoding="utf-8"))
        if not sim.get("ok"):
            raise RuntimeError(f"lab_simulate.json not ok: {sim}")
    return verify


def _put_graph(run_id: str, graph: dict) -> None:
    req = urllib.request.Request(
        f"{BASE}/api/runs/{run_id}/graph",
        method="PUT",
        data=json.dumps(graph).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        if resp.status != 200:
            raise RuntimeError(f"graph put failed {resp.status}")


def _patch_r1_in_graph(graph: dict, ohms: float) -> dict:
    g = json.loads(json.dumps(graph))
    for node in g.get("nodes") or []:
        if node.get("refdes") == "R1" or node.get("id") == "r1":
            node["value"] = ohms
    return g


def _wait_health() -> None:
    for _ in range(80):
        try:
            with urllib.request.urlopen(f"{BASE}/api/health", timeout=2):
                return
        except OSError:
            time.sleep(0.5)
    raise RuntimeError("UI not healthy")


def main() -> int:
    ngspice_version = _require_ngspice()
    print("ngspice:", ngspice_version)
    (OUT / ".ngspice_version").write_text(ngspice_version + "\n", encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright missing", file=sys.stderr)
        return 1

    if os.environ.get("ROUND11_START_UI") == "1":
        subprocess.check_call(["npm", "run", "build"], cwd=ROOT / "ui")
        env = {**os.environ, "EE_NO_BROWSER": "1"}
        server = subprocess.Popen(
            [sys.executable, "-m", "electrical_engineer", "ui"],
            cwd=ROOT,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            _wait_health()
            return _capture(sync_playwright)
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
    _wait_health()
    return _capture(sync_playwright)


def _capture(sync_playwright) -> int:
    from electrical_engineer.runner.execute import execute

    rlc_problem = {
        "kind": "series_rlc",
        "vin": 10,
        "v_step": 10,
        "r_ohm": 10,
        "l_h": 0.01,
        "c_f": 100e-6,
        "probe_node": 3,
        "analysis": "tran",
        "t_s": 0.003628,
        "probe": "v(3)",
        "tol": 0.02,
    }
    rlc = execute("series-rlc-transient", cwd=ROOT, problem=rlc_problem)
    rlc_id = rlc["run_id"]
    rlc_dir = Path(rlc["run_dir"])
    _assert_rlc_lab_agrees(rlc_dir, rlc_problem)
    control = execute(
        "solve-control-problem",
        cwd=ROOT,
        problem={
            "golden": "unity_first_order",
            "kind": "unity_feedback",
            "num": [10],
            "den": [1, 1],
            "tf": "10/(s+1)",
        },
    )
    ctl_id = control["run_id"]
    ctl_sid = None
    lab_meta_path = Path(control["run_dir"]) / "lab_meta.json"
    if lab_meta_path.is_file():
        ctl_sid = json.loads(lab_meta_path.read_text(encoding="utf-8")).get("control_session_id")

    control_step_id = _run_example("control-step")
    control_step_sid = None
    cs_meta = ROOT / "runs" / control_step_id / "lab_meta.json"
    if cs_meta.is_file():
        control_step_sid = json.loads(cs_meta.read_text(encoding="utf-8")).get("control_session_id")

    rect_id = None
    idmt_id = None
    if os.environ.get("ROUND11_FULL", "") == "1":
        rect_id = _run_example("rectifier-3ph")
        idmt_id = _run_example("idmt-relay")

    meta_path = OUT / "collab_capture_meta.json"
    meta_path.write_text(
        json.dumps(
            {
                "rlc_run_id": rlc_id,
                "control_run_id": ctl_id,
                "control_session_id": ctl_sid,
                "control_step_run_id": control_step_id,
                "control_step_session_id": control_step_sid,
                "rectifier_run_id": rect_id,
                "idmt_run_id": idmt_id,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    key_1024 = [
        ("?view=home", "home-empty", ".example-grid-six"),
        ("?view=problems", "problems-list", ".problems-table, .problems-empty"),
        ("?view=gallery", "gallery", ".gallery-card"),
        ("?view=library", "library", ".library"),
        ("?view=learn", "learn-landing", ".learn-page h1"),
        ("?view=settings", "settings-agents", ".settings-page"),
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for theme in ("light", "dark"):
            ctx = browser.new_context(viewport={"width": W, "height": H})
            if theme == "dark":
                _prepare_page_theme(ctx, "dark")
            page = ctx.new_page()
            page.goto(f"{BASE}/?view=home", wait_until="domcontentloaded")
            _set_theme(page, theme)

            if rect_id and idmt_id:
                for run_id, stem in [(rect_id, "run-rectifier"), (idmt_id, "run-idmt")]:
                    page.goto(f"{BASE}/?problem={run_id}", wait_until="domcontentloaded")
                    page.wait_for_selector(".answer-line, .problem-header", timeout=120_000)
                    _shot(page, stem, theme=theme)

            # Control-step example (gallery run + lab agreement)
            page.goto(f"{BASE}/?problem={control_step_id}", wait_until="domcontentloaded")
            page.wait_for_selector(".answer-line", timeout=120_000)
            page.wait_for_selector("#lab-verify-heading", timeout=60_000)
            _shot(page, "problem-control-checked", theme=theme)
            page.get_by_role("tab", name="Work").click()
            page.wait_for_selector(".step-timeline-row, .checked-tag", timeout=120_000)
            _shot(page, "problem-control-checked-work", theme=theme)
            if control_step_sid:
                page.goto(f"{BASE}/?view=studio&tab=control&session={control_step_sid}", wait_until="domcontentloaded")
                page.wait_for_selector(".cs-simulate-btn", timeout=30_000)
                page.locator(".cs-simulate-btn").click()
                page.wait_for_selector(".studio-margins .num, .studio-step-chart", timeout=120_000)
                page.wait_for_selector(".studio-step-chart svg", timeout=60_000)
                _wait_sim_idle(page)
                _shot(page, "problem-control-checked-lab-agreement", theme=theme, full_page=True)

            # Collab step 1 — agent solved RLC, Agrees
            page.goto(f"{BASE}/?problem={rlc_id}", wait_until="domcontentloaded")
            page.wait_for_selector("#lab-verify-heading", timeout=60_000)
            page.get_by_text("Agrees (limit", exact=False).first.wait_for(state="visible", timeout=120_000)
            _shot(page, "collab-01-run-sim-vs-derived-agrees", theme=theme)

            # Collab step 2 — open in lab
            page.goto(f"{BASE}/?view=studio&tab=circuits&run={rlc_id}", wait_until="domcontentloaded")
            page.wait_for_selector(".lab-provenance-bar", timeout=30_000)
            page.wait_for_selector(".studio-lab-drawer", timeout=30_000)
            page.locator(".react-flow__node").first.wait_for(state="visible", timeout=60_000)
            sim = page.locator(".studio-circuit-app .cs-simulate-btn")
            sim.click()
            _wait_sim_idle(page)
            page.wait_for_selector(".studio-circuit-results .se-waveform", timeout=120_000)
            _shot(page, "collab-02-lab-provenance-vc-activity", theme=theme, full_page=True)

            # Collab step 3 — human changes R1, re-simulate
            lab_body = json.loads(urllib.request.urlopen(f"{BASE}/api/runs/{rlc_id}/lab", timeout=30).read())
            patched = _patch_r1_in_graph(lab_body.get("graph") or {}, 20)
            _put_graph(rlc_id, patched)
            page.reload(wait_until="domcontentloaded")
            page.wait_for_selector(".lab-provenance-bar", timeout=30_000)
            page.locator(".studio-circuit-app .cs-simulate-btn").click()
            _wait_sim_idle(page)
            page.get_by_role("button", name="You", exact=True).click()
            page.wait_for_timeout(300)
            _shot(page, "collab-03-human-r1-resim-activity-you", theme=theme, full_page=True)

            # Collab step 4 — Changes view + Restore
            page.get_by_role("tab", name="Changes").click()
            page.wait_for_timeout(400)
            page.locator(".lab-provenance-bar button.button-secondary", has_text="Restore agent version").wait_for(
                state="visible", timeout=10_000
            )
            _shot(page, "collab-04-changes-restore-agent", theme=theme, full_page=True)

            # Collab step 5 — bad derive Needs review (temporary file edit)
            bad_dir = ROOT / "runs" / rlc_id
            verify_path = bad_dir / "lab_verify.json"
            verify_bak = verify_path.read_text(encoding="utf-8") if verify_path.is_file() else None
            if verify_path.is_file():
                verify = json.loads(verify_path.read_text(encoding="utf-8"))
                verify.update(
                    {
                        "derived": 11.963,
                        "simulated": 11.630,
                        "rel_err_pct": 2.9,
                        "mismatch": True,
                        "needs_review": True,
                        "ok": False,
                        "status": "differs",
                        "status_label": "Differs by 2.9% (limit 2.0%)",
                    }
                )
                if verify.get("metrics"):
                    verify["metrics"][0].update(
                        {
                            "derived": 11.963,
                            "rel_err_pct": 2.9,
                            "status": "differs",
                            "status_label": verify["status_label"],
                        }
                    )
                verify_path.write_text(json.dumps(verify, indent=2), encoding="utf-8")
            page.goto(f"{BASE}/?problem={rlc_id}", wait_until="domcontentloaded")
            page.wait_for_selector(".lab-needs-review, .lab-needs-review-banner", timeout=30_000)
            _shot(page, "collab-05-needs-review-bad-derive", theme=theme)
            if verify_bak is not None:
                verify_path.write_text(verify_bak, encoding="utf-8")

            # Collab step 6 — control unity run + lab
            page.goto(f"{BASE}/?problem={ctl_id}", wait_until="domcontentloaded")
            page.wait_for_selector(".answer-line", timeout=120_000)
            page.get_by_text("Agrees (limit", exact=False).first.wait_for(state="visible", timeout=120_000)
            _shot(page, "collab-06-control-unity-run-agrees", theme=theme)
            if ctl_sid:
                page.goto(f"{BASE}/?view=studio&tab=control&session={ctl_sid}", wait_until="domcontentloaded")
                page.wait_for_selector(".cs-simulate-btn", timeout=30_000)
                page.locator(".cs-simulate-btn").click()
                page.wait_for_selector(".studio-margins .num, .studio-step-chart", timeout=120_000)
                page.get_by_text("0.909", exact=False).first.wait_for(state="visible", timeout=60_000)
                page.get_by_text("0.36", exact=False).first.wait_for(state="visible", timeout=60_000)
                _wait_sim_idle(page)
                _shot(page, "collab-06-control-unity-lab-agreement", theme=theme, full_page=True)

            ctx.close()

            if os.environ.get("ROUND11_FULL", "") != "1":
                continue

            narrow_ctx = browser.new_context(viewport={"width": 1024, "height": H})
            if theme == "dark":
                _prepare_page_theme(narrow_ctx, "dark")
            narrow = narrow_ctx.new_page()
            narrow.goto(f"{BASE}/?view=home", wait_until="domcontentloaded")
            _set_theme(narrow, theme)
            divider_id = _run_example("divider")
            ctrl_req = urllib.request.Request(
                f"{BASE}/api/control-studio/sessions",
                method="POST",
                data=json.dumps({"title": "Round 11 · Unity", "golden": "pid_dc_motor"}).encode(),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(ctrl_req, timeout=60) as resp:
                ctrl_session = json.loads(resp.read().decode())["session_id"]
            key_1024_with_run = [
                *key_1024,
                (f"?problem={divider_id}", "problem-divider-run", ".answer-line"),
                (f"?view=studio&tab=control&session={ctrl_session}", "studio-control", ".cs-app.control-studio"),
                ("?view=studio&tab=circuits", "studio-circuit-sandbox", ".studio-circuit-app"),
            ]
            for route, stem, sel in key_1024_with_run:
                narrow.goto(f"{BASE}{route}", wait_until="domcontentloaded")
                narrow.wait_for_selector(sel, timeout=60_000)
                if stem == "studio-circuit-sandbox":
                    narrow.evaluate("() => localStorage.removeItem('arc-circuit-sandbox-v1')")
                    narrow.reload(wait_until="domcontentloaded")
                    narrow.wait_for_selector(".studio-circuit-app", timeout=30_000)
                narrow.wait_for_timeout(300)
                path = OUT / f"{stem}-1024-{theme}.png"
                _set_theme(narrow, theme)
                _assert_idle(narrow)
                narrow.screenshot(path=str(path), full_page=False)
                print("wrote", path)
            narrow_ctx.close()

        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
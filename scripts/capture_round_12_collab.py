#!/usr/bin/env python3
"""Round-12 collaboration loop + supplemental runs (isolated runs/ per theme)."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
_CAPTURE_SUBDIR = os.environ.get("ARC_UX_CAPTURE_DIR", "round-12")
OUT = ROOT / "artifacts" / "ux-review" / _CAPTURE_SUBDIR
CONTROL_STUDIO = ROOT / ".electrical-engineer" / "control_studio"
HOST = "127.0.0.1"
PORT = 8765
BASE = f"http://{HOST}:{PORT}"
W, H = 1440, 900
BAD_TEXT = re.compile(r"(\bNaN\b|undefined|\[object Object\]|Simulating…|Loading…)", re.IGNORECASE)


def _clear_runs() -> None:
    if RUNS.is_dir():
        shutil.rmtree(RUNS)
    RUNS.mkdir(parents=True, exist_ok=True)


def _clear_lab_state() -> None:
    if CONTROL_STUDIO.is_dir():
        shutil.rmtree(CONTROL_STUDIO)


def _api(method: str, path: str, data: dict | None = None) -> dict:
    body = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=body,
        method=method,
        headers={"Content-Type": "application/json"} if data is not None else {},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode())


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
    body = page.locator("body").inner_text()
    if BAD_TEXT.search(body):
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
    return str(_api("POST", f"/api/examples/{example_id}/run", {})["run_id"])


_RLC_STEP_CIR = """* series rlc step
V1 1 0 DC 10
R1 1 2 10
L1 2 3 10m
C1 3 0 100u
.tran 50u 20m
.end
"""


def _run_series_rlc_collab() -> str:
    """Same recipe path as CI collab tests; include cir so agent re-derive can refresh verify."""
    from electrical_engineer.engines.rlc_transient import series_rlc_step
    from electrical_engineer.runner.execute import execute

    meta = series_rlc_step(10, 0.01, 100e-6, 10.0)
    out = execute(
        "series-rlc-transient",
        cwd=ROOT,
        problem={
            "kind": "series_rlc",
            "vin": 10,
            "v_step": 10,
            "r_ohm": 10,
            "l_h": 0.01,
            "c_f": 100e-6,
            "analysis": "tran",
            "t_s": float(meta["t_Vc_peak_s"]),
            "probe": "v(3)",
            "tol": 0.02,
            "prompt": "Series RLC step",
        },
    )
    return out["run_id"]


def _prepare_rlc_rederive(run_id: str) -> None:
    """Agent re-derive must use RLC template (not stale ngspice netlist) after human R1 edit."""
    run_dir = RUNS / run_id
    prob_path = run_dir / "problem.json"
    if not prob_path.is_file():
        return
    prob = json.loads(prob_path.read_text(encoding="utf-8"))
    prob.pop("cir", None)
    prob.pop("netlist", None)
    prob["allow_template_fallback"] = True
    prob_path.write_text(json.dumps(prob, indent=2) + "\n", encoding="utf-8")


def _require_ngspice() -> str:
    if not shutil.which("ngspice"):
        raise RuntimeError(
            "ngspice is not on PATH. Install with: sudo apt-get update && sudo apt-get install -y ngspice"
        )
    proc = subprocess.run(["ngspice", "-v"], capture_output=True, text=True, check=False)
    banner = (proc.stdout + proc.stderr).strip()
    if not banner:
        raise RuntimeError("ngspice -v produced no output")
    return next(
        (ln.strip() for ln in banner.splitlines() if "ngspice" in ln.lower()),
        banner.splitlines()[0].strip(),
    )


def _set_r1_and_reverify(run_id: str, ohms: float) -> dict:
    lab = _api("GET", f"/api/runs/{run_id}/lab")
    graph = json.loads(json.dumps(lab.get("graph") or {}))
    for node in graph.get("nodes") or []:
        if node.get("id") == "r1" or node.get("refdes") == "R1":
            node["value"] = ohms
    _api("PUT", f"/api/runs/{run_id}/graph", graph)
    return _api("POST", f"/api/runs/{run_id}/lab/verify", {})


def _assert_text(page, pattern: str, label: str) -> None:
    body = page.locator("body").inner_text()
    if not re.search(pattern, body, re.IGNORECASE):
        raise RuntimeError(f"{label}: pattern {pattern!r} not found in page text")


def _wait_health() -> None:
    for _ in range(80):
        try:
            with urllib.request.urlopen(f"{BASE}/api/health", timeout=2):
                return
        except OSError:
            time.sleep(0.5)
    raise RuntimeError("UI not healthy")


_RECTIFIER_TOPOS = [
    ("hw1", "1φ half", 230, (30, 60)),
    ("semi1", "1φ semi", 230, (30, 60)),
    ("full1", "1φ full", 230, (30, 60)),
    ("hw3", "3φ half", 415, (30, 75)),
    ("semi3", "3φ semi", 415, (30, 75)),
    ("full3", "3φ full", 415, (30, 75)),
]


def _set_rectifier_lab(page, *, topo_label: str, v_rms: int, alpha: int, load: str = "R") -> None:
    page.goto(f"{BASE}/?view=studio&tab=labs&lab=rectifier", wait_until="domcontentloaded")
    page.wait_for_selector(".lab-shell", timeout=30_000)
    page.get_by_role("radio", name=topo_label).check()
    page.get_by_role("radio", name=load, exact=True).check()
    page.locator('label:has-text("Line voltage")').locator('input[type="number"]').first.fill(str(v_rms))
    page.locator('label:has-text("α (deg)")').locator('input[type="number"]').fill(str(alpha))
    page.wait_for_timeout(450)


def _capture_rectifier_topologies(page, *, theme: str) -> None:
    for topo_id, label, v_rms, angles in _RECTIFIER_TOPOS:
        for alpha in angles:
            _set_rectifier_lab(page, topo_label=label, v_rms=v_rms, alpha=alpha, load="R")
            _shot(page, f"lab-rectifier-{topo_id}-r-alpha{alpha}", theme=theme, full_page=True)
    _set_rectifier_lab(page, topo_label="3φ full", v_rms=415, alpha=75, load="RL")
    vo_txt = page.locator(".card").filter(has_text="Vo").locator("strong").inner_text()
    vo = float(vo_txt.split()[0])
    if abs(vo - 145.1) > 0.15:
        raise RuntimeError(f"rectifier full3 RL α=75: expected Vo≈145.1 V, got {vo_txt!r}")
    _shot(page, "lab-rectifier-full3-rl-alpha75", theme=theme, full_page=True)


def _capture_theme(browser, *, theme: str) -> dict:
    _clear_runs()
    _clear_lab_state()
    from playwright.sync_api import sync_playwright  # noqa: F401

    ctx = browser.new_context(viewport={"width": W, "height": H})
    if theme == "dark":
        _prepare_page_theme(ctx, "dark")
    page = ctx.new_page()
    page.goto(f"{BASE}/?view=home", wait_until="domcontentloaded")
    _set_theme(page, theme)

    meta: dict[str, str | None] = {}

    rect_id = _run_example("rectifier-3ph")
    idmt_id = _run_example("idmt-relay")
    meta["rectifier_run_id"] = rect_id
    meta["idmt_run_id"] = idmt_id
    for run_id, stem in [(rect_id, "run-rectifier"), (idmt_id, "run-idmt")]:
        page.goto(f"{BASE}/?problem={run_id}", wait_until="domcontentloaded")
        page.wait_for_selector(".answer-line, .problem-header", timeout=120_000)
        _shot(page, stem, theme=theme)

    control_step_id = _run_example("control-step")
    meta["control_step_run_id"] = control_step_id
    page.goto(f"{BASE}/?problem={control_step_id}", wait_until="domcontentloaded")
    page.wait_for_selector("#lab-verify-heading", timeout=60_000)
    _assert_text(page, r"0\.500", "control-step derived y_ss")
    _assert_text(page, r"1\.95", "control-step t_s")
    _assert_text(page, r"CONTROL", "control-step lab kind")
    _shot(page, "problem-control-checked", theme=theme)
    page.get_by_role("tab", name="Work").click()
    page.wait_for_selector(".step-timeline-row, .checked-tag", timeout=120_000)
    _shot(page, "problem-control-checked-work", theme=theme)
    lab = _api("GET", f"/api/runs/{control_step_id}/lab")
    cs_sid = (lab.get("lab_meta") or {}).get("control_session_id")
    meta["control_step_session_id"] = cs_sid
    if cs_sid:
        page.goto(f"{BASE}/?view=studio&tab=control&session={cs_sid}", wait_until="domcontentloaded")
        page.locator(".cs-simulate-btn").click()
        page.wait_for_selector(".studio-step-chart svg", timeout=120_000)
        _wait_sim_idle(page)
        _shot(page, "problem-control-checked-lab-agreement", theme=theme, full_page=True)

    rlc_id = _run_series_rlc_collab()
    meta["rlc_run_id"] = rlc_id

    page.goto(f"{BASE}/?problem={rlc_id}", wait_until="domcontentloaded")
    page.wait_for_selector("#lab-verify-heading", timeout=60_000)
    page.get_by_text("Agrees (limit", exact=False).first.wait_for(state="visible", timeout=120_000)
    _shot(page, "collab-01-run-sim-vs-derived-agrees", theme=theme)

    page.goto(f"{BASE}/?view=studio&tab=circuits&run={rlc_id}", wait_until="domcontentloaded")
    page.wait_for_selector(".lab-provenance-bar", timeout=30_000)
    page.wait_for_selector(".studio-lab-drawer", timeout=30_000)
    page.locator(".react-flow__node").first.wait_for(state="visible", timeout=60_000)
    page.locator(".studio-circuit-app .cs-simulate-btn").click()
    _wait_sim_idle(page)
    page.wait_for_selector(".studio-circuit-results .se-waveform", timeout=120_000)
    _assert_text(page, r"11\.630", "collab-02 Vc peak")
    r1_val = page.locator(".studio-circuit-inspector input").first
    if r1_val.count():
        assert "10" in (r1_val.input_value() or ""), "collab-02 R1 should be 10 Ω in inspector"
    _shot(page, "collab-02-lab-provenance-vc-activity", theme=theme, full_page=True)

    rev = _set_r1_and_reverify(rlc_id, 20.0)
    lv = rev.get("lab_verify") or {}
    sim_v = float(lv.get("simulated") or 0)
    if abs(sim_v - 10.0) > 0.05:
        raise RuntimeError(f"after R1→20 Ω: expected Vc max ~10 V from lab/verify, got {sim_v}")
    graph_now = _api("GET", f"/api/runs/{rlc_id}/lab").get("graph") or {}
    _api("POST", "/api/circuit-sandbox/simulate", {"graph": graph_now})
    _api("POST", f"/api/runs/{rlc_id}/lab/verify", {})
    page.goto(f"{BASE}/?problem={rlc_id}", wait_until="networkidle")
    page.wait_for_selector("#lab-verify-heading", timeout=60_000)
    page.get_by_text("Out of date", exact=False).first.wait_for(state="visible", timeout=120_000)
    if page.locator(".lab-verify-badge.is-mismatch").count():
        raise RuntimeError("collab-03: unexpected Mismatch badge")
    rederive_ctas = page.get_by_role("button", name="Ask agent to re-derive")
    if rederive_ctas.count() != 1:
        raise RuntimeError(f"collab-03: expected one Ask agent to re-derive CTA, got {rederive_ctas.count()}")
    if page.locator(".lab-verify-stale-banner.is-review").count() != 1:
        raise RuntimeError("collab-03: expected exactly one review CTA panel")
    _shot(page, "collab-03-out-of-date-ask-rederive", theme=theme)

    page.goto(f"{BASE}/?view=studio&tab=circuits&run={rlc_id}", wait_until="domcontentloaded")
    page.wait_for_selector(".lab-provenance-bar", timeout=30_000)
    page.get_by_role("tab", name="Changes").click()
    page.wait_for_selector(".lab-changes-chip", timeout=30_000)
    page.wait_for_selector(".studio-circuit-results", timeout=30_000)
    _assert_text(page, r"R1:\s*10.*20|R1.*10.*Ω.*20", "collab-04 R1 chip")
    _shot(page, "collab-04-changes-r1-chip", theme=theme, full_page=True)

    page.locator(".lab-provenance-bar button.button-secondary", has_text="Restore agent version").click()
    page.wait_for_timeout(800)
    page.wait_for_selector(".studio-circuit-results", timeout=30_000)
    _shot(page, "collab-04b-after-restore", theme=theme, full_page=True)

    _set_r1_and_reverify(rlc_id, 20.0)
    graph_now = _api("GET", f"/api/runs/{rlc_id}/lab").get("graph") or {}
    _api("POST", "/api/circuit-sandbox/simulate", {"graph": graph_now})
    _api("POST", f"/api/runs/{rlc_id}/lab/verify", {})
    _prepare_rlc_rederive(rlc_id)
    _api("POST", f"/api/runs/{rlc_id}/lab/re-derive", {})
    _api("POST", f"/api/runs/{rlc_id}/lab/verify", {})
    page.goto(f"{BASE}/?problem={rlc_id}", wait_until="domcontentloaded")
    page.wait_for_selector("#lab-verify-heading", timeout=60_000)
    page.get_by_text("Agrees", exact=False).first.wait_for(state="visible", timeout=120_000)
    _assert_text(
        page,
        r"No overshoot · Final value 10\.00 V · Settling \(2%\) 5\.83 ms",
        "collab-03b overshoot headline",
    )
    _assert_text(page, r"Series RLC step", "collab-03b breadcrumb")
    _assert_text(page, r"\b20\b", "collab-03b R1 = 20 Ω")
    lv = _api("GET", f"/api/runs/{rlc_id}/lab")["lab_verify"]
    prob = json.loads((RUNS / rlc_id / "problem.json").read_text(encoding="utf-8"))
    t_s = float(prob.get("t_s") or 0)
    if not (0.0057 < t_s < 0.0059):
        raise RuntimeError(f"collab-03b: expected problem t_s≈5.83 ms, got {t_s*1000:.3f} ms")
    if str(lv.get("status") or "") != "agrees":
        raise RuntimeError(f"collab-03b: expected agrees verify, got {lv.get('status')}")
    _shot(page, "collab-03b-after-rederive-agrees", theme=theme)

    bad_id = _run_example("rlc-bad-derive")
    meta["bad_derive_run_id"] = bad_id
    page.goto(f"{BASE}/?view=studio&tab=circuits&run={bad_id}", wait_until="domcontentloaded")
    page.wait_for_selector(".studio-circuit-app", timeout=30_000)
    page.locator(".studio-circuit-app .cs-simulate-btn").click()
    _wait_sim_idle(page)
    page.goto(f"{BASE}/?problem={bad_id}", wait_until="domcontentloaded")
    page.wait_for_selector(
        ".lab-needs-review, .lab-needs-review-banner, .lab-verify-badge.is-differs, .lab-verify-badge.is-mismatch",
        timeout=90_000,
    )
    lv_bad = _api("GET", f"/api/runs/{bad_id}/lab").get("lab_verify") or {}
    m0 = (lv_bad.get("metrics") or [{}])[0]
    derived_bad = float(m0.get("derived") or 0)
    sim_bad = m0.get("simulated")
    if abs(derived_bad - 11.96) > 0.08:
        raise RuntimeError(f"collab-05: expected forward-Euler derived ~11.96 V, got {derived_bad}")
    if str(lv_bad.get("status") or "") not in ("mismatch", "differs"):
        raise RuntimeError(f"collab-05: expected mismatch verify, got {lv_bad.get('status')}")
    if sim_bad is not None and abs(float(sim_bad) - 11.63) > 0.15:
        raise RuntimeError(f"collab-05: expected sim ~11.63 V, got {sim_bad}")
    _shot(page, "collab-05-forward-euler-mismatch", theme=theme)

    from electrical_engineer.runner.execute import execute

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
    meta["control_run_id"] = ctl_id
    ctl_sid = None
    lab_meta_path = Path(control["run_dir"]) / "lab_meta.json"
    if lab_meta_path.is_file():
        ctl_sid = json.loads(lab_meta_path.read_text(encoding="utf-8")).get("control_session_id")
    meta["control_session_id"] = ctl_sid

    page.goto(f"{BASE}/?problem={ctl_id}", wait_until="domcontentloaded")
    page.wait_for_selector(".answer-line", timeout=120_000)
    page.get_by_text("Agrees (limit", exact=False).first.wait_for(state="visible", timeout=120_000)
    _shot(page, "collab-06-control-unity-run-agrees", theme=theme)
    if ctl_sid:
        page.goto(f"{BASE}/?view=studio&tab=control&session={ctl_sid}", wait_until="domcontentloaded")
        page.locator(".cs-simulate-btn").click()
        page.wait_for_selector(".studio-margins .num, .studio-step-chart", timeout=120_000)
        page.get_by_text("0.909", exact=False).first.wait_for(state="visible", timeout=60_000)
        page.get_by_text("0.36", exact=False).first.wait_for(state="visible", timeout=60_000)
        _wait_sim_idle(page)
        _shot(page, "collab-06-control-unity-lab-agreement", theme=theme, full_page=True)

    _capture_rectifier_topologies(page, theme=theme)

    narrow_ctx = browser.new_context(viewport={"width": 1024, "height": H})
    if theme == "dark":
        _prepare_page_theme(narrow_ctx, "dark")
    narrow = narrow_ctx.new_page()
    narrow.goto(f"{BASE}/?view=home", wait_until="domcontentloaded")
    _set_theme(narrow, theme)
    key_1024 = [
        ("?view=home", "home-empty", ".example-grid-six"),
        ("?view=problems", "problems-list", ".problems-table, .problems-empty"),
        ("?view=gallery", "gallery", ".gallery-card"),
        ("?view=library", "library", ".library"),
        ("?view=learn", "learn-landing", ".learn-page h1"),
        ("?view=settings", "settings-agents", ".settings-page"),
    ]
    divider_id = _run_example("divider")
    ctrl_req = urllib.request.Request(
        f"{BASE}/api/control-studio/sessions",
        method="POST",
        data=json.dumps({"title": "Round 12 · Unity", "golden": "unity_first_order"}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(ctrl_req, timeout=60) as resp:
        ctrl_session = json.loads(resp.read().decode())["session_id"]
    for route, stem, sel in [
        *key_1024,
        (f"?problem={divider_id}", "problem-divider-run", ".answer-line"),
        (f"?view=studio&tab=control&session={ctrl_session}", "studio-control", ".cs-app.control-studio"),
        ("?view=studio&tab=circuits", "studio-circuit-sandbox", ".studio-circuit-app"),
    ]:
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
    ctx.close()
    return meta


def main() -> int:
    ngspice_version = _require_ngspice()
    print("ngspice:", ngspice_version)
    OUT.mkdir(parents=True, exist_ok=True)
    from electrical_engineer.engines.spice_runner import simulator_status

    if not simulator_status().get("available"):
        raise RuntimeError(f"ngspice unavailable: {simulator_status()}")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright missing", file=sys.stderr)
        return 1

    if os.environ.get("ROUND12_START_UI") == "1":
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
            return _capture_all(sync_playwright, ngspice_version)
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
    _wait_health()
    return _capture_all(sync_playwright, ngspice_version)


def _capture_all(sync_playwright, ngspice_version: str) -> int:
    metas: dict = {"ngspice_version": ngspice_version}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for theme in ("light", "dark"):
            metas[theme] = _capture_theme(browser, theme=theme)
        browser.close()
    (OUT / "collab_capture_meta.json").write_text(json.dumps(metas, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
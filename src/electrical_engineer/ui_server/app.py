"""Persistent UI HTTP server. Bind 127.0.0.1 only."""

from __future__ import annotations

import json
import logging
import os
import shutil
import threading
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

_LOG = logging.getLogger(__name__)

BIND_HOST = "127.0.0.1"
BIND_PORT = 8765
_UPLOAD_MAX = 20 * 1024 * 1024
_UPLOAD_SUFFIX = {".md", ".txt", ".pdf"}


def ui_page_url(run_id: str | None = None) -> str:
    base = f"http://{BIND_HOST}:{BIND_PORT}/"
    if not run_id:
        return base
    return f"{base}?run={run_id}"


_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00"
    b"\x00\x01\x01\x00\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)
_SVG = "<svg xmlns='http://www.w3.org/2000/svg' width='1' height='1'></svg>"


def _repo_root() -> Path:
    from electrical_engineer.paths import checkout_root, install_root

    return checkout_root() or install_root()


def _icon_path() -> Path | None:
    from electrical_engineer.paths import ui_dist_dir

    here = _repo_root()
    for cand in (
        ui_dist_dir() / "arc-icon.png",
        here / "ui" / "dist" / "arc-icon.png",
        here / "ui" / "public" / "arc-icon.png",
        here / "assets" / "brand" / "arc-icon.png",
    ):
        if cand.is_file():
            return cand
    return None


def _read_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _opaque_title(title: str, folder_name: str) -> bool:
    text = (title or "").strip()
    if not text or text == folder_name:
        return True
    if text.startswith("cs-") and len(text) <= 16:
        return True
    return "-" in text and " " not in text and text.lower() == text


def _human_run_title(folder: Path, evid: dict) -> str:
    from electrical_engineer.circuit.title import run_title, title_with_value

    title = str(evid.get("title") or "").strip()
    if title and not _opaque_title(title, folder.name):
        return title
    problem = _read_json(folder / "problem.json")
    recipe_id = str(evid.get("recipe_id") or problem.get("recipe_id") or "")
    if problem:
        derived = run_title(recipe_id or "solve-circuit-problem", problem)
        if derived and not _opaque_title(derived, folder.name):
            return derived
    diagram = _read_json(folder / "control_diagram.json")
    if isinstance(diagram.get("title"), str) and diagram["title"].strip():
        return str(diagram["title"]).strip()
    if folder.name.startswith("cs-"):
        return "PID on DC motor"
    val = evid.get("value")
    if recipe_id:
        return title_with_value(recipe_id, problem, val, bool(evid.get("unchecked")))
    return "Untitled run"


def _subject_tag(recipe_id: str, folder_name: str) -> str:
    rid = recipe_id or ""
    if "power-electronic" in rid or "electronics" in rid:
        return "Power electronics"
    if "drive" in rid or "machine" in rid:
        return "Machines"
    if rid.startswith("solve-circuit") or "circuit" in rid or "spice" in rid:
        return "Circuits"
    if "control" in rid or folder_name.startswith("cs-"):
        return "Control"
    if "power" in rid or "swing" in rid or rid.startswith("ed-") or "fault" in rid:
        return "Power"
    if "signal" in rid:
        return "Signals"
    if rid:
        return rid.replace("-", " ").title()
    return "General"


def _dedupe_run_items(items: list[dict]) -> list[dict]:
    """Keep the newest run per display title (Recent / Continue / Problems)."""
    best: dict[str, dict] = {}
    for item in items:
        key = str(item.get("display_title") or item.get("title") or item.get("id") or "").strip().lower()
        if not key:
            continue
        prev = best.get(key)
        if prev is None or float(item.get("modified_at") or 0) > float(prev.get("modified_at") or 0):
            best[key] = item
    return sorted(best.values(), key=lambda x: -float(x.get("modified_at") or 0))


def _relative_time_label(folder: Path, evid: dict) -> str:
    import time

    raw = evid.get("updated_at_ms")
    try:
        ts = float(raw) / 1000.0 if raw is not None else folder.stat().st_mtime
    except (OSError, TypeError, ValueError):
        return ""
    delta = max(0, int(time.time() - ts))
    if delta < 60:
        return "just now"
    if delta < 3600:
        return f"{delta // 60}m ago"
    if delta < 86400:
        return f"{delta // 3600}h ago"
    return f"{delta // 86400}d ago"


def _run_list_hidden(folder: Path) -> bool:
    name = folder.name
    if name.startswith(("_", "unmatched")):
        return True
    evid = _read_json(folder / "evidentiary.json") or _read_json(folder / "summary.json")
    title = str(evid.get("title") or "").strip()
    recipe = str(evid.get("recipe_id") or "")
    if name.startswith("cs-") and (not title or title == name):
        return True
    low = (title or name).lower()
    if low.startswith("unmatched") or "scratch" in low or "scratch" in name.lower():
        return True
    return recipe == "unmatched-cosolver"


def _is_sample_run(folder: Path) -> bool:
    return (folder / "sample.json").is_file()


def _mark_sample_run(folder: Path) -> None:
    try:
        (folder / "sample.json").write_text('{"sample":true}\n', encoding="utf-8")
    except OSError as exc:
        _LOG.warning("could not mark sample run %s: %s", folder, exc)


def _run_list_item(folder: Path) -> dict:
    evid = _read_json(folder / "evidentiary.json") or _read_json(folder / "summary.json")
    name = folder.name
    try:
        modified_at = folder.stat().st_mtime
    except OSError:
        modified_at = 0.0
    recipe_id = str(evid.get("recipe_id") or "")
    display_title = _human_run_title(folder, evid)
    return {
        "id": name,
        "title": display_title,
        "display_title": display_title,
        "subject": _subject_tag(recipe_id, name),
        "relative_time": _relative_time_label(folder, evid),
        "unchecked": bool(evid.get("unchecked")),
        "recipe_id": recipe_id,
        "modified_at": modified_at,
        "is_studio_session": name.startswith("cs-"),
        "sample": _is_sample_run(folder),
    }


def _visible_run_dirs(runs_dir: Path) -> list[Path]:
    if not runs_dir.is_dir():
        return []
    return [p for p in sorted(runs_dir.iterdir()) if p.is_dir() and not _run_list_hidden(p)]


def _seed_disabled() -> bool:
    return os.environ.get("EE_NO_SEED", "") in {"1", "true", "TRUE"}


def seed_sample_runs(cwd: Path, runs_dir: Path) -> int:
    """Execute curated UI examples into runs_dir; mark each with sample.json. Returns count seeded."""
    from electrical_engineer.runner.execute import execute

    runs_dir.mkdir(parents=True, exist_ok=True)
    seeded = 0
    for ex in _UI_EXAMPLES:
        try:
            out = execute(str(ex["recipe_id"]), cwd=cwd, problem=dict(ex["problem"]))
            rid = out.get("run_id")
            if not rid:
                continue
            folder = runs_dir / str(rid)
            if folder.is_dir():
                _mark_sample_run(folder)
                seeded += 1
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("sample seed skipped for %s: %s", ex.get("id"), exc)
    return seeded


def clear_sample_runs(runs_dir: Path) -> int:
    """Delete runs that carry sample.json. Returns count removed."""
    removed = 0
    if not runs_dir.is_dir():
        return 0
    for folder in list(runs_dir.iterdir()):
        if folder.is_dir() and _is_sample_run(folder):
            shutil.rmtree(folder, ignore_errors=True)
            removed += 1
    return removed


def _golden_thumb(rel: str) -> str:
    return f"/api/visual-kit/golden/{rel}"


_RLC_CIR = "\n".join(
    [
        "* series rlc step",
        "V1 1 0 DC 10",
        "R1 1 2 10",
        "L1 2 3 10m",
        "C1 3 0 100u",
        ".tran 50u 20m",
        ".end",
        "",
    ]
)

_UI_EXAMPLES = (
    {
        "id": "divider",
        "title": "Voltage divider",
        "caption": "Find Vout for 10 V into 1 kΩ / 1 kΩ",
        "subject": "Circuits",
        "thumbnail": _golden_thumb("circuits/schematic.divider.png"),
        "recipe_id": "solve-circuit-problem",
        "problem": {"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000},
    },
    {
        "id": "rlc-step",
        "title": "Series RLC step",
        "caption": "Underdamped capacitor voltage after a 10 V step",
        "subject": "Circuits",
        "thumbnail": _golden_thumb("circuits/schematic.rlc_series.png"),
        "recipe_id": "simulate-circuit",
        "problem": {
            "kind": "series_rlc",
            "vin": 10,
            "v_step": 10,
            "r_ohm": 10,
            "l_h": 0.01,
            "c_f": 100e-6,
            "probe_node": 3,
            "analysis": "tran",
            "prompt": "Series RLC step",
            "cir": _RLC_CIR,
        },
    },
    {
        "id": "control-step",
        "title": "First-order step",
        "caption": "Step response for 1/(s+1)",
        "subject": "Control",
        "thumbnail": _golden_thumb("control/control.step.png"),
        "recipe_id": "solve-control-problem",
        "problem": {"tf": "1/(s+1)", "prompt": "First-order step"},
    },
    {
        "id": "digital-stable",
        "title": "Digital loop",
        "caption": "Discrete pole inside the unit circle",
        "subject": "Control",
        "thumbnail": _golden_thumb("control/control.nyquist.png"),
        "recipe_id": "solve-digital-control-problem",
        "problem": {"num": [0.1], "den": [1.0, -0.5], "ts": 0.01, "prompt": "Digital loop"},
    },
    {
        "id": "smib-swing",
        "title": "SMIB swing",
        "caption": "Equal-area swing after a cleared fault",
        "subject": "Power",
        "thumbnail": _golden_thumb("swing/power.swing_equal_area.png"),
        "recipe_id": "smib-swing-study",
        "problem": {"prompt": "SMIB swing"},
    },
    {
        "id": "lg-fault",
        "title": "LG fault current",
        "caption": "Single line-to-ground fault from the sequence network",
        "subject": "Power",
        "thumbnail": _golden_thumb("oneline/power.oneline_bus.png"),
        "recipe_id": "simulate-power-fault",
        "problem": {
            "fault_type": "LG",
            "z1_pu": 0.1,
            "z2_pu": 0.1,
            "z0_pu": 0.3,
            "prompt": "LG fault current",
        },
    },
    {
        "id": "ed-dispatch",
        "title": "Economic dispatch",
        "caption": "Lambda iteration for a 500 MW load",
        "subject": "Power",
        "thumbnail": _golden_thumb("ed/power.dispatch_curve.png"),
        "recipe_id": "ed-lambda-study",
        "problem": {"PD": 500, "prompt": "Economic dispatch"},
    },
    {
        "id": "buck-ccm",
        "title": "Buck converter",
        "caption": "CCM duty for 12 V down to 5 V",
        "subject": "Power electronics",
        "thumbnail": _golden_thumb("circuits/waveform.phasor.png"),
        "recipe_id": "study-power-electronics-v2",
        "problem": {
            "solver": "ccm_buck",
            "vin": 12,
            "vout": 5,
            "l": 47e-6,
            "c": 100e-6,
            "fs": 100e3,
            "ripple_pct": 30,
            "i_out": 1.0,
            "prompt": "Buck converter",
        },
    },
    {
        "id": "dc-drive",
        "title": "DC drive speed",
        "caption": "Steady speed for an armature drive with load torque",
        "subject": "Machines",
        "thumbnail": _golden_thumb("control/control.step.png"),
        "recipe_id": "solve-drives-problem",
        "problem": {
            "kind": "dc",
            "v_dc": 120,
            "ra_ohm": 1,
            "k_torque": 0.5,
            "t_load_nm": 5,
            "prompt": "DC drive speed",
        },
    },
)

_NODE_ROLE = {
    "retrieve": "Look up a reference",
    "solve": "Draft the solution",
    "web": "Check the write-up",
    "check": "Numeric check",
    "trap": "Trap check",
    "label": "Verdict",
    "summary": "Save the run",
    "swing": "SMIB swing engine",
    "ctrl": "Step and Bode",
    "exam": "Exam solver",
    "dig": "Discrete-time check",
    "drive": "Drive steady state",
    "flow": "Load flow and fault",
    "ed": "Lambda dispatch",
    "prot": "Protection study",
    "spice": "Circuit simulation",
    "load": "Load the netlist",
    "derive": "Derive the circuit",
    "base": "Per-unit base",
}


def _work_steps(run_dir: Path) -> list[dict]:
    from electrical_engineer.ui_server.work_steps import work_steps

    return work_steps(run_dir)


def _recipe_from_prompt(prompt: str, subject: str) -> tuple[str, dict]:
    text = (prompt or "").strip().lower()
    subj = (subject or "circuits").strip().lower()
    if subj == "control" or "bode" in text or "transfer" in text:
        return "solve-control-problem", {"tf": "1/(s+1)", "prompt": prompt}
    if subj == "power" or "swing" in text or "fault" in text:
        return "smib-swing-study", {}
    if subj in {"machines", "drives"} or "motor" in text or "drive" in text:
        return "solve-drives-problem", {
            "kind": "dc",
            "v_dc": 120,
            "ra_ohm": 1,
            "k_torque": 0.5,
            "t_load_nm": 5,
        }
    if subj in {"power_electronics", "electronics"} or "z-transform" in text:
        return "solve-digital-control-problem", {"num": [0.1], "den": [1.0, -0.5], "ts": 0.01}
    if subj == "signals":
        return "solve-signals-problem", {"prompt": prompt}
    if "divider" in text or "vout" in text:
        return "solve-circuit-problem", {"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000}
    return "solve-circuit-problem", {"kind": "ohms_law", "v": 12, "r": 4, "prompt": prompt}


def _safe_book_id(raw: str | None) -> str:
    text = "".join(ch if ch.isalnum() or ch in "._-" else "-" for ch in str(raw or "").strip())
    return (text.strip("-") or "unknown")[:80]


def _rag_tags(
    book_id: str | None,
    chapter_id: str | None,
    folder_tag: str | None,
    domain_tag: str | None,
    licence_tag: str | None,
) -> dict:
    return {
        "book_id": _safe_book_id(book_id) if book_id else None,
        "chapter_id": chapter_id or None,
        "folder_tag": folder_tag or None,
        "domain_tag": domain_tag or None,
        "licence_tag": licence_tag or None,
    }


def create_app(root: Path | None = None) -> FastAPI:
    app = FastAPI()
    runs = (root or Path.cwd()) / "runs"
    cwd = root or Path.cwd()
    seed_state = {"active": False}

    def _start_seed_if_needed() -> None:
        if _seed_disabled() or seed_state["active"]:
            return
        if _visible_run_dirs(runs):
            return
        seed_state["active"] = True

        def _worker() -> None:
            try:
                seed_sample_runs(cwd, runs)
            finally:
                seed_state["active"] = False

        threading.Thread(target=_worker, name="arc-ui-seed", daemon=True).start()

    _start_seed_if_needed()

    @app.get("/arc-icon.png", response_model=None)
    def brand_icon() -> FileResponse | Response:
        path = _icon_path()
        if path is not None:
            return FileResponse(path, media_type="image/png")
        return Response(_PNG, media_type="image/png")

    @app.get("/api/health")
    def health() -> dict:
        return {"bind": BIND_HOST, "ok": True}

    @app.get("/api/engines")
    def engines_status() -> dict:
        from importlib import import_module

        from electrical_engineer import __version__

        def probe(label: str, module: str | None = None, *, detail: str = "") -> dict:
            if module is None:
                return {"name": label, "available": False, "detail": detail or "via Arc, not installed"}
            try:
                import_module(module)
                return {"name": label, "available": True, "detail": ""}
            except Exception:  # noqa: BLE001
                return {"name": label, "available": False, "detail": detail or "Not installed"}

        rows = [
            {"name": "Numeric (algebraic checks)", "available": True, "detail": ""},
            probe("SPICE (ngspice / PySpice)", "PySpice"),
            probe("python-control", "control"),
            probe("pandapower", "pandapower"),
            probe("MATLAB engine", detail="via Arc, not installed"),
            probe("Simulink engine", detail="via Arc, not installed"),
        ]
        return {"engines": rows, "version": __version__}

    @app.get("/api/runs")
    def list_runs() -> dict:
        items = []
        if runs.is_dir():
            items = [
                _run_list_item(p)
                for p in sorted(runs.iterdir())
                if p.is_dir() and not _run_list_hidden(p)
            ]
        items = _dedupe_run_items(items)
        return {"runs": items, "seeding": bool(seed_state["active"])}

    @app.delete("/api/runs/samples")
    def delete_samples() -> dict:
        n = clear_sample_runs(runs)
        return {"removed": n}

    @app.post("/api/runs/samples")
    def reseed_samples() -> dict:
        if seed_state["active"]:
            return JSONResponse({"error": "seeding already running"}, status_code=409)
        seed_state["active"] = True
        try:
            n = seed_sample_runs(cwd, runs)
        finally:
            seed_state["active"] = False
        return {"seeded": n}

    @app.get("/api/examples")
    def list_examples() -> dict:
        return {"examples": [{k: ex[k] for k in ex if k != "problem"} for ex in _UI_EXAMPLES]}

    @app.get("/api/reference")
    def reference_search(q: str = "", limit: int = 20) -> dict:
        from electrical_engineer.reference.catalog import list_domains, search_records

        domains = list_domains()
        hits = search_records(q, limit=max(1, min(limit, 50))) if q.strip() else []
        return {
            "domains": [{"id": k, "count": v} for k, v in sorted(domains.items())],
            "results": hits,
            "query": q,
        }

    @app.get("/api/reference/{record_id}")
    def reference_get(record_id: str) -> dict:
        from electrical_engineer.reference.catalog import get_record

        rec = get_record(record_id)
        if rec is None:
            return JSONResponse({"error": "missing"}, status_code=404)
        return {"record": rec}

    @app.get("/api/capabilities")
    def capabilities() -> dict:
        from electrical_engineer.catalog import list_workflow_ids, workflows_root

        root = workflows_root(cwd)
        packs = [
            {"id": "circuits", "label": "Circuits", "blurb": "Dividers, RLC, and SPICE checks"},
            {"id": "control", "label": "Control", "blurb": "Bode, step response, block diagrams"},
            {"id": "power", "label": "Power", "blurb": "Faults, swing, AGC, economic dispatch"},
            {"id": "signals", "label": "Signals", "blurb": "FFT and frequency-domain homework"},
            {"id": "machines", "label": "Machines", "blurb": "DC drives and steady-state speed"},
        ]
        ids = list_workflow_ids(cwd)
        out = []
        for pack in packs:
            folder = root / pack["id"]
            count = 0
            if folder.is_dir():
                count = len(list(folder.glob("**/*.yaml")))
            if count == 0:
                # fall back: count ids that mention the pack name
                count = sum(1 for i in ids if pack["id"] in i.replace("_", "-") or pack["id"] in i)
            out.append({**pack, "recipe_count": count})
        return {"packs": out, "recipe_total": len(ids)}

    @app.post("/api/problems")
    async def create_problem(request: Request) -> dict:
        from electrical_engineer.runner.execute import execute

        try:
            body = await request.json()
        except json.JSONDecodeError:
            return JSONResponse({"error": "invalid json"}, status_code=400)
        prompt = str(body.get("prompt") or "").strip()
        if not prompt:
            return JSONResponse({"error": "prompt required"}, status_code=400)
        subject = str(body.get("subject") or "circuits")
        recipe_id, problem = _recipe_from_prompt(prompt, subject)
        try:
            out = execute(str(recipe_id), cwd=cwd, problem=problem)
        except Exception as exc:  # noqa: BLE001
            return JSONResponse({"error": "run failed", "detail": str(exc)}, status_code=500)
        return {
            "run_id": out.get("run_id"),
            "recipe_id": recipe_id,
            "unchecked": bool((out.get("summary") or {}).get("unchecked")),
        }

    @app.post("/api/examples/{example_id}/run")
    def run_example(example_id: str) -> dict:
        from electrical_engineer.runner.execute import execute

        match = next((ex for ex in _UI_EXAMPLES if ex["id"] == example_id), None)
        if match is None:
            return JSONResponse({"error": "unknown example"}, status_code=404)
        try:
            out = execute(str(match["recipe_id"]), cwd=cwd, problem=dict(match["problem"]))
        except Exception as exc:  # noqa: BLE001
            return JSONResponse({"error": "run failed", "detail": str(exc)}, status_code=500)
        return {"run_id": out.get("run_id"), "unchecked": bool((out.get("summary") or {}).get("unchecked"))}

    @app.get("/api/runs/{run_id}")
    def run_detail(run_id: str) -> dict:
        d = runs / run_id
        summary = d / "evidentiary.json"
        if not summary.is_file():
            summary = d / "summary.json"
        if not summary.is_file():
            return JSONResponse({"error": "missing", "state": "failed"}, status_code=404)
        evid_text = summary.read_text(encoding="utf-8")
        evid_obj = _read_json(summary)
        argument = (d / "argument.md").read_text(encoding="utf-8") if (d / "argument.md").is_file() else ""
        plan = (d / "plan.md").read_text(encoding="utf-8") if (d / "plan.md").is_file() else ""
        observation = (d / "observation.json").read_text(encoding="utf-8") if (d / "observation.json").is_file() else "{}"
        obs_obj = _read_json(d / "observation.json")
        observation_excerpt = {
            "unchecked_reason": obs_obj.get("unchecked_reason"),
            "capabilities": obs_obj.get("capabilities") or [],
            "providers": obs_obj.get("providers") or [],
            "retrieve_empty": bool((obs_obj.get("retrieve") or {}).get("empty")),
            "unchecked": bool(evid_obj.get("unchecked")),
            "token": evid_obj.get("token"),
        }
        trace_excerpt: list[dict] = []
        activity_feed: list[dict] = []
        trace_path = d / "trace.jsonl"
        if trace_path.is_file():
            lines = [ln for ln in trace_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
            for ln in lines[-40:]:
                try:
                    ev = json.loads(ln)
                except json.JSONDecodeError:
                    continue
                if isinstance(ev, dict):
                    attrs = ev.get("attrs") or {}
                    node_id = attrs.get("node_id")
                    trace_excerpt.append(
                        {
                            "name": ev.get("name"),
                            "duration_ms": ev.get("duration_ms"),
                            "node_id": node_id,
                            "activity": attrs.get("activity") or _NODE_ROLE.get(str(node_id or ""), ""),
                            "ok": attrs.get("ok"),
                            "unchecked": attrs.get("unchecked"),
                        }
                    )
                    if ev.get("name") == "node.end":
                        activity_feed.append(
                            {
                                "node": node_id,
                                "role": _NODE_ROLE.get(str(node_id or ""), str(node_id or "step")),
                                "ok": attrs.get("ok"),
                                "unchecked": bool(attrs.get("unchecked")),
                                "duration_ms": ev.get("duration_ms"),
                            }
                        )
        waiting = (d / "draft.cir").is_file() and not (d / "confirmed.json").is_file()
        state = "waiting-human" if waiting else "done"
        graph = _read_json(d / "graph.json")
        control_diagram = _read_json(d / "control_diagram.json")
        problem = _read_json(d / "problem.json")
        try:
            modified_at = d.stat().st_mtime
        except OSError:
            modified_at = 0.0
        web_sources = _read_json(d / "evidence" / "web_sources.json")
        similar_probs = _read_json(d / "evidence" / "similar_problems.json")
        answer_cited = (
            (d / "evidence" / "answer_cited.md").read_text(encoding="utf-8")
            if (d / "evidence" / "answer_cited.md").is_file()
            else ""
        )
        wv = evid_obj.get("web_verification") or {}
        source_chips = []
        for c in web_sources.get("citations") or evid_obj.get("citations") or []:
            if not isinstance(c, dict):
                continue
            source_chips.append(
                {
                    "id": c.get("citation_id"),
                    "domain": c.get("domain"),
                    "title": c.get("title") or c.get("url"),
                    "url": c.get("url"),
                }
            )
        disagreement = wv.get("disagreement_banner") or evid_obj.get("disagreement_banner")
        return {
            "id": run_id,
            "title": _human_run_title(d, evid_obj),
            "problem": problem,
            "modified_at": modified_at,
            "summary": evid_text,
            "evidentiary": evid_text,
            "argument": argument or answer_cited,
            "answer_markdown": evid_obj.get("answer_markdown") or answer_cited or None,
            "web_verification": wv or None,
            "web_sources": web_sources or None,
            "similar_problems": similar_probs or None,
            "source_chips": source_chips,
            "disagreement_banner": disagreement,
            "plan": plan,
            "observation": observation,
            "observation_excerpt": observation_excerpt,
            "trace_excerpt": trace_excerpt,
            "graph": graph,
            "control_diagram": control_diagram,
            "work_steps": _work_steps(d),
            "activity_feed": activity_feed,
            "state": state,
        }

    @app.get("/api/runs/{run_id}/artifact.svg")
    def artifact_svg(run_id: str) -> Response:
        d = runs / run_id
        named = d / "artifact.svg"
        if named.is_file():
            return Response(named.read_text(), media_type="image/svg+xml")
        for path in sorted(d.glob("*.svg")):
            return Response(path.read_text(), media_type="image/svg+xml")
        return Response(_SVG, media_type="image/svg+xml")

    @app.get("/api/runs/{run_id}/artifact.png")
    def artifact_png(run_id: str) -> Response:
        path = runs / run_id / "artifact.png"
        body = path.read_bytes() if path.is_file() else _PNG
        return Response(body, media_type="image/png")

    @app.get("/api/runs/{run_id}/file/{name}")
    def run_file(run_id: str, name: str) -> Response:
        safe = Path(name).name
        path = runs / run_id / safe
        if not path.is_file():
            return JSONResponse({"error": "missing"}, status_code=404)
        if safe.endswith(".json"):
            return Response(path.read_text(encoding="utf-8"), media_type="application/json")
        if safe.endswith(".png"):
            return Response(path.read_bytes(), media_type="image/png")
        if safe.endswith(".svg"):
            return Response(path.read_text(encoding="utf-8"), media_type="image/svg+xml")
        return FileResponse(path)

    @app.put("/api/runs/{run_id}/graph", response_model=None)
    async def put_graph(run_id: str, request: Request):
        from electrical_engineer.circuit.graph import GraphError, write_graph

        d = runs / run_id
        d.mkdir(parents=True, exist_ok=True)
        try:
            body = await request.json()
            out = write_graph(d, body if isinstance(body, dict) else {})
        except GraphError as exc:
            return JSONResponse({"error": str(exc)}, status_code=400)
        return {"id": run_id, **out}

    @app.post("/api/runs/{run_id}/confirm")
    async def confirm(run_id: str, request: Request) -> dict:
        from electrical_engineer.circuit.graph import GraphError, write_graph

        d = runs / run_id
        d.mkdir(parents=True, exist_ok=True)
        raw = await request.body()
        payload: dict = {}
        if raw:
            try:
                loaded = json.loads(raw)
            except json.JSONDecodeError:
                loaded = {}
            if isinstance(loaded, dict):
                payload = loaded
        graph = payload.get("graph") if "graph" in payload else None
        if graph is None and (payload.get("schema") or payload.get("nodes")):
            graph = payload
        if graph is not None:
            try:
                write_graph(d, graph if isinstance(graph, dict) else {})
            except GraphError:
                pass
        (d / "confirmed.json").write_text(
            '{"confirmed": true, "simulate": false}', encoding="utf-8"
        )
        return {"id": run_id, "confirmed": True, "simulate": False}

    @app.get("/api/rag/inventory")
    def rag_inventory() -> dict:
        from electrical_engineer.rag.inventory import listed_inventory

        return {"items": listed_inventory(cwd)}

    @app.post("/api/rag/upload")
    async def rag_upload(request: Request) -> dict:
        from electrical_engineer.rag.inventory import add_doc, corpus_dir

        q = request.query_params
        rights = str(q.get("rights") or request.headers.get("x-ee-rights") or "")
        if rights.strip().lower() not in {"1", "true", "yes", "on"}:
            return JSONResponse({"error": "Confirm you have rights to this file."}, status_code=400)
        name = Path(str(q.get("filename") or request.headers.get("x-filename") or "upload.md")).name
        suffix = Path(name).suffix.lower()
        if suffix not in _UPLOAD_SUFFIX:
            return JSONResponse({"error": "Use a .pdf, .md, or .txt file."}, status_code=400)
        body = await request.body()
        if len(body) > _UPLOAD_MAX:
            return JSONResponse({"error": "File is larger than 20 MB."}, status_code=400)
        if not body:
            return JSONResponse({"error": "File is empty."}, status_code=400)
        bid = _safe_book_id(q.get("book_id") or Path(name).stem)
        dest_dir = corpus_dir(cwd) / bid
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / name
        dest.write_bytes(body)
        rec = add_doc(
            str(dest),
            tags=_rag_tags(
                bid,
                q.get("chapter_id"),
                q.get("folder_tag"),
                q.get("domain_tag"),
                q.get("licence_tag"),
            ),
            cwd=cwd,
        )
        return {"ok": True, "item": rec}

    @app.post("/api/rag/tag")
    async def rag_tag(request: Request) -> dict:
        from electrical_engineer.rag.inventory import tag_doc

        payload = await request.json()
        if not isinstance(payload, dict):
            return JSONResponse({"error": "tag body must be an object"}, status_code=400)
        path = str(payload.get("path") or payload.get("source") or "")
        if not path:
            return JSONResponse({"error": "path is required"}, status_code=400)
        hit = tag_doc(
            path,
            _rag_tags(
                payload.get("book_id"),
                payload.get("chapter_id"),
                payload.get("folder_tag"),
                payload.get("domain_tag"),
                payload.get("licence_tag"),
            ),
            cwd=cwd,
        )
        if hit is None:
            return JSONResponse({"error": "no matching document"}, status_code=404)
        return {"ok": True, "item": hit}

    @app.post("/api/rag/query")
    async def rag_query(request: Request) -> dict:
        from electrical_engineer.rag.retrieve import retrieve

        payload = await request.json()
        if not isinstance(payload, dict):
            return JSONResponse({"error": "query body must be an object"}, status_code=400)
        query = str(payload.get("query") or "").strip()
        if not query:
            return JSONResponse({"error": "query is required"}, status_code=400)
        hops = payload.get("hops", 1)
        try:
            hops_n = int(hops)
        except (TypeError, ValueError):
            hops_n = 1
        filters = {}
        for key in ("book_id", "chapter_id", "folder_tag", "domain_tag"):
            val = payload.get(key)
            if val:
                filters[key] = val
        return retrieve(filters, query=query, cwd=cwd, hops=hops_n)

    @app.get("/api/frontier/scorecard")
    def frontier_scorecard() -> dict:
        path = _repo_root() / "docs/planning/SCORECARD.md"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        return {"markdown": text, "path": str(path.relative_to(_repo_root()))}

    @app.get("/api/visual-kit")
    def visual_kit() -> dict:
        from electrical_engineer.visual_kit.registry import load_manifest

        return {
            "manifest_version": load_manifest().get("manifest_version"),
            "components": load_manifest().get("components") or [],
            "goldens_base": "/api/visual-kit/golden/",
        }

    from electrical_engineer.ui_server.studio_routes import register_studio_routes

    register_studio_routes(app, root=cwd)

    @app.get("/api/visual-kit/golden/{rel_path:path}", response_model=None)
    def visual_golden(rel_path: str):
        base = (_repo_root() / "artifacts" / "visual-goldens").resolve()
        target = (base / rel_path).resolve()
        if not str(target).startswith(str(base)) or not target.is_file():
            return JSONResponse({"error": "missing"}, status_code=404)
        media = "image/gif" if target.suffix == ".gif" else "image/png"
        return FileResponse(target, media_type=media)

    from electrical_engineer.paths import ui_dist_dir

    ui_dist = ui_dist_dir()
    index = ui_dist / "index.html"
    if index.is_file():
        app.mount("/assets", StaticFiles(directory=ui_dist / "assets"), name="assets")

        @app.get("/")
        def spa() -> FileResponse:
            return FileResponse(index)

        @app.get("/gallery")
        def gallery_spa() -> FileResponse:
            return FileResponse(index)

    return app


def bind_host() -> str:
    return BIND_HOST


def should_open_browser() -> bool:
    return os.environ.get("EE_NO_BROWSER", "") not in {"1", "true", "TRUE"}

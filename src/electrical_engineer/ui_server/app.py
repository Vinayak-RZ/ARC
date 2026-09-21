"""Persistent UI HTTP server. Bind 127.0.0.1 only."""

from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

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
    return Path(__file__).resolve().parents[3]


def _icon_path() -> Path | None:
    here = _repo_root()
    for cand in (
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


def _run_list_item(folder: Path) -> dict:
    evid = _read_json(folder / "evidentiary.json") or _read_json(folder / "summary.json")
    return {
        "id": folder.name,
        "title": str(evid.get("title") or folder.name),
        "unchecked": bool(evid.get("unchecked")),
        "recipe_id": str(evid.get("recipe_id") or ""),
    }


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

    @app.get("/arc-icon.png", response_model=None)
    def brand_icon() -> FileResponse | Response:
        path = _icon_path()
        if path is not None:
            return FileResponse(path, media_type="image/png")
        return Response(_PNG, media_type="image/png")

    @app.get("/api/health")
    def health() -> dict:
        return {"bind": BIND_HOST, "ok": True}

    @app.get("/api/runs")
    def list_runs() -> dict:
        items = []
        if runs.is_dir():
            items = [_run_list_item(p) for p in sorted(runs.iterdir()) if p.is_dir()]
        return {"runs": items}

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
                    trace_excerpt.append(
                        {
                            "name": ev.get("name"),
                            "duration_ms": ev.get("duration_ms"),
                            "node_id": attrs.get("node_id"),
                            "ok": attrs.get("ok"),
                            "unchecked": attrs.get("unchecked"),
                        }
                    )
        waiting = (d / "draft.cir").is_file() and not (d / "confirmed.json").is_file()
        state = "waiting-human" if waiting else "done"
        graph = _read_json(d / "graph.json")
        control_diagram = _read_json(d / "control_diagram.json")
        return {
            "id": run_id,
            "title": str(evid_obj.get("title") or run_id),
            "summary": evid_text,
            "evidentiary": evid_text,
            "argument": argument,
            "plan": plan,
            "observation": observation,
            "observation_excerpt": observation_excerpt,
            "trace_excerpt": trace_excerpt,
            "graph": graph,
            "control_diagram": control_diagram,
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

    ui_dist = Path(__file__).resolve().parents[3] / "ui" / "dist"
    index = ui_dist / "index.html"
    if index.is_file():
        app.mount("/assets", StaticFiles(directory=ui_dist / "assets"), name="assets")

        @app.get("/")
        def spa() -> FileResponse:
            return FileResponse(index)

    return app


def bind_host() -> str:
    return BIND_HOST


def should_open_browser() -> bool:
    return os.environ.get("EE_NO_BROWSER", "") not in {"1", "true", "TRUE"}

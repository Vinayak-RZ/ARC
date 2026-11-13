"""HTTP routes for Control Studio sessions."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, Response, StreamingResponse

from electrical_engineer.control_studio import analyze as analyze_mod
from electrical_engineer.control_studio import session as session_mod
from electrical_engineer.control_studio import simulate as simulate_mod
from electrical_engineer.control_studio.library import PALETTE, PALETTE_GROUPS
from electrical_engineer.control_studio.schema import StudioError
from electrical_engineer.control_studio.validate import validate
from electrical_engineer.ui_server.studio_events import sse_stream


def register_studio_routes(app: FastAPI, *, root: Path) -> None:
    @app.get("/api/control-studio/palette")
    def studio_palette() -> dict:
        return {"palette": PALETTE, "groups": PALETTE_GROUPS}

    @app.post("/api/control-studio/sessions")
    async def studio_create(request: Request) -> dict:
        body = await request.json()
        if not isinstance(body, dict):
            return JSONResponse({"error": "body must be object"}, status_code=400)
        golden = body.get("golden")
        title = str(body.get("title") or "Control Studio")
        seed = str(golden) if golden else ("pid_dc_motor" if body.get("seed_golden") else None)
        payload = session_mod.create_session(title, root, golden=seed)
        return payload

    @app.get("/api/control-studio/sessions/{session_id}")
    def studio_get(session_id: str) -> dict:
        try:
            return session_mod.load_session(session_id, root=root)
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=404)

    @app.put("/api/control-studio/sessions/{session_id}/diagram")
    async def studio_put_diagram(session_id: str, request: Request) -> dict:
        body = await request.json()
        if not isinstance(body, dict):
            return JSONResponse({"error": "body must be object"}, status_code=400)
        author = str(body.get("author") or "human")
        try:
            return session_mod.apply_diagram(
                session_id, body.get("diagram") or body, author=author, op="edit", root=root
            )
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=400)

    @app.post("/api/control-studio/sessions/{session_id}/undo")
    async def studio_undo(session_id: str, request: Request) -> dict:
        body = await request.json()
        author = "human"
        if isinstance(body, dict):
            author = str(body.get("author") or "human")
        try:
            return session_mod.undo(session_id, author=author, root=root)
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=400)

    @app.post("/api/control-studio/sessions/{session_id}/redo")
    async def studio_redo(session_id: str, request: Request) -> dict:
        try:
            return session_mod.redo(session_id, root=root)
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=400)

    @app.post("/api/control-studio/sessions/{session_id}/validate")
    def studio_validate(session_id: str) -> dict:
        try:
            payload = session_mod.load_session(session_id, root)
            return validate(payload["diagram"])
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=404)

    @app.post("/api/control-studio/sessions/{session_id}/simulate")
    def studio_sim(session_id: str) -> dict:
        try:
            payload = session_mod.load_session(session_id, root)
            run_dir = root / "runs" / session_id
            return simulate_mod.simulate(payload["diagram"], run_dir=run_dir)
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=404)

    @app.post("/api/control-studio/sessions/{session_id}/analyze")
    def studio_analyze(session_id: str) -> dict:
        try:
            payload = session_mod.load_session(session_id, root)
            run_dir = root / "runs" / session_id
            return analyze_mod.analyze(payload["diagram"], run_dir=run_dir)
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=404)

    @app.get("/api/control-studio/sessions/{session_id}/events")
    async def studio_events(session_id: str) -> StreamingResponse:
        return StreamingResponse(sse_stream(session_id), media_type="text/event-stream")

    @app.post("/api/control-studio/sessions/{session_id}/notes")
    async def studio_note(session_id: str, request: Request) -> dict:
        body = await request.json()
        if not isinstance(body, dict):
            return JSONResponse({"error": "body must be object"}, status_code=400)
        try:
            return session_mod.add_note(
                session_id,
                str(body.get("block_id") or ""),
                str(body.get("text") or ""),
                author=str(body.get("author") or "human"),
                root=root,
            )
        except StudioError as exc:
            return JSONResponse({"error": str(exc)}, status_code=400)

    @app.get("/api/control-studio/sessions/{session_id}/plot/{name}")
    def studio_plot(session_id: str, name: str) -> Response:
        safe = Path(name).name
        path = root / "runs" / session_id / f"studio_{safe}.png"
        if not path.is_file():
            return JSONResponse({"error": "missing"}, status_code=404)
        return FileResponse(path, media_type="image/png")

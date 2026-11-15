"""HTTP routes for Learn curriculum, notes, progress, and achievements."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from electrical_engineer.catalog import load_recipe_meta
from electrical_engineer.learn import courses as courses_mod
from electrical_engineer.learn import progress as progress_mod
from electrical_engineer.learn.curriculum import expand_topics, load_curriculum


def _err(code: str, message: str, status: int) -> JSONResponse:
    return JSONResponse({"error": {"code": code, "message": message}}, status_code=status)


def _notes_for_subject(subj: dict[str, Any], cwd: Path) -> list[dict[str, Any]]:
    code = subj.get("course") or subj.get("code")
    if not code:
        return []
    out: list[dict[str, Any]] = []
    for f in courses_mod.course_files_for(str(code), cwd):
        name = str(f.get("file") or "")
        path = courses_mod.resolve_course_file(cwd, str(code), name)
        out.append(
            {
                "label": f.get("label") or name,
                "kind": f.get("kind") or "notes",
                "url": f"/api/learn/courses/{code}/{name}",
                "available": path is not None,
            }
        )
    return out


def _recipe_refs(ids: list[str], cwd: Path) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for rid in ids:
        title = rid
        try:
            meta = load_recipe_meta(rid, cwd)
            title = str(meta.get("title") or rid)
        except FileNotFoundError:
            pass
        refs.append({"id": rid, "title": title})
    return refs


def curriculum_payload(cwd: Path, *, progress: dict[str, Any] | None = None) -> dict[str, Any]:
    data = load_curriculum(cwd)
    done = (progress or {}).get("topics_done") or {}
    semesters: list[dict[str, Any]] = []
    for sem in data.get("semesters") or []:
        subjects: list[dict[str, Any]] = []
        for subj in sem.get("subjects") or []:
            topics_raw = expand_topics(subj, cwd)
            topics: list[dict[str, Any]] = []
            for t in topics_raw:
                key = f"{subj['id']}/{t['id']}"
                topics.append(
                    {
                        "id": t["id"],
                        "title": t.get("title") or t["id"],
                        "anchor": t.get("anchor") or "",
                        "recipes": _recipe_refs(list(t.get("recipes") or []), cwd),
                        "labs": list(t.get("labs") or []),
                        "done": key in done,
                    }
                )
            n_done = sum(1 for t in topics if t["done"])
            subjects.append(
                {
                    "id": subj["id"],
                    "code": subj.get("code"),
                    "title": subj.get("title"),
                    "pack": subj.get("pack"),
                    "source": subj.get("source"),
                    "note": subj.get("note"),
                    "notes": _notes_for_subject(subj, cwd),
                    "topics": topics,
                    "progress": {"done": n_done, "total": len(topics)},
                }
            )
        semesters.append({"n": sem["n"], "subjects": subjects})
    return {
        "current_semester": data.get("current_semester"),
        "institute_basis": data.get("institute_basis"),
        "semesters": semesters,
    }


def register_learn_routes(app: FastAPI, *, root: Path) -> None:
    @app.get("/api/learn/curriculum")
    def learn_curriculum() -> dict:
        return curriculum_payload(root, progress=progress_mod.load(root))

    @app.get("/api/learn/courses/{code}/{file}")
    def learn_course_file(code: str, file: str) -> Response:
        path = courses_mod.resolve_course_file(root, code, file)
        if path is None:
            return _err("not_found", "course file not found", 404)
        body = path.read_bytes()
        return Response(
            content=body,
            media_type="text/html; charset=utf-8",
            headers={
                "Content-Security-Policy": "sandbox allow-scripts",
                "X-Content-Type-Options": "nosniff",
                "Referrer-Policy": "no-referrer",
            },
        )

    @app.get("/api/learn/progress")
    def learn_progress_get() -> dict:
        data = progress_mod.load(root)
        return {
            "schema": data.get("schema"),
            "topics_done": data.get("topics_done") or {},
            "labs_opened": data.get("labs_opened") or {},
        }

    @app.post("/api/learn/progress")
    async def learn_progress_post(request: Request) -> Response:
        try:
            body = await request.json()
        except Exception:
            return _err("invalid_progress", "invalid json", 422)
        if not isinstance(body, dict):
            return _err("invalid_progress", "body must be object", 422)
        try:
            updated = progress_mod.apply(root, body)
        except progress_mod.ProgressError as exc:
            return _err("invalid_progress", str(exc), 422)
        return {
            "schema": updated.get("schema"),
            "topics_done": updated.get("topics_done") or {},
            "labs_opened": updated.get("labs_opened") or {},
        }

    @app.get("/api/learn/achievements")
    def learn_achievements() -> dict:
        from electrical_engineer.learn import achievements as achievements_mod

        return achievements_mod.evaluate(root, root / "runs")

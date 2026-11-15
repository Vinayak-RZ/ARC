"""Course notes INDEX and path-safe resolve."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from electrical_engineer.runner.runs import project_root


def courses_dir(cwd: Path | None = None) -> Path:
    return project_root(cwd) / "knowledge" / "courses"


def index_path(cwd: Path | None = None) -> Path:
    return courses_dir(cwd) / "INDEX.yaml"


def load_index(cwd: Path | None = None) -> dict[str, Any]:
    path = index_path(cwd)
    if not path.is_file():
        return {"schema": "arc.courses.v1", "courses": []}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return {"schema": "arc.courses.v1", "courses": []}
    return data


def allowed_files(cwd: Path | None = None) -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    for course in load_index(cwd).get("courses") or []:
        code = str(course.get("code") or "")
        for f in course.get("files") or []:
            out.add((code, str(f.get("file") or "")))
    return out


def resolve_course_file(cwd: Path | None, code: str, file: str) -> Path | None:
    """Return absolute path only if (code, file) is in INDEX and under courses_dir."""
    # Reject path segments before any filesystem touch.
    if not code or not file:
        return None
    if "/" in code or "\\" in code or ".." in code:
        return None
    if "/" in file or "\\" in file or ".." in file:
        return None
    if (code, file) not in allowed_files(cwd):
        return None
    base = courses_dir(cwd).resolve()
    candidate = (base / code / file).resolve()
    try:
        if not candidate.is_relative_to(base):
            return None
    except AttributeError:  # pragma: no cover — py<3.9
        if base not in candidate.parents and candidate != base:
            return None
    if not candidate.is_file():
        return None
    return candidate


def course_files_for(code: str, cwd: Path | None = None) -> list[dict[str, Any]]:
    for course in load_index(cwd).get("courses") or []:
        if str(course.get("code")) == code:
            return list(course.get("files") or [])
    return []

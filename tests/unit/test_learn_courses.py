"""Course notes resolve and learn routes."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from electrical_engineer.learn.courses import resolve_course_file
from electrical_engineer.ui_server.app import create_app


def test_resolve_rejects_traversal(tmp_path: Path, monkeypatch) -> None:
    # Use real project root so INDEX exists; resolve must still reject.
    assert resolve_course_file(None, "EEC-303", "..%2F") is None
    assert resolve_course_file(None, "EEC-303", "../../pyproject.toml") is None
    assert resolve_course_file(None, "..", "power-electronics-notes.html") is None
    assert resolve_course_file(None, "EEC-303", "not-in-index.html") is None


def test_resolve_listed_file() -> None:
    path = resolve_course_file(None, "EEC-303", "power-electronics-notes.html")
    assert path is not None
    assert path.is_file()


def test_notes_route_csp_and_404() -> None:
    client = TestClient(create_app())
    bad = client.get("/api/learn/courses/EEC-303/..%2F..%2Fpyproject.toml")
    assert bad.status_code == 404
    abs_try = client.get("/api/learn/courses/EEC-303/not-in-index.html")
    assert abs_try.status_code == 404
    ok = client.get("/api/learn/courses/EEC-303/power-electronics-notes.html")
    assert ok.status_code == 200
    assert "sandbox allow-scripts" in ok.headers.get("content-security-policy", "")
    assert "text/html" in ok.headers.get("content-type", "")


def test_curriculum_endpoint() -> None:
    client = TestClient(create_app())
    body = client.get("/api/learn/curriculum").json()
    assert body["current_semester"] == 5
    assert len(body["semesters"]) == 8
    s5 = next(s for s in body["semesters"] if s["n"] == 5)
    codes = {subj["code"] for subj in s5["subjects"]}
    assert "EEC-303" in codes
    eec303 = next(s for s in s5["subjects"] if s["code"] == "EEC-303")
    assert any(n["available"] for n in eec303["notes"])

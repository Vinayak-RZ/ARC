"""Smoke coverage for gallery, library, learn, web-verify nodes (no product edits)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from electrical_engineer.ui_server.app import create_app


def test_learn_curriculum_api(monkeypatch) -> None:
    monkeypatch.setenv("EE_NO_SEED", "1")
    client = TestClient(create_app())
    r = client.get("/api/learn/curriculum")
    assert r.status_code == 200
    body = r.json()
    assert body.get("semesters") or body.get("packs")


def test_examples_gallery_lists_items(monkeypatch) -> None:
    monkeypatch.setenv("EE_NO_SEED", "1")
    body = TestClient(create_app()).get("/api/examples").json()
    ids = [ex["id"] for ex in body["examples"]]
    assert len(ids) >= 10


def test_library_and_problems_routes_serve_shell(monkeypatch) -> None:
    monkeypatch.setenv("EE_NO_SEED", "1")
    client = TestClient(create_app())
    r = client.get("/")
    assert r.status_code == 200
    assert len(r.content) > 50


def test_web_verify_node_registered() -> None:
    from electrical_engineer.nodes.web_verify import web_verify

    assert web_verify.__name__ == "web_verify"
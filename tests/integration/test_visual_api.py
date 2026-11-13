from __future__ import annotations

from fastapi.testclient import TestClient

from electrical_engineer.ui_server.app import create_app


def test_visual_kit_api_lists_components() -> None:
    client = TestClient(create_app())
    r = client.get("/api/visual-kit")
    assert r.status_code == 200
    body = r.json()
    assert body["goldens_base"] == "/api/visual-kit/golden/"
    assert any(c["id"] == "power.swing_equal_area" for c in body["components"])


def test_visual_golden_png_served() -> None:
    client = TestClient(create_app())
    r = client.get("/api/visual-kit/golden/swing/power.swing_equal_area.png")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("image/")

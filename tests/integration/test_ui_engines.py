from fastapi.testclient import TestClient

from electrical_engineer.ui_server.app import create_app


def test_engines_endpoint(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("EE_NO_SEED", "1")
    body = TestClient(create_app(tmp_path)).get("/api/engines").json()
    assert "engines" in body
    assert "version" in body
    assert any(e["name"].startswith("Numeric") and e["available"] for e in body["engines"])

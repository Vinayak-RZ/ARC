from fastapi.testclient import TestClient

from electrical_engineer.control_studio.goldens import GOLDENS
from electrical_engineer.ui_server.app import create_app


def test_studio_api_smoke(tmp_path) -> None:
    client = TestClient(create_app(root=tmp_path))
    pal = client.get("/api/control-studio/palette")
    assert pal.status_code == 200
    assert "palette" in pal.json()
    created = client.post("/api/control-studio/sessions", json={"title": "test"})
    assert created.status_code == 200
    sid = created.json()["session_id"]
    diagram = GOLDENS["unity_first_order"]()
    put = client.put(f"/api/control-studio/sessions/{sid}/diagram", json={"diagram": diagram, "author": "human"})
    assert put.status_code == 200
    val = client.post(f"/api/control-studio/sessions/{sid}/validate")
    assert val.status_code == 200
    assert val.json().get("ok") is True

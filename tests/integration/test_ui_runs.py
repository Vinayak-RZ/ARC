from fastapi.testclient import TestClient

from electrical_engineer.ui_server.app import create_app


def test_run_list_and_detail(tmp_path) -> None:
    runs = tmp_path / "runs" / "abcd-1"
    runs.mkdir(parents=True)
    (runs / "summary.json").write_text(
        '{"recipe_id":"x","unchecked":true,"title":"Voltage divider · Vout"}',
        encoding="utf-8",
    )
    client = TestClient(create_app(tmp_path))
    listed = client.get("/api/runs").json()["runs"]
    assert any(row["id"] == "abcd-1" for row in listed)
    item = next(row for row in listed if row["id"] == "abcd-1")
    assert item["title"] == "Voltage divider · Vout"
    assert item["unchecked"] is True
    assert item["recipe_id"] == "x"
    detail = client.get("/api/runs/abcd-1")
    assert detail.status_code == 200
    body = detail.json()
    assert "unchecked" in body["summary"]
    assert body["title"] == "Voltage divider · Vout"

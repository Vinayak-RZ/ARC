from pathlib import Path

from fastapi.testclient import TestClient

from electrical_engineer.ui_server.app import create_app

FIXTURE = Path("tests/fixtures/rag/ohm-law-cc-by.md")


def test_inventory_lists_oer_seed() -> None:
    r = TestClient(create_app()).get("/api/rag/inventory")
    assert r.status_code == 200
    items = r.json()["items"]
    assert items
    assert any(row.get("book_id") for row in items)


def test_upload_requires_rights(tmp_path) -> None:
    (tmp_path / "workflows").mkdir()
    client = TestClient(create_app(tmp_path))
    r = client.post(
        "/api/rag/upload?book_id=oer-ohm&licence_tag=CC-BY&filename=ohm.md",
        content=FIXTURE.read_bytes(),
    )
    assert r.status_code == 400
    assert "rights" in r.json()["error"].lower()


def test_upload_tag_and_query(tmp_path) -> None:
    (tmp_path / "workflows").mkdir()
    client = TestClient(create_app(tmp_path))
    up = client.post(
        "/api/rag/upload?rights=true&book_id=oer-ohm&chapter_id=1&domain_tag=circuits&licence_tag=CC-BY&filename=ohm.md",
        content=FIXTURE.read_bytes(),
    )
    assert up.status_code == 200
    rec = up.json()["item"]
    assert rec["book_id"] == "oer-ohm"
    assert rec["untrusted"] is True
    inv = client.get("/api/rag/inventory").json()["items"]
    assert any(row.get("book_id") == "oer-ohm" for row in inv)
    tagged = client.post(
        "/api/rag/tag",
        json={"path": rec["source"], "folder_tag": "lab-notes", "book_id": "oer-ohm"},
    )
    assert tagged.status_code == 200
    assert tagged.json()["item"]["folder_tag"] == "lab-notes"
    hit = client.post("/api/rag/query", json={"query": "ohm", "book_id": "oer-ohm"})
    assert hit.status_code == 200
    body = hit.json()
    assert body["empty"] is False
    miss = client.post("/api/rag/query", json={"query": "ohm", "book_id": "missing-book"})
    assert miss.json()["empty"] is True

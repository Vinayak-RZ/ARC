from pathlib import Path

from electrical_engineer.rag.inventory import add_doc, load_inventory
from electrical_engineer.rag.retrieve import retrieve

FIXTURE = Path("tests/fixtures/rag/ohm-law-cc-by.md")


def test_ingest_fixture_retrieve_hit(tmp_path) -> None:
    (tmp_path / "workflows").mkdir()
    assert "CC-BY" in FIXTURE.read_text()
    rec = add_doc(
        str(FIXTURE.resolve()),
        tags={"book_id": "oer-ohm", "licence_tag": "CC-BY"},
        cwd=tmp_path,
    )
    assert rec["book_id"] == "oer-ohm"
    assert Path(rec["path"]).is_file()
    items = load_inventory(tmp_path)
    assert items
    hit = retrieve({"book_id": "oer-ohm"}, query="ohm", cwd=tmp_path)
    assert hit["empty"] is False
    assert "ohm" in hit["passages"][0]["text"].lower()


def test_empty_retrieve_still_visible(tmp_path) -> None:
    (tmp_path / "workflows").mkdir()
    out = retrieve({"book_id": "missing-book"}, query="ohm", cwd=tmp_path)
    assert out["empty"] is True
    assert out["passages"] == []

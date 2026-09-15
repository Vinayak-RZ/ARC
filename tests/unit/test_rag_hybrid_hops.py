from pathlib import Path

from electrical_engineer.rag.graph_store import load_graph
from electrical_engineer.rag.inventory import add_doc, rag_root
from electrical_engineer.rag.retrieve import retrieve

FIXTURE = Path("tests/fixtures/rag/worked-example-with-figure.md")


def test_worked_example_and_figure_linked(tmp_path) -> None:
    (tmp_path / "workflows").mkdir()
    src = tmp_path / "ex.md"
    src.write_text(FIXTURE.read_text())
    # copy referenced image path as empty file so parse keeps relative link
    (tmp_path / "fig-ohm.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    text = src.read_text().replace("fig-ohm.png", str(tmp_path / "fig-ohm.png"))
    src.write_text(text)
    add_doc(
        str(src),
        tags={"book_id": "demo", "chapter_id": "1", "licence_tag": "CC-BY"},
        cwd=tmp_path,
    )
    g = load_graph(rag_root(tmp_path))
    kinds = {n["kind"] for n in g["nodes"].values()}
    assert "worked_example" in kinds
    assert "figure" in kinds
    assert any(e["type"] == "illustrates" for e in g["edges"])
    hit = retrieve({"book_id": "demo"}, query="Ohm's law example", cwd=tmp_path, hops=2)
    assert hit["empty"] is False
    assert hit["engine"] == "hybrid-graph"
    assert hit["elapsed_ms"] < 7000

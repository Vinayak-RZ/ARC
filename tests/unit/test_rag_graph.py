from electrical_engineer.rag.graph_store import add_edge, load_graph, neighbors, save_graph, upsert_node
from electrical_engineer.rag.ontology import ENGINE_ID, valid_edge, valid_node


def test_ontology_accepts_core_kinds() -> None:
    assert valid_node("worked_example")
    assert valid_node("figure")
    assert valid_edge("illustrates")
    assert ENGINE_ID == "hybrid-graph"


def test_graph_roundtrip(tmp_path) -> None:
    g = load_graph(tmp_path)
    upsert_node(g, "book:x", "book", title="x")
    upsert_node(g, "chunk:1", "prose", book_id="x")
    add_edge(g, edge_type="belongs_to", src="chunk:1", dst="book:x")
    save_graph(g, tmp_path)
    g2 = load_graph(tmp_path)
    assert "chunk:1" in g2["nodes"]
    assert neighbors(g2, "chunk:1") == [("belongs_to", "book:x")]

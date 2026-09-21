from electrical_engineer.circuit.graph import default_graph_for, series_rlc_graph
from electrical_engineer.control.diagram import SCHEMA, control_diagram_from_problem


def test_series_rlc_graph_seed() -> None:
    g = default_graph_for({"kind": "series_rlc"})
    assert g is not None
    types = {n["type"] for n in g["nodes"]}
    assert "resistor" in types and "inductor" in types and "capacitor" in types


def test_cir_infers_rlc_graph() -> None:
    g = default_graph_for(
        {"cir": "*\nV1 1 0 DC 10\nR1 1 2 1k\nL1 2 3 1m\nC1 3 0 1u\n.end\n"}
    )
    assert g is not None
    assert len(g["nodes"]) == len(series_rlc_graph()["nodes"])


def test_unity_feedback_diagram() -> None:
    d = control_diagram_from_problem(
        {
            "blocks": [{"id": "G", "tf": "10/(s+1)"}, {"id": "H", "tf": "1"}],
            "unity_feedback": {"forward": "G", "feedback": "H"},
        }
    )
    assert d is not None
    assert d["schema"] == SCHEMA
    assert any(n["id"] == "sum" for n in d["nodes"])
    assert any(n["type"] == "block" and n["id"] == "G" for n in d["nodes"])

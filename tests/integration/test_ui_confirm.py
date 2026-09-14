from fastapi.testclient import TestClient

from electrical_engineer.ui_server.app import create_app


def test_confirm_does_not_simulate() -> None:
    client = TestClient(create_app())
    r = client.post("/api/runs/x/confirm")
    assert r.json()["confirmed"] is True
    assert r.json()["simulate"] is False


def test_confirm_writes_flag(tmp_path) -> None:
    client = TestClient(create_app(tmp_path))
    client.post("/api/runs/x/confirm")
    flag = (tmp_path / "runs" / "x" / "confirmed.json").read_text(encoding="utf-8")
    assert '"simulate": false' in flag
    assert "run-spice" not in flag


def test_confirm_with_graph_does_not_simulate(tmp_path) -> None:
    client = TestClient(create_app(tmp_path))
    graph = {
        "schema": "arc.circuit.v1",
        "nodes": [
            {"id": "vin", "type": "source_v", "refdes": "Vin", "value": 10, "x": 0, "y": 0},
            {"id": "r1", "type": "resistor", "refdes": "R1", "value": 1000, "x": 1, "y": 0},
            {"id": "gnd", "type": "ground", "refdes": "Gnd", "value": 0, "x": 0, "y": 1},
        ],
        "edges": [
            {"id": "e1", "from": "vin.n1", "to": "r1.n1"},
            {"id": "e2", "from": "r1.n2", "to": "gnd.n1"},
            {"id": "e3", "from": "vin.n2", "to": "gnd.n1"},
        ],
    }
    r = client.post("/api/runs/g1/confirm", json={"graph": graph, "simulate": False})
    assert r.json()["simulate"] is False
    run = tmp_path / "runs" / "g1"
    assert '"simulate": false' in (run / "confirmed.json").read_text(encoding="utf-8")
    assert (run / "graph.json").is_file()
    assert (run / "netlist.cir").is_file()
    put = client.put("/api/runs/g1/graph", json=graph)
    assert put.json()["compiled"] is True
    assert "run-spice" not in (run / "netlist.cir").read_text(encoding="utf-8")

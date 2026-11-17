from pathlib import Path

from electrical_engineer.circuit.run_session import apply_graph, load_graph
from electrical_engineer.collab.lab_meta import ensure_lab_meta, load_lab_meta


def test_run_session_revision_and_op_log(tmp_path: Path) -> None:
    run_dir = tmp_path / "runs" / "r-collab-01"
    run_dir.mkdir(parents=True)
    ensure_lab_meta(run_dir, kind="circuit")
    graph = {
        "schema": "arc.circuit.v1",
        "nodes": [
            {"id": "gnd", "type": "ground", "refdes": "G", "value": 0, "unit": "", "x": 0, "y": 0, "rot": 0}
        ],
        "edges": [],
    }
    out = apply_graph(run_dir, graph, author="agent", op="seed")
    assert out["revision"] == 1
    meta = load_lab_meta(run_dir)
    assert meta["op_log"][-1]["author"] == "agent"
    assert load_graph(run_dir)["nodes"][0]["id"] == "gnd"
import json
from pathlib import Path

from electrical_engineer.circuit.graph import (
    ALLOWED_TYPES,
    MAX_EDGES,
    MAX_NODES,
    SCHEMA,
    GraphError,
    default_graph_for,
    divider_graph,
    parse_graph,
    write_graph,
)
from electrical_engineer.circuit.netlist import CompileError, compile_netlist

DIVIDER = divider_graph()
CONTRACT = json.loads(Path("src/electrical_engineer/circuit/arc.circuit.v1.json").read_text(encoding="utf-8"))


def test_contract_file_drives_caps() -> None:
    assert SCHEMA == CONTRACT["properties"]["schema"]["const"]
    assert MAX_NODES == CONTRACT["properties"]["nodes"]["maxItems"]
    assert MAX_EDGES == CONTRACT["properties"]["edges"]["maxItems"]
    assert ALLOWED_TYPES == frozenset(CONTRACT["$defs"]["partType"]["enum"])
    parsed = parse_graph(DIVIDER)
    assert parsed["nodes"][0]["rot"] == 0
    assert parsed["nodes"][2]["rot"] == 90
    rotated = parse_graph(
        {
            "schema": SCHEMA,
            "nodes": [{**DIVIDER["nodes"][1], "rot": 90}, DIVIDER["nodes"][3]],
            "edges": [],
        }
    )
    assert rotated["nodes"][0]["rot"] == 90
    try:
        parse_graph({"nodes": [{**DIVIDER["nodes"][1], "rot": 45}], "edges": []})
    except GraphError as exc:
        assert "rot" in str(exc)
    else:
        raise AssertionError("expected GraphError")


def test_default_graph_for_divider() -> None:
    g = default_graph_for({"kind": "voltage_divider", "vin": 12, "r1": 2000, "r2": 2000})
    assert g is not None
    assert g["nodes"][0]["value"] == 12
    assert default_graph_for({"kind": "ohms_law"}) is None
    parsed = parse_graph(DIVIDER)
    cir = compile_netlist(parsed)
    assert "Vin" in cir
    assert "R1" in cir
    assert "R2" in cir
    assert "DC 10" in cir
    assert " 1000" in cir
    assert ".end" in cir
    assert "run-spice" not in cir


def test_compile_current_source() -> None:
    graph = {
        "schema": SCHEMA,
        "nodes": [
            {"id": "i1", "type": "source_i", "refdes": "I1", "value": 0.002, "unit": "A", "x": 0, "y": 0},
            {"id": "r1", "type": "resistor", "refdes": "R1", "value": 1000, "unit": "ohm", "x": 1, "y": 0},
            {"id": "gnd", "type": "ground", "refdes": "Gnd", "value": 0, "x": 0, "y": 1},
        ],
        "edges": [
            {"id": "e1", "from": "i1.n1", "to": "r1.n1"},
            {"id": "e2", "from": "r1.n2", "to": "gnd.n1"},
            {"id": "e3", "from": "i1.n2", "to": "gnd.n1"},
        ],
    }
    cir = compile_netlist(parse_graph(graph))
    assert "I1 1 0 DC 0.002" in cir or "I1 " in cir
    assert "DC 0.002" in cir
    assert "R1" in cir


def test_missing_ground() -> None:
    bad = {"nodes": [{"id": "r1", "type": "resistor", "refdes": "R1", "value": 1}], "edges": []}
    try:
        compile_netlist(parse_graph(bad))
    except CompileError as exc:
        assert "ground" in str(exc)
    else:
        raise AssertionError("expected CompileError")


def test_cap() -> None:
    nodes = [{"id": f"r{i}", "type": "resistor", "value": 1} for i in range(17)]
    try:
        parse_graph({"nodes": nodes, "edges": []})
    except GraphError as exc:
        assert "16" in str(exc)
    else:
        raise AssertionError("expected GraphError")


def test_write_graph_no_spice(tmp_path) -> None:
    out = write_graph(tmp_path, DIVIDER)
    assert out["compiled"] is True
    assert (tmp_path / "graph.json").is_file()
    assert (tmp_path / "netlist.cir").is_file()
    assert (tmp_path / "netlist.cir").is_file()


def test_compile_error_sets_reason(tmp_path) -> None:
    (tmp_path / "observation.json").write_text("{}", encoding="utf-8")
    out = write_graph(
        tmp_path,
        {"nodes": [{"id": "r1", "type": "resistor", "refdes": "R1", "value": 1}], "edges": []},
    )
    assert out["compiled"] is False
    assert not (tmp_path / "netlist.cir").is_file()
    obs = (tmp_path / "observation.json").read_text(encoding="utf-8")
    assert "compile-error" in obs

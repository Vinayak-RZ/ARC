from electrical_engineer.circuit.graph import GraphError, parse_graph, write_graph
from electrical_engineer.circuit.netlist import CompileError, compile_netlist

DIVIDER = {
    "schema": "arc.circuit.v1",
    "nodes": [
        {"id": "vin", "type": "source_v", "refdes": "Vin", "value": 10, "unit": "V", "x": 80, "y": 40},
        {"id": "r1", "type": "resistor", "refdes": "R1", "value": 1000, "unit": "ohm", "x": 220, "y": 40},
        {"id": "r2", "type": "resistor", "refdes": "R2", "value": 1000, "unit": "ohm", "x": 220, "y": 160},
        {"id": "gnd", "type": "ground", "refdes": "Gnd", "value": 0, "unit": "", "x": 80, "y": 160},
    ],
    "edges": [
        {"id": "e1", "from": "vin.n1", "to": "r1.n1"},
        {"id": "e2", "from": "r1.n2", "to": "r2.n1"},
        {"id": "e3", "from": "r2.n2", "to": "gnd.n1"},
        {"id": "e4", "from": "vin.n2", "to": "gnd.n1"},
    ],
}


def test_parse_and_compile_divider() -> None:
    parsed = parse_graph(DIVIDER)
    cir = compile_netlist(parsed)
    assert "Vin" in cir
    assert "R1" in cir
    assert "R2" in cir
    assert "DC 10" in cir
    assert " 1000" in cir
    assert ".end" in cir
    assert "run-spice" not in cir


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

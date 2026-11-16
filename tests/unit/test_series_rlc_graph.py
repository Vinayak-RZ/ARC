from electrical_engineer.circuit.graph import (
    default_graph_for,
    graph_port_errors,
    parse_graph,
    series_rlc_graph,
)
from electrical_engineer.circuit.netlist import compile_netlist


def test_series_rlc_agent_graph_ports_and_netlist() -> None:
    graph = series_rlc_graph(vin=10, r_ohm=10, l_h=0.01, c_f=100e-6)
    parsed = parse_graph(graph)
    assert graph_port_errors(parsed) == []
    cir = compile_netlist(parsed)
    assert "R1 1 2 10" in cir.replace(".0", "")
    assert "L1 2 3" in cir
    assert "C1 3 0" in cir.replace("0.0001", "0.0001")
    assert "V1 1 0 DC 10" in cir


def test_workflow_default_series_rlc_seed() -> None:
    prob = {"kind": "series_rlc", "vin": 10, "r_ohm": 10, "l_h": 0.01, "c_f": 100e-6}
    graph = default_graph_for(prob)
    assert graph is not None
    assert graph_port_errors(parse_graph(graph)) == []
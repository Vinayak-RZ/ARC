from electrical_engineer.circuit.graph import (
    default_graph_for,
    graph_port_errors,
    parse_graph,
    series_rlc_graph,
    series_rlc_netlist_signature,
)
from electrical_engineer.circuit.netlist import compile_netlist


def test_series_rlc_agent_graph_ports_and_netlist() -> None:
    graph = series_rlc_graph(vin=10, r_ohm=10, l_h=0.01, c_f=100e-6)
    parsed = parse_graph(graph)
    assert graph_port_errors(parsed) == []
    cir = compile_netlist(parsed)
    sig = series_rlc_netlist_signature(cir)
    assert len(sig) == 4
    assert any(s.startswith("V1:") for s in sig)
    assert any(s.startswith("R1:") for s in sig)


def test_workflow_default_series_rlc_seed() -> None:
    prob = {"kind": "series_rlc", "vin": 10, "r_ohm": 10, "l_h": 0.01, "c_f": 100e-6}
    graph = default_graph_for(prob)
    assert graph is not None
    assert graph_port_errors(parse_graph(graph)) == []
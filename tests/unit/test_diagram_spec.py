from electrical_engineer.visual_kit.diagram_spec import diagram_for_run, voltage_divider
from electrical_engineer.visual_kit.diagram_validate import validate_diagram


def test_builders_validate() -> None:
    d = voltage_divider({"vin": 10, "r1": 1000, "r2": 1000})
    assert validate_diagram(d) == []
    out = diagram_for_run(None, "solve-circuit-problem", {"kind": "voltage_divider", "vin": 10, "r1": 1, "r2": 1})  # type: ignore[arg-type]
    assert out and validate_diagram(out) == []
    swing = diagram_for_run(None, "smib-swing-study", {})  # type: ignore[arg-type]
    assert swing and validate_diagram(swing) == []

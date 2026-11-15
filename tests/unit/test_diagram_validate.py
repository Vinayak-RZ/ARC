from electrical_engineer.visual_kit.diagram_validate import SCHEMA, validate_diagram


def test_ok_schematic() -> None:
    errs = validate_diagram(
        {
            "schema": SCHEMA,
            "panels": [
                {
                    "kind": "schematic",
                    "components": [{"id": "r1", "type": "resistor", "at": [0, 0], "rot": 0}],
                }
            ],
        }
    )
    assert errs == []


def test_bad_schema() -> None:
    assert validate_diagram({"schema": "x", "panels": []})

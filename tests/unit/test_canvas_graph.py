import json
from pathlib import Path

from electrical_engineer.circuit.graph import ALLOWED_TYPES, MAX_EDGES, MAX_NODES, SCHEMA


def _schema() -> dict:
    path = Path("src/electrical_engineer/circuit/arc.circuit.v1.json")
    return json.loads(path.read_text(encoding="utf-8"))


def test_canvas_adapter_contract() -> None:
    schema = _schema()
    text = Path("ui/src/slots/canvas/graph.js").read_text(encoding="utf-8")
    assert "export function toFlow" in text
    assert "export function fromFlow" in text
    assert f"MAX_NODES = {MAX_NODES}" in text
    assert f"MAX_EDGES = {MAX_EDGES}" in text
    assert SCHEMA in text
    assert "rot" in text
    canvas = Path("ui/src/slots/canvas/Canvas.jsx").read_text(encoding="utf-8")
    assert 'type: "smoothstep"' in canvas
    assert "snapToGrid" in canvas
    assert "height: 420" in canvas
    assert "hideAttribution" in canvas
    for kind in schema["$defs"]["partType"]["enum"]:
        assert kind in text
    assert ALLOWED_TYPES == frozenset(schema["$defs"]["partType"]["enum"])


def test_palette_and_inspector_labels() -> None:
    palette = Path("ui/src/slots/canvas/Palette.jsx").read_text(encoding="utf-8")
    inspector = Path("ui/src/slots/canvas/Inspector.jsx").read_text(encoding="utf-8")
    canvas = Path("ui/src/slots/canvas/Canvas.jsx").read_text(encoding="utf-8")
    assert 'aria-label="Palette"' in palette
    labels = Path("ui/src/slots/canvas/graph.js").read_text(encoding="utf-8")
    assert "Current" in labels
    nodes = Path("ui/src/slots/canvas/nodes.jsx").read_text(encoding="utf-8")
    assert "source_i" in nodes
    assert "is-vertical" in nodes
    assert "Passives" in palette
    assert "Sources" in palette
    assert "Make vertical" in inspector
    assert "Refdes" in inspector
    assert "Value" in inspector
    assert "Confirm topology" in canvas
    assert "Save graph" in canvas
    assert "16 parts or 24 wires is the cap for this lab." in canvas

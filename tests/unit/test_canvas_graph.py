from pathlib import Path


def test_canvas_adapter_contract() -> None:
    text = Path("ui/src/slots/canvas/graph.js").read_text(encoding="utf-8")
    assert "export function toFlow" in text
    assert "export function fromFlow" in text
    assert "MAX_NODES = 16" in text
    assert "MAX_EDGES = 24" in text
    assert "arc.circuit.v1" in text
    for kind in ("resistor", "capacitor", "inductor", "source_v", "ground"):
        assert kind in text


def test_palette_and_inspector_labels() -> None:
    palette = Path("ui/src/slots/canvas/Palette.jsx").read_text(encoding="utf-8")
    inspector = Path("ui/src/slots/canvas/Inspector.jsx").read_text(encoding="utf-8")
    canvas = Path("ui/src/slots/canvas/Canvas.jsx").read_text(encoding="utf-8")
    assert 'aria-label="Palette"' in palette
    labels = Path("ui/src/slots/canvas/graph.js").read_text(encoding="utf-8")
    for label in ("Resistor", "Capacitor", "Inductor", "Voltage", "Ground"):
        assert label in labels
    assert "Refdes" in inspector
    assert "Value" in inspector
    assert "Confirm topology" in canvas
    assert "Save graph" in canvas
    assert "16 parts or 24 wires is the cap for this lab." in canvas

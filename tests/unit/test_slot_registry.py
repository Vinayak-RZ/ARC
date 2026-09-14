from pathlib import Path


def test_registry_exports() -> None:
    text = Path("ui/src/slots/registry.js").read_text(encoding="utf-8")
    assert "export function register" in text
    assert "export function renderSlot" in text
    root = Path("ui/src/slots/root.jsx").read_text(encoding="utf-8")
    for slot in (
        "run.result",
        "run.canvas",
        "run.inspector",
        "run.argument",
        "photo.confirm",
    ):
        assert slot in root
    assert 'register("run.evidentiary"' not in root
    assert "<details>" in root


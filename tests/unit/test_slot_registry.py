from pathlib import Path


def test_registry_exports() -> None:
    text = Path("ui/src/slots/registry.js").read_text()
    assert "export function register" in text
    assert "export function renderSlot" in text
    root = Path("ui/src/slots/root.jsx").read_text()
    for slot in (
        "run.evidentiary",
        "run.argument",
        "run.plan",
        "run.observation",
        "photo.confirm",
    ):
        assert slot in root


from pathlib import Path


def test_zustand_store() -> None:
    text = Path("ui/src/store.js").read_text()
    assert "currentRunId" in text
    assert "graphDirty" in text
    assert "create" in text

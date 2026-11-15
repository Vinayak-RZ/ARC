from pathlib import Path


def test_spike_protocol_forbids_commercial_pdf() -> None:
    text = Path("research/notes/rag-spike-2026-09.md").read_text(encoding="utf-8")
    assert "No commercial PDFs" in text
    assert "LightRAG" in text
    assert "lock the engine" in text.lower() or "Do **not** lock" in text

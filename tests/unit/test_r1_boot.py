from pathlib import Path


def test_r1_boot_log_has_three_commands() -> None:
    text = Path("docs/planning/R1_BOOT.md").read_text(encoding="utf-8")
    assert "electrical-engineer --help" in text
    assert "electrical-engineer run solve-circuit-problem" in text
    assert "MCP" in text
    assert "127.0.0.1" in text
    assert "0.0.0.0" not in text

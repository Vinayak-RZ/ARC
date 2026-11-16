from pathlib import Path

import pytest


def test_t1_has_at_least_nine_scenarios() -> None:
    path = Path("docs/planning/T1_TRIALS.md")
    if not path.is_file():
        pytest.skip("docs/planning/T1_TRIALS.md not in repo")
    text = path.read_text(encoding="utf-8")
    assert text.count("**PASS**") >= 9
    assert "MCP" in text
    assert "unchecked" in text
    assert "DESIGN-coinbase" in text or "0052ff" in text

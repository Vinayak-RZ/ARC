from pathlib import Path

PACKS = (
    "circuits",
    "signals",
    "electronics",
    "machines",
    "power",
    "control",
    "power_electronics",
    "measurements",
    "em",
    "maths",
)

VERBS = (
    "list_workflows",
    "retrieve",
    "open_ui",
    "simulate_attachment",
    "propose_composition",
    "label",
)


def test_host_docs_exist() -> None:
    base = Path("docs/hosts")
    for name in ("README.md", "cursor.md", "claude-code.md", "openai.md", "chatgpt-desktop.md"):
        text = (base / name).read_text()
        assert "electrical-engineer mcp" in text or "stdio" in text.lower()


def test_chatgpt_desktop_names_live_verbs() -> None:
    text = Path("docs/hosts/chatgpt-desktop.md").read_text()
    for verb in VERBS:
        assert verb in text, verb
    root = Path("skills/SKILL.md").read_text()
    assert "propose_composition" in root


def test_ee_packs_not_in_cursor_skills() -> None:
    root = Path(".cursor/skills")
    for pack in PACKS:
        assert not (root / pack).exists(), pack


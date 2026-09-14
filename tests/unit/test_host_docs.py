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


def test_host_docs_forbid_peer_matlab_mcp() -> None:
    base = Path("docs/hosts")
    for name in ("README.md", "cursor.md", "claude-code.md", "openai.md", "chatgpt-desktop.md"):
        text = (base / name).read_text()
        assert "Coming next" not in text, name
        assert "do **not**" in text.lower(), name
    cursor = Path("docs/hosts/cursor.md").read_text()
    assert "Do **not** add MATLAB MCP" in cursor
    assert "Simulink" in cursor
    assert "hosts install" in cursor
    harness = Path("docs/ON_THE_HARNESS.md").read_text()
    assert "How Arc mediates MATLAB" in harness
    assert "This is not shipped" not in harness
    assert "hosts" in Path("docs/ON_THE_HARNESS.md").read_text()
    assert "Simulink" in harness



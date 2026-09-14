"""hosts install copies catalog cards into a homework tree, not product .cursor/."""

from pathlib import Path

from electrical_engineer.hosts_install import PACKS, card_paths, cursor_name, install


def test_catalog_has_twelve_cards() -> None:
    cards = card_paths()
    names = {p.stem for p in cards}
    assert len(cards) == 12
    assert "ee-simulink" in names
    for pack in PACKS:
        assert cursor_name(pack) in names
    index = Path("hosts/agents/INDEX.md").read_text()
    assert "**Count: 12**" in index
    assert "ee-simulink" in index


def test_install_all_hosts_into_temp(tmp_path: Path) -> None:
    written = install(tmp_path, host="all")
    assert len(written) == 12 * 3
    for card in card_paths():
        name = card.stem
        cursor = tmp_path / ".cursor" / "agents" / f"{name}.md"
        claude = tmp_path / ".claude" / "agents" / f"{name}.md"
        assert cursor.is_file(), name
        assert claude.is_file(), name
        body = cursor.read_text()
        assert "evaluate_matlab_code" in body
        assert "model_read" in body
        assert "/in-cloud" in body
        assert "Retrieve (scaffold)" in body
        assert "nested" in body.lower() or "Do not spawn further" in body
    circuits_toml = tmp_path / ".codex" / "agents" / "ee_circuits.toml"
    assert circuits_toml.is_file()
    toml = circuits_toml.read_text()
    assert "developer_instructions" in toml
    assert "ee_circuits" in toml
    assert (tmp_path / ".cursor" / "agents" / "ee-cross.md").is_file()
    assert (tmp_path / ".cursor" / "agents" / "ee-power-electronics.md").is_file()
    assert (tmp_path / ".cursor" / "agents" / "ee-simulink.md").is_file()
    sim = (tmp_path / ".cursor" / "agents" / "ee-simulink.md").read_text()
    assert "CD-SIMULINK-PLANT" in sim
    assert "model_*" in sim or "model_read" in sim


def test_install_does_not_touch_product_cursor(tmp_path: Path) -> None:
    install(tmp_path, host="cursor")
    product_agents = Path(".cursor/agents")
    if product_agents.exists():
        names = {p.name for p in product_agents.glob("ee-*.md")}
        assert not names
    assert not Path(".cursor/agents/ee-circuits.md").exists()
    assert (tmp_path / ".cursor" / "agents" / "ee-circuits.md").is_file()


def test_cli_hosts_install(tmp_path: Path) -> None:
    from electrical_engineer.cli import main

    assert main(["hosts", "install", "--into", str(tmp_path), "--host", "cursor"]) == 0
    assert (tmp_path / ".cursor" / "agents" / "ee-circuits.md").is_file()
    assert (tmp_path / ".cursor" / "agents" / "ee-simulink.md").is_file()
    assert not (tmp_path / ".codex" / "agents").exists()

"""hosts install writes per-pack wrappers into a homework tree, not product .cursor/."""

from pathlib import Path

from electrical_engineer.hosts_install import PACKS, cursor_name, install


def test_install_all_hosts_into_temp(tmp_path: Path) -> None:
    written = install(tmp_path, host="all")
    assert written
    for pack in PACKS:
        cursor = tmp_path / ".cursor" / "agents" / f"{cursor_name(pack)}.md"
        claude = tmp_path / ".claude" / "agents" / f"{cursor_name(pack)}.md"
        assert cursor.is_file(), pack
        assert claude.is_file(), pack
        body = cursor.read_text()
        assert "evaluate_matlab_code" in body
        assert "Retrieve (scaffold)" in body
        assert "electrical-engineer" in body or "EE MCP" in body
        assert "knowledge/" in body
    circuits_toml = tmp_path / ".codex" / "agents" / "ee_circuits.toml"
    assert circuits_toml.is_file()
    toml = circuits_toml.read_text()
    assert "developer_instructions" in toml
    assert "ee_circuits" in toml
    cross = tmp_path / ".cursor" / "agents" / "ee-cross.md"
    assert cross.is_file()
    pe = tmp_path / ".cursor" / "agents" / "ee-power-electronics.md"
    assert pe.is_file()


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
    assert not (tmp_path / ".codex" / "agents").exists()

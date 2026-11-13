"""Vertical EE pack install, doctor, smoke contract."""

import json
from pathlib import Path

import pytest

from electrical_engineer import vertical_pack
from electrical_engineer.hosts_install import install as install_agents_only


def test_manifest_skills_include_b8_domains() -> None:
    manifest = vertical_pack.load_manifest()
    ids = {e["id"] for e in manifest["skills"]}
    for name in (
        "power",
        "control",
        "circuits",
        "machines",
        "power_electronics",
        "protection-standards",
        "web-verify",
        "reference",
    ):
        assert name in ids, name
    for skill in manifest["skills"]:
        if skill["id"] not in ids:
            continue
        if skill["id"] in {"psa-swing", "psa-agc", "psa-ed", "cross", "root"}:
            continue
        text = (vertical_pack.repo_root() / skill["path"]).read_text()
        assert "unchecked" in text.lower() or "provenance" in text.lower(), skill["id"]


def test_install_pack_all_hosts(tmp_path: Path) -> None:
    written = vertical_pack.install_pack(tmp_path, host="all")
    assert len(written) > 36
    assert (tmp_path / ".cursor" / "mcp.json").is_file()
    assert (tmp_path / ".mcp.json").is_file()
    assert (tmp_path / ".codex" / "config.toml").is_file()
    assert (tmp_path / ".cursor" / "skills" / "arc-ee-protection-standards" / "SKILL.md").is_file()
    state = vertical_pack.state_path(tmp_path)
    assert state.is_file()
    data = json.loads(state.read_text())
    assert data["pack_id"] == "arc-ee-vertical"


def test_install_idempotent(tmp_path: Path) -> None:
    first = vertical_pack.install_pack(tmp_path, host="cursor")
    second = vertical_pack.install_pack(tmp_path, host="cursor")
    assert len(first) == len(second)
    assert (tmp_path / ".cursor" / "mcp.json").read_text() == (
        tmp_path / ".cursor" / "mcp.json"
    ).read_text()


def test_uninstall_reverses_install(tmp_path: Path) -> None:
    vertical_pack.install_pack(tmp_path, host="all")
    mcp = tmp_path / ".cursor" / "mcp.json"
    assert mcp.is_file()
    vertical_pack.uninstall_pack(tmp_path)
    assert not mcp.is_file()
    assert not vertical_pack.state_path(tmp_path).exists()
    assert not (tmp_path / ".cursor" / "agents" / "ee-circuits.md").exists()


def test_agents_only_install_unchanged(tmp_path: Path) -> None:
    written = install_agents_only(tmp_path, host="cursor")
    assert len(written) == 12
    assert not (tmp_path / ".cursor" / "mcp.json").exists()


def test_doctor_reports_engines() -> None:
    report = vertical_pack.doctor()
    assert report["pack_manifest"] is True
    assert "engines" in report
    assert report["mcp_stdio"]["ok"] is True
    assert report["mcp_stdio"]["tool_count"] >= 5


def test_smoke_contract_json() -> None:
    out = vertical_pack.smoke_contract()
    assert isinstance(out["pack_install_smoke"], bool)
    assert isinstance(out["matlab_optional"], bool)
    assert out["pack_install_smoke"] is True
    assert out["matlab_optional"] is True


def test_cli_hosts_smoke(capsys: pytest.CaptureFixture[str]) -> None:
    from electrical_engineer.cli import main

    assert main(["hosts", "smoke"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == vertical_pack.smoke_contract()

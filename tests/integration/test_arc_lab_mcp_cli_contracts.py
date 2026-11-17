"""Contract tests: arc_circuit_lab_* MCP tools and electrical-engineer lab CLI."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from electrical_engineer.circuit import mcp_lab
from electrical_engineer.circuit.mcp_tools import handle_tool as circuit_mcp
from electrical_engineer.collab.mcp_tools import TOOL_DEFS as COLLAB_TOOL_DEFS

LAB_TOOL_NAMES = {
    "arc_circuit_lab_open",
    "arc_circuit_lab_set_graph",
    "arc_circuit_lab_add_part",
    "arc_circuit_lab_connect",
    "arc_circuit_lab_simulate",
    "arc_circuit_lab_finish_solve",
    "arc_circuit_lab_get",
    "arc_circuit_lab_re_derive",
}


@pytest.mark.parametrize("name", sorted(LAB_TOOL_NAMES))
def test_mcp_lab_tool_schema_has_name_and_input_schema(name: str) -> None:
    defs_by_name = {t["name"]: t for t in mcp_lab.TOOL_DEFS}
    assert name in defs_by_name
    sch = defs_by_name[name].get("inputSchema") or {}
    assert sch.get("type") == "object"


def test_arc_lab_finish_control_in_collab_defs() -> None:
    names = {t["name"] for t in COLLAB_TOOL_DEFS}
    assert "arc_lab_finish_control" in names


def test_mcp_lab_unknown_tool_error() -> None:
    out = mcp_lab.handle_tool("arc_circuit_lab_nope", {})
    assert "error" in out


def test_mcp_finish_solve_requires_problem(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "runs").mkdir()
    with pytest.raises(KeyError):
        circuit_mcp("arc_circuit_lab_finish_solve", {"run_id": "x"})


def test_mcp_set_graph_missing_run_id_raises() -> None:
    with pytest.raises(KeyError):
        mcp_lab.handle_tool("arc_circuit_lab_set_graph", {"graph": {"schema": "arc.circuit.v1", "nodes": [], "edges": []}})


def test_cli_lab_help_lists_subcommands() -> None:
    from electrical_engineer.cli import COMMANDS, build_parser

    assert "lab" in COMMANDS
    text = build_parser().format_help().lower()
    assert "lab" in text


def test_cli_lab_get_exit_code(tmp_path: Path, monkeypatch, capsys) -> None:
    from electrical_engineer.cli import main

    monkeypatch.chdir(tmp_path)
    rid = "cli-lab-01"
    (tmp_path / "runs" / rid).mkdir(parents=True)
    code = main(["lab", "get", "--run", rid])
    assert code == 0
    out = capsys.readouterr().out
    body = json.loads(out)
    assert body.get("run_id") == rid


def test_cli_lab_finish_missing_problem_exit_2(tmp_path: Path, monkeypatch, capsys) -> None:
    from electrical_engineer.cli import main

    monkeypatch.chdir(tmp_path)
    rid = "cli-empty"
    (tmp_path / "runs" / rid).mkdir(parents=True)
    code = main(["lab", "finish", "--run", rid])
    assert code == 2
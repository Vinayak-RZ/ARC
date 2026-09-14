"""MATLAB MCP client: missing fail-closed; fake stdio stub can return ok."""

from pathlib import Path

import pytest

from electrical_engineer.matlab_mcp import (
    MatlabMissing,
    call_tool,
    matlab_bin,
    result_text,
    simulink_extension,
    spawn_cmd,
)
from electrical_engineer.nodes import sim as _sim  # noqa: F401
from electrical_engineer.nodes.registry import get

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "fake_matlab_mcp.py"


def test_missing_bin_is_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("EE_MATLAB_MCP_BIN", raising=False)
    monkeypatch.setattr("electrical_engineer.matlab_mcp.shutil.which", lambda _n: None)
    assert matlab_bin() is None
    with pytest.raises(MatlabMissing):
        call_tool("evaluate_matlab_code", {"code": "1"})


def test_stub_evaluate(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("EE_MATLAB_MCP_BIN", str(FIXTURE))
    monkeypatch.setenv("EE_MATLAB_MCP_TIMEOUT", "10")
    FIXTURE.chmod(0o755)
    out = call_tool(
        "evaluate_matlab_code",
        {"code": "1+1", "project_path": str(tmp_path)},
        run_dir=str(tmp_path),
    )
    assert "42" in result_text(out)


def test_run_matlab_if_present_missing_clear() -> None:
    out = get("run-matlab-if-present")({"id": "m"}, {})
    assert out["ok"] is False
    assert "matlab" in out["error"].lower()
    assert out["unchecked"] is True


def test_run_matlab_if_present_stub(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("EE_MATLAB_MCP_BIN", str(FIXTURE))
    monkeypatch.setenv("EE_MATLAB_MCP_TIMEOUT", "10")
    FIXTURE.chmod(0o755)
    out = get("run-matlab-if-present")(
        {"id": "m", "run_dir": str(tmp_path), "problem": {"code": "disp(42)"}},
        {},
    )
    assert out["ok"] is True
    assert out["unchecked"] is False
    assert "42" in out["output"]
    assert out["tool"] == "matlab-mcp"


def test_stub_error_is_unchecked(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("EE_MATLAB_MCP_BIN", str(FIXTURE))
    monkeypatch.setenv("EE_MATLAB_MCP_TIMEOUT", "10")

    def boom(*_a, **_k):
        raise MatlabMissing("forced")

    monkeypatch.setattr("electrical_engineer.matlab_mcp.evaluate_code", boom)
    out = get("run-matlab-if-present")(
        {"id": "m", "run_dir": str(tmp_path), "problem": {"code": "1"}},
        {},
    )
    assert out["ok"] is False
    assert out["unchecked"] is True


FIXTURE_TOOLS = Path(__file__).resolve().parents[1] / "fixtures" / "fake_simulink_tools.json"


def test_simulink_missing_json_is_cannot_do(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("EE_SIMULINK_TOOLS_JSON", raising=False)
    monkeypatch.delenv("MW_MCP_SERVER_EXTENSION_FILE", raising=False)
    assert simulink_extension() is None
    out = get("run-simulink-if-present")({"id": "s"}, {})
    assert out["ok"] is False
    assert out["unchecked"] is True
    assert out["cannot_do"] == "CD-SIMULINK-PLANT"
    assert "simulink" in out["error"].lower()


def test_spawn_cmd_passes_extension_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("EE_MATLAB_MCP_BIN", str(FIXTURE))
    monkeypatch.setenv("EE_SIMULINK_TOOLS_JSON", str(FIXTURE_TOOLS))
    cmd = spawn_cmd(str(tmp_path))
    assert any(p.startswith("--extension-file=") and p.endswith("fake_simulink_tools.json") for p in cmd)


def test_run_simulink_stub_not_checked(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("EE_MATLAB_MCP_BIN", str(FIXTURE))
    monkeypatch.setenv("EE_MATLAB_MCP_TIMEOUT", "10")
    monkeypatch.setenv("EE_SIMULINK_TOOLS_JSON", str(FIXTURE_TOOLS))
    FIXTURE.chmod(0o755)
    out = get("run-simulink-if-present")(
        {
            "id": "s",
            "run_dir": str(tmp_path),
            "problem": {"model_path": str(tmp_path / "plant.slx")},
        },
        {},
    )
    assert out["ok"] is False
    assert out["unchecked"] is True
    assert out["cannot_do"] == "CD-SIMULINK-PLANT"
    assert "5.0" not in str(out.get("output") or "")


"""MATLAB MCP client: missing fail-closed; fake stdio stub can return ok."""

from pathlib import Path

import pytest

from electrical_engineer.matlab_mcp import MatlabMissing, call_tool, matlab_bin, result_text
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

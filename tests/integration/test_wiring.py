import importlib
import json

from electrical_engineer import CAPABILITIES, bind
from electrical_engineer.mcp.server import handle


def test_import_cycle_clean() -> None:
    for name in (
        "electrical_engineer.cli",
        "electrical_engineer.ui_server.app",
        "electrical_engineer.mcp.server",
        "electrical_engineer.rag.retrieve",
        "electrical_engineer.local_llm.client",
        "electrical_engineer.runner.execute",
        "electrical_engineer.vision.fixtures",
        "electrical_engineer.capabilities",
    ):
        importlib.import_module(name)


def test_mcp_run_wires_execute() -> None:
    raw = handle(
        "tools/call",
        {"name": "run_workflow", "arguments": {"workflow_id": "unmatched-cosolver"}},
    )
    body = json.loads(raw["content"][0]["text"])
    assert body["waits"] is False
    assert body.get("run_id")


def test_public_capability_bind() -> None:
    assert "algebraic-check" in CAPABILITIES
    bound = bind("algebraic-check")
    assert bound.provider == "check-numeric"
    assert bind("lumped-circuit-sim").capability == "lumped-circuit-sim"

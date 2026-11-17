"""Cross-lab MCP hooks (control finish on a run)."""

from __future__ import annotations

from typing import Any

from electrical_engineer.collab.workflow import finish_control_lab
from electrical_engineer.runner.runs import create_run_dir, new_run_id, project_root

TOOL_DEFS: list[dict[str, Any]] = [
    {
        "name": "arc_lab_finish_control",
        "description": "Seed Control Studio for a run, simulate, optional derive check.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "run_id": {"type": "string"},
                "problem": {"type": "object"},
                "derived_value": {"type": "number"},
                "golden": {"type": "string"},
            },
            "required": ["run_id", "problem"],
        },
    },
]


def handle_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name != "arc_lab_finish_control":
        return {"error": f"unknown {name}", "waits": False}
    root = project_root()
    rid = str(args.get("run_id") or new_run_id())
    run_dir = root / "runs" / rid
    if not run_dir.is_dir():
        create_run_dir(root, rid)
    verify = finish_control_lab(
        run_dir,
        dict(args["problem"]),
        golden=args.get("golden"),
        derived_value=args.get("derived_value"),
    )
    return {"run_id": rid, "verify": verify, "mismatch": verify.get("mismatch"), "waits": False}
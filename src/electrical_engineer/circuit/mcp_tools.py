"""MCP tools for verify-after-derive circuits and schematic ingest."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.engines.circuit_multimodal import (
    confirm_and_write,
    propose_netlist_from_component,
    propose_netlist_from_image,
)
from electrical_engineer.engines.circuit_verify import verify_after_derive
from electrical_engineer.runner.execute import execute
from electrical_engineer.runner.runs import create_run_dir, new_run_id, project_root

TOOL_DEFS: list[dict[str, Any]] = [
    {
        "name": "arc_circuit_derive_verify",
        "description": "Run derive-circuit workflow on a problem.json-shaped payload.",
        "inputSchema": {
            "type": "object",
            "properties": {"problem": {"type": "object"}},
            "required": ["problem"],
        },
    },
    {
        "name": "arc_circuit_image_to_netlist",
        "description": "Propose SPICE netlist from schematic PNG or Visual Kit component id; optional confirm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string"},
                "component_id": {"type": "string"},
                "confirm": {"type": "boolean"},
                "run_id": {"type": "string"},
            },
        },
    },
    {
        "name": "arc_circuit_unit_benchmark",
        "description": "Return frontier B4 contract JSON (circuit_unit_pass_rate, multimodal_path_smoke).",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def handle_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name == "arc_circuit_derive_verify":
        problem = dict(args.get("problem") or {})
        root = project_root()
        out = execute("derive-circuit", cwd=root, problem=problem)
        run_dir = Path(out["run_dir"])
        verify_path = run_dir / "circuit_verify.json"
        verify = json.loads(verify_path.read_text()) if verify_path.is_file() else {}
        return {
            "run_id": out["run_id"],
            "summary": out["summary"],
            "verify": verify,
            "paths": [str(run_dir / "evidentiary.json"), str(verify_path)],
            "waits": False,
        }
    if name == "arc_circuit_image_to_netlist":
        root = project_root()
        run_id = str(args.get("run_id") or new_run_id())
        run_dir = create_run_dir(root, run_id)
        if args.get("component_id"):
            prop = propose_netlist_from_component(str(args["component_id"]))
        else:
            prop = propose_netlist_from_image(Path(str(args.get("image_path") or "")), cwd=root)
        if args.get("confirm") and prop.get("ok"):
            confirm_and_write(run_dir, cir=str(prop["cir"]), graph=prop.get("graph"))
            sim = verify_after_derive(
                {"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000, "value": 5.0, "tol": 1e-3},
                run_dir=run_dir,
            )
            prop["verify"] = sim
        prop["run_id"] = run_id
        prop["paths"] = [str(run_dir / "draft.cir"), str(run_dir / "confirmed.json")]
        prop["waits"] = not bool(args.get("confirm"))
        return prop
    if name == "arc_circuit_unit_benchmark":
        import subprocess
        import sys

        script = root / "scripts" / "run_circuit_benchmark.py"
        proc = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            cwd=root,
            check=False,
        )
        if proc.returncode != 0:
            return {"error": proc.stderr or proc.stdout, "waits": False}
        try:
            contract = json.loads(proc.stdout.strip().splitlines()[-1])
        except json.JSONDecodeError:
            contract = {"raw": proc.stdout}
        contract["waits"] = False
        return contract
    return {"error": f"unknown tool {name}", "waits": False}

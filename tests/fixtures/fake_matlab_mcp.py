#!/usr/bin/env python3
"""Fake MATLAB MCP stdio server for CI. No MATLAB process, no network."""

from __future__ import annotations

import json
import sys


def main() -> None:
    argv = " ".join(sys.argv)
    simulink = "--extension-file=" in argv
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        msg = json.loads(line)
        method = msg.get("method")
        if method == "notifications/initialized":
            continue
        if "id" not in msg:
            continue
        if method == "initialize":
            result: dict = {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "fake-matlab-mcp", "version": "0"},
                "capabilities": {"tools": {}},
            }
        elif method == "tools/list":
            tools = [
                {"name": "detect_matlab_toolboxes", "inputSchema": {"type": "object"}},
                {"name": "check_matlab_code", "inputSchema": {"type": "object"}},
                {"name": "evaluate_matlab_code", "inputSchema": {"type": "object"}},
                {"name": "run_matlab_file", "inputSchema": {"type": "object"}},
                {"name": "run_matlab_test_file", "inputSchema": {"type": "object"}},
            ]
            if simulink:
                tools.extend(
                    [
                        {"name": "model_read", "inputSchema": {"type": "object"}},
                        {"name": "model_check", "inputSchema": {"type": "object"}},
                        {"name": "model_scan", "inputSchema": {"type": "object"}},
                    ]
                )
            result = {"tools": tools}
        elif method == "tools/call":
            params = msg.get("params") or {}
            name = params.get("name")
            if name == "evaluate_matlab_code":
                text = "ans =\n    42"
                err = False
            elif name == "run_matlab_file":
                text = "file ok"
                err = False
            elif name in ("model_read", "model_check", "model_scan", "model_edit", "model_test"):
                # ponytail: stub is not a plant result
                text = "simulink stub: not a plant number"
                err = True
            else:
                text = str(name)
                err = False
            result = {"content": [{"type": "text", "text": text}]}
            if err:
                result["isError"] = True
        else:
            sys.stdout.write(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": msg["id"],
                        "error": {"code": -32601, "message": method},
                    }
                )
                + "\n"
            )
            sys.stdout.flush()
            continue
        sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": msg["id"], "result": result}) + "\n")
        sys.stdout.flush()
        if method == "tools/call":
            return


if __name__ == "__main__":
    main()

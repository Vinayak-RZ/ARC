"""Kernel stdio NDJSON client for MATLAB MCP Server. Host never lists these tools."""

from __future__ import annotations

import json
import os
import select
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

PROTOCOL = "2024-11-05"
DEFAULT_TIMEOUT = 120.0


class MatlabMissing(Exception):
    """Binary absent or not executable."""


class MatlabMcpError(Exception):
    """Spawn, protocol, or tool call failed. Callers fail closed."""


def matlab_bin() -> str | None:
    env = os.environ.get("EE_MATLAB_MCP_BIN")
    if env:
        path = Path(env)
        if path.is_file():
            return str(path)
        found = shutil.which(env)
        return found
    return shutil.which("matlab-mcp-server")


def timeout_s() -> float:
    raw = os.environ.get("EE_MATLAB_MCP_TIMEOUT")
    if not raw:
        return DEFAULT_TIMEOUT
    return float(raw)


def spawn_cmd(run_dir: str | None = None) -> list[str]:
    binary = matlab_bin()
    if not binary:
        raise MatlabMissing("matlab-mcp-server not available")
    cmd = [
        binary,
        "--matlab-session-mode=new",
        "--matlab-display-mode=nodesktop",
        "--disable-telemetry=true",
    ]
    root = os.environ.get("MW_MCP_SERVER_MATLAB_ROOT")
    if root:
        cmd.append(f"--matlab-root={root}")
    if run_dir:
        cmd.append(f"--initial-working-folder={run_dir}")
    if binary.endswith(".py"):
        # ponytail: CI stub is a Python file; real binary is a Go executable
        cmd.insert(0, sys.executable)
    return cmd


def _readline(proc: subprocess.Popen[str], timeout: float) -> dict[str, Any]:
    assert proc.stdout is not None
    ready, _, _ = select.select([proc.stdout], [], [], timeout)
    if not ready:
        raise MatlabMcpError("MATLAB MCP timeout")
    line = proc.stdout.readline()
    if not line:
        raise MatlabMcpError("MATLAB MCP closed stdout")
    try:
        msg = json.loads(line)
    except json.JSONDecodeError as exc:
        raise MatlabMcpError(f"MATLAB MCP non-JSON: {line[:200]}") from exc
    if msg.get("error"):
        raise MatlabMcpError(str(msg["error"]))
    return msg


def _send(proc: subprocess.Popen[str], payload: dict[str, Any]) -> None:
    assert proc.stdin is not None
    proc.stdin.write(json.dumps(payload) + "\n")
    proc.stdin.flush()


def call_tool(
    name: str,
    arguments: dict[str, Any],
    *,
    run_dir: str | None = None,
    timeout: float | None = None,
) -> dict[str, Any]:
    cmd = spawn_cmd(run_dir)
    limit = timeout if timeout is not None else timeout_s()
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError as exc:
        raise MatlabMissing(str(exc)) from exc
    try:
        _send(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": PROTOCOL,
                    "capabilities": {},
                    "clientInfo": {"name": "electrical-engineer", "version": "0.1.0"},
                },
            },
        )
        init = _readline(proc, limit)
        if "result" not in init:
            raise MatlabMcpError("initialize failed")
        _send(
            proc,
            {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
        )
        _send(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": name, "arguments": arguments},
            },
        )
        reply = _readline(proc, limit)
        result = reply.get("result")
        if not isinstance(result, dict):
            raise MatlabMcpError("tools/call missing result")
        return result
    except MatlabMissing:
        raise
    except MatlabMcpError:
        raise
    except Exception as exc:
        raise MatlabMcpError(str(exc)) from exc
    finally:
        if proc.stdin:
            proc.stdin.close()
        try:
            proc.wait(timeout=min(5.0, limit))
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()


def evaluate_code(code: str, project_path: str, *, timeout: float | None = None) -> dict[str, Any]:
    return call_tool(
        "evaluate_matlab_code",
        {"code": code, "project_path": str(Path(project_path).resolve())},
        run_dir=project_path,
        timeout=timeout,
    )


def run_file(script_path: str, *, timeout: float | None = None) -> dict[str, Any]:
    path = Path(script_path).resolve()
    return call_tool(
        "run_matlab_file",
        {"script_path": str(path)},
        run_dir=str(path.parent),
        timeout=timeout,
    )


def result_text(result: dict[str, Any]) -> str:
    chunks: list[str] = []
    for item in result.get("content") or []:
        if isinstance(item, dict) and item.get("type") == "text":
            chunks.append(str(item.get("text") or ""))
    return "\n".join(chunks).strip()

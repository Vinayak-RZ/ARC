"""Port reservation for UX/collab capture scripts."""

from __future__ import annotations

import os
import socket
import subprocess
import time
import urllib.error
import urllib.request

HOST = "127.0.0.1"
DEFAULT_PORT = 8765


def kill_port(port: int) -> None:
    try:
        subprocess.run(
            ["fuser", "-k", f"{port}/tcp"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except FileNotFoundError:
        pass
    time.sleep(0.3)


def _health_ok(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://{HOST}:{port}/api/health", timeout=1) as resp:
            return resp.status == 200
    except (OSError, urllib.error.URLError):
        return False


def _bind_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((HOST, port))
        except OSError:
            return False
    return True


def reserve_capture_port(preferred: int | None = None) -> int:
    """Free preferred port or pick the next free one; fail if stale server still answers health."""
    port = int(os.environ.get("ARC_CAPTURE_PORT", preferred or DEFAULT_PORT))
    kill_port(port)
    if _health_ok(port):
        raise RuntimeError(
            f"port {port} still serves /api/health after fuser -k — stale UI server; "
            "stop it manually or set ARC_CAPTURE_PORT to another port"
        )
    if _bind_free(port):
        return port
    for candidate in range(DEFAULT_PORT, DEFAULT_PORT + 32):
        if candidate == port:
            continue
        kill_port(candidate)
        if _health_ok(candidate):
            continue
        if _bind_free(candidate):
            print(f"capture port {port} busy; using {candidate}", flush=True)
            return candidate
    raise RuntimeError(f"no free capture port in {DEFAULT_PORT}-{DEFAULT_PORT + 31}")
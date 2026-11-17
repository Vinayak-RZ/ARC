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
    """Free preferred port or pick the next free one; skip ports that still answer health after kill."""
    start = int(os.environ.get("ARC_CAPTURE_PORT", preferred or DEFAULT_PORT))
    seen: set[int] = set()
    order = [start, *range(DEFAULT_PORT, DEFAULT_PORT + 32)]
    for port in order:
        if port in seen:
            continue
        seen.add(port)
        kill_port(port)
        if _health_ok(port):
            print(
                f"port {port} still serves /api/health after fuser -k (stale UI); trying another",
                flush=True,
            )
            continue
        if _bind_free(port):
            if port != start:
                print(f"capture using port {port} (preferred {start} unavailable)", flush=True)
            return port
    raise RuntimeError(
        f"no free capture port in {DEFAULT_PORT}-{DEFAULT_PORT + 31}; "
        "stop stale electrical-engineer ui processes or set ARC_CAPTURE_PORT"
    )
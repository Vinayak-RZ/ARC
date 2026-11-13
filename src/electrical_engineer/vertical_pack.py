"""Installable Arc EE vertical pack: skills, MCP stubs, doctor, smoke contract."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

MANIFEST_REL = Path("hosts/pack/manifest.json")
STATE_NAME = "vertical-pack.json"
STATE_DIR = ".electrical-engineer"


def repo_root() -> Path:
    env = os.environ.get("EE_REPO_ROOT")
    if env:
        path = Path(env)
        if path.is_dir():
            return path.resolve()
    cand = Path(__file__).resolve().parents[2]
    if (cand / MANIFEST_REL).is_file():
        return cand
    raise FileNotFoundError("Arc repo root not found; set EE_REPO_ROOT")


def load_manifest() -> dict[str, Any]:
    return json.loads((repo_root() / MANIFEST_REL).read_text(encoding="utf-8"))


def _mcp_command_block(arc_root: Path) -> dict[str, Any]:
    exe = shutil.which("electrical-engineer")
    if exe:
        return {"command": exe, "args": ["mcp"]}
    # ponytail: homework may only have the checkout + uv
    return {
        "command": "uv",
        "args": ["run", "--directory", str(arc_root), "electrical-engineer", "mcp"],
    }


def _cursor_mcp(into: Path, arc_root: Path) -> Path:
    path = into / ".cursor" / "mcp.json"
    body = {
        "mcpServers": {
            "electrical-engineer": _mcp_command_block(arc_root),
        }
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    return path


def _claude_mcp(into: Path, arc_root: Path) -> Path:
    path = into / ".mcp.json"
    body = {
        "mcpServers": {
            "electrical-engineer": _mcp_command_block(arc_root),
        }
    }
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    return path


def _codex_mcp(into: Path, arc_root: Path) -> Path:
    block = _mcp_command_block(arc_root)
    path = into / ".codex" / "config.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    cmd = block["command"].replace('"', '\\"')
    args = " ".join(block["args"])
    text = (
        f'[mcp_servers.electrical_engineer]\n'
        f'command = "{cmd}"\n'
        f'args = "{args}"\n'
    )
    path.write_text(text, encoding="utf-8")
    return path


def skill_dest(host: str, into: Path, host_name: str) -> Path:
    if host == "cursor":
        return into / ".cursor" / "skills" / host_name / "SKILL.md"
    if host == "claude":
        return into / ".claude" / "skills" / host_name / "SKILL.md"
    return into / ".codex" / "skills" / host_name / "SKILL.md"


def install_skills(
    into: Path, host: str, arc_root: Path, manifest: dict[str, Any] | None = None
) -> list[Path]:
    manifest = manifest or load_manifest()
    written: list[Path] = []
    for entry in manifest["skills"]:
        src = arc_root / entry["path"]
        if not src.is_file():
            raise FileNotFoundError(f"pack skill missing: {src}")
        dest = skill_dest(host, into, entry["host_name"])
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        written.append(dest)
    bench_src = arc_root / "hosts" / "pack" / "BENCHMARKS.md"
    if bench_src.is_file():
        if host == "cursor":
            bench_dest = into / ".cursor" / "skills" / "arc-ee-benchmarks" / "SKILL.md"
        elif host == "claude":
            bench_dest = into / ".claude" / "skills" / "arc-ee-benchmarks" / "SKILL.md"
        else:
            bench_dest = into / ".codex" / "skills" / "arc-ee-benchmarks" / "SKILL.md"
        bench_dest.parent.mkdir(parents=True, exist_ok=True)
        bench_dest.write_text(bench_src.read_text(encoding="utf-8"), encoding="utf-8")
        written.append(bench_dest)
    return written


def install_mcp(into: Path, host: str, arc_root: Path) -> list[Path]:
    if host == "cursor":
        return [_cursor_mcp(into, arc_root)]
    if host == "claude":
        return [_claude_mcp(into, arc_root)]
    return [_codex_mcp(into, arc_root)]


def state_path(into: Path) -> Path:
    return into / STATE_DIR / STATE_NAME


def write_state(
    into: Path,
    arc_root: Path,
    hosts: tuple[str, ...],
    paths: list[str],
) -> Path:
    path = state_path(into)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {
        "pack_id": load_manifest().get("pack_id"),
        "version": load_manifest().get("version"),
        "arc_repo": str(arc_root),
        "hosts": list(hosts),
        "installed_paths": paths,
    }
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    return path


def install_pack(into: Path, host: str = "all") -> list[Path]:
    from electrical_engineer.hosts_install import HOSTS
    from electrical_engineer.hosts_install import install as install_agents

    target = Path(into)
    if not str(target):
        raise ValueError("--into is required")
    chosen = HOSTS if host == "all" else (host,)
    for name in chosen:
        if name not in HOSTS:
            raise ValueError(f"unknown host {name!r}")
    arc_root = repo_root()
    manifest = load_manifest()
    written: list[Path] = []
    written.extend(install_agents(target, host=host))
    for name in chosen:
        written.extend(install_skills(target, name, arc_root, manifest))
        written.extend(install_mcp(target, name, arc_root))
    rel_paths = [str(p.relative_to(target)) for p in written]
    written.append(write_state(target, arc_root, chosen, rel_paths))
    return written


def uninstall_pack(into: Path) -> list[Path]:
    target = Path(into)
    state = state_path(target)
    if not state.is_file():
        return []
    data = json.loads(state.read_text(encoding="utf-8"))
    removed: list[Path] = []
    for rel in data.get("installed_paths") or []:
        path = target / rel
        if path.is_file():
            path.unlink()
            removed.append(path)
            parent = path.parent
            if parent.name != ".cursor" and parent.name != ".claude" and parent.name != ".codex":
                try:
                    parent.rmdir()
                except OSError:
                    pass
    state.unlink()
    if state.parent.exists() and not any(state.parent.iterdir()):
        state.parent.rmdir()
    return removed


def matlab_status() -> dict[str, Any]:
    from electrical_engineer.matlab_mcp import matlab_bin, simulink_extension

    bin_path = matlab_bin()
    present = bool(bin_path)
    message = "matlab-mcp-server available" if present else "matlab-mcp-server not on PATH (optional)"
    sim_ext = simulink_extension()
    from electrical_engineer.nodes.sim import run_matlab_if_present

    miss = run_matlab_if_present({"run_dir": str(Path.cwd())}, {})
    degraded_ok = bool(miss.get("unchecked")) and miss.get("ok") is not True
    if not present:
        message = str(miss.get("error") or message)
    return {
        "present": present,
        "binary": bin_path,
        "simulink_tools_json": sim_ext,
        "degrades_cleanly": degraded_ok,
        "host_message": message,
    }


def doctor() -> dict[str, Any]:
    from electrical_engineer.engines.control_runner import control_available
    from electrical_engineer.engines.power_runner import pandapower_available
    from electrical_engineer.engines.spice_runner import spice_available
    from electrical_engineer.matlab_mcp import matlab_bin, simulink_extension

    manifest_ok = (repo_root() / MANIFEST_REL).is_file()
    mcp_probe = _probe_mcp_tools()
    return {
        "pack_manifest": manifest_ok,
        "engines": {
            "ngspice": spice_available(),
            "python_control": control_available(),
            "pandapower": pandapower_available(),
        },
        "matlab_mcp": {
            "binary": matlab_bin(),
            "simulink_extension": simulink_extension(),
        },
        "matlab_optional": matlab_status(),
        "mcp_stdio": mcp_probe,
    }


def _probe_mcp_tools() -> dict[str, Any]:
    try:
        from electrical_engineer.mcp.server import TOOLS

        names = [str(t.get("name")) for t in TOOLS if t.get("name")]
        return {"ok": True, "tool_count": len(names), "tools": names}
    except ImportError as exc:
        return {"ok": False, "error": str(exc)[:500]}


def smoke_contract(into: Path | None = None) -> dict[str, bool]:
    target = into or Path.cwd() / ".vertical-pack-smoke"
    target = Path(target)
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    try:
        paths = install_pack(target, host="all")
        pack_install_smoke = len(paths) > 0
        mcp_paths = {
            "cursor": target / ".cursor" / "mcp.json",
            "claude": target / ".mcp.json",
            "codex": target / ".codex" / "config.toml",
        }
        for host, mcp_path in mcp_paths.items():
            assert mcp_path.is_file(), host
        assert (target / ".cursor/skills/arc-ee/SKILL.md").is_file()
        assert (target / ".cursor/skills/arc-ee-web-verify/SKILL.md").is_file()
        assert (target / ".cursor/agents/ee-circuits.md").is_file()
        removed = uninstall_pack(target)
        assert removed, "uninstall removed nothing"
        assert not state_path(target).exists()
    except (AssertionError, OSError, ValueError, FileNotFoundError):
        pack_install_smoke = False
    mat = matlab_status()
    matlab_optional = bool(mat.get("degrades_cleanly"))
    return {"pack_install_smoke": pack_install_smoke, "matlab_optional": matlab_optional}

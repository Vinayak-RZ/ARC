"""Copy catalog cards into a homework tree. Not this product .cursor/."""

from __future__ import annotations

import os
from pathlib import Path

PACKS = (
    "circuits",
    "signals",
    "electronics",
    "machines",
    "power",
    "control",
    "power_electronics",
    "measurements",
    "em",
    "maths",
    "_cross",
)

HOSTS = ("cursor", "codex", "claude")


def pack_slug(pack: str) -> str:
    if pack == "_cross":
        return "cross"
    if pack == "simulink":
        return "simulink"
    return pack.replace("_", "-")


def cursor_name(pack: str) -> str:
    return f"ee-{pack_slug(pack)}"


def codex_name(pack: str) -> str:
    return f"ee_{pack_slug(pack).replace('-', '_')}"


def adapters_dir() -> Path:
    env = os.environ.get("EE_ADAPTERS_DIR")
    if env:
        path = Path(env)
        if path.is_dir():
            return path
        raise FileNotFoundError(f"EE_ADAPTERS_DIR not a directory: {env}")
    cand = Path(__file__).resolve().parents[2] / "hosts" / "adapters"
    if cand.is_dir():
        return cand
    raise FileNotFoundError("hosts/adapters not found; run from checkout or set EE_ADAPTERS_DIR")


def agents_dir() -> Path:
    env = os.environ.get("EE_AGENTS_DIR")
    if env:
        path = Path(env)
        if path.is_dir():
            return path
        raise FileNotFoundError(f"EE_AGENTS_DIR not a directory: {env}")
    cand = adapters_dir().parent / "agents"
    if cand.is_dir():
        return cand
    raise FileNotFoundError("hosts/agents not found; run from checkout or set EE_AGENTS_DIR")


def card_paths() -> list[Path]:
    return sorted(p for p in agents_dir().glob("ee-*.md"))


def parse_card(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"missing frontmatter: {path}")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"bad frontmatter: {path}")
    meta: dict[str, str] = {}
    for line in parts[1].strip().splitlines():
        key, _, val = line.partition(":")
        meta[key.strip()] = val.strip()
    return meta, parts[2].lstrip("\n")


def _codex_toml(meta: dict[str, str], body: str) -> str:
    name = meta["name"].replace("-", "_")
    desc = meta["description"].replace('"', "'")
    # ponytail: TOML triple-quote; cards have no """ by contract
    return (
        f'name = "{name}"\n'
        f'description = "{desc}"\n'
        f'developer_instructions = """\n'
        f"{body.rstrip()}\n"
        f'"""\n'
    )


def install(into: Path, host: str = "all") -> list[Path]:
    target = Path(into)
    if not str(target):
        raise ValueError("--into is required")
    chosen = HOSTS if host == "all" else (host,)
    for name in chosen:
        if name not in HOSTS:
            raise ValueError(f"unknown host {name}")
    cards = card_paths()
    if not cards:
        raise FileNotFoundError("no ee-*.md cards in hosts/agents")
    written: list[Path] = []
    for name in chosen:
        for card in cards:
            meta, body = parse_card(card)
            cursor = meta["name"]
            if name == "cursor":
                path = target / ".cursor" / "agents" / f"{cursor}.md"
                text = card.read_text(encoding="utf-8")
            elif name == "claude":
                path = target / ".claude" / "agents" / f"{cursor}.md"
                text = card.read_text(encoding="utf-8")
            else:
                path = target / ".codex" / "agents" / f"{cursor.replace('-', '_')}.toml"
                text = _codex_toml(meta, body)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            written.append(path)
    return written

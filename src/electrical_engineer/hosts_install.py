"""Copy per-pack host adapters into a homework tree. Not this product .cursor/."""

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

HINTS = {
    "circuits": "KCL/KVL, phasors, transients, Thevenin, two-ports",
    "signals": "LTI, convolution, Fourier/Laplace/z, sampling",
    "electronics": "devices, op-amps, small-signal, UG digital",
    "machines": "transformers, DC/IM/synchronous equivalent circuits",
    "power": "per-unit, load flow, faults, study-level protection",
    "control": "TF/SS, Routh, Bode/Nyquist, simple compensators",
    "power_electronics": "rectifiers, buck/boost, PWM, averaged models",
    "measurements": "errors, bridges, instrument specs",
    "em": "electrostatics, magnetostatics, TEM lines at UG",
    "maths": "complex algebra, ODE/Laplace/Fourier as EE tools",
    "_cross": "unmatched or multi-pack; no auto-SPICE",
}

HOSTS = ("cursor", "codex", "claude")


def pack_slug(pack: str) -> str:
    if pack == "_cross":
        return "cross"
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


def specialist_body() -> str:
    path = adapters_dir() / "specialist-body.md"
    return path.read_text(encoding="utf-8").strip() + "\n"


def _description(pack: str) -> str:
    hint = HINTS[pack]
    return (
        f"UG EE {pack_slug(pack)} pack specialist. Use for {hint}. "
        f"Load skills/{pack}. Same EE MCP. Do not mint checked ohms. "
        "Never evaluate_matlab_code."
    )


def _cursor_md(pack: str, body: str) -> str:
    name = cursor_name(pack)
    return (
        f"---\n"
        f"name: {name}\n"
        f"description: {_description(pack)}\n"
        f"model: inherit\n"
        f"---\n\n"
        f"Load `skills/{pack}/SKILL.md` (and root `skills/SKILL.md`).\n\n"
        f"{body}"
    )


def _claude_md(pack: str, body: str) -> str:
    return _cursor_md(pack, body)


def _codex_toml(pack: str, body: str) -> str:
    name = codex_name(pack)
    instructions = (
        f"Load skills/{pack}/SKILL.md and skills/SKILL.md.\n\n{body}"
    )
    # ponytail: TOML triple-quote; body has no """ by contract
    return (
        f'name = "{name}"\n'
        f'description = "{_description(pack)}"\n'
        f'developer_instructions = """\n'
        f"{instructions}"
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
    body = specialist_body()
    written: list[Path] = []
    for name in chosen:
        for pack in PACKS:
            if name == "cursor":
                path = target / ".cursor" / "agents" / f"{cursor_name(pack)}.md"
                text = _cursor_md(pack, body)
            elif name == "claude":
                path = target / ".claude" / "agents" / f"{cursor_name(pack)}.md"
                text = _claude_md(pack, body)
            else:
                path = target / ".codex" / "agents" / f"{codex_name(pack)}.toml"
                text = _codex_toml(pack, body)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            written.append(path)
    return written

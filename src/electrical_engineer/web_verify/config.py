"""Load web-verify provider settings from arc.toml and environment."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from electrical_engineer.runner.runs import project_root


@dataclass(frozen=True)
class WebVerifyConfig:
    provider: str = "host"
    search_url: str | None = None
    search_api_key: str | None = None
    offline_fixtures_root: Path | None = None


def _read_arc_toml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        import tomllib
    except ImportError:
        return {}
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    section = data.get("web_verify")
    return section if isinstance(section, dict) else {}


def load_web_verify_config(cwd: Path | None = None) -> WebVerifyConfig:
    root = project_root(cwd)
    section = _read_arc_toml(root / "arc.toml")
    provider = (
        os.environ.get("EE_WEB_VERIFY_PROVIDER")
        or os.environ.get("ARC_WEB_VERIFY_PROVIDER")
        or section.get("provider")
        or "host"
    )
    search_url = os.environ.get("EE_WEB_SEARCH_URL") or section.get("search_url")
    search_api_key = os.environ.get("EE_WEB_SEARCH_API_KEY") or section.get("search_api_key")
    fixtures = os.environ.get("EE_WEB_VERIFY_FIXTURES")
    fix_path = Path(fixtures) if fixtures else root / "eval" / "fixtures" / "web_verify"
    return WebVerifyConfig(
        provider=str(provider).strip().lower(),
        search_url=str(search_url).strip() if search_url else None,
        search_api_key=str(search_api_key).strip() if search_api_key else None,
        offline_fixtures_root=fix_path if fix_path.is_dir() else None,
    )

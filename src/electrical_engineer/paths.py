"""Install root: packaged wheel bundle or editable checkout."""

from __future__ import annotations

import os
from pathlib import Path

# Bundle layout inside the installed package (hatch force-include).
_BUNDLE = Path(__file__).resolve().parent / "_bundle"


def bundle_root() -> Path | None:
    """Return packaged asset root when workflows/ are shipped in the wheel."""
    if (_BUNDLE / "workflows").is_dir():
        return _BUNDLE
    return None


def checkout_root() -> Path | None:
    """Repo root when running from an editable/src checkout."""
    env = os.environ.get("EE_REPO_ROOT")
    if env:
        path = Path(env)
        if path.is_dir():
            return path.resolve()
    # src/electrical_engineer/paths.py → parents[2] == repo root
    cand = Path(__file__).resolve().parents[2]
    if (cand / "workflows").is_dir() or (cand / "hosts" / "pack" / "manifest.json").is_file():
        return cand
    return None


def install_root() -> Path:
    """Product asset root for recipes, hosts, and UI static files.

    Prefer checkout (editable/dev), then wheel bundle, then EE_REPO_ROOT-only
    fallbacks already handled above.
    """
    root = checkout_root()
    if root is not None:
        return root
    bundled = bundle_root()
    if bundled is not None:
        return bundled
    raise FileNotFoundError(
        "Arc install root not found; set EE_REPO_ROOT or install a wheel with bundled assets"
    )


def workflows_dir(cwd: Path | None = None) -> Path:
    """Recipe YAML root: CWD project first, else install_root/workflows."""
    from electrical_engineer.runner.runs import project_root

    proj = project_root(cwd)
    local = proj / "workflows"
    if local.is_dir():
        return local
    return install_root() / "workflows"


def hosts_dir() -> Path:
    env = os.environ.get("EE_ADAPTERS_DIR")
    if env:
        # EE_ADAPTERS_DIR points at hosts/adapters; parent is hosts/
        return Path(env).resolve().parent
    return install_root() / "hosts"


def ui_dist_dir() -> Path:
    return install_root() / "ui" / "dist"

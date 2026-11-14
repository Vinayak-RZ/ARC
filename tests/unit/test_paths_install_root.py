"""install_root resolves checkout vs packaged bundle."""

from __future__ import annotations

from pathlib import Path

import electrical_engineer.paths as paths


def test_checkout_root_finds_repo_workflows() -> None:
    root = paths.checkout_root()
    assert root is not None
    assert (root / "workflows").is_dir()
    assert (root / "hosts" / "pack" / "manifest.json").is_file()


def test_install_root_prefers_checkout() -> None:
    assert paths.install_root() == paths.checkout_root()


def test_workflows_dir_uses_install_when_cwd_has_none(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    root = paths.workflows_dir(tmp_path)
    assert root.is_dir()
    assert any(root.glob("**/*.yaml"))


def test_hosts_and_ui_under_install_root() -> None:
    assert (paths.hosts_dir() / "adapters").is_dir()
    # ui/dist may be absent until npm build; path still resolves under install root
    dist = paths.ui_dist_dir()
    assert dist == paths.install_root() / "ui" / "dist"


def test_bundle_root_when_workflows_present(tmp_path: Path, monkeypatch) -> None:
    fake_pkg = tmp_path / "electrical_engineer"
    bundle = fake_pkg / "_bundle"
    (bundle / "workflows").mkdir(parents=True)
    (bundle / "hosts" / "pack").mkdir(parents=True)
    (bundle / "hosts" / "pack" / "manifest.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(paths, "_BUNDLE", bundle)
    monkeypatch.setattr(paths, "checkout_root", lambda: None)
    assert paths.bundle_root() == bundle
    assert paths.install_root() == bundle
    assert paths.workflows_dir(tmp_path) == bundle / "workflows"

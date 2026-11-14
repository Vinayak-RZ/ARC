from pathlib import Path


def test_extensive_paths_exist() -> None:
    text = Path("docs/EXTENSIVE.md").read_text()
    for p in (
        "src/electrical_engineer/cli.py",
        "src/electrical_engineer/runner/execute.py",
        "ui/src/tokens.css",
        "eval/gold/",
        "assets/brand/arc-icon.png",
        "assets/brand/arc-lockup.png",
        "ui/public/arc-icon.png",
        "scripts/build_release_wheel.py",
    ):
        assert p in text
        if not p.endswith("/"):
            assert Path(p).exists()
    readme = Path("README.md").read_text()
    assert readme.count("docs/EXTENSIVE.md") >= 1
    assert "unchecked" in readme
    assert "assets/brand/arc-lockup.png" in readme
    assert "uvx electrical-engineer" in readme
    assert "PyPI" in text  # consumer install / publish track
    assert "uvx" in text or "build_release_wheel" in text

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_coverage_floors() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_coverage_floors.py")],
        cwd=ROOT,
        check=False,
    )
    assert r.returncode == 0


def test_strict_knowledge_tree() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_knowledge_tree.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    assert "units=" in r.stdout


def test_glossary_exists() -> None:
    assert (ROOT / "knowledge" / "GLOSSARY.md").is_file()

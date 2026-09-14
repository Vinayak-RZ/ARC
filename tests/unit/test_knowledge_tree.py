from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def test_coverage_floors() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_coverage_floors.py")],
        cwd=ROOT,
        check=False,
    )
    assert r.returncode == 0


def test_allow_empty_or_strict_tree() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_knowledge_tree.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        r2 = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "check_knowledge_tree.py"),
                "--allow-empty",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        assert r2.returncode == 0, r2.stderr
    else:
        assert "units=" in r.stdout

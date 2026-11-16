#!/usr/bin/env python3
"""Install the built wheel into a clean venv and smoke-test CLI paths."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _latest_wheel() -> Path:
    wheels = sorted((ROOT / "dist").glob("electrical_engineer-*.whl"))
    if not wheels:
        raise SystemExit("no wheel in dist/; run scripts/build_release_wheel.py first")
    return wheels[-1]


def _venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def main() -> int:
    wheel = _latest_wheel()
    with tempfile.TemporaryDirectory(prefix="ee-wheel-smoke-") as tmp:
        tmp_path = Path(tmp)
        venv_dir = tmp_path / "venv"
        work = tmp_path / "work"
        work.mkdir()
        venv.create(venv_dir, with_pip=True)
        py = _venv_python(venv_dir)
        subprocess.check_call([str(py), "-m", "pip", "install", "-q", "--upgrade", "pip"])
        subprocess.check_call([str(py), "-m", "pip", "install", "-q", str(wheel)])
        env = {**os.environ, "EE_NO_BROWSER": "1"}
        # Non-checkout cwd: must use bundled assets, not the git tree.
        wf = subprocess.check_output(
            [str(py), "-m", "electrical_engineer", "workflows"],
            cwd=work,
            env=env,
            text=True,
        )
        if "solve-circuit-problem" not in wf and "solve-control-problem" not in wf:
            print(f"unexpected workflows output:\n{wf}", file=sys.stderr)
            return 1
        doctor = subprocess.run(
            [str(py), "-m", "electrical_engineer", "hosts", "doctor"],
            cwd=work,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        if doctor.returncode != 0:
            print(doctor.stdout + doctor.stderr, file=sys.stderr)
            return doctor.returncode
        # Bundle UI index must resolve without checkout
        check = subprocess.check_output(
            [
                str(py),
                "-c",
                (
                    "from electrical_engineer.paths import ui_dist_dir, bundle_root; "
                    "assert bundle_root() is not None; "
                    "assert (ui_dist_dir() / 'index.html').is_file(); "
                    "print('ui_ok')"
                ),
            ],
            cwd=work,
            env=env,
            text=True,
        )
        if "ui_ok" not in check:
            print("ui dist check failed", file=sys.stderr)
            return 1
    print(f"ok smoke {wheel.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

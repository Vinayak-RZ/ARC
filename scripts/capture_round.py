#!/usr/bin/env python3
"""Single entry: UX capture → collab (+ rectifier sweep) → postflight for round N."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
CONTROL_STUDIO = ROOT / ".electrical-engineer" / "control_studio"
CAPTURE_PREFIX = "artifacts/ux-review/"


def _git_ci_status() -> dict:
    try:
        out = subprocess.check_output(
            ["gh", "pr", "view", "--json", "statusCheckRollup", "-q", ".statusCheckRollup"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        checks = json.loads(out or "[]")
        return {
            "checks": [
                {
                    "name": c.get("name"),
                    "state": c.get("state") or c.get("conclusion"),
                    "url": c.get("detailsUrl"),
                }
                for c in checks
            ]
        }
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        return {"checks": [], "note": "CI status unavailable from gh"}


def _assert_clean_tree() -> None:
    dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip()
    if not dirty:
        return
    bad: list[str] = []
    for ln in dirty.splitlines():
        if not ln.strip():
            continue
        path = ln[3:].strip() if len(ln) > 3 else ln
        if ln.startswith("??") and path.startswith(CAPTURE_PREFIX):
            continue
        if ln.startswith("??") and path.startswith("ui/test-results"):
            continue
        bad.append(ln)
    if bad:
        raise RuntimeError(f"refusing capture on dirty tree ({len(bad)} lines): {bad[:12]}")


def _write_capture_preflight(out_dir: Path) -> None:
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    sha_short = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, text=True).strip()
    data = {
        "git_sha": sha,
        "git_sha_short": sha_short,
        "git_branch": branch,
        "capture_entry": "scripts/capture_round.py",
        "ci": _git_ci_status(),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "preflight.json"
    if path.is_file():
        try:
            data = {**json.loads(path.read_text(encoding="utf-8")), **data}
        except json.JSONDecodeError:
            pass
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("wrote", path)


def _run_fail_fast(cmd: list[str], *, env: dict[str, str] | None = None) -> None:
    print(">>>", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT, env=env or os.environ)


def main() -> int:
    parser = argparse.ArgumentParser(description="Round N UX + collab capture with postflight")
    parser.add_argument("--round", type=int, required=True)
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="CI subset: collab-01 headline, one rectifier shot, studio resize wires",
    )
    parser.add_argument(
        "--keep-artifacts",
        action="store_true",
        help="Do not delete the round output directory before capture",
    )
    args = parser.parse_args()

    subdir = f"round-{args.round}"
    out = ROOT / CAPTURE_PREFIX.rstrip("/") / subdir
    capture_env = {**os.environ, "ARC_UX_CAPTURE_DIR": subdir}

    if args.smoke:
        _run_fail_fast([sys.executable, str(ROOT / "scripts" / "capture_round_smoke.py")], env=capture_env)
        return 0

    _assert_clean_tree()
    sys.path.insert(0, str(ROOT / "scripts"))
    from capture_port import reserve_capture_port

    port = reserve_capture_port()
    port_s = str(port)
    capture_env = {**capture_env, "ARC_CAPTURE_PORT": port_s, "EE_UI_PORT": port_s}
    print(f"capture UI port {port_s}", flush=True)

    if not args.keep_artifacts and out.is_dir():
        shutil.rmtree(out)
    if RUNS.is_dir():
        shutil.rmtree(RUNS)
    RUNS.mkdir(parents=True, exist_ok=True)
    if CONTROL_STUDIO.is_dir():
        shutil.rmtree(CONTROL_STUDIO)

    _write_capture_preflight(out)
    subprocess.check_call(["npm", "run", "build"], cwd=ROOT / "ui")

    collab_env = {**capture_env, "ROUND12_START_UI": "1"}
    steps: list[tuple[list[str], dict[str, str]]] = [
        (
            [sys.executable, str(ROOT / "scripts" / "capture_ux_review_round.py"), "--round", str(args.round)],
            capture_env,
        ),
        ([sys.executable, str(ROOT / "scripts" / "capture_round_12_collab.py")], collab_env),
    ]
    for script, env in steps:
        try:
            _run_fail_fast(script, env=env)
        except subprocess.CalledProcessError as exc:
            raise SystemExit(exc.returncode) from exc

    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    env_pf = {
        **capture_env,
        "ROUND12_CI_RUN_ID": os.environ.get("ROUND12_CI_RUN_ID", ""),
        "ROUND12_CI_STATUS": os.environ.get("ROUND12_CI_STATUS", "not_reported"),
        "ROUND13_CAPTURE_SHA": sha,
    }
    _run_fail_fast([sys.executable, str(ROOT / "scripts" / "round_12_postflight.py")], env=env_pf)
    _write_capture_preflight(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
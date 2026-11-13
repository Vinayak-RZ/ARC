#!/usr/bin/env python3
"""Package EEE-Coursework-Trap v0.1 from non-sealed Arc gold sets."""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import shutil
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "artifacts" / "benchmarks" / "eee-coursework-trap" / "v0.1"
STAGING = OUT_DIR / "_stage"


def _stable_summary(summary: dict | None, expect: dict) -> dict:
    """Drop run ids and paths so tarball SHA is reproducible."""
    if not summary:
        return {}
    stable: dict = {}
    if "value" in summary:
        stable["value"] = summary["value"]
    if "recipe_id" in summary:
        stable["recipe_id"] = summary["recipe_id"]
    if "recomputed" in summary:
        stable["recomputed"] = summary["recomputed"]
    engine = expect.get("engine")
    if engine:
        stable["engine"] = engine
        for key in (
            "delta0_deg",
            "delta_cr_deg",
            "tcr_s",
            "t_to_delta_cr_s",
            "primary_df1_Hz",
            "primary_P12_MW",
            "agc_ss_df1_Hz",
            "agc_ss_Pm1_MW",
            "lam",
            "cases",
        ):
            if key in summary:
                stable[key] = summary[key]
    return stable


def _collect_eval_items() -> list[dict]:
    from electrical_engineer.eval_runner.score import run_item

    items: list[dict] = []
    for pack in ("power", "control", "circuits"):
        pack_dir = ROOT / "eval" / "gold" / pack
        for item in sorted(pack_dir.iterdir()):
            if not item.is_dir() or not (item / "expect.json").is_file():
                continue
            row = run_item(item, run_root=ROOT / "runs" / "_benchmark_build")
            expect = json.loads((item / "expect.json").read_text())
            items.append(
                {
                    "id": f"{pack}/{item.name}",
                    "domain": pack,
                    "source": str(item.relative_to(ROOT)),
                    "expect_mode": "engine" if expect.get("engine") else "recipe",
                    "oracle_ok": bool(row.get("ok")),
                    "grading": {
                        "tol": expect.get("tol", expect.get("tolerance_deg", 1e-3)),
                        "engine": expect.get("engine"),
                        "recipe_id": expect.get("recipe_id"),
                    },
                    "summary": _stable_summary(row.get("summary"), expect),
                }
            )
    trap_index = json.loads((ROOT / "artifacts/frontier/trap_suite_index.json").read_text())
    from electrical_engineer.rlvr_env.rewards import oracle_submission

    for trap in trap_index["traps"]:
        tid = trap["id"]
        sub = oracle_submission(tid)
        items.append(
            {
                "id": f"trap/{tid}",
                "domain": "trap",
                "source": trap["path"],
                "expect_mode": "trap_verifier",
                "oracle_ok": True,
                "grading": {"trap_id": tid},
                "summary": {"oracle_submission": sub},
            }
        )
    return items


def _write_datasheet(items: list[dict]) -> dict:
    by_domain: dict[str, int] = {}
    for it in items:
        by_domain[it["domain"]] = by_domain.get(it["domain"], 0) + 1
    return {
        "schema": "arc.benchmark.datasheet.v0.1",
        "version": "v0.1",
        "name": "eee-coursework-trap",
        "task_counts_by_domain": by_domain,
        "total_tasks": len(items),
        "grading_tolerance_rules": (
            "Recipe items: value within expect.json tol vs evidentiary recompute. "
            "PSA engine items: tolerances in expect.json (deg, seconds, MW). "
            "Trap items: binary pass via rlvr_env.rewards.grade_trap."
        ),
        "licence": "Apache-2.0; prompts are license-clean reconstructions. No copyrighted exam PDFs.",
        "excluded": "live-ab, exam-v4/v5/v6, sealed REFERENCE.json",
        "gold_sources": "eval/gold/{power,control,circuits} and knowledge/traps via trap_suite_index",
    }


def _answer_key(items: list[dict]) -> dict:
    answers = {}
    for it in items:
        answers[it["id"]] = {
            "domain": it["domain"],
            "oracle_ok": it["oracle_ok"],
            "reference": it["summary"],
            "grading": it["grading"],
        }
    return {"schema": "arc.benchmark.answer_key.v0.1", "answers": answers}


def main() -> int:
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)
    items = _collect_eval_items()
    datasheet = _write_datasheet(items)
    key = _answer_key(items)
    manifest = {
        "version": "v0.1",
        "items": [it["id"] for it in items],
        "datasheet": datasheet,
    }
    paths = {
        "benchmark_items.json": items,
        "datasheet.json": datasheet,
        "answer_key.json": key,
        "manifest.json": manifest,
        "trap_suite_index.json": json.loads(
            (ROOT / "artifacts/frontier/trap_suite_index.json").read_text()
        ),
        "trap_prompts.yaml": (ROOT / "proofs/ablation/trap_prompts.yaml").read_text(),
        "rlvr_env_manifest.json": __import__(
            "electrical_engineer.rlvr_env", fromlist=["contract_json"]
        ).contract_json(),
    }
    staged_files: list[Path] = []
    for name, content in paths.items():
        dest = STAGING / name
        if isinstance(content, str):
            dest.write_text(content, encoding="utf-8")
        else:
            dest.write_text(json.dumps(content, indent=2), encoding="utf-8")
        staged_files.append(dest)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tarball = OUT_DIR / "eee-coursework-trap-v0.1.tar.gz"
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        for path in staged_files:
            info = tar.gettarinfo(path, arcname=f"eee-coursework-trap-v0.1/{path.name}")
            info.mtime = 0
            with path.open("rb") as handle:
                tar.addfile(info, handle)
    tarball.write_bytes(gzip.compress(buf.getvalue(), mtime=0))
    digest = hashlib.sha256(tarball.read_bytes()).hexdigest()
    release_manifest = {
        "version": "v0.1",
        "sha256": digest,
        "tarball": tarball.name,
        "files": [p.name for p in staged_files],
        "total_tasks": len(items),
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(release_manifest, indent=2))
    print(json.dumps({"tarball": str(tarball), "sha256": digest, "tasks": len(items)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

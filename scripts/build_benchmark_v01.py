#!/usr/bin/env python3
"""Package EEE-Coursework-Trap v0.1: public questions tarball + private answer key."""

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
KEY_DIR = OUT_DIR / "_key"


def _write_tarball(paths: list[Path], dest: Path, prefix: str) -> str:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        for path in paths:
            info = tar.gettarinfo(path, arcname=f"{prefix}/{path.name}")
            info.mtime = 0
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            with path.open("rb") as handle:
                tar.addfile(info, handle)
    dest.write_bytes(gzip.compress(buf.getvalue(), mtime=0))
    return hashlib.sha256(dest.read_bytes()).hexdigest()


def main() -> int:
    from electrical_engineer.benchmark_v01.catalog import build_task_catalog

    if STAGING.exists():
        shutil.rmtree(STAGING)
    if KEY_DIR.exists():
        shutil.rmtree(KEY_DIR)
    STAGING.mkdir(parents=True)
    KEY_DIR.mkdir(parents=True)

    questions, answer_map, catalog_meta = build_task_catalog()
    by_domain = catalog_meta["by_domain"]

    datasheet = {
        "schema": "arc.benchmark.datasheet.v0.1",
        "version": "v0.1",
        "name": "eee-coursework-trap",
        "task_counts_by_domain": by_domain,
        "difficulty_tiers": catalog_meta.get("difficulty_tiers", {}),
        "total_tasks": len(questions),
        "unique_question_givens": catalog_meta["unique_question_givens"],
        "grading_tolerance_rules": "Submit only fields named in answer_schema within listed tolerances and units.",
        "licence": "Apache-2.0; license-clean reconstructions only.",
        "excluded": "live-ab, exam-v4/v5/v6, sealed REFERENCE.json",
        "public_artifact": "eee-coursework-trap-v0.1-questions.tar.gz",
        "private_artifact": "answer_key.json (not in questions tarball)",
    }

    public_questions = {"schema": "arc.benchmark.questions.v0.1", "tasks": questions}
    key_body = {
        "schema": "arc.benchmark.answer_key.v0.1",
        "key_sha256": hashlib.sha256(
            json.dumps(answer_map, sort_keys=True).encode()
        ).hexdigest(),
        "answers": answer_map,
    }

    pub_files = {
        "questions.json": public_questions,
        "datasheet.json": datasheet,
        "README.txt": (
            "Public questions only. Submit answers.json to grade_benchmark_v01.py with the "
            "matching answer key held by Arc maintainers."
        ),
    }
    staged: list[Path] = []
    for name, content in pub_files.items():
        dest = STAGING / name
        if isinstance(content, str):
            dest.write_text(content, encoding="utf-8")
        else:
            dest.write_text(json.dumps(content, indent=2), encoding="utf-8")
        staged.append(dest)

    key_path = KEY_DIR / "answer_key.json"
    key_path.write_text(json.dumps(key_body, indent=2))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    q_tar = OUT_DIR / "eee-coursework-trap-v0.1-questions.tar.gz"
    q_sha = _write_tarball(staged, q_tar, "eee-coursework-trap-v0.1-questions")

    release_manifest = {
        "version": "v0.1",
        "questions_sha256": q_sha,
        "questions_tarball": q_tar.name,
        "answer_key_path": str(key_path.relative_to(ROOT)),
        "answer_key_sha256": key_body["key_sha256"],
        "total_tasks": len(questions),
        "unique_question_givens": catalog_meta["unique_question_givens"],
        "task_counts_by_domain": by_domain,
        "difficulty_tiers": catalog_meta.get("difficulty_tiers", {}),
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(release_manifest, indent=2))
    print(
        json.dumps(
            {
                "questions_tarball": str(q_tar),
                "tarball_sha256": q_sha,
                "tasks": len(questions),
                "unique_tasks": catalog_meta["unique_question_givens"],
                "by_domain": by_domain,
                "difficulty_tiers": catalog_meta.get("difficulty_tiers", {}),
            }
        )
    )
    return 0 if len(questions) >= 60 else 1


if __name__ == "__main__":
    raise SystemExit(main())

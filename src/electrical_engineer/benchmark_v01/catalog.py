"""Build public questions and private answer keys for v0.1 (60+ tasks)."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from electrical_engineer.eval_runner.psa_score import run_psa_item
from electrical_engineer.eval_runner.score import run_item
from electrical_engineer.rlvr_env import problems as trap_problems
from electrical_engineer.rlvr_env.rewards import naive_submission, oracle_submission

ROOT = Path(__file__).resolve().parents[3]


def iter_circuit_gold_dirs(circuits_root: Path | None = None) -> Iterator[Path]:
    """All eval/gold/circuits/* with expect.json (auto-picks new items)."""
    root = circuits_root or ROOT / "eval" / "gold" / "circuits"
    if not root.is_dir():
        return
    for item in sorted(root.iterdir()):
        if item.is_dir() and (item / "expect.json").is_file():
            yield item


def _read_task_md(item_dir: Path) -> str:
    path = item_dir / "task.md"
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    return ""


def _fixtures(item_dir: Path) -> dict[str, Any]:
    out: dict[str, Any] = {}
    fx = item_dir / "fixtures"
    if not fx.is_dir():
        return out
    for name in ("problem.json", "case.json", "payload.json", "graph.json"):
        p = fx / name
        if p.is_file():
            out[name] = json.loads(p.read_text())
    return out


def _recipe_question(item_dir: Path, expect: dict[str, Any], fixtures: dict[str, Any]) -> str:
    task = _read_task_md(item_dir)
    if task:
        return task
    rid = expect.get("recipe_id", "unknown")
    prob = fixtures.get("problem.json") or {}
    if prob:
        return f"Run recipe {rid} with givens: {json.dumps(prob, sort_keys=True)}"
    return f"Solve using Arc workflow {rid} and return the checked numeric result."


def _answer_schema_recipe(expect: dict[str, Any]) -> dict[str, Any]:
    tol = float(expect.get("tol", 1e-6))
    fields = [{"name": "value", "type": "float", "unit": "SI or as stated", "tolerance": tol}]
    if expect.get("recomputed"):
        fields.extend(
            {"name": k, "type": "float", "tolerance": tol} for k in expect["recomputed"]
        )
    return {
        "fields": fields,
        "rule": (
            "Recompute with the same recipe_id and givens; match within tolerance. "
            "Self-reported unchecked tokens are not graded."
        ),
    }


def _answer_schema_engine(expect: dict[str, Any]) -> dict[str, Any]:
    engine = str(expect.get("engine"))
    if engine == "smib_swing":
        return {
            "fields": [
                {"name": "delta0_deg", "type": "float", "unit": "deg", "tolerance": 0.01},
                {"name": "delta_cr_deg", "type": "float", "unit": "deg", "tolerance": 0.01},
                {"name": "tcr_s", "type": "float", "unit": "s", "tolerance": 0.002},
            ],
            "rule": "Arc smib_swing PSA engine on fixture case.json.",
        }
    if engine == "agc_two_area":
        return {
            "fields": [
                {"name": "primary_df1_Hz", "type": "float", "unit": "Hz"},
                {"name": "agc_ss_df1_Hz", "type": "float", "unit": "Hz"},
            ],
            "rule": "Arc agc_two_area simulate_two_area gold fields.",
        }
    if engine == "ed_lambda":
        return {
            "fields": [{"name": "cases", "type": "array"}, {"name": "lam", "type": "float"}],
            "rule": "Arc ed_lambda solve_lambda_ed for PD cases in expect.",
        }
    return {"fields": [], "rule": f"Engine {engine} per expect.json."}


def _eval_variants(item_dir: Path, expect: dict[str, Any], pack: str) -> list[dict[str, Any]]:
    """Seeded variants for eval gold (2 per item)."""
    base_id = item_dir.name
    variants: list[dict[str, Any]] = []
    for v in range(2):
        seed = 100 + v * 17 + int(hashlib.sha256(base_id.encode()).hexdigest()[:6], 16) % 50
        fixtures = _fixtures(item_dir)
        givens = {**fixtures}
        if pack == "control" and "problem.json" in fixtures:
            prob = dict(fixtures["problem.json"])
            if prob.get("num"):
                prob["num"] = [float(prob["num"][0]) * (1.0 + 0.01 * v)]
            givens = {"problem.json": prob}
        variants.append(
            {
                "suffix": f"v{v}",
                "seed": seed,
                "givens": givens,
                "item_dir": item_dir,
                "expect": expect,
                "pack": pack,
            }
        )
    return variants


def _question_record_eval(
    *,
    task_id: str,
    pack: str,
    item_dir: Path,
    expect: dict[str, Any],
    givens: dict[str, Any],
    seed: int,
) -> dict[str, Any]:
    fixtures = _fixtures(item_dir)
    merged_givens = {**fixtures, **givens}
    is_engine = bool(expect.get("engine"))
    question = _recipe_question(item_dir, expect, merged_givens)
    if is_engine:
        question = f"{question}\n\nUse Arc PSA engine {expect['engine']} (fixture case.json)."
    schema = _answer_schema_engine(expect) if is_engine else _answer_schema_recipe(expect)
    return {
        "id": task_id,
        "domain": pack,
        "seed": seed,
        "question": question,
        "givens": merged_givens,
        "answer_schema": schema,
        "grading_rule": schema["rule"],
        "expect_mode": "engine" if is_engine else "recipe",
        "recipe_id": expect.get("recipe_id"),
        "engine": expect.get("engine"),
        "source_note": "eval/gold license-clean; no repo paths required to attempt.",
    }


def _oracle_eval(question: dict[str, Any], item_dir: Path, expect: dict[str, Any]) -> dict[str, Any]:
    if expect.get("engine"):
        row = run_psa_item(item_dir, expect)
        return dict(row.get("summary") or {})
    row = run_item(item_dir, run_root=ROOT / "runs" / "_benchmark_build")
    summ = row.get("summary") or {}
    if "value" in summ:
        return {"value": summ["value"]}
    return summ


def _trap_variants() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for trap_id in trap_problems.list_trap_ids():
        for v in range(5):
            seed = 200 + int(trap_id[1:]) * 10 + v
            givens = trap_problems.sample_trap_givens(trap_id, seed)
            obs = trap_problems.build_observation(trap_id, seed)
            rows.append(
                {
                    "id": f"trap/{trap_id}-s{seed}",
                    "domain": "trap",
                    "seed": seed,
                    "question": obs["question"],
                    "givens": givens,
                    "givens_units": obs.get("givens_units", {}),
                    "answer_schema": obs["answer_schema"],
                    "grading_rule": obs["answer_schema"]["rule"],
                    "trap_id": trap_id,
                }
            )
    return rows


def build_task_catalog() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Returns (public_questions, answer_key_by_id)."""
    questions: list[dict[str, Any]] = []
    answers: dict[str, dict[str, Any]] = {}

    for pack in ("power", "control"):
        pack_dir = ROOT / "eval" / "gold" / pack
        for item_dir in sorted(pack_dir.iterdir()):
            if not item_dir.is_dir() or not (item_dir / "expect.json").is_file():
                continue
            expect = json.loads((item_dir / "expect.json").read_text())
            for var in _eval_variants(item_dir, expect, pack):
                task_id = f"{pack}/{item_dir.name}-{var['suffix']}"
                q = _question_record_eval(
                    task_id=task_id,
                    pack=pack,
                    item_dir=item_dir,
                    expect=expect,
                    givens=var["givens"],
                    seed=var["seed"],
                )
                questions.append(q)
                ref = _oracle_eval(q, item_dir, expect)
                answers[task_id] = {
                    "reference": ref,
                    "grading": {
                        "tol": expect.get("tol", expect.get("tolerance_deg", 1e-3)),
                        "engine": expect.get("engine"),
                        "recipe_id": expect.get("recipe_id"),
                    },
                }

    for item_dir in iter_circuit_gold_dirs():
        expect = json.loads((item_dir / "expect.json").read_text())
        for v in range(2):
            seed = 300 + int(hashlib.sha256(item_dir.name.encode()).hexdigest()[:4], 16) % 20 + v
            task_id = f"circuits/{item_dir.name}-v{v}"
            fixtures = _fixtures(item_dir)
            q = _question_record_eval(
                task_id=task_id,
                pack="circuits",
                item_dir=item_dir,
                expect=expect,
                givens=fixtures,
                seed=seed,
            )
            questions.append(q)
            ref = _oracle_eval(q, item_dir, expect)
            answers[task_id] = {
                "reference": ref,
                "grading": {"tol": expect.get("tol", 1e-6), "recipe_id": expect.get("recipe_id")},
            }

    for row in _trap_variants():
        tid = row.pop("trap_id")
        qid = row["id"]
        questions.append(row)
        givens = row["givens"]
        answers[qid] = {
            "reference": oracle_submission(tid, givens),
            "grading": {"trap_id": tid, "givens": givens},
            "naive": naive_submission(tid, givens),
        }

    return questions, answers

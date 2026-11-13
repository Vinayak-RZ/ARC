"""Build public questions and private answer keys for v0.1 (60+ unique tasks)."""

from __future__ import annotations

import copy
import hashlib
import json
import random
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from electrical_engineer.benchmark_v01.givens_units import givens_units_map
from electrical_engineer.benchmark_v01.oracle_givens import oracle_eval, oracle_trap
from electrical_engineer.benchmark_v01.public_schema import public_answer_schema
from electrical_engineer.benchmark_v01.question_copy import eval_question
from electrical_engineer.benchmark_v01.sanitize import (
    flatten_public_givens,
    grading_hints_from_fixtures,
    strip_grader_fields,
)
from electrical_engineer.rlvr_env import problems as trap_problems
from electrical_engineer.rlvr_env.schema import TRAP_ANSWER_SCHEMAS, TRAP_VERIFIER_NOTES

ROOT = Path(__file__).resolve().parents[3]

DEFAULT_SMIB = {
    "h_mj_mva": 5.0,
    "f0_hz": 50.0,
    "pm_pu": 0.9,
    "pmax_pre_pu": 2.0,
    "pmax_fault_pu": 0.5,
    "pmax_post_pu": 1.5,
}


def iter_circuit_gold_dirs(circuits_root: Path | None = None) -> Iterator[Path]:
    root = circuits_root or ROOT / "eval" / "gold" / "circuits"
    if not root.is_dir():
        return
    for item in sorted(root.iterdir()):
        if item.is_dir() and (item / "expect.json").is_file():
            yield item


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


def _read_task_md(item_dir: Path) -> str:
    path = item_dir / "task.md"
    return path.read_text(encoding="utf-8").strip() if path.is_file() else ""


def _perturb_givens(g: dict[str, Any], seed: int) -> dict[str, Any]:
    out = copy.deepcopy(g)
    rng = random.Random(seed)

    def bump(key: str, scale: float = 0.01) -> None:
        if key in out and isinstance(out[key], (int, float)):
            out[key] = float(out[key]) * (1.0 + scale * (1 + seed % 5))

    for key in ("v", "r", "c", "l", "t", "vc0", "i0", "vin", "r1", "r2", "pm_pu", "dpl1_pu", "PD_MW"):
        bump(key, 0.01 * (1 + seed % 3))
    if isinstance(out.get("num"), list) and out["num"]:
        out["num"] = [float(out["num"][0]) * (1.0 + 0.02 * (seed % 7))]
    units = out.get("units")
    if isinstance(units, list) and units and isinstance(units[0], dict) and seed % 2:
        out["units"][0]["b"] = float(units[0]["b"]) + rng.random() * 0.01
    return out


def _engine_public_givens(item_name: str, expect: dict[str, Any]) -> dict[str, Any]:
    if expect.get("engine") == "smib_swing":
        fixtures = _fixtures(ROOT / "eval" / "gold" / "power" / item_name)
        case = fixtures.get("case.json") or DEFAULT_SMIB
        return strip_grader_fields(case)
    if expect.get("engine") == "agc_two_area":
        g = trap_problems.sample_trap_givens("T4", 0)
        g["K_agc"] = 0.3
        g["agc_t_end_s"] = 60.0
        return strip_grader_fields(g)
    if expect.get("engine") == "ed_lambda":
        g = trap_problems.sample_trap_givens("T6", 0)
        cases = expect.get("cases") or []
        g["PD_cases_MW"] = [float(str(c).removeprefix("PD_")) for c in cases]
        return strip_grader_fields(g)
    return {}


def _difficulty_tier(domain: str, item_name: str) -> str:
    if domain == "trap":
        return "hard"
    if domain == "circuits":
        if item_name in {"divider-dc-01"}:
            return "easy"
        if item_name in {"rl-step-01", "rlc-natural-01"}:
            return "medium"
        return "medium"
    if item_name.endswith("eec301-01") or "penalty" in item_name:
        return "hard"
    if domain == "control" and item_name in {"margin-40-01", "block-feedback-01", "digital-pole-01"}:
        return "medium"
    if domain == "power" and item_name.startswith(("lg-", "ll", "pu-base")):
        return "medium"
    return "medium"


def _public_schema(expect: dict[str, Any]) -> dict[str, Any]:
    if expect.get("engine") == "smib_swing":
        return public_answer_schema(
            [
                {"name": "delta0_deg", "type": "float", "unit": "deg", "tolerance": 0.02},
                {"name": "delta_cr_deg", "type": "float", "unit": "deg", "tolerance": 0.05},
                {"name": "tcr_s", "type": "float", "unit": "s", "tolerance": 0.002},
                {"name": "t_to_delta_cr_s", "type": "float", "unit": "s", "tolerance": 0.002},
            ]
        )
    if expect.get("engine") == "agc_two_area":
        return public_answer_schema(
            [
                {"name": "primary_df1_Hz", "type": "float", "unit": "Hz", "tolerance": 0.002},
                {"name": "primary_P12_MW", "type": "float", "unit": "MW", "tolerance": 0.5},
                {"name": "agc_ss_df1_Hz", "type": "float", "unit": "Hz", "tolerance": 0.002},
                {"name": "agc_ss_P12_MW", "type": "float", "unit": "MW", "tolerance": 0.05},
            ]
        )
    if expect.get("engine") == "ed_lambda":
        return public_answer_schema(
            [
                {"name": "lam", "type": "float", "unit": "Rs/MWh", "tolerance": 0.05},
                {"name": "cases", "type": "array"},
            ]
        )
    tol = float(expect.get("tol", 1e-6))
    return public_answer_schema([{"name": "value", "type": "float", "tolerance": tol, "unit": "1"}])


def _dedupe_tasks(questions: list[dict[str, Any]], answers: dict[str, dict[str, Any]]) -> tuple:
    seen: set[str] = set()
    q_out: list[dict[str, Any]] = []
    a_out: dict[str, dict[str, Any]] = {}
    for q in questions:
        fp = hashlib.sha256(
            json.dumps({"question": q["question"], "givens": q["givens"]}, sort_keys=True).encode()
        ).hexdigest()
        if fp in seen:
            continue
        seen.add(fp)
        q_out.append(q)
        a_out[q["id"]] = answers[q["id"]]
    return q_out, a_out, len(seen)


def build_task_catalog() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, int]]:
    questions: list[dict[str, Any]] = []
    answers: dict[str, dict[str, Any]] = {}

    for pack in ("power", "control"):
        pack_dir = ROOT / "eval" / "gold" / pack
        for item_dir in sorted(pack_dir.iterdir()):
            if not item_dir.is_dir() or not (item_dir / "expect.json").is_file():
                continue
            expect = json.loads((item_dir / "expect.json").read_text())
            fixtures = _fixtures(item_dir)
            grading = grading_hints_from_fixtures(fixtures, expect)
            base_name = item_dir.name
            for v in range(2):
                seed = 100 + v * 31 + int(hashlib.sha256(base_name.encode()).hexdigest()[:6], 16) % 50
                if expect.get("engine"):
                    givens = _engine_public_givens(base_name, expect)
                else:
                    givens = flatten_public_givens(fixtures)
                if base_name == "divider-dc-01" and "vin" in givens:
                    givens = {
                        "vin_V": float(givens.get("vin", 10)),
                        "r1_ohm": float(givens.get("r1", 1000)),
                        "r2_ohm": float(givens.get("r2", 1000)),
                        "kind": givens.get("kind", "voltage_divider"),
                    }
                givens = _perturb_givens(givens, seed)
                task_id = f"{pack}/{base_name}-s{seed}"
                schema = _public_schema(expect)
                qtext = eval_question(base_name, pack, givens, task_md=_read_task_md(item_dir))
                public = {
                    "id": task_id,
                    "domain": pack,
                    "difficulty_tier": _difficulty_tier(pack, base_name),
                    "seed": seed,
                    "question": qtext,
                    "givens": givens,
                    "givens_units": givens_units_map(givens),
                    "answer_schema": schema,
                }
                questions.append(public)
                ref = oracle_eval(givens, grading)
                grading_pub = {**grading, "public_givens": givens}
                answers[task_id] = {"reference": ref, "grading": grading_pub}

    for item_dir in iter_circuit_gold_dirs():
        expect = json.loads((item_dir / "expect.json").read_text())
        fixtures = _fixtures(item_dir)
        grading = grading_hints_from_fixtures(fixtures, expect)
        base_name = item_dir.name
        for v in range(2):
            seed = 400 + int(hashlib.sha256(base_name.encode()).hexdigest()[:4], 16) % 30 + v * 11
            givens = flatten_public_givens(fixtures)
            if base_name == "divider-dc-01" and "vin" in givens:
                givens = {
                    "vin_V": float(givens.get("vin", 10)),
                    "r1_ohm": float(givens.get("r1", 1000)),
                    "r2_ohm": float(givens.get("r2", 1000)),
                }
            givens = _perturb_givens(givens, seed)
            task_id = f"circuits/{base_name}-s{seed}"
            schema = _public_schema(expect)
            public = {
                "id": task_id,
                "domain": "circuits",
                "difficulty_tier": _difficulty_tier("circuits", base_name),
                "seed": seed,
                "question": eval_question(base_name, "circuits", givens, task_md=_read_task_md(item_dir)),
                "givens": givens,
                "givens_units": givens_units_map(givens),
                "answer_schema": schema,
            }
            questions.append(public)
            ref = oracle_eval(givens, grading)
            grading_pub = {**grading, "public_givens": givens}
            answers[task_id] = {"reference": ref, "grading": grading_pub}

    from electrical_engineer.rlvr_env.rewards import naive_submission

    for trap_id in trap_problems.list_trap_ids():
        for v in range(5):
            seed = 200 + int(trap_id[1:]) * 17 + v
            givens = strip_grader_fields(trap_problems.sample_trap_givens(trap_id, seed))
            task_id = f"trap/{trap_id}-s{seed}"
            schema = TRAP_ANSWER_SCHEMAS[trap_id]
            obs = trap_problems.build_observation(trap_id, seed)
            public = {
                "id": task_id,
                "domain": "trap",
                "difficulty_tier": "hard",
                "seed": seed,
                "question": obs["question"],
                "givens": givens,
                "givens_units": obs.get("givens_units", {}),
                "answer_schema": schema,
            }
            questions.append(public)
            answers[task_id] = {
                "reference": oracle_trap(trap_id, givens),
                "grading": {
                    "trap_id": trap_id,
                    "givens": givens,
                    "verifier_note": TRAP_VERIFIER_NOTES[trap_id],
                },
                "naive": naive_submission(trap_id, givens),
            }

    questions, answers, unique = _dedupe_tasks(questions, answers)
    by_domain: dict[str, int] = {}
    by_tier: dict[str, int] = {}
    for q in questions:
        by_domain[q["domain"]] = by_domain.get(q["domain"], 0) + 1
        tier = q.get("difficulty_tier", "medium")
        by_tier[tier] = by_tier.get(tier, 0) + 1
    meta = {"unique_question_givens": unique, "by_domain": by_domain, "difficulty_tiers": by_tier}
    return questions, answers, meta

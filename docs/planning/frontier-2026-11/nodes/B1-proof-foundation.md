# Node plan: B1: proof foundation fix

| Field | Value |
|-------|-------|
| **Node id** | `B1` |
| **Job** | Fix eval runner schema so `electrical-engineer eval` and `--pack power` complete |
| **Wave** | 2 |
| **Depends on (data)** | `doc_truth_manifest` |
| **Write paths** | `src/electrical_engineer/eval_runner/**`, `eval/gold/power/**`, `tests/integration/test_eval_*` |
| **Model** | inherit |

## Objective

Product CLI proves what CI proves for PSA (audit #04 KeyError on `recipe_id`).

## Contract

**Output:** `{ "eval_schema_v2": "...", "all_packs_pass": true, "trap_suite_index": "artifacts/..." }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 4-6 | schema v2, KeyError fix, regression test | `electrical-engineer eval` exit 0 |

## Kill criteria

If schema unfixable without owner decision on gold format, escalate to Gate 0 addendum.

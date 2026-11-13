# Node plan: T1: trials pass^k

| Field | Value |
|-------|-------|
| **Node id** | `T1` |
| **Job** | Run multiple trials (happy, empty prompt, wrong pack, regression) on AB harness |
| **Wave** | 8 |
| **Depends on (data)** | R1 smoke |
| **Write paths** | `artifacts/frontier-ab/trials/**` |
| **Model** | inherit |

## Objective

pass^k thresholds from §16 met or documented miss.

## Contract

**Output:** `{ "proof_artifacts_bundle": "artifacts/...", "pass_k_met": true }`

## Commits

Coalesce with R1/D1 per budget.

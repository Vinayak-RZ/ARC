# Node plan: B6: LIVE host A/B harness

| Field | Value |
|-------|-------|
| **Node id** | `B6` |
| **Job** | Runnable driver for same prompts on bare host vs Arc attach; store transcripts |
| **Wave** | 4 |
| **Depends on (data)** | `trap_suite_index`, `ab_host_models` from Gate 0 |
| **Write paths** | `scripts/frontier_ab/**`, `artifacts/frontier-ab/**`, `proofs/**` |
| **Model** | inherit |

## Objective

Replace scripted-only bare baseline with LIVE evidence (audit #04, report #03 Harvey pattern).

## Contract

**Output:** `{ "live_ab_results": { "models": [], "pass_k": {}, "held_out_count": 8 } }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 27-29 | CLI runner, held-out prompts, pass^k stats | dry run + sample JSON |

## Human checkpoint

API budget cap per Gate 0 T2.

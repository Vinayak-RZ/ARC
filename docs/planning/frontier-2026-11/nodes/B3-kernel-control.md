# Node plan: B3: kernel control depth

| Field | Value |
|-------|-------|
| **Node id** | `B3` |
| **Job** | ControlEval adapter + ControlBench subset with python-control verifier |
| **Wave** | 3 |
| **Depends on (data)** | `capability_delta_spec` |
| **Write paths** | `src/electrical_engineer/engines/control_*`, `scripts/benchmarks/control_*`, `eval/gold/control/**`, `artifacts/benchmarks/` |
| **Model** | inherit |

## Objective

Close frequency-domain gap (report #02 ControlBench 33% design bare) toward **≥70%** tool-augmented target.

## Contract

**Output:** `{ "controleval_asr": 0.9, "controlbench_subset_acc": 0.7 }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 11-14 | harness, golds, bode verifier, docs | subset scripts exit 0 |

## Kill criteria

ASR < 85% at week 6 → descope to PSA-only frontier claim.

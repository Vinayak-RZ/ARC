# Node plan: D1: scorecard and execution proof

| Field | Value |
|-------|-------|
| **Node id** | `D1` |
| **Job** | Publish SCORECARD, PROGRESS cutover, execution evidence paths (not final README) |
| **Wave** | 9 |
| **Depends on (data)** | `proof_artifacts_bundle` from T1; B10 benchmark tarball |
| **Write paths** | `artifacts/benchmarks/SCORECARD.md`, `docs/planning/frontier-2026-11/PROGRESS.md` |
| **Model** | inherit |

## Objective

Internal and PR proof artifacts are frozen with numbers. **Final user-facing README lives in D2.**

## Contract

**Output:** `{ "scorecard_published": true, "progress_complete": true }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 1 | `docs(bench): SCORECARD actuals and PROGRESS complete` | validate_frontier.sh |

# Node plan: B10: public benchmark release

| Field | Value |
|-------|-------|
| **Node id** | `B10` |
| **Job** | Publish `eee-coursework-trap v0.1` + SCORECARD with actuals vs targets |
| **Wave** | 6 |
| **Depends on (data)** | `live_ab_results`, `rlvr_env_manifest`, benchmark runners |
| **Write paths** | `artifacts/benchmarks/**`, `docs/**` |
| **Model** | inherit |

## Objective

Public standard for "bare agent fails EE coursework" (report #02 white space #10).

## Contract

**Output:** `{ "tarball_sha256": "...", "scorecard_rows": [] }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 34-35 | release + SCORECARD | checksum + review |

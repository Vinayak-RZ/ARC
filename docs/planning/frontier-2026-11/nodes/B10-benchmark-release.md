# Node plan: B10: public benchmark release

| Field | Value |
|-------|-------|
| **Node id** | `B10` |
| **Job** | Publish `eee-coursework-trap v0.1` + SCORECARD with actuals vs targets |
| **Wave** | 6 |
| **Depends on (data)** | `live_ab_results`, `rlvr_env_manifest`, `benchmark_figure_bundle` from B11, benchmark runners |
| **Write paths** | `artifacts/benchmarks/**`, `docs/**` |
| **Model** | inherit |

## Objective

Public standard for "bare agent fails EE coursework" (report #02 white space #10).

## Contract

**Output:** `{ "tarball_sha256": "...", "scorecard_rows": [] }`

Produce via:

```bash
uv run python scripts/build_benchmark_v01.py
uv run python scripts/benchmark_scorecard.py
uv run python scripts/grade_benchmark_v01.py
```

Artifacts under `artifacts/benchmarks/eee-coursework-trap/v0.1/` (no GitHub release; PR attachment only).

## Commits

| # | Commit | Gate |
|---|--------|------|
| 34-35 | release + SCORECARD | checksum + `grade_benchmark_v01.py` |

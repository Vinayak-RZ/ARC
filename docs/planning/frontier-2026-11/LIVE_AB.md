# LIVE host A/B harness (B6)

## Held-out sheets (13 Nov 2026)

| Run | Submission | Score | Notes |
|-----|------------|-------|-------|
| First Arc-driven | Y (`artifacts/.../arc/answers.json`) | **21/25** (0.84) | Lost to bare agent X **24/25**; P5 margin crossover swap + GM linear-as-dB; P8 slip/torque gaps |
| Engine + CLI rerun | `artifacts/frontier-ab/live-run-2026-11-13/arc-rerun/` | **25/25** | After margin, IM EC, ED table, primary f0, complex Z, RLC analytic fixes |

Grading authority: `artifacts/frontier-ab/live-run-2026-11-13/grading/REFERENCE.json`  
Blind scores: `grading/SCORES.json` (X vs first Y). Rerun: `arc-rerun/SCORES.json`.

```bash
uv run python scripts/rerun_arc_live_sheets.py
uv run python scripts/grade_frontier_ab.py
```

## Automated LIVE harness (API keys)

```bash
uv run python scripts/run_live_ab.py
```

### Required environment variables

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | GPT-5 host path |
| `ANTHROPIC_API_KEY` | Claude Sonnet host path |
| `CURSOR_API_KEY` | Optional Composer API if exposed |

Optional:

| Variable | Default | Purpose |
|----------|---------|---------|
| `FRONTIER_AB_BUDGET_USD` | `50` | Nightly spend cap |
| `FRONTIER_AB_HELD_OUT` | `8` | Held-out sheet count |

Output: `artifacts/frontier-ab/live_ab_status.json` (status `blocked` until keys present).

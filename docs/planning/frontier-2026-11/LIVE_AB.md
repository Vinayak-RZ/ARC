# LIVE host A/B harness (B6)

Run (blocked without keys):

```bash
uv run python scripts/run_live_ab.py
```

## Required environment variables

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

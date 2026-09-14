# R1 boot — Kernel harden

**Date:** 2026-09-14  
**Branch:** `cursor/ee-kernel-harden-trace-8db3`

## Commands

```bash
uv run electrical-engineer --help
uv run python scripts/kernel_harden/trial_driver.py scripts/kernel_harden/scenarios/unmatched/unmatched-unmatched-cosolver-00-0107.json
./scripts/validate.sh
```

## Results

| Check | Exit | Notes |
|-------|------|-------|
| `electrical-engineer --help` | 0 | CLI boots |
| trial_driver smoke | 0 | wrote `trace.jsonl` + index row |
| `./scripts/validate.sh` | 0 | 165 pytest + gold packs; bind grep OK |

## Artifacts

- Sample run under `artifacts/kernel-harden/raw/runs/<id>/`
- `observation.json` and `trace.jsonl` present on smoke run
- UI: `/api/runs/{id}` returns `observation_excerpt` + `trace_excerpt`

## Observation

Host-path trial driver is the Wave 3 corpus entrypoint. Exact token `unchecked` preserved on unmatched recipe.

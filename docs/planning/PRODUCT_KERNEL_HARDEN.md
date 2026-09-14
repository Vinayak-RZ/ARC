# Product overlay — Kernel harden graph

Extends [`docs/PRODUCT.md`](../PRODUCT.md). Does not replace the base user/job.

## User

Dual: (1) kernel owner/designer; (2) UG EE student (same as PRODUCT.md).

## Job

Make Arc’s domain kernel measurably more deterministic and honest under host-heavy UG EE load, with durable JSONL traces, patched failure classes, UI visibility, and a publishable domain-kernel case study.

## Done looks like

- Every execute path used by trials writes `runs/<id>/trace.jsonl`
- `artifacts/kernel-harden/CORPUS_INDEX.md` lists ≥100 host-mediated runs with `trace_path`
- `docs/planning/FAILURE_REPORT_KERNEL_HARDEN.md` links failure classes to `run_id`s
- Architecture critique before/after with corpus evidence
- Localhost UI shows human-readable observation + trace excerpt (not raw dump only)
- Unagent + Improveness reports under `artifacts/kernel-harden/`
- Case study + integration docs + `LEARNING.md`
- `./scripts/validate.sh` green

## P0 (this graph)

- Wave 0: extensive loop plans + plan-harden check (no `src/` product edits)
- Stdlib JSONL tracing in runner `wrap()` + run bookends
- ≥100 host-heavy trials (target 120–150); held-out id file
- Failure taxonomy + ≥1 improve cycle with gold locks
- UI trace surface
- Validate green

## P1 (same execution, later waves)

- Unagent custom export + recommend report
- Improveness tooling notes applied
- Second improve cycle + held-out retest
- Hardening wave (bind / secrets / held-out integrity)
- Docs-out: case study, integrations, PRODUCT/README/PROGRESS sync

## Non-goals

- H5 owned multi-turn agent loop
- OTel / Langfuse / SaaS telemetry
- Training models
- Full curriculum gold completeness (gold only for regression locks)
- Deep Coinbase visual redesign
- Product code in Wave 0

## Honest holes

- Host-heavy trials are scripted MCP/CLI paths scored on evidentiary honesty, not viva eloquence
- If Unagent/Improveness clone fails, offline substitute reports with an honest limitation section
- Raw corpus stays gitignored; index + samples committed

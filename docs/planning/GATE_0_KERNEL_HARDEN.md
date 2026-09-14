# Gate 0 — Kernel harden (JSONL trace + host-heavy corpus)

**Status:** locked 2026-09-14  
**Graph:** kernel-harden (live `LOOP_GRAPH.md`)  
**Branch:** `cursor/ee-kernel-harden-trace-8db3`

## Users (dual)

1. Arc kernel owner / designer shipping a world-facing domain-kernel case study.
2. UG EE end-user who hires Arc for checked coursework.

## Job

Add kernel tracing → run ≥100–150 diverse host-mediated UG EE cases → mine failures with Unagent + Improveness → add only minimal gates/structure where agents fail → ship patched kernel + failure corpus + design learnings.

## Done looks like

- Failure report linked to persistent trace corpus
- Patched kernel
- Full-architecture critique (before/after)
- Unagent + Improveness integration docs as case study
- Localhost UI surfaces traces
- `LEARNING.md` + PRODUCT / README / PROGRESS sync

## Non-goals

- H5 owned agent loop
- Weight training
- Public Terminal-Bench as fitness
- OTel / Langfuse SDK in Arc runtime
- Secrets in git
- MATLAB-as-required
- Rewriting Cursor / Claude hosts
- Inventing out-of-curriculum packs

## P0 vs P1 (one continuous execution)

| Tier | Scope |
|------|--------|
| **P0** | Extensive plans on disk → JSONL tracing → ≥100 host runs → failure taxonomy → ≥1 improve cycle → UI trace surface → validate |
| **P1** | Unagent recommend; Improveness tooling; second improve cycle; held-out retest; case-study docs; UI polish depth; hardening; docs-out sync |

## Success check

Written critique of current whole architecture + failure points + how patches closed them, with corpus evidence paths.

## Technical locks

| Topic | Decision |
|-------|----------|
| Repo | Extend Arc; clone Unagent / Improveness as sibling tools |
| Tracing | Stdlib append-only `trace.jsonl` (+ keep `observation.json`). No OpenTelemetry |
| Export | Mapper → Unagent **custom** adapter |
| Persist | `runs/<id>/` + `artifacts/kernel-harden/` (raw gitignored) |
| Secrets | Env only |
| UI | Surface traces; polish under DESIGN-coinbase; bind `127.0.0.1` |
| Target | Local cloud-agent VM |
| Commits | Budget **40** (cap 42) |
| Trials | Option C host-heavy (lead + cloud as host) |
| PRIORITY | QUALITY > CONSISTENCY > SPEED > AVAILABILITY > COST |
| Improveness | Option B — run tooling; adapt frozen-physics / held-in/out |
| Cloud subagents | ON |
| Inner critique | `T_HOST`, `C_AUDIT`, `I1`, `I2` (max_rounds 3–4) |
| Wave 0 | **Plans only** — no product code until plan-harden passes |

## Exact token

`unchecked` — never paraphrase.

# Case study — Designing an undergraduate EE domain kernel (Arc)

## What we built

Arc is a **domain kernel**, not an agent harness. Hosts (Cursor / Claude / Codex) own the loop; Arc owns capabilities, providers, YAML recipes, gates, `unchecked`, run artifacts, and now **stdlib JSONL traces**.

This graph added:

1. Durable `trace.jsonl` per run (no OpenTelemetry)
2. A 120-run host-mediated UG EE corpus
3. Failure mining with **Unagent** + **Improveness** principles
4. Minimal structural fixes where agents/obs lied
5. Localhost UI excerpts for observation + trace
6. Harden + docs-out for a publishable case study

## Design principles that held

| Principle | Practice in Arc |
|-----------|-----------------|
| Minimal hardness | Structure only where corpus proved a lie or hole |
| Host owns the loop (H3) | No Python multi-turn agent; MCP/CLI only |
| Exact `unchecked` | Never euphemize; extend reasons carefully (`labeled`) |
| Frozen physics | Gold scorer untouched; observation enum ADR’d |
| Evidence on disk | Runs + corpus index + advisor reports |
| Advisors don’t auto-apply | Unagent ABSTAIN; humans/I1–I2 patch |

## Failure → structure

**Before:** `_unchecked_reason` fell through to `unmatched`, so explain/pack runs looked like router misses.

**After:** `labeled` for honest label-unverified paths; `unmatched` only for unmatched recipes. Locked by unit tests + retest table.

Unagent recommended **no FlipToDet** on SPICE/check/label nodes — confirmation that the kernel is already tool-shaped.

## How to design domain kernels (takeaways)

1. **Instrument before you harden** — JSONL spans beat guesswork.
2. **Run many cheap host trials** — 100+ beats golden anecdotes.
3. **Taxonomy before patches** — F1–F5 with run_ids.
4. **Prefer honest labels over fake success**.
5. **Import advisor tools as offline critics**, not as a second loop.
6. **UI shows reasons humans can audit** without downloading JSONL.

## Boot

```bash
uv sync --extra dev
./scripts/validate.sh
uv run electrical-engineer run solve-circuit-problem
# inspect runs/<id>/trace.jsonl and observation.json
```

## Corpus

See `artifacts/kernel-harden/CORPUS_INDEX.md` (120 completed with traces).

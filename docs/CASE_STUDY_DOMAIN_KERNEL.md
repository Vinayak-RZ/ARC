# Case study — Designing an undergraduate EE domain kernel (Arc)

## What we built

Arc is a **domain kernel**, not an agent harness. Hosts (Cursor / Claude / Codex) own the loop; Arc owns capabilities, providers, YAML recipes, gates, `unchecked`, run artifacts, **local RAG ingest/index/retrieve**, and now **stdlib JSONL traces**.

This graph added:

1. Durable `trace.jsonl` per run (no OpenTelemetry)
2. A 120-run host-mediated UG EE corpus
3. Failure mining with **Unagent** + **Improveness** principles
4. Minimal structural fixes where agents/obs lied
5. Localhost UI excerpts for observation + trace
6. Harden + docs-out for a publishable case study

## Kernel RAG (Layer 2, not Layer 0)

The host may call `retrieve`. The kernel **is** the RAG system:

| Kernel does | Kernel does not |
|-------------|-----------------|
| `rag add`: gate, OCR/extract, figure link, graph write, inventory | Compact the host context window |
| `retrieve-citation`: filters, hybrid BM25+dense, 1–2 hops, pack 3 × 1500 chars | Run GRASP agent sub-agents or GraphRAG global map-reduce |
| Persist the index on the student machine | Treat a BYO PDF as a new capability or a checked ohm |

Ingest vs query graphs: [`architecture/rag.md`](architecture/rag.md). Freeze: [`ARCHITECTURE.md`](ARCHITECTURE.md) §10 and §2.5 hook 1. Harness split: [`ON_THE_HARNESS.md`](ON_THE_HARNESS.md). Approach notes: [`../research/notes/rag-ingest-query-architecture.md`](../research/notes/rag-ingest-query-architecture.md).

As-built extract/chunk/graph is `hybrid-graph`; commercial-scan layout fidelity remains `CD-RAG-PARSE` (optional MinerU adapter). That remaining hole is parse depth, not a harness hole.

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

**After I1:** `labeled` for honest label-unverified paths; `unmatched` only for unmatched recipes.

**After I3 (self-audit):** `labeled` is residual. A missing tool is `no-provider` even when the recipe names the provider id directly; an unconfirmed draft is `gate-closed`; a node that never reports `ok` is not a tool crash. The 120-run corpus is now graded (120/120 PASS on this machine).

Unagent recommended **no FlipToDet** on SPICE/check/label nodes — confirmation that the kernel is already tool-shaped. The first advisor export overstated failure_rate because `bool(None)` made label/explain nodes look crashed; I3 closed that.

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

See `artifacts/kernel-harden/CORPUS_INDEX.md` (120 completed with traces, graded). Audit of the canes: [`docs/planning/AUDIT_KERNEL_HARDEN.md`](planning/AUDIT_KERNEL_HARDEN.md).

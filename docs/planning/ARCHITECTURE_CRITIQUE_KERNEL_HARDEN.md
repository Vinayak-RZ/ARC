# Architecture critique — Kernel harden (from corpus)

**Corpus:** `artifacts/kernel-harden/CORPUS_INDEX.jsonl` (120/120 traces)  
**Date:** 2026-09-14

## Before (as-built)

Arc’s domain kernel already had capability binding, YAML recipes, `observation.json`, MCP/CLI, and fail-closed `unchecked`. Observability stopped at a single observation blob: no span stream, no cross-run index, UI dumped raw JSON. `_unchecked_reason` fell through to **`unmatched`** whenever a run was unchecked without a more specific detector — so explain/pack recipes that honestly labeled unverified work were mis-tagged as router misses.

## Failure classes (with run evidence)

| Class | Signal | Example scenario / run | Count (approx) |
|-------|--------|------------------------|----------------|
| F1 Mislabel reason | `unchecked=true` but reason=`unmatched` though `recipe_id` lacks `unmatched` | `explain-*`, `derive-circuit`, many packs | ~96 |
| F2 No provider | `unchecked_reason=no-provider` | `simulate-circuit` variants | 6 |
| F3 Gate closed | `gate-closed` | `simulate-after-confirm` | 8 |
| F4 Healthy check | `unchecked=false` | `solve-circuit-problem` + voltage_divider problem | 10 |
| F5 Intentional unmatched | recipe `unmatched-cosolver` | unmatched pack | 8 |

## After (this graph so far)

- Every execute writes `trace.jsonl` (run/node spans).
- Host corpus of 120 runs with index.
- UI shows observation excerpt + trace list.
- **I1 target:** stop lying with `unmatched` fallback; emit honest `labeled` when the label-unverified path produced unchecked without provider/gate/retrieve failure; extend ARCHITECTURE enum.

## Residual risks

- Scenario problem payloads remain thin for non-circuits packs (many still unchecked — sometimes correctly).
- Raw corpus gitignored; only index + samples committed.
- Unagent/Improveness offline if clone fails.

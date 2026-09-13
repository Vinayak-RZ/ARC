# PHASE 3 COMPLETE — U1 + B_KERNEL + B_RAG + B_HOST

## Completed work

Two-band UI IA, capability bind + observation/FR9, BYO RAG extract/chunk/index, host docs name live ACI verbs.

## Files modified

`docs/ui-ia.md`, `src/electrical_engineer/capabilities.py`, compose/runner/nodes/rag, `docs/hosts/**`, `hosts/adapters/README.md`, unit tests, `tests/fixtures/rag/`.

## Architectural changes

Capability ids bind providers or `CD-NO-PROVIDER`. `solve-explain` cannot mint checked. `evidentiary.json` aliases `summary.json`. RAG ingest writes chunks + index.

## Validation

U1 grep stop; `pytest` kernel four files; `test_rag_ingest`; `test_host_docs`. Related circuits/unmatched/rag filter tests green.

## Known issues

`render-figure` has no dedicated provider this pass (honest `CD-NO-PROVIDER`). MCP still two verbs until B_ACI.

## Next phase

Wave 4: B_ACI, B_WF, B_UI, B_PACKS.

## What you learned

- Coverage is a path (bind or `unchecked`), not gold depth.
- Argument-band numerics must stay unlabeled unless an algebraic-check provider recomputes them.
- Inventory-only RAG was a retrieve miss waiting to happen; chunk files are the index.
- Host docs must name the live verb list or ChatGPT desktop drifts from ACI.

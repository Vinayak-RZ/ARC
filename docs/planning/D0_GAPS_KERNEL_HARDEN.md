# D0 gaps — Kernel harden (docs-in)

Observed against as-built Arc before this graph's product waves.

## observation.json

- Writer: `src/electrical_engineer/runner/execute.py` emits `observation.json` with `run_id`, `capabilities`, `providers`, `nodes`, `unchecked_reason`, `retrieve`.
- Gaps: no per-node wall clock; no span stream; no cross-run corpus index; P1 `wall_ms` noted in ARCHITECTURE but unimplemented.

## trace

- No `trace.jsonl` today. Host/debug must reassemble from `nodes/*/out.json` + observation.
- Gap: Unagent-ingestible append-only span log missing (this graph's B_TRACE).

## gold

- Scored packs under `eval/gold/`: circuits, explain, injection, rag-retrieval, signals, unmatched (~6 expect.json items).
- Gap: thin depth vs curriculum; control pack empty; host-heavy scenarios not represented as gold locks yet.

## UI

- `ui/src/slots/root.jsx` + `ui_server/app.py`: observation shown as raw JSON string in a disclosure.
- Gaps: no human excerpt for `unchecked_reason` / capabilities; no `trace.jsonl` panel; unused IA slots for observation remain conceptual.

## export / advisors

- No Unagent custom adapter; no Improveness mapping scripts.
- Gap: B_EXPORT / X_* nodes.

## Host path

- MCP verbs + CLI exist; T1_HOST doc patterns exist.
- Gap: no scripted ≥100 host-trial driver or CORPUS_INDEX.

## Authority paths

- `docs/ARCHITECTURE.md`, `docs/PRODUCT.md`, `docs/CANNOT_DO.md` remain authority; this graph extends, does not invent capability ids.

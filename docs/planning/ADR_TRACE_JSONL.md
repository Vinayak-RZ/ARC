# ADR — Stdlib JSONL trace (no OpenTelemetry)

**Status:** Accepted 2026-09-14  
**Context:** Kernel-harden graph needs durable, Unagent-ingestible traces without heavy APM.

## Decision

1. Emit append-only `runs/<id>/trace.jsonl` from `electrical_engineer.runner` using the Python standard library only (`json`, `time`, `pathlib`).
2. Keep existing `observation.json` / `evidentiary.json` / `summary.json` writers unchanged in contract (gold still scores evidentiary only).
3. **Do not** add OpenTelemetry, Langfuse, LangSmith, or similar runtime dependencies.
4. Export to Unagent via a **custom** adapter that maps JSONL spans → Unagent Trace/Span models (or Unagent’s documented custom load path). No OTLP SDK in Arc.
5. Held-out scenario ids live in `artifacts/kernel-harden/HELD_OUT_IDS.txt` and must not appear in improver prompts.
6. Scorer / gold contract changes require a new ADR (frozen physics).

## Schema (v1)

Each JSONL line is one event object:

```json
{
  "schema_version": "1",
  "trace_id": "<run_id>",
  "span_id": "<uuid-or-counter>",
  "parent_span_id": null,
  "name": "run.start|node.start|node.end|run.end",
  "ts_ms": 0,
  "duration_ms": null,
  "attrs": {
    "recipe_id": "",
    "node_id": "",
    "activity": "",
    "ok": true,
    "unchecked": false,
    "unchecked_reason": null
  }
}
```

## Consequences

- Pros: zero deps; CI-friendly; disk-auditable; Unagent-compatible via custom adapter.
- Cons: no distributed collector; host must copy files for offline analysis.
- Rejected alternative: OTel GenAI spans — too heavy for this graph (Gate 0).

## Links

- Gate 0: [`GATE_0_KERNEL_HARDEN.md`](GATE_0_KERNEL_HARDEN.md)
- Product overlay: [`PRODUCT_KERNEL_HARDEN.md`](PRODUCT_KERNEL_HARDEN.md)

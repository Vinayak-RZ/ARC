# Loop plan — `B_TRACE` — JSONL writer

> Extensive node plan for kernel-harden graph. Parent: [`LOOP_GRAPH.md`](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_TRACE` |
| **Job** | JSONL writer |
| **Wave** | 1 |
| **Depends on (data)** | A1 PLANH |
| **Write paths** | `src/electrical_engineer/runner/trace.py src/electrical_engineer/runner/execute.py tests/unit/test_trace.py` |
| **Read paths** | `docs/planning/ADR_TRACE_JSONL.md src/electrical_engineer/runner/execute.py` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | explore (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **Inner critique loop** | no |
| **State** | [`B_TRACE.state.json`](B_TRACE.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail; learn-while-building |

---

## Stop (required)

```text
uv run pytest -q tests/unit/test_trace.py
```

Exit 0 = pass. Prose-only judgment is illegal.

---

## Objective

stdlib TraceWriter appends run.start/node.start/node.end/run.end lines to runs/<id>/trace.jsonl; tests lock schema_version and names.

## Non-goals

- OTel
- Changing evidentiary schema
- Scoring traces in gold

---

## Contract

**Input (lead → maker):**

```json
{ "node_id": "B_TRACE", "findings": [] }
```

**Maker output:**

```json
{ "files_touched": [], "notes": "", "artifacts": [] }
```

**Checker output:**

```json
{ "pass": false, "command": "uv run pytest -q tests/unit/test_trace.py", "exit_code": 1, "findings": [] }
```

---

## Maker procedure

1. Add runner/trace.py TraceWriter
2. Hook wrap() around node fn
3. Bookend execute() start/end
4. Unit tests with tmp_path
5. Ponytail: stdlib only

---

## Failure modes

- Missing schema_version
- Breaks observation.json

On fail with rounds left: remake using **checker findings only** (no whole-graph paste).

---

## Hardening notes

- No new deps
- Never log secrets/env
- unchecked attrs only booleans/reasons

- Exact token `unchecked` never paraphrased.
- No H5 agent loop.
- No OpenTelemetry dependency.
- Maker must not be checker.

---

## Commits (this node)

Lead commits after **passed**, mapping to IMPLEMENTATION_PLAN / master §9 rows for this node. Subagents do not commit.

---

## Escalate

After `3` failures, or if Stop cannot run: set state `escalated`, stop dependents, ask human.

---

## Do not

- Commit / push / open PR from the maker Task
- Write outside **Write paths**
- Expand into another graph
- Load sibling loop plans (lead passes artifacts)
- Use Cursor `/loop` timers

---

## Return to graph

Maker: files + notes. Checker: pass/exit/findings. Lead updates `B_TRACE.state.json` (`round`, `status`).

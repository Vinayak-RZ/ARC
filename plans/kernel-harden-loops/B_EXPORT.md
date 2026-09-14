# Loop plan — `B_EXPORT` — Unagent adapter

> Extensive node plan for kernel-harden graph. Parent: [`LOOP_GRAPH.md`](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_EXPORT` |
| **Job** | Unagent adapter |
| **Wave** | 1 |
| **Depends on (data)** | B_TRACE |
| **Write paths** | `src/electrical_engineer/export/unagent_adapter.py tests/unit/test_unagent_export.py scripts/kernel_harden/export_unagent.py` |
| **Read paths** | `docs/planning/ADR_TRACE_JSONL.md src/electrical_engineer/runner/trace.py` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | explore (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **Inner critique loop** | no |
| **State** | [`B_EXPORT.state.json`](B_EXPORT.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail; learn-while-building |

---

## Stop (required)

```text
uv run pytest -q tests/unit/test_unagent_export.py
```

Exit 0 = pass. Prose-only judgment is illegal.

---

## Objective

JSONL→dict Trace list / Unagent-custom payload without OTel; round-trip unit test on fixture spans.

## Non-goals

- pip installing Unagent into Arc runtime deps for CI
- Auto-applying Unagent refactors

---

## Contract

**Input (lead → maker):**

```json
{ "node_id": "B_EXPORT", "findings": [] }
```

**Maker output:**

```json
{ "files_touched": [], "notes": "", "artifacts": [] }
```

**Checker output:**

```json
{ "pass": false, "command": "uv run pytest -q tests/unit/test_unagent_export.py", "exit_code": 1, "findings": [] }
```

---

## Maker procedure

1. Implement load_jsonl + to_unagent_custom
2. CLI helper scripts/kernel_harden/export_unagent.py
3. Fixture-based pytest
4. Document shape in module docstring

---

## Failure modes

- Imports opentelemetry

On fail with rounds left: remake using **checker findings only** (no whole-graph paste).

---

## Hardening notes

- No network
- No API keys

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

Maker: files + notes. Checker: pass/exit/findings. Lead updates `B_EXPORT.state.json` (`round`, `status`).

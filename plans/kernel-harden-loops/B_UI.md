# Loop plan — `B_UI` — trace panel polish

> Extensive node plan for kernel-harden graph. Parent: [`LOOP_GRAPH.md`](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_UI` |
| **Job** | trace panel polish |
| **Wave** | 1 |
| **Depends on (data)** | U1 B_TRACE |
| **Write paths** | `src/electrical_engineer/ui_server/app.py ui/src/slots/root.jsx ui/src/slots/**` |
| **Read paths** | `docs/planning/U1_TRACE_UX.md` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | explore (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **Inner critique loop** | no |
| **State** | [`B_UI.state.json`](B_UI.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail; learn-while-building |

---

## Stop (required)

```text
rg -n "trace" src/electrical_engineer/ui_server/app.py ui/src/slots/root.jsx
```

Exit 0 = pass. Prose-only judgment is illegal.

---

## Objective

API returns trace excerpt; UI shows observation summary + last spans; polish spacing/contrast under existing tokens.

## Non-goals

- Brand rewrite
- Binding 0.0.0.0

---

## Contract

**Input (lead → maker):**

```json
{ "node_id": "B_UI", "findings": [] }
```

**Maker output:**

```json
{ "files_touched": [], "notes": "", "artifacts": [] }
```

**Checker output:**

```json
{ "pass": false, "command": "rg -n \"trace\" src/electrical_engineer/ui_server/app.py ui/src/slots/root.jsx", "exit_code": 1, "findings": [] }
```

---

## Maker procedure

1. Extend run_detail with trace_excerpt
2. Parse observation for unchecked_reason display
3. Render details section
4. Polish typography/spacing
5. Ensure keyboard details

---

## Failure modes

- Raw-only dump remains sole UI
- grep finds 0.0.0.0

On fail with rounds left: remake using **checker findings only** (no whole-graph paste).

---

## Hardening notes

- 127.0.0.1 only
- Truncate huge JSONL

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

Maker: files + notes. Checker: pass/exit/findings. Lead updates `B_UI.state.json` (`round`, `status`).

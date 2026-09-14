# Loop plan — `X_IMPROV` — Improveness tooling

> Extensive node plan for kernel-harden graph. Parent: [`LOOP_GRAPH.md`](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `X_IMPROV` |
| **Job** | Improveness tooling |
| **Wave** | 5 |
| **Depends on (data)** | T_RETEST |
| **Write paths** | `artifacts/kernel-harden/improveness-notes.md` |
| **Read paths** | `docs/planning/FAILURE_REPORT_KERNEL_HARDEN.md` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | explore (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **Inner critique loop** | no |
| **State** | [`X_IMPROV.state.json`](X_IMPROV.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail; learn-while-building |

---

## Stop (required)

```text
test -f artifacts/kernel-harden/improveness-notes.md
```

Exit 0 = pass. Prose-only judgment is illegal.

---

## Objective

Improveness tooling/principles applied: frozen physics, held-in/out, grader≠improver; notes for I2.

## Non-goals

- Mounting DeepSeek Harness as Arc runtime

---

## Contract

**Input (lead → maker):**

```json
{ "node_id": "X_IMPROV", "findings": [] }
```

**Maker output:**

```json
{ "files_touched": [], "notes": "", "artifacts": [] }
```

**Checker output:**

```json
{ "pass": false, "command": "test -f artifacts/kernel-harden/improveness-notes.md", "exit_code": 1, "findings": [] }
```

---

## Maker procedure

1. Clone Improveness or use docs
2. Map techniques to Arc scripts
3. Write improveness-notes.md with actionable I2 bullets

---

## Failure modes

- Empty notes

On fail with rounds left: remake using **checker findings only** (no whole-graph paste).

---

## Hardening notes

- Grader never writes itself

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

Maker: files + notes. Checker: pass/exit/findings. Lead updates `X_IMPROV.state.json` (`round`, `status`).

# Loop plan — `T_RETEST` — retest after I1

> Extensive node plan for kernel-harden graph. Parent: [`LOOP_GRAPH.md`](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `T_RETEST` |
| **Job** | retest after I1 |
| **Wave** | 4 |
| **Depends on (data)** | I1 |
| **Write paths** | `docs/planning/T_RETEST.md` |
| **Read paths** | `docs/planning/IMPROVE_LOG.md scripts/kernel_harden/trial_driver.py` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | explore (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **Inner critique loop** | no |
| **State** | [`T_RETEST.state.json`](T_RETEST.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail; learn-while-building |

---

## Stop (required)

```text
test -f docs/planning/T_RETEST.md && rg -n "pass|fail|PASS|FAIL" docs/planning/T_RETEST.md
```

Exit 0 = pass. Prose-only judgment is illegal.

---

## Objective

Retest log for previously failing classes shows measured improvement or honest remaining fails.

## Non-goals

- New features

---

## Contract

**Input (lead → maker):**

```json
{ "node_id": "T_RETEST", "findings": [] }
```

**Maker output:**

```json
{ "files_touched": [], "notes": "", "artifacts": [] }
```

**Checker output:**

```json
{ "pass": false, "command": "test -f docs/planning/T_RETEST.md && rg -n \"pass|fail|PASS|FAIL\" docs/planning/T_RETEST.md", "exit_code": 1, "findings": [] }
```

---

## Maker procedure

1. Re-run failing scenario ids
2. Record pass/fail
3. Link run_ids

---

## Failure modes

- Empty retest

On fail with rounds left: remake using **checker findings only** (no whole-graph paste).

---

## Hardening notes

- Do not delete old corpus

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

Maker: files + notes. Checker: pass/exit/findings. Lead updates `T_RETEST.state.json` (`round`, `status`).

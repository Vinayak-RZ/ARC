# Loop plan — `X_UNAGENT` — Unagent recommend

> Extensive node plan for kernel-harden graph. Parent: [`LOOP_GRAPH.md`](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `X_UNAGENT` |
| **Job** | Unagent recommend |
| **Wave** | 5 |
| **Depends on (data)** | T_RETEST |
| **Write paths** | `artifacts/kernel-harden/unagent-report.md artifacts/kernel-harden/unagent-report.json` |
| **Read paths** | `src/electrical_engineer/export/unagent_adapter.py artifacts/kernel-harden/CORPUS_INDEX.md` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | explore (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **Inner critique loop** | no |
| **State** | [`X_UNAGENT.state.json`](X_UNAGENT.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail; learn-while-building |

---

## Stop (required)

```text
test -f artifacts/kernel-harden/unagent-report.md
```

Exit 0 = pass. Prose-only judgment is illegal.

---

## Objective

Unagent (or offline substitute) recommend report over exported traces; FlipToDet/ABSTAIN noted.

## Non-goals

- Auto-applying refactors into src without I2

---

## Contract

**Input (lead → maker):**

```json
{ "node_id": "X_UNAGENT", "findings": [] }
```

**Maker output:**

```json
{ "files_touched": [], "notes": "", "artifacts": [] }
```

**Checker output:**

```json
{ "pass": false, "command": "test -f artifacts/kernel-harden/unagent-report.md", "exit_code": 1, "findings": [] }
```

---

## Maker procedure

1. Clone or fetch Unagent sibling if possible
2. Export sample traces via adapter
3. Run recommend or offline analysis
4. Write unagent-report.md with limitations if tool missing

---

## Failure modes

- Missing report file

On fail with rounds left: remake using **checker findings only** (no whole-graph paste).

---

## Hardening notes

- No secrets
- Simulation ≠ production disclaimer

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

Maker: files + notes. Checker: pass/exit/findings. Lead updates `X_UNAGENT.state.json` (`round`, `status`).

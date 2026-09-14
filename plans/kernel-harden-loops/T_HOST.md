# Loop plan — `T_HOST` — host trials ≥100

> Extensive node plan for kernel-harden graph. Parent: [`LOOP_GRAPH.md`](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `T_HOST` |
| **Job** | host trials ≥100 |
| **Wave** | 3 |
| **Depends on (data)** | R1 |
| **Write paths** | `artifacts/kernel-harden/CORPUS_INDEX.md artifacts/kernel-harden/raw/** scripts/kernel_harden/count_corpus.py` |
| **Read paths** | `scripts/kernel_harden/scenarios/** scripts/kernel_harden/trial_driver.py` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | explore (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 4 |
| **Inner critique loop** | yes |
| **State** | [`T_HOST.state.json`](T_HOST.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail; learn-while-building |

---

## Stop (required)

```text
uv run python scripts/kernel_harden/count_corpus.py | rg "completed: (1[0-9]{2}|[2-9][0-9]{2})"
```

Exit 0 = pass. Prose-only judgment is illegal.

---

## Objective

≥100 completed host-mediated trials with trace_path in CORPUS_INDEX; target 120–150; categories per master plan.

## Non-goals

- Scoring viva eloquence
- Committing raw dumps

---

## Contract

**Input (lead → maker):**

```json
{ "node_id": "T_HOST", "findings": [] }
```

**Maker output:**

```json
{ "files_touched": [], "notes": "", "artifacts": [] }
```

**Checker output:**

```json
{ "pass": false, "command": "uv run python scripts/kernel_harden/count_corpus.py | rg \"completed: (1[0-9]{2}|[2-9][0-9]{2})\"", "exit_code": 1, "findings": [] }
```

---

## Maker procedure

1. Implement count_corpus.py
2. Run batches via CLI/MCP paths as host
3. Cloud batches to disjoint raw/batch-*
4. Merge CORPUS_INDEX.md
5. Inner round: if count low, expand variants not rewrite driver

---

## Failure modes

- completed <100
- Missing traces

On fail with rounds left: remake using **checker findings only** (no whole-graph paste).

---

## Hardening notes

- gitignore raw/
- Index commits only samples
- Score honesty of unchecked

- Exact token `unchecked` never paraphrased.
- No H5 agent loop.
- No OpenTelemetry dependency.
- Maker must not be checker.

---

## Commits (this node)

Lead commits after **passed**, mapping to IMPLEMENTATION_PLAN / master §9 rows for this node. Subagents do not commit.

---

## Escalate

After `4` failures, or if Stop cannot run: set state `escalated`, stop dependents, ask human.

---

## Do not

- Commit / push / open PR from the maker Task
- Write outside **Write paths**
- Expand into another graph
- Load sibling loop plans (lead passes artifacts)
- Use Cursor `/loop` timers

---

## Return to graph

Maker: files + notes. Checker: pass/exit/findings. Lead updates `T_HOST.state.json` (`round`, `status`).

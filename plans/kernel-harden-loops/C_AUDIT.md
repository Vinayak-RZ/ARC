# Loop plan — `C_AUDIT` — architecture critique

> Extensive node plan for kernel-harden graph. Parent: [`LOOP_GRAPH.md`](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `C_AUDIT` |
| **Job** | architecture critique |
| **Wave** | 4 |
| **Depends on (data)** | T_HOST |
| **Write paths** | `docs/planning/ARCHITECTURE_CRITIQUE_KERNEL_HARDEN.md docs/planning/FAILURE_REPORT_KERNEL_HARDEN.md` |
| **Read paths** | `artifacts/kernel-harden/CORPUS_INDEX.md runs/**/trace.jsonl docs/ARCHITECTURE.md` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | explore (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 4 |
| **Inner critique loop** | yes |
| **State** | [`C_AUDIT.state.json`](C_AUDIT.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail; learn-while-building |

---

## Stop (required)

```text
rg -n "Failure class|Before|After|run_id" docs/planning/ARCHITECTURE_CRITIQUE_KERNEL_HARDEN.md docs/planning/FAILURE_REPORT_KERNEL_HARDEN.md
```

Exit 0 = pass. Prose-only judgment is illegal.

---

## Objective

Critique of whole kernel architecture + failure taxonomy with run_id evidence; Before/After placeholders for I1.

## Non-goals

- Patching code (I1)
- Handwavy critique without run_ids

---

## Contract

**Input (lead → maker):**

```json
{ "node_id": "C_AUDIT", "findings": [] }
```

**Maker output:**

```json
{ "files_touched": [], "notes": "", "artifacts": [] }
```

**Checker output:**

```json
{ "pass": false, "command": "rg -n \"Failure class|Before|After|run_id\" docs/planning/ARCHITECTURE_CRITIQUE_KERNEL_HARDEN.md docs/planning/FAILURE_REPORT_KERNEL_HARDEN.md", "exit_code": 1, "findings": [] }
```

---

## Maker procedure

1. Sample traces for failure patterns
2. Taxonomize classes
3. Write critique of layering/gates/router/observation gaps
4. Write FAILURE_REPORT with class→run_ids
5. Checker rejects if no run_id citations; remake

---

## Failure modes

- No Failure class headings
- No run_ids

On fail with rounds left: remake using **checker findings only** (no whole-graph paste).

---

## Hardening notes

- Cite only corpus evidence
- Do not invent capabilities

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

Maker: files + notes. Checker: pass/exit/findings. Lead updates `C_AUDIT.state.json` (`round`, `status`).

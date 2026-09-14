# Loop plan — `B_CORPUS` — scenario bank

> Extensive node plan for kernel-harden graph. Parent: [`LOOP_GRAPH.md`](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_CORPUS` |
| **Job** | scenario bank |
| **Wave** | 1 |
| **Depends on (data)** | A1 PLANH |
| **Write paths** | `scripts/kernel_harden/scenarios/** scripts/kernel_harden/count_scenarios.py artifacts/kernel-harden/HELD_OUT_IDS.txt` |
| **Read paths** | `eval/gold/** docs/planning/T1_HOST.md hosts/` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | explore (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **Inner critique loop** | no |
| **State** | [`B_CORPUS.state.json`](B_CORPUS.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail; learn-while-building |

---

## Stop (required)

```text
uv run python scripts/kernel_harden/count_scenarios.py | rg "total: (1[2-9][0-9]|[2-9][0-9]{2})"
```

Exit 0 = pass. Prose-only judgment is illegal.

---

## Objective

≥120 scenario specs across packs (circuits/signals/control/explain/rag/unmatched/injection) with held-out ~20% ids listed.

## Non-goals

- Running trials (T_HOST)
- Editing kernel

---

## Contract

**Input (lead → maker):**

```json
{ "node_id": "B_CORPUS", "findings": [] }
```

**Maker output:**

```json
{ "files_touched": [], "notes": "", "artifacts": [] }
```

**Checker output:**

```json
{ "pass": false, "command": "uv run python scripts/kernel_harden/count_scenarios.py | rg \"total: (1[2-9][0-9]|[2-9][0-9]{2})\"", "exit_code": 1, "findings": [] }
```

---

## Maker procedure

1. Scaffold scenarios dirs by pack
2. Write count_scenarios.py
3. Author ≥120 JSON/YAML scenario files
4. Pick held-out ids → HELD_OUT_IDS.txt
5. Cloud fan-out OK on disjoint pack dirs

---

## Failure modes

- Count <120
- Held-out empty

On fail with rounds left: remake using **checker findings only** (no whole-graph paste).

---

## Hardening notes

- Held-out file committed
- No secrets in fixtures
- Scenarios name recipe_id or MCP verb

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

Maker: files + notes. Checker: pass/exit/findings. Lead updates `B_CORPUS.state.json` (`round`, `status`).

# Loop plan — `T_FINAL` — final trials

> Extensive node plan for kernel-harden graph. Parent: [`LOOP_GRAPH.md`](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `T_FINAL` |
| **Job** | final trials |
| **Wave** | 5 |
| **Depends on (data)** | I2 |
| **Write paths** | `docs/planning/T1_TRIALS_KERNEL_HARDEN.md` |
| **Read paths** | `artifacts/kernel-harden/HELD_OUT_IDS.txt scripts/kernel_harden/trial_driver.py` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | explore (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **Inner critique loop** | no |
| **State** | [`T_FINAL.state.json`](T_FINAL.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail; learn-while-building |

---

## Stop (required)

```text
test -f docs/planning/T1_TRIALS_KERNEL_HARDEN.md && rg -c "PASS|FAIL|pass|fail" docs/planning/T1_TRIALS_KERNEL_HARDEN.md | awk "END{exit !(\$1>=5)}"
```

Exit 0 = pass. Prose-only judgment is illegal.

---

## Objective

Final verification queue including held-out; ≥5 scored rows in T1_TRIALS_KERNEL_HARDEN.md.

## Non-goals

- Training

---

## Contract

**Input (lead → maker):**

```json
{ "node_id": "T_FINAL", "findings": [] }
```

**Maker output:**

```json
{ "files_touched": [], "notes": "", "artifacts": [] }
```

**Checker output:**

```json
{ "pass": false, "command": "test -f docs/planning/T1_TRIALS_KERNEL_HARDEN.md && rg -c \"PASS|FAIL|pass|fail\" docs/planning/T1_TRIALS_KERNEL_HARDEN.md | awk \"END{exit !(\$1>=5)}\"", "exit_code": 1, "findings": [] }
```

---

## Maker procedure

1. Run held-out + regression set
2. Fill T1 table
3. Note residual fails honestly

---

## Failure modes

- <5 rows

On fail with rounds left: remake using **checker findings only** (no whole-graph paste).

---

## Hardening notes

- Held-out never used in I2 prompts

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

Maker: files + notes. Checker: pass/exit/findings. Lead updates `T_FINAL.state.json` (`round`, `status`).

# Loop plan — `B_PACKS` — `pack coverage`

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_PACKS` |
| **Job** | Each pack default capability requestable; provider or cannot-do. |
| **Wave** | 4 |
| **Depends on (data)** | `B_KERNEL id_list` |
| **Write paths** | `skills/circuits/** skills/signals/** skills/electronics/** skills/machines/** skills/power/** skills/control/** skills/power_electronics/** skills/measurements/** skills/em/** skills/maths/** skills/_cross/** docs/CANNOT_DO.md tests/unit/test_pack_coverage.py` |
| **Read paths** | `docs/ARCHITECTURE.md docs/CANNOT_DO.md skills/` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | generalPurpose (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [B_PACKS.state.json](B_PACKS.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail |

---

## Stop (required)

```text
uv run pytest -q tests/unit/test_pack_coverage.py
```

---

## Objective

test_pack_coverage passes for every curriculum pack.

## Non-goals

- gold depth, rewriting skills into essays, reference/ files

---

## Contract

**Input:**

```json
{ "from": "B_KERNEL id_list" }
```

**Maker output:**

```json
{ "files_touched": [], "notes": "" }
```

**Checker output:**

```json
{ "pass": false, "command": "", "exit_code": 1, "findings": [] }
```

---

## Escalate

After `max_rounds` failures, or if the checker cannot run the stop: set `escalated`, wait for the human. Do not start dependents.

---

## Commits (this node only)

| # | Commit | Contents | Gate |
|---|--------|----------|------|
| | `feat(skills): pack coverage paths` | write paths above | stop command |

---

## Do not

- Commit, push, or open a PR
- Write outside **Write paths**
- Checker: write product files, or be the same Task as the maker
- Expand into another graph
- Load sibling loop plans
- Use Cursor `/loop` timers

---

## Return to graph

Maker: files touched, notes. Checker: pass, command, exit code, findings.
Lead updates `B_PACKS.state.json`.

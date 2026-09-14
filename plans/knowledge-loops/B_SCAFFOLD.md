# Loop plan — `B_SCAFFOLD` — schema and checker

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_SCAFFOLD` |
| **Job** | Schema, LICENCE, empty required paths, check_knowledge_tree.py, pytest |
| **Wave** | 0 |
| **Depends on (data)** | A1 ADR |
| **Write paths** | `knowledge/SCHEMA.md`, `knowledge/LICENCE.md`, `knowledge/SOURCE_LEDGER.md`, `knowledge/ug-ee/**` (placeholders), `scripts/check_knowledge_tree.py`, `tests/unit/test_knowledge_tree.py` |
| **Read paths** | `knowledge/COVERAGE.yaml` |
| **Maker type** | lead |
| **Maker model** | inherit |
| **Checker type** | explore |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [B_SCAFFOLD.state.json](B_SCAFFOLD.state.json) |
| **Isolation** | path-ownership; checker writes nothing |
| **Companion skills** | ponytail |

---

## Stop (required)

**Command:**

```text
python scripts/check_knowledge_tree.py --allow-empty
```


---

## Objective

Checker runs; every COVERAGE unit path exists (may be empty placeholders); SPDX rules documented.

## Non-goals

- Do not fill encyclopedic notes

---

## Contract

**Input:**

```json
{}
```

**Maker output:** `{ "files_touched": [], "notes": "" }`

**Checker output:** `{ "pass": false, "command": "", "exit_code": 1, "findings": [] }`

---

## Escalate

After `max_rounds` failures, or if the checker cannot run the stop: **stop the loop**, set status `escalated`, wait for the human. Do not start the next dependent node.

---

## Commits (this node only)

| # | Commit | Contents | Gate |
|---|--------|----------|------|
| 4 | `feat(knowledge): add coverage manifest schema and tree checker` | schema, checker, placeholders | `python scripts/check_knowledge_tree.py --allow-empty` |

---

## Do not

- Commit, push, or open a PR
- Write outside **Write paths**
- Checker: write product files, or be the same Task as the maker
- Expand into another graph
- Load sibling loop plans
- Touch `src/`, `ui/`, `workflows/`, `eval/gold/`, `docs/PID.md`, `docs/PRD.md`, `docs/ARCHITECTURE.md`, `docs/PRODUCT.md`
- Use Cursor `/loop` timers

---

## Return to graph

Maker: files touched, notes. Checker: pass, command, exit code, findings.
Lead updates `B_SCAFFOLD.state.json`.

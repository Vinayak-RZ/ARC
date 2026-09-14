# Loop plan — `B_MACHINES` — machines handbook

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_MACHINES` |
| **Job** | Fill encyclopedic handbook for machines |
| **Wave** | 2 |
| **Depends on (data)** | B_SCAFFOLD schema+checker+COVERAGE units |
| **Write paths** | `knowledge/ug-ee/machines/**` |
| **Read paths** | `knowledge/COVERAGE.yaml`, `knowledge/SCHEMA.md`, `knowledge/LICENCE.md` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | explore |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [B_MACHINES.state.json](B_MACHINES.state.json) |
| **Isolation** | path-ownership; checker writes nothing |
| **Companion skills** | ponytail |

---

## Stop (required)

**Command:**

```text
python scripts/check_knowledge_tree.py --pack machines
```


---

## Objective

Every COVERAGE unit under machines has notes.md (≥1500 words, required headings), questions.md (≥5 original worked Qs with Given/Find/Solution/Answer), sources.md. original-only; no fake SPDX.

## Non-goals

- Do not write other packs
- Do not commit commercial book or GATE paper text
- Do not copy NC-licensed OER
- Do not wire RAG

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
| 9 | `feat(knowledge): electrical machines handbook` | knowledge/ug-ee/machines/** | `python scripts/check_knowledge_tree.py --pack machines` |

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
Lead updates `B_MACHINES.state.json`.

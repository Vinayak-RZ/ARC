# Loop plan — `B_MEAS_EM` — measurements and EM

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_MEAS_EM` |
| **Job** | Fill encyclopedic handbook for measurements+em |
| **Wave** | 3 |
| **Depends on (data)** | B_SCAFFOLD schema+checker+COVERAGE units |
| **Write paths** | `knowledge/ug-ee/measurements/**, knowledge/ug-ee/em/**` |
| **Read paths** | `knowledge/COVERAGE.yaml`, `knowledge/SCHEMA.md`, `knowledge/LICENCE.md` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | explore |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [B_MEAS_EM.state.json](B_MEAS_EM.state.json) |
| **Isolation** | path-ownership; checker writes nothing |
| **Companion skills** | ponytail |

---

## Stop (required)

**Command:**

```text
python scripts/check_knowledge_tree.py --pack measurements && python scripts/check_knowledge_tree.py --pack em
```


---

## Objective

Every COVERAGE unit under measurements+em has notes.md (≥1500 words, required headings), questions.md (≥5 original worked Qs with Given/Find/Solution/Answer), sources.md. Ellingson Vol 1 oer/ for em.

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
| 13 | `feat(knowledge): measurements and EM fields handbooks` | knowledge/ug-ee/measurements/**, knowledge/ug-ee/em/** | `python scripts/check_knowledge_tree.py --pack measurements && python scripts/check_knowledge_tree.py --pack em` |

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
Lead updates `B_MEAS_EM.state.json`.

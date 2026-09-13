# Loop plan — `B_RAG` — `RAG ingest`

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_RAG` |
| **Job** | BYO ingest extract/chunk/index; CI licence-clean fixture; empty retrieve visible. |
| **Wave** | 3 |
| **Depends on (data)** | `A1 retrieve_port` |
| **Write paths** | `src/electrical_engineer/rag/** tests/unit/test_rag_ingest.py tests/fixtures/rag/**` |
| **Read paths** | `docs/rag-byo.md src/electrical_engineer/rag/` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | generalPurpose (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [B_RAG.state.json](B_RAG.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail backend-architecture agentic-system-design |

---

## Stop (required)

```text
uv run pytest -q tests/unit/test_rag_ingest.py
```

---

## Objective

rag add of a fixture yields inventory + retrieve hit.

## Non-goals

- LightRAG as harness, commercial PDFs

---

## Contract

**Input:**

```json
{ "from": "A1 retrieve_port" }
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
| | `feat(rag): ingest extract chunk index` | write paths above | stop command |

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
Lead updates `B_RAG.state.json`.

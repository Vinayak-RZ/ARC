# Loop plan — `B_HOST` — `host contract`

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_HOST` |
| **Job** | ChatGPT desktop + adapters name live 5-7 verbs; root skill short; no Python orchestrator. |
| **Wave** | 3 |
| **Depends on (data)** | `A1 verb_names` |
| **Write paths** | `docs/hosts/** hosts/** skills/SKILL.md tests/unit/test_host_docs.py` |
| **Read paths** | `docs/PRD.md docs/ARCHITECTURE.md skills/SKILL.md` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | generalPurpose (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [B_HOST.state.json](B_HOST.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | agentic-system-design |

---

## Stop (required)

```text
uv run pytest -q tests/unit/test_host_docs.py
```

---

## Objective

Host docs name propose_composition; packs stay out of .cursor/skills/.

## Non-goals

- Skills-over-MCP implementation, pack spawn on Chat/Work

---

## Contract

**Input:**

```json
{ "from": "A1 verb_names" }
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
| | `docs(hosts): ChatGPT desktop verbs match ACI` | write paths above | stop command |

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
Lead updates `B_HOST.state.json`.

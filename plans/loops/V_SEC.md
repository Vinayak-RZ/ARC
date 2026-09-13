# Loop plan — `V_SEC` — `security review`

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `V_SEC` |
| **Job** | Readonly: bind, secrets, MCP wait, RAG path traversal, PII in run dirs. |
| **Wave** | 7 |
| **Depends on (data)** | `M1 wired` |
| **Write paths** | `docs/planning/SECURITY_REVIEW.md` |
| **Read paths** | `src/ ui/ .github/` |
| **Maker type** | lead |
| **Maker model** | inherit |
| **Checker type** | generalPurpose (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [V_SEC.state.json](V_SEC.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | core-engineering security baseline |

---

## Stop (required)

```text
test -f docs/planning/SECURITY_REVIEW.md && grep -q '127.0.0.1' docs/planning/SECURITY_REVIEW.md && grep -qi 'secret' docs/planning/SECURITY_REVIEW.md
```

---

## Objective

SECURITY_REVIEW.md names 127.0.0.1 and secrets handling.

## Non-goals

- rewriting product in this loop

---

## Contract

**Input:**

```json
{ "from": "M1 wired" }
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
| | `docs: security review findings` | write paths above | stop command |

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
Lead updates `V_SEC.state.json`.

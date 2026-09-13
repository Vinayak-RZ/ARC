# Loop plan — `V_PONY` — `ponytail-review`

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `V_PONY` |
| **Job** | Readonly over-engineering review of the branch diff. |
| **Wave** | 5 |
| **Depends on (data)** | `B* diffs` |
| **Write paths** | `docs/planning/PONYTAIL_REVIEW.md` |
| **Read paths** | `src/ ui/ workflows/` |
| **Maker type** | lead |
| **Maker model** | inherit |
| **Checker type** | generalPurpose (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [V_PONY.state.json](V_PONY.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail-review |

---

## Stop (required)

```text
test -f docs/planning/PONYTAIL_REVIEW.md && grep -q '## Findings' docs/planning/PONYTAIL_REVIEW.md
```

---

## Objective

Findings file exists; M1 applies P0-blocking cuts.

## Non-goals

- product code writes, new features

---

## Contract

**Input:**

```json
{ "from": "B* diffs" }
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
| | `docs: ponytail-review findings` | write paths above | stop command |

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
Lead updates `V_PONY.state.json`.

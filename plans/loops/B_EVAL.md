# Loop plan — `B_EVAL` — `gold FR9`

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_EVAL` |
| **Job** | Gold scores evidentiary; FR9 no minted checked; one non-circuits complete-path item. |
| **Wave** | 6 |
| **Depends on (data)** | `M1 wired` |
| **Write paths** | `eval/gold/** src/electrical_engineer/eval_runner/** tests/integration/test_eval_scoring.py` |
| **Read paths** | `eval/gold/ src/electrical_engineer/eval_runner/` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | generalPurpose (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [B_EVAL.state.json](B_EVAL.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail |

---

## Stop (required)

```text
uv run electrical-engineer eval --pack circuits && uv run pytest -q tests/integration/test_eval_scoring.py
```

---

## Objective

circuits eval green; scoring does not treat solve-explain mint as checked.

## Non-goals

- large gold bank

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
| | `test(eval): FR9 evidentiary and pack path` | write paths above | stop command |

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
Lead updates `B_EVAL.state.json`.

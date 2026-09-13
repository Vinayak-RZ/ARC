# Loop plan — `B_UI` — `two-band UI`

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_UI` |
| **Job** | Render two bands, plan, observation; empty/error/waiting-human; 127.0.0.1; a11y. |
| **Wave** | 4 |
| **Depends on (data)** | `U1 slot_and_state_map B_KERNEL artifact_schema` |
| **Write paths** | `ui/** src/electrical_engineer/ui_server/** tests/unit/test_slot_registry.py tests/integration/test_ui_artifacts.py tests/integration/test_ui_bind.py tests/integration/test_ui_a11y.py` |
| **Read paths** | `docs/ui-ia.md docs/design/DESIGN-coinbase.md` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | generalPurpose (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [B_UI.state.json](B_UI.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail frontend-architecture impeccable audit |

---

## Stop (required)

```text
uv run pytest -q tests/unit/test_slot_registry.py tests/integration/test_ui_artifacts.py tests/integration/test_ui_bind.py tests/integration/test_ui_a11y.py
```

---

## Objective

UI shows evidentiary+argument without flipping unchecked; bind localhost.

## Non-goals

- restyle, 0.0.0.0, Cordis, new palette

---

## Contract

**Input:**

```json
{ "from": "U1 slot_and_state_map B_KERNEL artifact_schema" }
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
| | `feat(ui): two-band slots and a11y states` | write paths above | stop command |

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
Lead updates `B_UI.state.json`.

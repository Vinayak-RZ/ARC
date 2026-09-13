# Loop plan — `B_WF` — `short attachments`

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_WF` |
| **Job** | Short YAML bind capabilities; host-path without solve-explain; unmatched no auto-spice. |
| **Wave** | 4 |
| **Depends on (data)** | `B_KERNEL capability_ids` |
| **Write paths** | `workflows/** tests/unit/test_attachments_host_path.py tests/integration/test_unmatched_no_spice.py` |
| **Read paths** | `docs/WORKFLOWS.md src/electrical_engineer/catalog.py` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | generalPurpose (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [B_WF.state.json](B_WF.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail |

---

## Stop (required)

```text
uv run pytest -q tests/integration/test_unmatched_no_spice.py tests/unit/test_attachments_host_path.py
```

---

## Objective

Host catalog rows are short attachments; unmatched still cannot auto-spice.

## Non-goals

- inventing capability ids, gold-depth every pack

---

## Contract

**Input:**

```json
{ "from": "B_KERNEL capability_ids" }
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
| | `feat(workflows): bind attachments to capabilities` | write paths above | stop command |

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
Lead updates `B_WF.state.json`.

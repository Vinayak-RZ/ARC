# Loop plan — `B_ACI` — `MCP ACI`

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_ACI` |
| **Job** | 5-7 MCP verbs including propose_composition; CLI omitted-id classifier; never wait. |
| **Wave** | 4 |
| **Depends on (data)** | `B_KERNEL capability_api B_WF attachment_ids` |
| **Write paths** | `src/electrical_engineer/mcp/** src/electrical_engineer/cli.py src/electrical_engineer/router/** tests/unit/test_mcp_aci.py tests/unit/test_cli_classifier.py tests/integration/test_mcp_fail_closed.py` |
| **Read paths** | `src/electrical_engineer/compose/ src/electrical_engineer/capabilities.py` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | generalPurpose (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [B_ACI.state.json](B_ACI.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail agentic-system-design |

---

## Stop (required)

```text
uv run pytest -q tests/unit/test_mcp_aci.py tests/unit/test_cli_classifier.py tests/integration/test_mcp_fail_closed.py
```

---

## Objective

tools/list is 5-7 verbs; photo fail-closed with ui_url; apply:false records plan.

## Non-goals

- Python interview loop, HTTP MCP, graph body in MCP return

---

## Contract

**Input:**

```json
{ "from": "B_KERNEL capability_api B_WF attachment_ids" }
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
| | `feat(mcp): 5-7 verbs and CLI classifier` | write paths above | stop command |

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
Lead updates `B_ACI.state.json`.

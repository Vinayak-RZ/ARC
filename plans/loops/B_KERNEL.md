# Loop plan — `B_KERNEL` — `capability kernel`

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_KERNEL` |
| **Job** | Capability registry, validator, provider bind, observation/evidentiary, FR9 no-mint. |
| **Wave** | 3 |
| **Depends on (data)** | `A1 layout_aci` |
| **Write paths** | `src/electrical_engineer/nodes/** src/electrical_engineer/runner/** src/electrical_engineer/compose/** src/electrical_engineer/gates/** src/electrical_engineer/unchecked.py src/electrical_engineer/capabilities.py tests/unit/test_capabilities.py tests/unit/test_composition.py tests/unit/test_observation.py tests/unit/test_fr9_no_mint.py` |
| **Read paths** | `docs/ARCHITECTURE.md DECISIONS.md` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | generalPurpose (readonly) |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [B_KERNEL.state.json](B_KERNEL.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail backend-architecture |

---

## Stop (required)

```text
uv run pytest -q tests/unit/test_capabilities.py tests/unit/test_composition.py tests/unit/test_observation.py tests/unit/test_fr9_no_mint.py
```

---

## Objective

Allowlisted capabilities bind providers or CD-NO-PROVIDER; solve-explain cannot mint checked.

## Non-goals

- cli.py mcp rag ui_server YAML catalog rewrite

---

## Contract

**Input:**

```json
{ "from": "A1 layout_aci" }
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
| | `feat(kernel): capability bind observation and FR9` | write paths above | stop command |

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
Lead updates `B_KERNEL.state.json`.

# Loop plan — `B_PACKS` — skills and adapters

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `B_PACKS` |
| **Job** | Knowledge-linked 10 pack skills + retrieve scaffold; Cursor/Codex/Claude per-pack adapters; hosts install. |
| **Wave** | 2 |
| **Depends on (data)** | A1 |
| **Write paths** | `skills/`, `hosts/adapters/`, `src/electrical_engineer/` hosts-install CLI, `tests/unit/test_host_adapters.py`, `tests/unit/test_pack_skills.py` |
| **Read paths** | `knowledge/ug-ee/`, `knowledge/COVERAGE.yaml`, `docs/ARCHITECTURE.md` |
| **Maker type** | generalPurpose |
| **Maker model** | inherit |
| **Checker type** | explore |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [B_PACKS.state.json](B_PACKS.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | ponytail |

---

## Stop (required)

**Command:**

```text
python -m pytest tests/unit/test_host_adapters.py tests/unit/test_pack_skills.py -q
```

---

## Objective

Every core pack has SKILL.md scaffold + three host adapter files; tests green.

## Non-goals

- Electives
- Real retrieval
- EE files in this repo .cursor/agents/

---

## Contract

**Input:** `docs/planning/GATE_0_SKILLS_MATLAB.md` plus upstream artifacts.

**Maker output:** files_touched + notes. **Do NOT commit.**

**Checker output:** `{ pass, command, exit_code, findings }`. Readonly.

---

## Escalate

After 3 failed rounds, status `escalated`; wait for the human.

---

## Commits (this node only)

7–14 skills/hosts/cli/tests — lead commits after **passed**.

---

## Do not

- Commit, push, or open a PR
- Write outside write paths
- Checker: write product files or be the maker
- Expand into another graph
- Use Cursor `/loop` timers

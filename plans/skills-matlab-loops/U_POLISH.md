# Loop plan — `U_POLISH` — impeccable UI

> Collapsed plan for **one loop node**. Parent: [LOOP_GRAPH.md](../../LOOP_GRAPH.md).

| Field | Value |
|-------|-------|
| **Node id** | `U_POLISH` |
| **Job** | Critique live UI; fix copy/a11y/empty/error/chip honesty. No teach. |
| **Wave** | 6 |
| **Depends on (data)** | T1 |
| **Write paths** | `ui/`, `docs/ui-ia.md`, `docs/planning/U_CRITIQUE.md` |
| **Read paths** | `docs/PRODUCT.md`, `docs/design/DESIGN-coinbase.md`, live UI |
| **Maker type** | lead |
| **Maker model** | inherit |
| **Checker type** | explore |
| **Checker model** | composer-2.5-fast else inherit |
| **Max rounds** | 3 |
| **State** | [U_POLISH.state.json](U_POLISH.state.json) |
| **Isolation** | path-ownership; checker writes nothing in product trees |
| **Companion skills** | impeccable |

---

## Stop (required)

**Command:**

```text
python -m pytest tests/integration/test_ui_a11y.py -q && grep -q 'what we changed' docs/planning/U_CRITIQUE.md
```

---

## Objective

U_CRITIQUE.md has issues and changelog; a11y green.

## Non-goals

- New visual system
- In-window chat

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

22: feat(ui) critique fixes — lead commits after **passed**.

---

## Do not

- Commit, push, or open a PR
- Write outside write paths
- Checker: write product files or be the maker
- Expand into another graph
- Use Cursor `/loop` timers

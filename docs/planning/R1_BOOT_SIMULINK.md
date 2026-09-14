# R1 boot — Simulink agents graph

Recorded 2026-09-14 on this Cloud checkout. No live MATLAB / Simulink.

## 1. electrical-engineer --help

```text
usage: electrical-engineer [-h] [--version]
                           {run,workflows,mcp,eval,ui,rag,memory,hosts} ...
```

## 2. hosts install — 12 cards

```text
uv run electrical-engineer hosts install --into /tmp/ee-hw-sim --host all
```

Wrote 12 Cursor + 12 Codex + 12 Claude files. Includes `ee-simulink`. Product `.cursor/agents/ee-*.md` count: 0.

## 3. MCP tools/list

Seven verbs: `list_workflows`, `retrieve`, `open_ui`, `simulate_attachment`, `propose_composition`, `label`, `run_workflow`.

`MATLAB_TOOLS = []`. `SIMULINK_TOOLS = []` (`model_read` absent).

## 4. run-simulink-if-present missing

`ok: false`, `cannot_do: CD-SIMULINK-PLANT`, `unchecked: true`. This VM has no toolkit `tools.json`.

## 5. Catalog on disk

`hosts/agents/` has 12 `ee-*.md` files plus `INDEX.md`.

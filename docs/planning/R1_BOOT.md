# R1 boot evidence

Recorded 2026-09-13 on Ubuntu after D19/D20 loops. Re-run **2026-09-14** on this skills/MATLAB graph. Bind is **127.0.0.1** only. Local LLM skipped (unset).

## 1. electrical-engineer --help

```text
usage: electrical-engineer [-h] [--version]
                           {run,workflows,mcp,eval,ui,rag,memory,hosts} ...
```

`hosts` is the specialist install command. `electrical-engineer --version` → `electrical-engineer 0.1.0`.

## 2. electrical-engineer run solve-circuit-problem

With `eval/gold/circuits/divider-dc-01/fixtures/problem.json` as cwd `problem.json`:

```text
e54q-20260913T083849Z
recipe_id solve-circuit-problem
unchecked false
value 5.0
verifier algebraic-check via check-numeric
solve node unchecked true (FR9: solve-explain does not mint checked)
check node unchecked false ok true
```

Also `electrical-engineer run simulate-circuit` → token `unchecked` (no ngspice in this environment).

## 3. MCP stdio initialize + tools/list

Seven verbs: `list_workflows`, `retrieve`, `open_ui`, `simulate_attachment`, `propose_composition`, `label`, `run_workflow`. **No MATLAB tool names.** `propose_composition` of `lookup_vout_guess` returns `unknown id` with `waits: false`. Photo `simulate_attachment` returns `ui_url` `http://127.0.0.1:8765/` and `waits: false`.

2026-09-14 live `tools/list` names: `list_workflows`, `retrieve`, `open_ui`, `simulate_attachment`, `propose_composition`, `label`, `run_workflow`. MATLAB_TOOLS = [].

## 4. UI health on 127.0.0.1

```text
{"bind":"127.0.0.1","ok":true}
GET / → 200 (Vite SPA)
GET /api/runs → list (honest empty when none)
```

UI health JSON `{"bind":"127.0.0.1","ok":true}`. Loopback only (validate.sh refuses WAN binds).

## 5. hosts install

```text
electrical-engineer hosts install --into /tmp/ee-hw --host cursor
```

Writes 11 files under `.cursor/agents/ee-*.md` (10 cores + maths + cross). Not this product `.cursor/`.

## Local LLM

EE_LOCAL_LLM_URL unset → skip-if-missing (see tests/unit/test_local_llm.py).

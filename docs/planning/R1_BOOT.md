# R1 boot evidence

Recorded 2026-09-13 on Ubuntu after D19/D20 loops. Bind is **127.0.0.1** only. Local LLM skipped (unset).

## 1. electrical-engineer --help

```text
usage: electrical-engineer [-h] [--version]
                           {run,workflows,mcp,eval,ui,rag,memory} ...

positional arguments:
  {run,workflows,mcp,eval,ui,rag,memory}

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
```

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

Seven verbs: `list_workflows`, `retrieve`, `open_ui`, `simulate_attachment`, `propose_composition`, `label`, `run_workflow`. `propose_composition` of `lookup_vout_guess` returns `unknown id` with `waits: false`. Photo `simulate_attachment` returns `ui_url` `http://127.0.0.1:8765/` and `waits: false`.

## 4. UI health on 127.0.0.1

```text
{"bind":"127.0.0.1","ok":true}
GET /api/runs → list (honest empty when none)
GET /api/runs/nope → 404 state failed
```

UI health JSON `{"bind":"127.0.0.1","ok":true}`. Loopback only (validate.sh refuses WAN binds).

## Local LLM

EE_LOCAL_LLM_URL unset → skip-if-missing (see tests/unit/test_local_llm.py).

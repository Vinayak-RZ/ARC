# Node plan: B4: circuits + multimodal

| Field | Value |
|-------|-------|
| **Node id** | `B4` |
| **Job** | CIRCUIT subset runner, photo/diagram confirm → netlist → ngspice |
| **Wave** | 3 |
| **Depends on (data)** | `capability_delta_spec` (multimodal scope) |
| **Write paths** | `src/electrical_engineer/engines/spice_*`, ingest paths, `eval/gold/circuits/**`, `tests/**` |
| **Model** | inherit |

## Objective

Beat CircuitSense symbolic gap with **verify-after-derive** pipeline (report #02 white space #2).

## Contract

**Output:** `{ "circuit_unit_pass_rate": <measured>, "multimodal_path_smoke": <bool> }`

Run: `uv run python scripts/run_circuit_benchmark.py` (writes `artifacts/frontier/b4_contract.json`).

## Commits

| # | Commit | Gate |
|---|--------|------|
| 15-19 | CIRCUIT runner, ingest v1, golds, property tests | ngspice integration |

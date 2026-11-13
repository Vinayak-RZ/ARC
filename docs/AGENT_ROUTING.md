# Agent routing — problem types to Arc commands

Fresh agents should copy the **problem.json** pattern, then run the **recipe** (CLI or MCP `run_recipe`). Each `study-*-v2` recipe runs `run-ee-v2-solver` → `check-numeric` (recompute vs `expected`) → summary.

## CLI

```bash
electrical-engineer run <recipe-id> --problem path/to/problem.json
# or eval gold:
electrical-engineer eval --pack power
```

## MCP

`list_workflows` → `propose_composition` / host `run_recipe` with the same `recipe_id` and `problem.json`.

## `problem.json` shape

| Field | Role |
|-------|------|
| `solver` | Required for v2 recipes (`run-ee-v2-solver`). Same id as `check_kind` for verify. |
| `value_key` | Scalar in the engine result to surface as `value` (optional; has defaults). |
| `unit` | Documented on output (e.g. `V`, `A`, `MW/MW`). |
| `expected` | Gold answer for `check-numeric`. |
| `tol` | Numeric tolerance (default `1e-6`). |

Inputs are plain numbers or `{"value": 10, "unit": "V"}` objects.

## Solver → recipe → pack

| Problem type | `solver` | Recipe id | Pack / skill |
|--------------|----------|-----------|--------------|
| RC step response | `rc_step` | `study-circuits-v2` | `skills/circuits` |
| RL step response | `rl_step` | `study-circuits-v2` | circuits |
| Source-free RLC | `rlc_natural` | `study-circuits-v2` | circuits |
| Phasor / PFC | `phasor_pfc` | `study-circuits-v2` | circuits |
| Balanced 3φ power | `three_phase_balanced` | `study-circuits-v2` | circuits |
| Transformer regulation % | `transformer_regulation` | `study-machines-v2` | `skills/machines` |
| DC shunt motor speed | `dc_motor_shunt` | `study-machines-v2` | machines |
| IM air-gap power split | `induction_air_gap_split` | `study-machines-v2` | machines |
| CCM buck duty / ripple | `ccm_buck` | `study-power-electronics-v2` | `skills/power_electronics` |
| ED with B losses (T13) | `ed_with_losses` | `ed-penalty-study` | `skills/power` |
| Symmetrical fault Z₁ pu | *(use `symmetrical-fault-study`)* | `symmetrical-fault-study` | power |
| Mini load flow | `load_flow_json` | `solve-power-problem` or custom problem on v2 node | power |
| Z-transform / diff eq | `z_inverse` | `study-circuits-v2` or signals pack | signals / circuits |
| Root locus breakaway | `breakaway_real_axis` | `study-control-exam` or `solve-control-problem` | `skills/control` |
| Steady-state error type 0/1/2 | `steady_state_error` | `study-control-exam` or `solve-control-problem` | control |
| Bode / margins (python-control) | *(omit `solver`)* | `solve-control-problem` | control |
| Sequence fault I₀/I₁/I₂ | *(omit `solver`)* | `simulate-power-fault` | power |
| PU base aggregation (T12) | *(use `run-symmetrical-fault-base`)* | `symmetrical-fault-study` | power |
| RLC ngspice missing | `series_rlc` keys + `run-rlc-analytic` | `simulate-circuit` | circuits |

## Example commands

```bash
# RC transient (gold rc-step-01)
electrical-engineer run study-circuits-v2 --problem eval/gold/circuits/rc-step-01/fixtures/problem.json

# ED with losses (T13)
electrical-engineer run ed-penalty-study --problem eval/gold/power/ed-penalty-t13-01/fixtures/problem.json

# Breakaway on 1+K/(s(s+3)(s+6))
electrical-engineer run study-control-exam --problem eval/gold/control/breakaway-3pole-01/fixtures/problem.json
```

## When ngspice is missing

`run-spice` returns `hint` and `analytic_recipe: run-rlc-analytic` for problems with `r_ohm`, `l_h`, `c_f`. Prefer `study-circuits-v2` / `run-rlc-analytic` for series RLC steps without a netlist.

## Trap catalog

See `proofs/ablation/trap_prompts.yaml` (T11 margins, T12 pu base, T13 ED penalty).

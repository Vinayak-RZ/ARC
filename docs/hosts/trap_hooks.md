# Host hook: trap PRM (pre-final verifier)

Arc exposes a **deterministic process reward model (PRM)** on the trap catalog (T1–T10). It grades working steps, not only the final scalar. Use it in the host loop **after** engine runs and **web-verify**, and **before** you finalize `argument.md` or tell the student the answer is checked.

## When to call

1. Engine activity nodes have produced evidentiary numbers (`run-smib-swing`, `run-agc-two-area`, `run-ed-lambda`, …).
2. `web-verify` has run (or is offline-skipped with fixtures).
3. You are about to label the run checked or paste the final answer.

Do **not** skip because the outcome number looks plausible. Bare agents often hit the right final while violating procedure (T1 stage mix-up, T2 `ode45`, T4 ACE sign, T5 AGC dip story, T6 limits).

## Solution trace shape

Pass a trace the verifier can walk:

```json
{
  "trap_ids": ["T1", "T2"],
  "givens": {
    "domain": "smib",
    "h_mj_mva": 5.0,
    "f0_hz": 50.0,
    "pm_pu": 0.9,
    "pmax_pre_pu": 2.0,
    "pmax_fault_pu": 0.5,
    "pmax_post_pu": 1.5,
    "h_s": 0.01
  },
  "steps": [
    { "id": "derive", "text": "Equal-area with staged Pmax", "delta_cr_deg": 79.53 }
  ],
  "final": { "delta_cr_deg": 79.53, "t_to_dcr_s": 0.3097 }
}
```

- **`givens`** drive engine recomputation. Detectors **abstain** (`process_status: unchecked`) when givens or numeric claims are missing. They never compare to a fixed lab JSON.
- **`trap_ids`** must be explicit (or `givens.domain` set). Topic keywords alone do not select traps.
- Text cues (`ode45`, “ignore limits”, …) are **advisories** unless a structural field (`solver_used`, `ignore_limits`, …) or a numeric mismatch confirms the trap.
- Empty traces → trap `process_status: unchecked` (not a process pass). Engine-checked runs may still label checked when `check-numeric` / simulators pass; trap **fail** always blocks checked.

## Workflow (YAML recipes)

Solve recipes include a `trap-verify` node between `check-numeric` / `web-verify` and `label-unchecked`:

```yaml
trap:
  activity: trap-verify
  needs: [web, check, solve]
label:
  activity: label-unchecked
  needs: [trap, check, web]
```

Kernel output: `runs/<id>/evidence/trap_prm.json` with `outcome_pass`, `process_pass`, `process_score`, and per-trap `checks[]` (`trap_id`, `passed`, `offending_step`, `message`).

## MCP / CLI for hosts

| Path | Use |
|------|-----|
| Recipe `trap-verify` | Automatic when running a solve workflow |
| `electrical-engineer` workflow with `problem.json` → `solution_trace` | Host-supplied trace in problem payload |
| `python scripts/trap_prm_contract.py` | Contract plus ablation metrics (CI / scorecard) |

Planned MCP verb (same payload as the activity): submit `solution_trace` on the run before `label`.

## Host actions on failure

If `process_pass` is false:

1. Surface `offending_step` and `message` to the model (course correction).
2. Re-run the Arc engine for that domain; do not patch only the final number.
3. Keep `unchecked: true` until a passing `trap_prm.json` exists.

If `outcome_pass` is false but process passed, fix numerics against golden or engine output.

## Automated traps (this pass)

Detectors ship for **T1, T2, T3, T4, T5, T6, T7, T9, T10** (see `artifacts/frontier/trap_suite_index.json`). T8 (diagram signal flow) remains host/visual validation until Control Studio exports a machine-readable trace.

## Metrics contract

```bash
python scripts/generate_trap_prm_eval.py   # engine-only corpus (61+ cases)
PYTHONPATH=src python scripts/trap_prm_contract.py
```

Emits `eval_metrics` (precision/recall per trap, abstain rate, false-positive rate on correct traces) from `eval/fixtures/trap_prm/eval_traces.json`. Regenerate the eval file when engines change; do not tune detectors against it.

### Workflows without `label-unchecked`

`solve-*` and `study-*` recipes with `web-verify` include `trap-verify`. `symmetrical-fault-study` includes `trap-verify` before summary (numeric label is `check-numeric`; trap still writes `trap_prm.json` and blocks checked via evidentiary inputs when wired).

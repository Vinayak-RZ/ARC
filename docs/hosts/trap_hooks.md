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
  "topic": "smib",
  "trap_ids": ["T1", "T2"],
  "steps": [
    { "id": "derive", "text": "Equal-area with staged Pmax", "delta_cr_deg": 79.53241 }
  ],
  "final": {
    "delta_cr_deg": 79.53241,
    "text": "Student-facing summary",
    "expected": { "delta_cr_deg": 79.53240997193419 },
    "outcome_tolerance": 0.01
  }
}
```

- `steps` plus `final` are the trace. Each step may carry numeric fields the detectors read (`delta_cr_deg`, `cct_s`, `P2_mw`, `delta_f1_hz`, …).
- `expected` in `final` is optional; when present it powers the **outcome** score separate from **process**.

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

## Ablation contract

```bash
python scripts/trap_prm_contract.py
```

Emits:

```json
{
  "traps_automated": ["T1", "T2", "..."],
  "hook_contract_path": "docs/hosts/trap_hooks.md",
  "ablation": { "outcome_only_pass_rate": ..., "with_verifier_pass_rate": ... }
}
```

Numbers are computed from `eval/fixtures/trap_prm/traces.json`, not hand-edited.

# AGC two-area (primary + integral AGC)

Load for **EEC-301 Exp 7** style two-area load-frequency control: governor–turbine–
swing–tie–ACE. OSS twin only (no Simulink in CI).

## Given / find

1. Identify **primary** (K=0) vs **AGC** (K>0) run.
2. Confirm `f0 = 60 Hz` and `B = β = 1/R + D` per area (trap **T4**).
3. Load step timing: step at `t = 1 s`, report `t_after_step` for dips.

## Capabilities

- Steady primary: `analytic_primary_steady()` or `simulate_two_area(..., run="primary")`.
- AGC transient: `simulate_two_area(..., run="agc")` with `TwoAreaAgcCase.with_k(0.3)`.
- Gain sweep / stability: `gain_sweep()` — expect **K=1** diverges.

## ACE / tie (trap T4)

- `ACE1 = B1·Δf1 + ΔP12` (not `−ΔP12` on Area 1).
- `ACE2 = B2·Δf2 − ΔP12`.
- Tie: `dΔP12/dt = 2·(Δf1 − Δf2)` with PDF `two_pi_T12 = 2`.

## Primary vs AGC (trap T5)

- Primary leaves **Δf ≈ −0.16 Hz** and **ΔP12 ≈ −45 MW** after 100 MW Area-1 step.
- AGC restores **Δf → 0**, **ΔP12 → 0**, Area 1 carries **~100 MW** steady gen.
- Do not expect AGC to erase the **first frequency dip** (integral is slow).

## Goldens

`artifacts/eec301-lab-goldens/exp07.json` · parity `docs/planning/eec301-lift/EXP7_SIMULINK_PARITY.md`.

## Spawn

`ee-power` + `skills/power/SKILL.md` for context; load this skill for AGC prompts.

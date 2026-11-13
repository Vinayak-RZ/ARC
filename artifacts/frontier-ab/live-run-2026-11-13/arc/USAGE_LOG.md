# Arc usage log — held-out sheet live run (2026-11-13)

Install: `uv sync --extra dev --extra engines` from repo root (pip-first equivalent via README). CLI: `uv run electrical-engineer …`.

## P1 — SMIB CCT (Arc-covered)

| Item | Detail |
|------|--------|
| Commands | `uv run electrical-engineer run smib-swing-study` with `problem.json` SMIB overrides; `uv run electrical-engineer eval --pack power` (smib-eec301-01 PASS) |
| Skills / traps | `skills/swing-equation/SKILL.md`; traps T1 (stage Pmax), T2 (RK grid / no ode45) |
| Engine | `electrical_engineer.engines.smib_swing` — `eec301_reference`, `time_to_angle_during_fault`, `critical_clearing_time_bisection`, RK4 h=1e-5 |
| Worked | δ₀, δ_cr, t_cr match workflow output `runs/*/psa_smib.json` (δ_cr 78.317°) |
| Friction | Workflow bisection uses h=0.001 s by default; sheet asks stated step — used h=1e-5 in engine calls for reported t_cr |

## P2 — SMIB clearing check (Arc-covered)

| Item | Detail |
|------|--------|
| Commands | Engine call only (no dedicated recipe); same `problem.json` case as P1 |
| Skills / traps | `skills/swing-equation/SKILL.md` |
| Engine | `smib_swing.simulate_clearing(tc=0.25 s, h=1e-5, t_end=5 s)` |
| Worked | Stable; max δ ≈ 102.06° (< 180°) |
| Friction | None |

## P3 — Economic dispatch (Arc-covered)

| Item | Detail |
|------|--------|
| Commands | `uv run electrical-engineer run ed-lambda-study` (default EEC-301 units only); custom coeffs via `ed_lambda.solve_lambda_ed` |
| Skills / traps | `skills/economic-dispatch-lambda/SKILL.md`; T6 limits, T7 IC factor 2 |
| Engine | `ed_lambda.EdCase.from_coeff_lists` + `solve_lambda_ed(case, PD=900)` |
| Worked | P1=350, P2=250, P3=300 MW, λ=9.8 Rs/MWh |
| Friction | `run ed-lambda-study` ignores per-sheet b,c,Pmin,Pmax — only `PD` from `problem.json`; wrong dispatch if workflow used blindly (observed λ≈8.88, ΣP=570 for PD=900 on default units) |

## P4 — Two-area primary AGC (partly covered)

| Item | Detail |
|------|--------|
| Commands | `uv run electrical-engineer run agc-two-area-study` (EEC-301 100 MW @ 60 Hz case, not this sheet) |
| Skills / traps | `skills/agc-two-area/SKILL.md`; T4 ACE sign |
| Engine | `agc_two_area.analytic_primary_steady` for pu partition; manual f0=50 Hz scaling |
| Worked | Δf≈−0.0595 Hz, ΔP12≈−25 MW from β=21, ΔPL=50 MW, 1000 MVA base |
| Friction | No `problem.json` hook for custom β or 50 MW step / f0=50; `analytic_primary_steady` returns `df_hz` using **60 Hz**; full `simulate_two_area` is different machine data than simplified sheet |

## P5 — Control margins (partly covered)

| Item | Detail |
|------|--------|
| Commands | `uv run electrical-engineer run solve-control-problem` with `num`/`den` in `problem.json` |
| Skills | `skills/control/SKILL.md` (via pack) |
| Engine | `control_runner.run_control_plots` — plots only; margins via `import control; control.margin` (dev extra) |
| Worked | ω_gc≈4.47 rad/s, PM≈43.2°, ω_pc≈1.56 rad/s, GM≈6 dB |
| Friction | Workflow does not emit crossover/margin numbers; value field is step steady-state (misleading for this ask) |

## P6 — Series RLC transient (not covered)

| Item | Detail |
|------|--------|
| Commands | `uv run electrical-engineer run simulate-circuit` with handcrafted `.cir` |
| Skills | circuits pack / `knowledge/ug-ee/maths/02-ode-linear-systems` |
| Engine | ngspice path **not available** — `spice` node `unchecked: true`, error path `ngspice/PySpice not available` |
| Worked | User-side ODE integration (scipy) after ζ, ωn classification |
| Friction | No checked Arc transient engine for this RLC numeric ask in CI |

## P7 — SLG symmetrical components (partly covered)

| Item | Detail |
|------|--------|
| Commands | `uv run electrical-engineer eval --pack power` (lg-01 PASS); `run simulate-power-fault` **crashed** |
| Skills | `skills/power/SKILL.md` |
| Engine | `power_runner._sequence_fault` |
| Worked | 4.286 pu, 7.498 kA |
| Friction | `simulate-power-fault` with string `z1_pu` → `ValueError: complex() arg is a malformed string` |

## P8 — Induction motor EC (not covered)

| Item | Detail |
|------|--------|
| Commands | None applicable |
| Skills | `skills/machines/SKILL.md` (conceptual) |
| Engine | `drives_study` / `im_slip_torque` — rated slip/torque only, **not** exact equivalent circuit |
| Worked | Manual complex impedance solve |
| Friction | No Arc engine for exact 6-parameter IM EC at arbitrary slip |

## Summary

| Problem | Coverage |
|---------|----------|
| P1 | Arc-covered |
| P2 | Arc-covered |
| P3 | Arc-covered |
| P4 | Partly (kernel formula; not sheet-parameter workflow) |
| P5 | Partly (plots workflow; margins manual via python-control) |
| P6 | Not covered (no ngspice) |
| P7 | Partly (engine function; CLI fault workflow broken for z string) |
| P8 | Not covered |

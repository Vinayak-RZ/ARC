# Exp 7 — Simulink Fig. 1 parity notes (OSS twin)

Arc ships `electrical_engineer.engines.agc_two_area` as an **RK4 OSS twin** of the
EEC-301 Simulink model (governor → turbine → swing → tie → ACE integral).

## Block mapping

| Simulink (conceptual) | OSS state / equation |
|-----------------------|----------------------|
| Governor | `dxg/dt = (−Δf/R − u − xg)/Tg`, `u = K·∫ACE` |
| Turbine | `dxm/dt = (xg − xm)/Tt` |
| Generator / load | `M·dΔf/dt = xm − ΔPL − D·Δf ± ΔP12` |
| Tie line | `dΔP12/dt = 2·(Δf1 − Δf2)` (`tie_sync_gain=2`) |
| ACE area 1 | `ACE1 = B1·Δf1 + ΔP12` |
| ACE area 2 | `ACE2 = B2·Δf2 − ΔP12` |

**Sign law (trap T4):** positive ΔP12 is export from Area 1; Area 1 power balance
subtracts tie flow; Area 2 adds it.

## Parameters (PDF)

- `f0 = 60 Hz`, `SB = 1000 MVA`
- Area 1/2: `Tg, Tt, M, D, R`, `B = β = 1/R + D`
- Load step: **+100 MW** (`0.1 pu`) in Area 1 at `t = 1 s`

## What matches tightly

| Metric | Lab JSON | OSS twin tolerance |
|--------|----------|-------------------|
| Primary Δf | −0.160 Hz | ±2 mHz |
| Primary ΔP12 | −45.07 MW | ±0.5 MW |
| AGC SS Δf, ΔP12 | ≈0 | ±0.1 mHz / ±0.01 MW |
| AGC SS Pm1 | ≈100 MW | ±0.05 MW |
| First dip (AGC) | −0.411 Hz | ±2 mHz |
| Peak tie (AGC) | −17.52 MW | ±0.05 MW |

## Known residuals

- Primary steady `Pm` shares differ ~0.1 MW from analytic β partition (damping).
- First-dip **time** is step-sensitive; compare `t_after_step` not absolute clock.
- `K = 1.0` **must** diverge (`run4_gain_sweep`); `Kcr ≈ 0.74` in lab notes.

Golden authority: `artifacts/eec301-lab-goldens/exp07.json`.

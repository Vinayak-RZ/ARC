# EEC-301 Exp 6 — golden reference (Arc evals)

Source: IIT Roorkee EEC-301 Software Laboratory, Experiment 6 (parameter table).

## Case data

| Quantity | Value |
|----------|-------|
| H | 5.0 MJ/MVA |
| f₀ | 50 Hz |
| Pm | 0.9 pu |
| Pmax pre / fault / post | 2.0 / 0.5 / 1.5 pu |

## Analytical (equal-area)

| Quantity | Expected | Tolerance (Arc tests) |
|----------|----------|------------------------|
| δ₀ | 26.74° (0.4668 rad) | ±0.05° |
| δmax | 143.13° (2.4981 rad) | ±0.05° |
| δcr | 79.53° (1.3881 rad) | ±0.05° |
| cos δcr | 0.1817 | ±0.002 |

Computed via `electrical_engineer.engines.smib_swing` (`eec301_reference`, `critical_clearing_angle`).

## Critical clearing time (RK4 bisection)

| Quantity | Lab table | Tolerance |
|----------|-----------|-----------|
| tcr | 0.3097 s | ±2 ms |

Method: bisection on tc with instability = first-swing peak δ > π rad within 2 s window; RK4 with **h = 0.0005 s**; tc aligned to integer multiple of h (lab procedure §5). Clearing angle at tcr matches δcr within angle tolerance when integrated during-fault only.

## Integrators

Euler, modified Euler (Heun), and RK4 are implemented explicitly. **No** `ode45`, SciPy `solve_ivp`, or MATLAB built-in solvers in the kernel helper path.

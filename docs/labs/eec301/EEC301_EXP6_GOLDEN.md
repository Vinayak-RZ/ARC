# EEC-301 Exp 6 — golden reference (Arc evals)

**Authority:** `artifacts/eec301-lab-goldens/exp06.json` (lab pack, PDF-matching).

## Case data

| Quantity | Value |
|----------|-------|
| H | 5.0 MJ/MVA |
| f₀ | 50 Hz |
| Pm | 0.9 pu |
| Pmax pre / fault / post | 2.0 / 0.5 / 1.5 pu |

## Equal-area (full precision)

| Quantity | Lab JSON | PDF table (rounded) |
|----------|----------|---------------------|
| δ₀ | 26.743683950403007° | 26.74° |
| δmax | 143.13010235415598° | 143.13° |
| δcr | 79.53240997193419° | 79.53° |
| cos δcr | 0.18167930768699725 | 0.1817 |

Kernel: `eec301_reference()` / `critical_clearing_angle()` must match JSON
`equal_area` within floating noise (< 1e-9° in CI).

## Critical clearing time

| Metric | Value | Notes |
|--------|-------|-------|
| tcr (bisection, lab pack) | **0.3096875 s** | `cct_bisection.tcr_s`; PDF prints 0.3097 s |
| t to δcr (during-fault RK4) | 0.30971631056004756 s | h = 1×10⁻⁵; primary analytic cross-check |
| Arc headline | **≈ 0.309688 s** | Use lab JSON, not invented rounding |

**Tests:** `time_to_angle_during_fault` at lab `h` vs JSON; kernel bisection within **2 ms**
of `cct_bisection.tcr_s` (integrator/grid sensitivity).

## Integrators

Euler, modified Euler (Heun), and RK4 only in kernel. No `ode45` / `solve_ivp` (trap T9).

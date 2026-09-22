# Economic dispatch — λ iteration

Load for **EEC-301 Exp 8** quadratic cost dispatch with limits.

## Model

- Fuel: `C_i(P) = a_i + b_i P + c_i P²` (MW, Rs/hr style coefficients as lab).
- IC: `dC/dP = b_i + 2 c_i P` — **factor 2** on `c` (trap **T7**).
- Unconstrained: `P_i = (λ − b_i)/(2 c_i)`, solve λ from `Σ P = P_D`.

## Algorithm (trap T6)

1. Start all units **free**.
2. Solve λ on free set; clip to `[Pmin, Pmax]`.
3. Fix limited units; **recompute λ on residual demand** — do not leave stale λ.
4. KT check at max: need `IC_i ≤ λ` when at `Pmax` (Unit 2 @ PD=500: IC2=7.30 < λ).

## Forbidden (trap T9)

No `scipy.optimize.minimize`, `linprog`, or `fmincon` when the lab requires
hand λ-iteration.

## Kernel

`electrical_engineer.engines.ed_lambda.solve_lambda_ed(EdCase.eec301_default(), PD)`.

Goldens: `artifacts/eec301-lab-goldens/exp08.json` (450 / 500 / 300 MW).

## Spawn

`ee-power` pack.

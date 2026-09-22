# T2 — CCT clearing model / step alignment

**Domain:** SMIB numerical CCT (EEC-301 Exp 6) · Trap catalog T2

## Failure modes (bare agent)

1. Switch Pmax at `t ≤ tc` vs `t < tc` inconsistently → effective clearing shifts by **one step**.
2. Choose **h** so `tc/h` is **not** an integer → method comparison corrupted (PDF procedure §5).
3. Declare CCT from “peak δ = δmax” instead of bisection on **δ > 180°** instability, or skip
   **during-fault-only** integration until δ = δcr (PDF step 10).
4. Report analytical **δcr** as if it were a **time**.

## Lab truth (do not invent)

From `artifacts/eec301-lab-goldens/exp06.json`:

| Check | Value |
|-------|-------|
| `cct_bisection.tcr_s` | **0.3096875 s** (PDF table 0.3097 s) |
| `time_to_delta_cr.t_to_dcr` | 0.30971631056004756 s (RK4, h = 1×10⁻⁵) |
| Agreement | Within ~1 ms (bisection vs during-fault time) |

Headline for Arc docs: **tcr ≈ 0.309688 s**.

## Arc path

1. `simulate_clearing()` — align clearing to step grid; fault for `t < tc`, post thereafter.
2. `time_to_angle_during_fault()` + `critical_clearing_time_bisection()` cross-check.
3. CI: `test_exp06_cct_time_to_delta_cr_matches_lab_json`, `test_exp06_cct_bisection_lab_value_documented`.

## Bare-agent prompt that should fail

> “Estimate CCT with ode45 and tc=0.3097 s off-grid step 0.01.”

Forbidden solver + misaligned switch (T9 overlap).

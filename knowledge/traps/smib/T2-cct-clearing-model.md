# T2 — CCT clearing model / step alignment

**Domain:** SMIB numerical CCT (EEC-301 Exp 6)

## Symptom

- Uses `ode45` or `solve_ivp` when the lab forbids built-in solvers.
- Switches from fault to post-fault **between** RK4 stages without landing
  \(t_c\) on a step boundary (effective clearing time shifts by \(h/2\)).
- Declares instability at \(\delta > 180^\circ\) on a **post-fault** sample only,
  ignoring that clearing angle at \(t_c\) must match \(\delta_{\mathrm{cr}}\) check.

## Why it fails

Procedure step 5 requires \(t_c/h\) integer so all methods see the same
clearing instant. Bisection must use the **same** integrator and step as the
reported tables. CCT from angle-only (parabolic \(\delta(t)\) with \(P_e=0\))
is invalid when \(P_{\max}^{(2)}=0.5\neq 0\).

## Arc path

1. `simulate_clearing()` aligns clearing to `round(tc/h)*h`.
2. `critical_clearing_time_bisection()` + `time_to_angle_during_fault()` cross-check.
3. Golden: \(t_{\mathrm{cr}}\approx 0.3097\) s at default data (`EEC301_EXP6_GOLDEN.md`).

## Bare-agent prompt that should fail

> “Estimate CCT with ode45 and tc=0.3097 s off-grid step 0.01.”

Forbidden solver + misaligned switch.

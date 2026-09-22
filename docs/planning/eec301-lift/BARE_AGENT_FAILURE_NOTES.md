# Bare-agent failure notes — EEC-301 Exp 6–8

Concrete places a **generic coding agent without a domain kernel** gets wrong.
These feed Arc skills / knowledge traps / golden evals (plan traps T1–T10).

---

## T1 — Equal-area uses wrong Pmax stage (Exp6)

**Failure mode:** Compute δcr with a single Pmax, or swap fault/post amplitudes:
`cos δcr = (Pm(δmax−δ0) + Pmax_post cos δmax − Pmax_fault cos δ0) / (Pmax_post − Pmax_fault)`.
Using Pmax_pre=2.0 in the denominator/numerator, or setting Pmax_fault=0 “for a bolted fault”
when the PDF gives 0.5, shifts δcr by many degrees (e.g. ~79.5° → wrong).

**Also:** δmax = π − arcsin(Pm/Pmax_post) must use **post-fault** Pmax=1.5, not pre-fault 2.0.

**Lab truth:** δ0=arcsin(0.9/2.0)≈26.74°, δmax≈143.13°, δcr≈79.53°, cos δcr≈0.1817.

---

## T2 — CCT clearing model / step off-by-one (Exp6)

**Failure modes:**
1. Switch Pmax at `t ≤ tc` vs `t < tc` inconsistently → effective clearing shifts by one step.
2. Choose h so `tc/h` is **not** an integer → method comparison corrupted (PDF §Procedure 5).
3. Declare CCT from “peak δ = δmax” instead of bisection on **δ > 180°** instability, or
   forget to verify by integrating **during-fault only** until δ=δcr.
4. Report analytical δcr as if it were a time.

**Lab truth:** tcr≈0.3097 s; during-fault time-to-δcr must agree within ~1 ms of bisection.

---

## T3 — H vs M and frequency base (Exp6 / Exp7)

**Failure modes:**
- Swing form: PDF uses `dΔω/dt = (π f0 / H)(Pm − Pe)`. Agents often write `ωs/(2H)` with
  `ωs=2πf0` correctly (= πf0/H) **or** wrongly use `f0/H`, `2πf0/H`, or treat Δω in Hz.
- Confuse inertia constant **H** (MJ/MVA) with AGC area inertia **M** (pu·s) — different models.
- Exp7: report Δf in pu as Hz (forget ×60), or use f0=50 from Exp6 inside the Exp7 twin (PDF: 60 Hz).

---

## T4 — ACE / bias B ≠ β; tie sign (Exp7)

**Failure modes:**
- ACE1 = B1 Δf1 − ΔP12 (wrong sign) or both areas use +ΔP12.
- Set B = 1/R only (omit D) or B = D only; PDF requires B = β = 1/R + D (20.6 and 16.9).
- Tie: `dΔP12/dt = 2πT12 (Δf1−Δf2)` with gain **2** on the integrator; agents use T12=2 directly.
- Positive ΔP12 means Area1→Area2; power balance must subtract P12 from Area1 and add to Area2.

---

## T5 — Primary vs secondary dynamics (Exp7)

**Failure modes:**
- Expect AGC to change the **first frequency dip** as much as the steady state (integral is slow).
- With K=0, claim Δf→0 “because governors regulate”; governors leave steady Δf = −ΔPL/(β1+β2).
- Move load to Area2 but still expect Area1 to permanently carry it under AGC with correct B=β.

---

## T6 — ED limits / Kuhn–Tucker / λ update (Exp8)

**Failure modes:**
- Ignore Pmin/Pmax; for PD=500 report all-free λ and P2>150.
- Fix a unit at limit but **do not** recompute λ on the residual demand / free set.
- Check KT backwards: at Pmax, need IC ≤ λ (unit would like to produce more); agents assert IC=λ always.
- Hard-code N=3 inside the solver (PDF: general N).

**Lab truth:** PD=500 → P2=150, λ≈7.3923, IC2=7.30 < λ; PD=450 interior λ≈7.1737.

---

## T7 — Incremental cost / fuel cost units (Exp8)

**Failure modes:**
- Use Ci = ai + bi Pi + ci Pi^2 but set IC = bi + ci Pi (missing factor 2).
- Minimize sum bi Pi (linear) or treat ai as affecting dispatch (ai cancels in IC; affects UC only).
- Mix Rs/hr totals with Rs/MWh λ when reporting “savings”.

---

## T8 — Pretty but wrong signal-flow diagrams (Exp7)

**Failure modes:** Draw droop feedback into the turbine instead of governor; put ACE integral
after the tie only; omit opposite-sign tie injection; label B as “bias in Hz” without pu MW/pu Hz.

---

## T9 — Forbidden solvers (all exps)

**Failure modes:**
- Exp6: call `scipy.integrate.solve_ivp` / ode45 and call it “RK45 reference” for the **student** methods.
- Exp8: `scipy.optimize.minimize` / linprog / CVXPY instead of λ-iteration.
- Exp7: claim Simulink-only so ship an empty folder; or use a DAE solver without documenting parity.

**Lab rule:** Euler / ME / RK4 handwritten; λ closed-form + limit loop; Exp7 = OSS twin + parity notes.

---

## T10 — Silent wrong defaults (Pm, Pmax stages, PD)

**Failure modes:** Default Pm=1.0, Pmax_fault=0, f0=60 in Exp6; swap Area Tg/Tt; PD=400 “because round”;
fabricate goldens to match PDF table without running the integrator.

**Lab rule:** PDF data wins; residual documented if transient metrics differ by solver.

---

## How these map to Arc

| Trap | Skill / engine | Golden |
|------|----------------|--------|
| T1 | equal-area helper + Pmax stage validation | exp06.json equal_area |
| T2 | CCT bisection + during-fault time-to-δcr | exp06.json cct_* |
| T3 | unit guard H/M/f0 | swing RHS coeff test |
| T4–T5 | AGC twin + scenario knowledge | exp07.json runs |
| T6–T7 | λ-ED solver with KT | exp08.json cases |
| T9 | constraint knowledge in host card | “no ode45/fmincon” |
| T10 | engine input validation | param schemas |

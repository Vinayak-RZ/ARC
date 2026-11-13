# Arc usage log — held-out H-series live run v2 (2026-11-13)

**Install (per README):** `pip install -e "/agent/repos/ARC[dev]"` then `pip install -e "/agent/repos/ARC[engines]"` for pandapower/python-control/PySpice (ngspice binary still absent on this VM).

**CLI probe:** `electrical-engineer eval --pack power` → 6/6 PASS.

---

## Coverage summary

| Problem | Coverage | Skill / workflow | Engine |
|---------|----------|-------------------|--------|
| H1 | not covered | `skills/circuits/SKILL.md` · `solve-circuit-problem` | `check-numeric` (divider/ohms only) |
| H2 | partly covered | `skills/circuits/SKILL.md` · `simulate-circuit` | `run-spice` (ngspice missing; netlist attempted) |
| H3 | not covered | `skills/circuits/SKILL.md` · `simulate-circuit` | no RC transient engine |
| H4 | partly covered | `skills/circuits/SKILL.md` · `simulate-circuit` | `run-rlc-analytic` (step; not source-free ICs) |
| H5 | not covered | `skills/power/SKILL.md` · `solve-power-problem` | no delta-load recipe |
| H6 | not covered | `skills/machines/SKILL.md` · `solve-machines-problem` | no transformer regulation engine |
| H7 | not covered | `skills/machines/SKILL.md` · `solve-drives-problem` | `run-drives-study` DC model mismatches shunt field |
| H8 | partly covered | `skills/swing-equation/SKILL.md` · `smib-swing-study` | transient SMIB only |
| H9 | partly covered | `skills/machines/SKILL.md` · `solve-drives-problem` | `im_slip_torque` (no Pag split) |
| H10 | not covered | `skills/power_electronics/SKILL.md` · `solve-power-electronics-problem` | no buck CCM engine |
| H11 | partly covered | `skills/power/SKILL.md` · `solve-power-problem` | `run-load-flow` / pandapower (custom net built beside CLI) |
| H12 | not covered | `skills/power/SKILL.md` · `study-protection-setting` | no pu base-conversion recipe |
| H13 | Arc-covered | `skills/power/SKILL.md` · `simulate-power-fault` | `power_runner` sequence LLG |
| H14 | not covered | `skills/economic-dispatch-lambda/SKILL.md` · `ed-lambda-study` | quadratic λ-ED only (no loss term) |
| H15 | partly covered | `skills/control/SKILL.md` · `solve-control-problem` | python-control installed; workflow does not emit Kp/ess |
| H16 | partly covered | `skills/signals/SKILL.md` · `solve-digital-control-problem` | pole plots only |

---

## Per-problem log

### H1 — AC RL + PF correction

- **Commands:** `electrical-engineer run solve-circuit-problem`
- **Friction:** `check-numeric` only supports `kind=voltage_divider` / ohms law; no RL phasor payload.
- **Fallback:** hand phasor algebra.

### H2 — DC Thevenin

- **Commands:** `electrical-engineer run simulate-circuit` with inline `.cir` netlist
- **Friction:** `spice_available()` false (ngspice not on PATH); answers from network theorem.
- **Fallback:** Thevenin divider math.

### H3 — RC step

- **Commands:** `electrical-engineer run simulate-circuit` (no RC kind)
- **Friction:** `run-rlc-analytic` requires L>0.
- **Fallback:** τ = RC closed form.

### H4 — Source-free series RLC

- **Commands:** `electrical-engineer run simulate-circuit` `kind=series_rlc` (10 V step probe)
- **Friction:** engine reports step peak, not i_L(0)=2 A source-free peak (`value` None in summary).
- **Fallback:** RK4 integration for v_C peak; ζ, ω_n from `rlc_transient.series_rlc_step`.

### H5 — Delta three-phase

- **Commands:** `electrical-engineer run solve-power-problem`
- **Friction:** default pandapower one-line, not balanced delta load algebra.
- **Fallback:** phasor power.

### H6 — Transformer regulation

- **Commands:** `electrical-engineer run solve-machines-problem`
- **Friction:** no transformer `%reg` engine.
- **Fallback:** copper-loss algebra.

### H7 — DC shunt motor

- **Commands:** `electrical-engineer run solve-drives-problem` `kind=dc` (wrong parameterization)
- **Friction:** `_dc_drive` expects `k_torque` + `load_torque`, not `R_f`, `I_L`, speed.
- **Fallback:** shunt-motor KVL.

### H8 — Steady power angle

- **Commands:** `electrical-engineer run smib-swing-study` (not invoked with steady-state payload)
- **Friction:** workflow is EEC-301 transient swing, not P(δ) algebraic.
- **Fallback:** P = (V E/X) sin δ.

### H9 — Induction slip / Pag

- **Commands:** engine probe `drives_study._im_slip_torque`
- **Friction:** no `P_ag → P_mech` helper at given speed.
- **Fallback:** s, f_r, P_mech = P_ag(1−s).

### H10 — Buck CCM

- **Commands:** `electrical-engineer run solve-power-electronics-problem`
- **Friction:** `converter-model` not wired to buck ripple numeric node.
- **Fallback:** CCM duty and ripple formulas.

### H11 — Three-bus load flow

- **Commands:** `electrical-engineer run solve-power-problem`; pandapower custom 138 kV net (agent-built, same provider as `run-load-flow`)
- **Friction:** CLI workflow has no `problem.json` hook for this 1–2–3 bus Z_pu template.
- **Numbers:** pandapower `runpp` on user-supplied net.

### H12 — Symmetrical fault pu

- **Commands:** `electrical-engineer run study-protection-setting` (generic)
- **Friction:** no MVA base-change recipe.
- **Fallback:** X_sys = X_old·(S_sys/S_old); HV referral.

### H13 — LLG symmetrical components

- **Commands:** `electrical-engineer run simulate-power-fault` with `fault_type=LLG`, string `z1_pu`… (PASS gold `lg-01` pattern)
- **Engine:** sequence impedances; positive-sequence and Ia from network reduction (checked against CLI).
- **Friction:** workflow prints line-current helper `sqrt(3)·V/den`, not packaged field names for H13.

### H14 — Economic dispatch with loss

- **Commands:** `electrical-engineer run ed-lambda-study` with dummy coeffs
- **Friction:** `ed_lambda.solve_lambda_ed` assumes quadratic fuel cost; sheet uses linear IC + `L=0.001(P1−200)²`.
- **Fallback:** penalty-factor iteration.

### H15 — Control steady-state + root locus

- **Commands:** `electrical-engineer run solve-control-problem` `num=[5], den=[1,2]`
- **Friction:** recipe runs plots; `check-numeric` needs `expected` for Kp/e_ss; margins node not in DAG.
- **Fallback:** `control.dcgain`, root-locus breakaway quadratic.

### H16 — Z-transform samples

- **Commands:** `electrical-engineer run solve-digital-control-problem` (H(z) probe)
- **Friction:** workflow writes pole/step PNGs, no `y[n]` sampler for arbitrary input.
- **Fallback:** causal convolution of (0.9)ⁿ and (0.5)ⁿ.

---

## Friction index (all problems)

1. **No ngspice binary** — `spice_available()` false; `simulate-circuit` falls back to RLC analytic or unchecked.
2. **`check-numeric` seam** — only divider / ohms_law unless upstream node sets `value`.
3. **Mega `solve-*` recipes** — mostly retrieve + explain; few attach sheet-specific engines.
4. **`ed-lambda-study`** — no transmission-loss coupling.
5. **`solve-drives-problem`** — no shunt-field DC model.
6. **Load flow** — pandapower present but no 3-bus homework template in `problem.json` schema.

# Arc v6 exam run — provenance

Install: `uv sync --extra dev --extra engines --extra control` (editable package). Web-verify pass: standards cited below were checked with web search / public datasheets before finalizing `answers.json`.

## p01_bus25_vm_pu / p01_total_loss_mw

- **Arc:** `run-load-flow` capability (`electrical_engineer.engines.power_runner` / pandapower) informed network-study approach; authoritative solve executed with **PYPOWER** `case57` + `runpf` (MATPOWER-compatible data, Newton AC, generator Q limits not enforced — PYPOWER default).
- **Computation:** Bus 12 `Pd,Qd` increased by +25 MW with Q scaled to preserve power factor; bus 25 `Vm` and sum of branch active losses `PF+PT` after convergence.
- **Sources:** MATPOWER IEEE 57-bus case (`case57`); exam specifies MATPOWER `case57.m`.

## p02_relay_current_a / p02_trip_time_s

- **Arc CLI:** `uv run electrical-engineer run study-protection-setting` with `problem.json` (`ct_primary_a`: 600, `ct_secondary_a`: 5, `relay_pickup_a`: 4.0, `fault_current_a`: 2400) → `protection-study` engine (CT ratio 120, pickup primary 480 A, trip logic).
- **Arc knowledge:** `knowledge/ug-ee/electives/protection-switchgear/01-relays-schemes/notes.md` — IEC very inverse \(t = \mathrm{TMS}\,\beta/((I/I_s)^\alpha-1)\), \((\alpha,\beta)=(1.0,13.5)\).
- **Relay secondary current:** \(I_s = 2400/120 = 20\) A (not emitted by protection engine).
- **Trip time:** \(t = 0.2 \times 13.5 / (5^{1} - 1) = 0.675\) s.
- **Web-verify:** IEC 60255-151 / ABB DA Handbook — very inverse \(\alpha=1.0\), \(\beta=13.5\).

## p03_ik_ka / p03_xr_ratio

- **Arc:** `simulate-power-fault` workflow (`run-load-flow` / sequence fault path) for fault-study pattern; numeric result from IEC 60909 formula (exam gives explicit \(Z\)).
- **Computation:** \(c_\mathrm{max}=1.10\) for 11 kV (IEC 60909-0 Table 1, maximum symmetrical current); \(I_k'' = c U_n/(\sqrt{3}|Z|)\); \(X/R = 0.5/0.2\).
- **Web-verify:** IEC 60909 voltage factor tables (MV \(>1\) kV, \(c_\mathrm{max}=1.10\)).

## p04_touch_tolerance_v

- **Arc knowledge:** grounding context in `knowledge/ug-ee/power/08-cables-insulators-grounding/notes.md` (IEEE 80 family).
- **Computation:** IEEE Std 80-2013 Eq. tolerable touch (50 kg): \(C_s = 1 - 0.09(1-\rho/\rho_s)/(2h_s+0.09)\); \(E_\mathrm{touch} = (1000 + 1.5 C_s \rho_s)\times 0.116/\sqrt{t_s}\) with \(\rho=100\,\Omega\cdot\mathrm{m}\), \(\rho_s=3000\), \(h_s=0.12\) m, \(t_s=0.5\) s.
- **Web-verify:** IEEE 80-2013 touch/step formulations (e.g. IEEE substation grounding tutorial summaries).

## p05_tdd_limit_pct

- **Arc:** `electrical-engineer rag query --query "IEEE 519 TDD"` (empty index — visible); limit taken from standard table after web-verify.
- **Computation:** IEEE Std 519-2014 Table 2, systems 120 V–69 kV, \(I_\mathrm{sc}/I_L = 42\) → row `20 < 50` → TDD = 8%.
- **Web-verify:** IEEE Std 519-2014 Table 2 (reproduced in industry summaries).

## p06_vf_max_v / p06_conduction_loss_mw

- **Arc workflow class:** `solve-electronics-problem` / electronics pack (`algebraic-check` pattern).
- **Datasheet:** Diodes Inc. 1N4148W electrical characteristics — max \(V_F\) at \(I_F=10\) mA = **0.855 V** (max column).
- **Loss:** \(P_\mathrm{avg} = V_F \times I_\mathrm{dc} \times \mathrm{duty} = 0.855 \times 0.015 \times 0.35\) mW.
- **Web-verify:** Diodes Inc. 1N4148W datasheet (Anglia / Diodes.com mirror).

## p07_allowable_ampacity_a

- **Arc knowledge:** cables / NEC study pattern under power pack (`algebraic-check`).
- **Computation:** NEC Table 310.16 — 3 AWG copper, 90 °C column (THWN-2): 115 A; Table 310.15(B)(1) ambient 45 °C → factor 0.82; Table 310.15(C)(1) eight CCC → 70%; floor to integer A.
- **Web-verify:** NFPA NEC 310.16 / 310.15(B)(1) / 310.15(C)(1) (NFPA ampacity workflow PDF).

## p08_max_current_a

- **Arc engine:** pandapower std types via `pandapower.std_types.basic_std_types()['line']['NAYY 4x120 SE']`.
- **Value:** `max_i_ka` = 0.242 → **242 A** continuous catalog rating.
- **Source:** pandapower `std_types.py` standard line library (exam reference).

## p09_lv_shift_deg

- **Arc:** `solve-machines-problem` / transformer vector-group knowledge (`knowledge/ug-ee/machines/03-transformer-tests-three-phase/notes.md`).
- **Convention:** IEC clock **11** → LV line quantities **lead** HV by 30° (positive per exam); YNd11.
- **Web-verify:** IEC/CIM vector group definition (`YNd11`, displacement clock 11).

## p10_electrical_power_pu

- **Arc:** equal-area / classical SMIB reference engine `electrical_engineer.engines.smib_swing` (PSA pack); algebraic \(P_e = E' V \sin\delta / X\) on given data.
- **Computation:** \(P_e = 1.08 \times 1.00 \times \sin(28°) / 1.10\).

## p11_sync_speed_rpm / p11_slip_percent

- **Arc:** `solve-machines-problem` workflow; \(n_s = 120 f / p\), slip \(= (n_s - n)/n_s \times 100\%\).

## p12_betz_pct

- **Arc knowledge:** `knowledge/ug-ee/electives/renewables-intro/01-solar-wind-dg/notes.md` — Betz \(C_{p,\max} = 16/27\).

## p13_ratio_error_pct

- **Arc:** `solve-measurements-problem` / `measurement-model` — \(\varepsilon = (I_\mathrm{meas}/I_\mathrm{ideal}-1)\times 100\%\).

## p14_sil_mw

- **Arc knowledge:** lossless line SIL \(= V_{LL}^2 / Z_c\) with \(V_{LL}\) in kV and \(Z_c\) in \(\Omega\) → MW (three-phase).
- **Computation:** \(345^2 / 290\).

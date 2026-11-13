# Arc usage log — held-out exam (live-run-v3)

**Install:** `pip install -e '.[dev,engines]' --user` from repo root (on branch `cursor/reference-library-0bf6`).

**CLI:** `electrical-engineer reference {search,get,engine}`; Python `electrical_engineer.engines.ed_lambda`; pandapower via `load_flow` engine dependency.

**Wall time:** ~2 min 10 s (start `2026-11-13T11:20:41Z`, finish `2026-11-13T11:22:50Z`).

---

## p01 — IEEE 14-bus AC losses

| Item | Detail |
|------|--------|
| Reference | `IEEE_CASE_14` (`reference get` / search) |
| Engine / commands | `reference engine load_flow '{"case_id":"IEEE_CASE_14"}'`; pandapower `case14()` + `runpp` for gen+ext_grid−load loss |
| Coverage | **Partly** — `load_flow` confirms convergence but does not emit `loss_mw`; loss from pandapower results (same stack the engine uses) |
| Friction | No loss field on reference `load_flow` output; manual post-processing required |

## p02 — IEC IDMT coordination

| Item | Detail |
|------|--------|
| Reference | `IEC_SI` (curve A), `IEC_VI` (curve B) |
| Engine / commands | `reference engine idmt` with `i_ratio=7`, `tms=0.15` on `IEC_VI`; `idmt_operating_time_s` for primary TMS from CTI=0.25 s |
| Coverage | **Fully** (curve constants + formula via reference engine) |
| Friction | No `reference engine coordination` CLI; margin solved in Python with `idmt_operating_time_s` |

## p03 — IEC 60909 Ik″

| Item | Detail |
|------|--------|
| Reference | `IEC60909_CMAX_LV` (c=1.1) |
| Engine / commands | `reference engine iec60909 '{"voltage_kv":11,"z_ohm":0.18,"c_factor_id":"IEC60909_CMAX_LV"}'` |
| Coverage | **Fully** |
| Friction | None |

## p04 — ACSR Zebra inductance

| Item | Detail |
|------|--------|
| Reference | `ACSR_ZEBRA` (GMR 0.01058 m) |
| Engine / commands | `reference get ACSR_ZEBRA`; `L = 0.2*ln(6.0/GMR)` mH/km per problem; cross-check `line_params` X at 6 m spacing |
| Coverage | **Fully** (GMR from catalog; closed form from sheet) |
| Friction | `line_params` returns X/R/C, not the syllabus L=0.2 ln(D/GMR) directly |

## p05 — MCB Type B magnetic band

| Item | Detail |
|------|--------|
| Reference | `MCB_TYPE_B` |
| Engine / commands | `reference get MCB_TYPE_B`; lower withstand = `magnetic_multiple_min × In` = 3×40 A |
| Coverage | **Fully** (band from record; lower bound is engineering interpretation of IEC table) |
| Friction | `mcb` engine tests instantaneous band membership, not “withstand lower bound” as a named output |

## p06 — IEEE 80 touch voltage

| Item | Detail |
|------|--------|
| Reference | `IEEE80_BODY_70KG` |
| Engine / commands | `reference engine ieee80 '{"body_id":"IEEE80_BODY_70KG","rho_s_ohm_m":200,"cs":1,"t_s":0.4}'` |
| Coverage | **Fully** (simplified engine form documented in record) |
| Friction | Touch/step identical in engine; not full IEEE 80 mesh equations |

## p07 — IEEE 519 TDD

| Item | Detail |
|------|--------|
| Reference | `IEEE519_TDD_BAND_20_50` (Isc/Il=35 → 8% limit) |
| Engine / commands | `reference engine ieee519 '{"isc_il_ratio":35}'`; TDD = √(90²+45²)/1200×100 |
| Coverage | **Partly** — limit from Arc; harmonic TDD sum is manual |
| Friction | Catalog cites IEEE 519-2014 Table 3; problem cites 519-2022 Table 2 (band 8% at ratio 35 assumed same); no `tdd_percent` engine |

## p08 — Dyn11 phase shift

| Item | Detail |
|------|--------|
| Reference | `VECTOR_DYN11` |
| Engine / commands | `reference engine vector_group '{"group_id":"VECTOR_DYN11"}'` |
| Coverage | **Fully** |
| Friction | None (trap −30° documented)

## p09 — NEMA code G locked-rotor current

| Item | Detail |
|------|--------|
| Reference | `NEMA_CODE_G` (upper kVA/hp 6.29) |
| Engine / commands | `reference get NEMA_CODE_G`; I = S_ll / (√3·460) at 75 hp |
| Coverage | **Partly** — band from Arc; amperes not a reference engine |
| Friction | No machines engine for LRC from code letter |

## p10 — IEGC frequency band

| Item | Detail |
|------|--------|
| Reference | `IEGC_FREQ_BAND` (49.9–50.05 Hz) |
| Engine / commands | `reference get IEGC_FREQ_BAND`; width = f_max − f_min |
| Coverage | **Fully** (numeric width is trivial on record values) |
| Friction | None |

## p11 — Case9 lambda economic dispatch

| Item | Detail |
|------|--------|
| Reference | `IEEE_CASE_9`; costs from pandapower `case9` `poly_cost` (MATPOWER case9) |
| Engine / commands | `ed_lambda.EdCase.from_coeff_lists` + `solve_lambda_ed(PD=315)`; gen 3 out of scope (only two `gen` rows in case) |
| Coverage | **Partly** — dispatch kernel is Arc; cost coefficients via pandapower net, not `reference engine` |
| Friction | No `reference engine economic_dispatch`; case9 in pandapower has 2 gens + ext_grid, not 3 explicit units |

## p12 — IRF540N conduction loss

| Item | Detail |
|------|--------|
| Reference | `MOSFET_IRF540N_RDSON` (0.077 Ω max) |
| Engine / commands | `reference get MOSFET_IRF540N_RDSON`; P = I²R = 144×0.077 |
| Coverage | **Partly** — Rds(on) from Arc; loss not a reference engine |
| Friction | None |

## p13 — IEC 60909 κ and ip

| Item | Detail |
|------|--------|
| Reference | `IEC60909_CMAX_LV`; κ formula IEC 60909-0 eq. (57) **outside Arc** |
| Engine / commands | `reference engine iec60909` on Z=0.05+j0.45 Ω; κ=1.02+0.98·exp(−3R/X); ip=κ√2·Ik″ |
| Coverage | **Partly** — Ik″ fully; κ/ip only `KAPPA_PEAK_FACTOR` teaching point at R/X=10, not a calculator |
| Outside Arc | [Logoscalc / IEC 60909-0:2016 §8.1.1 eq. (57)](https://www.logoscalc.com/en/blog/iec-60909-peak-short-circuit-current-kappa) for κ(R/X) |

## p14 — Zebra 75 °C resistive drop

| Item | Detail |
|------|--------|
| Reference | `ACSR_ZEBRA` (`r_ac_ohm_per_km_75c`) |
| Engine / commands | `reference engine line_params '{"conductor_id":"ACSR_ZEBRA","length_km":50,"temp_c":75,"spacing_m":6}'`; V_LL = √3·I·R_phase |
| Coverage | **Fully** for R; drop formula manual |
| Friction | None

---

## Coverage summary

| Problem | Coverage |
|---------|----------|
| p01 | Partly |
| p02 | Fully |
| p03 | Fully |
| p04 | Fully |
| p05 | Fully |
| p06 | Fully |
| p07 | Partly |
| p08 | Fully |
| p09 | Partly |
| p10 | Fully |
| p11 | Partly |
| p12 | Partly |
| p13 | Partly |
| p14 | Fully |

## Friction list (aggregate)

1. **`load_flow`:** no network loss MW (p01).
2. **`line_params`:** no direct mH/km inductance field (p04).
3. **`mcb`:** band check API, not named lower-bound withstand (p05).
4. **`ieee519`:** limit lookup only; no TDD calculator; edition label 2014 vs 2022 on sheet (p07).
5. **No coordination / ED / LRC / κ engines** in reference CLI (p02 margin, p09, p11, p13).
6. **`IEEE_CASE_9`:** pandapower case has two gens; third unit unavailable per sheet is implicit (p11).

## Outside Arc

| Use | Reason |
|-----|--------|
| IEC 60909 κ = 1.02 + 0.98·e^(−3R/X) | Not implemented as reference engine (p13) |
| Pandapower gen−load arithmetic | p01 loss |
| Harmonic RSS for TDD | p07 |
| `ed_lambda.solve_lambda_ed` | p11 (non-reference engine) |

## Verification

- `pytest tests/unit/test_reference_engines.py` — 8 passed.
- Reference CLI engines exercised for idmt, iec60909, ieee80, ieee519, vector_group, mcb, line_params, load_flow.

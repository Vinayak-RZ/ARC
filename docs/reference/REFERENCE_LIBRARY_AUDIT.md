# Reference library audit (post-exam remediation)

Audit of all records after exam failures (12/19). Each row lists status, confidence, and material value changes.

## Summary

| Status | Count |
| --- | ---: |
| verified (changed values) | 8 |
| verified (unchanged) | 28 |
| removed | 7 |
| added | 1 |
| **Active records** | **41** |

## Removed records

| ID | Reason |
| --- | --- |
| WSCC9_GEN_INERTIA_GEN2 | Only one weak open table; no dual authoritative reproduction |
| TEMP_COEFF_CU | Duplicate of Al coeff without independent Cu citation this pass |
| SVERAK_GRID_RESISTANCE_FORMULA | No numeric golden; formula-only left to problem data |
| NEMA_DESIGN_B | Unsourced typical slip |
| IE3_MOTOR_CLASS | No per-rating numeric without nameplate |
| XFMR_Z_PU_TYPICAL_DIST | Wide range, not exam-grade factual |
| KAPPA_PEAK_FACTOR | Replaced by `IEC60909_KAPPA_XR10` with corrected kappa |

## Record audit table

| ID | Status | Old → New (material) | Confidence |
| --- | --- | --- | --- |
| ACSR_ZEBRA | **changed** | GMR 0.01058→**0.01144** m; R75 0.0789→**0.0856** Ω/km | verified_dual |
| ACSR_DOG | **changed** | Re-tabulated IS 398 dual source | verified_dual |
| ACSR_DRAKE | **changed** | Conditions clarified; GMR unchanged | verified_dual |
| TEMP_COEFF_AL | **changed** | α 0.00393→**0.00403** /°C (IS 398) | verified_dual |
| IEEE_CASE_9 | **changed** | Links `IEEE_CASE_9_GENCOST`; warns on poly_cost | verified_dual |
| IEEE_CASE_9_GENCOST | **added** | MATPOWER mpc.gencost rows buses 1–3 | verified_dual |
| IEEE_CASE_14 | verified | — | verified_dual |
| IEEE_CASE_30 | verified | — | verified_dual |
| MOSFET_IRF540N_RDSON | **changed** | max 77 mΩ→**44 mΩ @ 25°C**; split typ/hot fields | verified_dual |
| DIODE_LOSS_FORMULA_COND | verified | formula only | single_source |
| IEEE80_BODY_50KG | **changed** | `k_factor` → `k_touch`/`k_step` 0.157 | verified_dual |
| IEEE80_BODY_70KG | **changed** | touch uses **0.157**; step **0.313** (fixes 643 V bug) | verified_dual |
| IEC60909_KAPPA_XR10 | **changed** | kappa 1.73→**1.632** at R/X=0.1 | verified_dual |
| IEC60909_* (c, Kt) | verified | — | verified_dual / single_source |
| IEEE519_* bands | **changed** | Labelled **IEEE Std 519-2022 Table 2** | verified_dual |
| IEEE519_2022_TABLE2_HEADER | **added** | Edition metadata | verified_dual |
| MCB_TYPE_* | verified | exposes `magnetic_trip_lower_in_a` in engine | verified_dual |
| IEC curves / IEEE CO-* | verified | constants unchanged | verified_dual |
| NEMA_CODE_G | verified | — | verified_dual |
| VECTOR_* | verified | — | verified_dual |
| course_context * | verified | pointers only | verified_dual |
| IEGC_FREQ_BAND | verified | — | verified_dual |
| IS12360_KV_11 | verified | — | single_source |
| CTI_NORM | verified | — | single_source |

## Engine fixes

| Engine | Fix |
| --- | --- |
| `ieee80` | Touch vs step split; Eq. 32 uses `k_touch` |
| `line_params` | Adds `l_mh_per_km`; Zebra IS 398 R/GMR |
| `load_flow` | Adds `network_loss_mw` |
| `economic_dispatch` | **New** — MATPOWER gencost rows, OOS buses |
| `iec60909_peak` | **New** — kappa and `ip_ka` |
| `nema_locked_rotor` | **New** — code-letter I_lr |
| `ieee519` | `tdd_compliance` with 2022 Table 2 label |
| `mcb` | Named lower/upper magnetic multiples |

## Golden tests

See `tests/unit/test_reference_golden.py` (IEEE 80 touch 322.71 V, case9 ED λ≈33.06, IEC 60909 peak chain, IEEE 519 compliance, NEMA code G).

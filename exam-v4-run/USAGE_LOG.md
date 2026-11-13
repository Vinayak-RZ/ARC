# Exam v4 — Arc usage log

**Branch:** `cursor/arc-v4-exam-run`  
**Wall time:** 138 s (branch checkout → answers committed)  
**Install:** `uv sync --extra dev --extra engines`

## Summary of Arc vs web disagreements

| Problem | Arc / engine | Web / other | Trusted |
|---------|--------------|-------------|---------|
| P04 | No Moose record | GMR 12.67 mm (Engineering Devotion + Janaki) | Web GMR |
| P08 | No YNd5 vector record | IEC clock 5 → −150° (DEIF, DATSAN) | Web |
| P10 | No IEEE_CASE_39 | pandapower case39 + MATPOWER | pandapower |
| P11 | No IEEE_CASE_30_GENCOST | MATPOWER mpc.gencost rows | MATPOWER + ed_lambda |
| P12 | No FGH40N60SFD record | onsemi max V_CE(sat) 2.9 V | Datasheet |
| P13 | `iec60909_peak` default κ=1.632 (XR10) | κ=1.5231 from Eq. 57 at R/X=0.222 | IEC Eq. 57 |
| P14 | R75 table 0.347 vs α-scaled 0.341 | IS table AC column | Table 0.347 |

---

## Per-problem

### p01
- **Arc:** `reference search case30`; `reference engine load_flow` → `IEEE_CASE_30`
- **Web:** MATPOWER case30.m, UW PSTCA

### p02
- **Arc:** `reference get IEC_VI`, `IEC_EI`; `reference engine idmt`
- **Python:** primary TMS from coordination interval
- **Web:** IEC 60255-151 publication index

### p03
- **Arc:** `reference get IEC60909_CMAX_LV`; `reference engine iec60909`
- **Web:** IEC 60909-0 Table 1 c_max

### p04
- **Arc:** search moose (empty)
- **Python:** L = 0.2 ln(GMD/GMR)
- **Web:** Engineering Devotion (GMR 1.267 cm); Janaki IS 398 Moose row

### p05
- **Arc:** (no cable record)
- **Python:** 96×0.87×0.38
- **Web:** IEC 60364-5-52 B.52.14 (Ca 0.87 @ 40°C); problem Ci=0.38

### p06
- **Arc:** `reference get IEEE80_BODY_50KG`; `reference engine ieee80`

### p07
- **Arc:** `reference engine ieee519`; band `IEEE519_TDD_BAND_LT20`
- **Python:** TDD magnitude from I₃, I₉

### p08
- **Arc:** search (no YNd5); convention from IEC 60076 clock
- **Web:** DEIF, DATSAN vector group tables

### p09
- **Arc:** `induction_motor._n_sync_rpm` (in-repo engine)
- **Web:** IEC 60034 synchronous speed identity

### p10
- **Arc:** search case39 (empty)
- **Python:** pandapower case39 load flow
- **Web:** MATPOWER case39.m, PSTCA

### p11
- **Arc:** `ed_lambda.solve_lambda_ed` (engines package); costs from MATPOWER via web
- **Web:** raw case30.m gencost rows 1–2

### p12
- **Arc:** search FGH (empty)
- **Python:** I×VCEsat max
- **Web:** onsemi + Fairchild datasheets (2.9 V max)

### p13
- **Arc:** `reference engine iec60909` for Ik″
- **Python:** κ = 1.02+0.98·exp(−3R/X); ip = κ√2 Ik″
- **Web:** pandapower + LogosCalc IEC 60909 κ article

### p14
- **Arc:** `reference get ACSR_DOG`, `TEMP_COEFF_AL`; `reference engine line_params`
- **Python:** √3 I R L drop with table R75
- **Web:** Janaki + Lumino IS 398 Dog resistance

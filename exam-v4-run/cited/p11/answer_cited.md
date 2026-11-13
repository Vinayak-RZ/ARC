# P11 — Lossless λ-dispatch (case30 gens 1 & 2)

**Answers:** `gen1_mw` = **84.96**, `gen2_mw` = **104.24**, `lambda_usd_per_mwh` = **5.40**

## Arc

- `reference get IEEE_CASE_30`; `reference search gencost` → only `IEEE_CASE_9_GENCOST` (no case30 gencost record)
- `electrical_engineer.engines.ed_lambda.solve_lambda_ed` with MATPOWER mpc.gencost rows for gens at buses 1 & 2 (lossless, no limits):

| Bus | c2 | c1 | c0 |
|-----|-----|------|-----|
| 1 | 0.020 | 2.00 | 0 |
| 2 | 0.0175 | 1.75 | 0 |

## Web verification

- [MATPOWER case30.m gencost block](https://raw.githubusercontent.com/MATPOWER/matpower/master/data/case30.m) — quadratic coefficients for rows 1–2
- λ equality: c₁ + 2c₂P₁ = c₁′ + 2c₂′P₂ with P₁+P₂ = 189.2 MW

## Disagreements

Arc `economic_dispatch` engine could not run (no `IEEE_CASE_30_GENCOST` id); used in-repo `ed_lambda` solver with web-sourced costs. Unconstrained λ solution (Pmax 80 MW each would cap at 160 MW < 189.2 MW load — standard lossless ED assumes infinite limits unless stated).

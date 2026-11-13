# P13 — Peak short-circuit (κ)

**Answers:** `kappa_factor` = **1.5231**, `peak_current_ka` = **81.61**

## Arc

- `reference get IEC60909_CMAX_LV`
- `reference engine iec60909` with Z = 0.04 + j0.18 Ω @ 11 kV → Ik″ = 37.887 kA
- **Did not use** `reference engine iec60909_peak` default `IEC60909_KAPPA_XR10` (κ = 1.632 for R/X = 0.1, wrong for this fault)

## Web + Python

- κ from IEC 60909-0 Eq. 57: **κ = 1.02 + 0.98·e^(−3·R/X)** with R/X = 0.04/0.18 = 0.2222
- Sources: [pandapower ip documentation](https://pandapower.readthedocs.io/en/latest/shortcircuit/ip.html), [LogosCalc κ article](https://www.logoscalc.com/en/blog/iec-60909-peak-short-circuit-current-kappa)
- ip = κ·√2·Ik″

## Disagreements

| Quantity | Arc default peak engine | Trusted |
|----------|------------------------|---------|
| κ | 1.632 (`KAPPA_XR10`) | **1.5231** (from fault R/X) |
| ip (kA) | ~87.6 | **81.61** |

Used web IEC Eq. 57 for κ; Arc catalog kappa id is only valid for R/X ≈ 0.1.

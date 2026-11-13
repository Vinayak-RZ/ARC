# P07 — IEEE 519-2022 TDD

**Answers:** `tdd_percent` = **7.55 %**, `meets_tdd_limit` = **1**

## Arc

- `reference engine ieee519 '{"isc_il_ratio":15,"measured_tdd_percent":7.5522605}'`
- TDD magnitude (Python): √(I₃² + I₉²)/I_L × 100 = √(55²+25²)/800×100

## Web verification

- [IEEE Std 519-2022](https://standards.ieee.org/standard/519-2022.html) — Table 2 TDD vs I_SC/I_L
- Arc band `IEEE519_TDD_BAND_LT20` limit **12 %** for I_SC/I_L = 15 (< 20)

## Disagreements

None.

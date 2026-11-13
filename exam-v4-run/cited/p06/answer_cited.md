# P06 — IEEE 80 tolerable step voltage

**Answer:** `tolerable_step_v` = **364.9 V**

## Arc

- `reference get IEEE80_BODY_50KG`
- `reference engine ieee80 '{"body_id":"IEEE80_BODY_50KG","rho_s_ohm_m":250,"cs":1,"t_s":0.35}'`
- Step uses k_step = 0.157 (same as k_touch for 50 kg record)

## Web verification

- [IEEE Std 80-2013](https://standards.ieee.org/standard/80-2013.html) — Eq. 32/35 family; (1000 + 1.5·Cs·ρ_s)·k/√t
- Manual check: (1000 + 1.5·250)·0.157/√0.35 = **364.9 V**

## Disagreements

None.

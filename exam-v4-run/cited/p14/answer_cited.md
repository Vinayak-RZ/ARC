# P14 — ACSR Dog voltage drop

**Answer:** `line_line_drop_kv` = **2.254 kV**

## Arc

- `reference get ACSR_DOG`, `reference get TEMP_COEFF_AL`
- `reference engine line_params` (confirms r = 0.347 Ω/km at 75 °C key)
- Drop (Python, resistive only): ΔV_LL = √3 · I · R_75 · L

## Web verification

- [Janaki IS 398 PDF](https://janakicable.com/media/hlmpxhae/basic-data-for-aluminium-conductors-steel-reinforced-acsr-as-per-is-398-part-ii-1996.pdf) — Dog R20 = 0.2792 Ω/km
- [Lumino IS 398 PDF](https://luminoindustries.com/wp-content/uploads/2024/04/IS-398-PART-II-1996.pdf) — corroborates Dog row

## Disagreements

| R at 75 °C | Value (Ω/km) | Notes |
|------------|--------------|-------|
| Arc table `r_ac_ohm_per_km_75c` | **0.347** | Used for answer |
| Linear α from R20 (Arc `TEMP_COEFF_AL` 0.00403) | 0.341 | Ignores AC/skin; **0.347** retained per IS table column |

ΔV = √3 × 150 × 0.347 × 25 / 1000 = **2.254 kV**

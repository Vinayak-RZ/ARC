# P04 — Moose line inductance

**Answer:** `inductance_mh_per_km` = **1.313 mH/km**

## Arc

- `reference search moose` — **no catalog record** (Moose not in `conductors.yaml`)
- Python: L = 0.2·ln(GMD/GMR) with GMD = 9.0 m, GMR from web-verified tables

## Web verification (GMR)

- [Engineering Devotion bundled-conductor drill](https://www.engineeringdevotion.com/electric-power-systems/solved-problems/bundled-conductors-problems.html) — Moose GMR = **1.267 cm** (12.67 mm)
- [Janaki Cable IS 398 Part II PDF](https://janakicable.com/media/hlmpxhae/basic-data-for-aluminium-conductors-steel-reinforced-acsr-as-per-is-398-part-ii-1996.pdf) — Moose overall diameter 31.77 mm, R20 0.05595 Ω/km (cross-check code word)

Calculation: L = 0.2·ln(9.0/0.01267) = **1.313 mH/km**

## Disagreements

Arc library has **no Moose conductor**; used dual-sourced GMR (Engineering Devotion + Janaki IS 398 geometry). No Arc numeric to disagree with.

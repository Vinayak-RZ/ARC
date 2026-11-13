# P09 — Induction motor slip

**Answers:** `synchronous_speed_rpm` = **1500**, `slip_percent` = **1.6 %**

## Arc

- No nameplate-only slip workflow in `reference engine`; used `electrical_engineer.engines.induction_motor._n_sync_rpm` formula (120·f/poles) via Python driver

## Web verification

- [IEC 60034-1 rotating machines](https://webstore.iec.ch/en/publication/3277) — synchronous speed n_s = 120f/p (4-pole, 50 Hz → 1500 r/min)
- Slip s = (n_s − n)/n_s × 100 = (1500 − 1476)/1500 × 100 = **1.6 %** (identity check)

## Disagreements

None.

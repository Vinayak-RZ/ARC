# P08 — YNd5 phase shift

**Answer:** `hv_to_lv_phase_shift_deg` = **-150**

## Arc

- `reference search YNd` — only `VECTOR_DYN11`, `VECTOR_YD1` in library (no YNd5 record)
- Python / standards convention: clock **5** → LV lags HV by 5×30° = 150° → **−150°** relative to HV reference

## Web verification

- [DEIF vector group handbook](https://documentation.deif.com/r/agc-150-generator-mains-btb-designers-handbook-4189341307-uk/general-functions/step-up-and-step-down-transformers/vector-group-for-step-up-transformer) — YNd5: **−150°** phase shift, 150° LV lag
- [DATSAN transformer vector groups](https://datsan.com.tr/en/technical-library-transformer/transformer-vector-groups-explained) — clock 5 = 150° lag for YNd5

## Disagreements

Arc library lacks YNd5 entry; trusted IEC 60076-1 clock notation from web sources over absent Arc record.

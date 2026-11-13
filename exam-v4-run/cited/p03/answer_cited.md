# P03 — IEC 60909 Ik″

**Answer:** `ik3_symmetrical_ka` = **74.849 kA**

## Arc

- `reference get IEC60909_CMAX_LV` (c = 1.1 for 1–35 kV)
- `reference engine iec60909 '{"voltage_kv":33,"z_ohm":{"re":0.28,"im":0}}'`

## Web verification

- [IEC TR 60909-4 / 60909-0 publications](https://webstore.iec.ch/en/publication/24172) — voltage factor c_max = 1.1 for MV
- [IEC TR 60909-4 examples](https://webstore.iec.ch/en/publication/28674) — Ik″ = c·U_n/(√3·|Z|) chain

## Disagreements

None.

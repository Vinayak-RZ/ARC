# P02 — IDMT coordination

**Answers:** `backup_operating_time_s` = **0.5334 s**, `primary_relay_tms` = **0.647**

## Arc

- `reference search very inverse` → `IEC_VI`; `reference get IEC_VI`
- `reference search extremely inverse` → `IEC_EI`; `reference get IEC_EI`
- `reference engine idmt '{"curve_id":"IEC_VI","tms":0.18,"i_ratio":5.5555555556}'`
- Python (coordination algebra): `t_primary = t_backup − 0.20 s`; invert EI curve for TMS at I/Ipickup = 12.5

## Web verification

- [IEC 60255-151 publication](https://webstore.iec.ch/en/publication/6762) — inverse curve families (constants k, α from library match SI/VI/EI tables in protection texts)
- [IEEE C37.112-1996](https://standards.ieee.org/standard/C37_112-1996.html) — secondary check on inverse-time formulation (not used for this IEC problem)

## Disagreements

None (library `IEC_VI` k=13.5, α=1; `IEC_EI` k=80, α=2 match IEC 60255-151 textbook values).

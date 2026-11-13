# Reference library skill

Use when a problem names a **standard symbol, curve, conductor, test case, or limit table** instead of giving numbers. Arc stores open/factual records under `src/electrical_engineer/reference/data/`.

## Retrieve (mandatory triggers)

| Problem mentions | Action |
| --- | --- |
| IEC SI / VI / EI, IEEE CO-8, "standard inverse" | `arc_reference_search` then `arc_reference_get`; run `reference engine idmt` with curve id |
| IEC 60909, c factor, Ik'' | get `IEC60909_CMAX_LV` or `CMIN`; engine `iec60909` |
| Dog / Wolf / Zebra / Drake ACSR | get conductor id (`ACSR_ZEBRA`); engine `line_params`; cite temp (20 °C vs 75 °C) |
| IEEE 9 / 14 / 30 bus | get `IEEE_CASE_*`; `load_flow` (includes `network_loss_mw`) |
| case9 economic dispatch | get `IEEE_CASE_9_GENCOST`; engine `economic_dispatch` — **not** pandapower poly_cost |
| MCB type B/C/D trip | get `MCB_TYPE_*`; engine `mcb` |
| IEEE 519 TDD | band id or `ieee519` with Isc/Il ratio |
| Dyn11 / Yd1 | get `VECTOR_*`; engine `vector_group` — **do not flip sign** |
| IEEE 80 touch/step | engine `ieee80` — requires `kind` and `body_mass_kg`; k=0.116/0.157 by weight only |
| IEC 60909 peak ip | engine `iec60909_peak` after Ik'' |
| NEMA code letter I_lr | get `NEMA_CODE_*`; engine `nema_locked_rotor` |
| NEC 310.16 / 310.15 ampacity + derating | get `NEC_TABLE_310_16_CU_90C`, `NEC_TABLE_310_15B1_AMBIENT`, `NEC_TABLE_310_15C1_ADJUSTMENT`; engine `nec_ampacity` |
| EEC-301 Exp 6–8 | get `EEC301_EXP*` pointer; use existing PSA workflows |

Never guess curve constants, conductor R, or c factors. If `get` returns missing, say so and check `docs/reference/GAPS.md`.

**Provenance:** `arc_reference_get` is not a web-verify. Do not write `Web-verify:` in the answer until `arc_web_evidence_submit` (or the workflow `web-verify` node) stored session evidence with URL, snippet, and timestamp. Otherwise label **unverified (from memory)**.

## CLI

```text
electrical-engineer reference search "Zebra"
electrical-engineer reference get IEC_SI
electrical-engineer reference engine idmt '{"curve_id":"IEC_SI","tms":0.1,"i_ratio":10}'
```

## Traps (eval-aligned)

1. **IEC vs IEEE IDMT:** different formulas — use `values.standard` on the record.
2. **c factor omitted:** Ik'' without c is wrong for IEC 60909 wording.
3. **GMR vs radius:** line reactance uses GMR (bundled formula in engine).
4. **75 °C vs 20 °C R:** conductor record keys differ; state which you used.
5. **Dyn11:** HV-to-LV shift is **-30°**, not +30°.

Cite `source.title`, `edition`, `clause`, and `verification` in student-facing answers.

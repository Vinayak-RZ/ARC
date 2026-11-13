# Protection and standards pack

Load for study-level protection, coordination, relay settings, and normative tables (IEC/IEEE/NEC), not live EMS or field commissioning.

## When to use which engine or reference

| Task | Capability / engine | Reference record |
|------|---------------------|------------------|
| IDMT pickup / time | `algebraic-check` or `study-protection-setting` | `arc_reference_get` on curve id (IEC SI/VI/EI, IEEE CO-8) |
| Symmetrical / LG fault current | `simulate-power-fault` | IEC 60909 c factor via `IEC60909_CMAX_LV` |
| Distance zone reach | `study-protection-setting` with `zone_reach_ohm` | Line params via `line_params` engine |
| MCB / fuse coordination (paper) | `algebraic-check` | `MCB_TYPE_B/C/D` records |
| Touch / step (study) | `reference engine ieee80` | Requires `kind` and `body_mass_kg` |
| Vector group for differential | `reference engine vector_group` | `VECTOR_DYN11` etc. |

Full table triggers: `skills/reference/SKILL.md`. Power SLD + fault inset: `skills/ui-diagrams/SKILL.md`.

## Provenance honesty

`arc_reference_get` is curated open data, not live web proof. Do not write `Web-verify:` or `web-verified` unless the same run stored evidence via `arc_web_evidence_submit` or the workflow `web-verify` node (URL + quoted snippet + timestamp). Otherwise label **unverified (from memory)**. Run `electrical-engineer provenance audit <answer.md>` before submitting.

Missing provider or unknown constant → exact token `unchecked`, never a fluent relay setting.

## Benchmarks

Trap-aligned items: `knowledge/traps/` (protection units). Workflow goldens: `eval/gold/` protection-related recipes. IEC/IEEE coverage gaps: `docs/reference/GAPS.md`.

## Retrieve (scaffold)

Filters: book_id, chapter_id, domain_tag. Index: `knowledge/ug-ee/power/INDEX.md` (protection units). Call `retrieve` for handbook citations; call `arc_reference_*` for tables.

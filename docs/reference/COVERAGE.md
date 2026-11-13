# Reference library coverage

Generated from `src/electrical_engineer/reference/data/*.yaml`. Run `uv run python -c "from electrical_engineer.reference.catalog import list_domains; print(list_domains())"` to refresh counts.

| Domain | Records | Engines / notes |
| --- | ---: | --- |
| standard_test_systems | 4 | `load_flow` on IEEE_CASE_9/14/30 (pandapower MATPOWER loaders) |
| overcurrent_protection | 7 | `idmt` IEC/IEEE curves; CT class metadata; CTI norm |
| short_circuit | 4 | `iec60909` Ik'' with c and K_T |
| overhead_conductors | 5 | `line_params` R/L/C from conductor id |
| low_voltage_protection | 4 | `mcb` magnetic band check; TN disconnection time |
| earthing_safety | 3 | `ieee80` tolerable touch/step (simplified) |
| power_quality | 5 | `ieee519` TDD band lookup |
| transformers | 3 | `vector_group` phase shift (Dyn11 trap) |
| machines | 3 | NEMA code/design stubs; IE class label |
| indian_grid | 2 | IEGC frequency band; 11 kV nominal |
| course_context | 3 | Pointers to EEC-301 goldens (existing PSA engines) |
| semiconductors | 2 | Datasheet scalar + loss formula note |

**Retrieval:** `electrical-engineer reference search/get`, MCP `arc_reference_search` / `arc_reference_get`.

**Traps covered in eval:** IEC vs IEEE IDMT constants; Dyn11 sign; 75 °C vs 20 °C conductor R keys; GMR bundled vs solid radius; IEC 60909 c factor required.

# Reference library coverage

**41** active records (post-audit). Full audit: [`REFERENCE_LIBRARY_AUDIT.md`](REFERENCE_LIBRARY_AUDIT.md).

Learn course notes (EEC-301, EEC-303, EET-123, rectifier lab HTML) live under `knowledge/courses/` and are indexed by `INDEX.yaml` for the Learn page — separate from this reference-engine table. Recipe catalog size: **80** (`electrical-engineer workflows`).

| Domain | Records | Engines |
| --- | ---: | --- |
| overcurrent_protection | 7 | `idmt` |
| power_quality | 6 | `ieee519`, `tdd_compliance` |
| standard_test_systems | 4 | `load_flow`, `economic_dispatch` |
| overhead_conductors | 4 | `line_params` (+ `l_mh_per_km`) |
| low_voltage_protection | 4 | `mcb` (+ lower multiple fields) |
| short_circuit | 4 | `iec60909`, `iec60909_peak` |
| course_context | 3 | PSA workflow pointers |
| earthing_safety | 2 | `ieee80` (touch vs step) |
| indian_grid | 2 | — |
| semiconductors | 2 | — |
| transformers | 2 | `vector_group` |
| machines | 1 | `nema_locked_rotor` |

**Retrieval:** `reference get` returns `value_conditions` and `confidence` per field guidance.

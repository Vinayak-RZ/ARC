# Measurements pack

Load for electrical measurements and instrumentation: errors, uncertainty,
bridges, instrument specs, analog meters, digital meters at UG. Not driving a
physical bench (`CD-MEAS-BENCH`).

## Any question in this pack

1. Name the measurand, instrument, range, and error model (limiting error,
   probable error, loading).
2. Use `measurement-model` / `algebraic-check`. There is no “simulate the lab
   bench” provider in v1 — that path is exact token `unchecked` (`CD-MEAS-BENCH`).
3. Bridge and potentiometer circuits may use `algebraic-check`; SPICE only if
   the student supplied a netlist **and** the unknown is a circuit quantity.

## Genres

Review a lab reading for loading error. Report genre = error budget +
assumptions in `argument.md`. Never claim a live instrument was polled.

## Spawn

Host-native name: `ee-measurements`. At most two live children. CLI/MCP/UI never spawn.
Never call `evaluate_matlab_code`. Host talks only to Arc MCP.

## Retrieve (scaffold)

When: a citation, page, or handbook claim is needed.
Filters: book_id, chapter_id, domain_tag, folder_tag.
Index: TBD (empty this graph). Call `retrieve` anyway. Empty is visible. Do not
dump `knowledge/`.

## Knowledge

- `knowledge/ug-ee/measurements/INDEX.md`
- Coverage units: `knowledge/COVERAGE.yaml` pack `measurements`
- Sibling packs: electronics (instrument analog), circuits (bridges as networks)

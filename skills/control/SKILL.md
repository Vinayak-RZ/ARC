# Control pack

Load for classical UG control: models, TF/SS, stability, time response,
Bode/Nyquist/root locus, simple compensators. Not graduate optimal control.

## Any question in this pack

1. Name the plant (TF or SS), the unknown (pole, Gm/Pm, Kv, settling, PID
   gains), and assumptions (LTI, SISO unless stated).
2. Write the characteristic equation / Routh / final-value **before** plots.
3. Request capabilities:
   - `algebraic-check` for Routh, residues, gain formulas
   - `lti-analysis` for step/Bode/Nyquist/rlocus (python-control or MATLAB)
   - `render-figure` for library plots — never invent a Bode bitmap
   - `ingest-figure` for block-diagram / Bode photos (`control-diagram-to-model`,
     UI confirm, no silent sim)
   - **OSS block diagram:** `control-diagram-to-model` with `problem.json`
     `blocks[]` + `structure` (`series`/`parallel`/`feedback`) or
     `unity_feedback` → composed plant → Bode/step via python-control.
   - **Digital intro:** `solve-digital-control-problem` with discrete `num`/`den`
     and `ts`, or `continuous_*` + ZOH sample — pole plot + discrete step.
4. MATLAB-only toolboxes missing → `unchecked`, not a fake plot.

## Genres

Solve and design-to-spec use the same capabilities. Simulate means `lti-analysis`
on a typed TF/SS, not SPICE by default. Explain stays in `argument.md`.

## UI construction

Unity-feedback figures and Bode/step in the lab: **`skills/ui-diagrams/SKILL.md`**. Prefer `control_diagram.json` with `diagramKind: unity_feedback` (see example) or recipe `control-diagram-to-model`. Check artifacts before `open_ui`.

## Do not

Drop `control-diagram-to-model`. Use `simulate-circuit` for a compensator
homework unless there is actually a lumped netlist.

## Spawn

Host-native name: `ee-control`. At most two live children. CLI/MCP/UI never spawn.
Never call `evaluate_matlab_code`. Host talks only to Arc MCP.

## Retrieve (scaffold)

When: a citation, page, or handbook claim is needed.
Filters: book_id, chapter_id, domain_tag, folder_tag.
Index: TBD (empty this graph). Call `retrieve` anyway. Empty is visible. Do not
dump `knowledge/`.

## Knowledge

- `knowledge/ug-ee/control/INDEX.md`
- Coverage units: `knowledge/COVERAGE.yaml` pack `control`
- Sibling packs: signals (LTI identities), maths (Routh/Laplace), machines (plant models)

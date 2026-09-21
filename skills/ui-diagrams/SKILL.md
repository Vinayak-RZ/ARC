# UI diagrams — host method skill

Load when the student must **see** a schematic, block diagram, or one-line study figure in the Arc localhost UI (`127.0.0.1:8765`), not only a library plot file.

Normative visuals: `docs/planning/DIAGRAM_IITR_VISUAL_CONVENTIONS.md` (IITR / IITD UG EE sheet law).

Gold templates: `skills/ui-diagrams/examples/` and `eval/gold/ui-diagrams/` (must pass `scripts/check_ui_diagram_artifacts.py --examples`).

## When to use what

| Student need | Path | Artifact |
|--------------|------|----------|
| Place/edit lumped RLC (confirm topology) | `open_ui` + recipe or manual run dir | `graph.json` on run |
| Read-only IIT sheet RLC (series seed) | Write `graph.json` with `vin,r1,l1,c1,gnd` ids | UI renders `SeriesRlcSchematic` |
| Unity feedback, Bode/step below | `control-diagram-to-model` **or** write `control_diagram.json` | `diagramKind: unity_feedback` |
| Power LG/LL fault study | `simulate-power-fault` **or** write diagram | `diagramKind: power_fault` + `sequence` |
| Protection 50/51 feeder | `study-protection-setting` **or** write diagram | `diagramKind: protection_5051` + `meta` |
| DC drive chain | `solve-drives-problem` **or** write diagram | `diagramKind: drives_dc` + `meta` |
| Bode/Nyquist/step PNG only (no canvas) | `render-figure` capability | `artifact.svg` in run — **not** a substitute for blank canvas |
| Photo of student sketch | `ingest-figure` | UI confirm; then fix `graph.json` |

**Rule:** If the answer references “the diagram in Arc”, you must seed **either** `graph.json` **or** `control_diagram.json` before `open_ui`. Empty `.lab-surface` is a failed handoff.

## Agent construction steps

1. **Pick domain** (circuits / control / power / protection / drives).
2. **Copy** the matching example JSON from `skills/ui-diagrams/examples/`.
3. **Edit** numeric labels only (values, pu, CT ratio, TF text). Do not rename `diagramKind` or drop `title`.
4. **Validate** locally:
   ```bash
   python scripts/check_ui_diagram_artifacts.py --path runs/<id>/control_diagram.json
   ```
5. **Write run dir**: `evidentiary.json` (title, `recipe_id`), optional `argument.md`. Use kernel helpers or recipe `run` so `seed_run_visuals` does not fight your files (study diagrams overwrite `control_diagram.json` when recipe provides one).
6. **`open_ui`** with `?run=<id>`. For editable RLC, student uses palette; inspector is **bottom-right overlay only** — never add a left column strip.
7. **Confirm topology** before claiming sim checked (`Confirm topology` on canvas).

Programmatic paths:

- Copy template: `compose_agent_trial_run(domain, runs_root)`
- **From student prompt (no example file):** `build_artifact_from_prompt(domain)` in `electrical_engineer.ui_diagrams.build_from_prompt`
- Sidecars (plots/tables): `attach_sidecar_artifacts(domain, run_dir, payload)` — **required for control** (`bode.png`, `step.png`)

### Worked example — student prompt → JSON

**Prompt:** “Series RLC with V1=12 V, R1=470 Ω, L1=2 mH, C1=0.5 µF.”

1. Map fields → `series_rlc_graph(vin=12, r_ohm=470, l_h=2e-3, c_f=0.5e-6)` (or build nodes `vin,r1,l1,c1,gnd`).
2. Write `runs/<id>/graph.json`, `evidentiary.json` with `recipe_id: agent-ui-rlc`.
3. `python scripts/check_ui_diagram_artifacts.py --path runs/<id>/graph.json`
4. `open_ui ?run=<id>`

**Prompt:** “Unity feedback G(s)=5/(s+2), H(s)=1 — show Bode and step.”

1. Build `control_diagram.json` via `control_diagram_from_problem({blocks, unity_feedback})` with `diagramKind: unity_feedback` and title **Unity feedback system**.
2. Call `run_control_plots` (or `attach_sidecar_artifacts("control", ...)`) so `bode.png` and `step.png` exist **before** `open_ui`.
3. Checker + visual: block diagram band non-empty **and** plot images load (natural width > 80px).

See `STUDENT_PROMPTS` in `build_from_prompt.py` for all five domains.

### Self-score rubric (before `open_ui`)

| Dimension | 5 = pass | 1 = fail |
|-----------|----------|----------|
| Symbols | RLC glyphs / Σ / G / CT / CB / M visible | Generic boxes only |
| Orthogonal | Horizontal/vertical segments only | Diagonal clipart |
| Labels | `R1=…`, pu, CT ratio, TF in blocks | Missing refdes/title |
| No empty band | Ink in diagram crop | White `.lab-surface` |
| Control plots | `bode.png` + `step.png` render | Broken-image placeholders |

Target **overall ≥ 4/5**. Stress gate: `python scripts/trial_agent_ui_diagrams_stress.py`.

## IITR visual law (normative)

### Global

- Orthogonal segments only on study diagrams (renderer enforces); RLC sheet uses horizontal series + bottom return.
- **No blank diagram band** — ≥2 SVG strokes or schematic lines visible.
- **No left inspector strip** splitting the canvas; inspector overlays bottom-right on editable circuit runs.
- Study runs (`control_diagram.nodes.length > 0`) hide inspector; full-width diagram.
- Caps: **16 parts / 24 wires** on `graph.json` (`arc.circuit.v1`).

### RLC (`graph.json`)

- Nodes: `vin`, `r1`, `l1`, `c1`, `gnd` with types `source_v`, `resistor`, `inductor`, `capacitor`, `ground`.
- Labels: `V1=10 V`, `R1=1 kΩ`, `L1=1 mH`, `C1=1 µF` style via `refdes` + `value`.
- Edges: series top branch + return to GND (see example).

### Control (`diagramKind: unity_feedback`)

- Caption/title: **Unity feedback system**.
- Topology: `R(s)` → Σ (+/−) → `G(s)` (TF inside block) → `C(s)`; feedback `H(s)` from output to minus input.
- Blocks need `tf` string; include `type: sum` and `type: block` nodes.

### Power (`diagramKind: power_fault`)

- Single-line: generator **G**, thick bus, line Z labels, load, **LG** (or fault type) to ground.
- `sequence`: `{ "fault", "z1", "z2", "z0" }` for inset series network.

### Protection (`diagramKind: protection_5051`)

- Bus — CT (ratio in label) — **50/51** — CB — feeder; dashed secondary/trip path (renderer).
- `meta`: `ct_ratio`, `pickup_sec`.

### Drives (`diagramKind: drives_dc`)

- `V_a` → `R_a` → motor **M** → `T_L`; `meta`: `v_dc`, `ra_ohm`, `t_load`.

## Pre-show checklist (agent must self-check)

- [ ] `check_ui_diagram_artifacts` passes on your JSON
- [ ] `title` / caption set on study diagrams
- [ ] ≥2 visible shapes in diagram band (manual or trial script)
- [ ] Result strip does not show raw `label-unverified` chrome to students
- [ ] Bode/step plots present for control runs (recipe output), not replacing block diagram

## Anti-patterns — do not ship to student

- Empty white `.lab-surface` with only sidebar runs
- Generic rounded boxes with diagonal signal lines (use `diagramKind` + static renderer)
- `ControlDiagram` React Flow for power/protection (wrong surface)
- Left-side “Select a part…” column layout (legacy split)
- Inventing bitmap diagrams when `control_diagram.json` is required
- Skipping confirm on edited `graph.json` then claiming SPICE checked

## References

- `skills/ui-diagrams/examples/README.md`
- `docs/ui-ia.md` — agent construction path
- `docs/planning/UI_DIAGRAM_AGENT_TRIALS.md` — automated trial report
- `scripts/trial_agent_ui_diagrams.py` — compose + Playwright + Pillow gate

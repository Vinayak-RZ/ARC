# IITR / IITD UG EE diagram conventions (README media)

Reference style for Arc localhost screenshots: Nagrath & Kothari one-lines, Ogata/Nagrath unity-feedback figures, network lab RLC sheets, PSA protection SLDs.

| Domain | Renderer | Conventions |
|--------|----------|-------------|
| RLC | `SeriesRlcSchematic.jsx` | Horizontal series branch, bottom return, battery/zigzag/coil/plate/GND glyphs; labels `V1=10 V`, `R1=1 kΩ`, … |
| Control | `StaticStudyDiagram` `unity_feedback` | `R(s)` → Σ(+/−) → `G(s)` with TF inside → `C(s)`; `H(s)` on vertical feedback; orthogonal arrows only |
| Power | `power_fault` | Thick bus, generator circle **G**, line Z labels, LG fault arrow, inset Z1–Z2–Z0 series |
| Protection | `protection_5051` | Bus bar, CT donut on feeder, **50/51** block, CB square, dashed secondary/trip path |
| Drives | `drives_dc` | `V_a`, `R_a`, motor **M**, load `T_L` with orthogonal power-flow arrows |

Seeds set `diagramKind` / `title` in `control_diagram.json`. Capture: 1280×900, Pillow ink gate (`scripts/capture_readme_ui_screenshots.py`).

## Normative rules for host agents

These are enforced by skill `skills/ui-diagrams/SKILL.md` and `scripts/check_ui_diagram_artifacts.py`:

1. **Never ship an empty diagram band** — write `graph.json` or `control_diagram.json` before `open_ui`.
2. **Orthogonal only** on study figures; RLC uses the sheet schematic renderer when ids `vin,r1,l1,c1,gnd` match.
3. **Inspector** on editable circuits is bottom-right overlay only (no left strip bisecting the canvas).
4. **Study runs** use `control_diagram.json` with a valid `diagramKind` and student-facing `title`.
5. **Caps** — 16 parts / 24 wires on graphs; confirm topology before claiming simulation.
6. **Anti-patterns** — diagonal box-and-line clipart, wrong React surface for power/protection, library-only `render-figure` when the UI canvas is empty.

Templates: `skills/ui-diagrams/examples/` · Gold: `eval/gold/ui-diagrams/`.

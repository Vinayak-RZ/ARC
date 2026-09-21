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

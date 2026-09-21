# Diagram UI fix plan (PR #41)

## Goal

Every README domain screenshot (RLC, control, power, protection, drives) shows a non-empty diagram at 1280×900; circuit runs use a full-width schematic with inspector as a bottom-right overlay (no side split).

## Scope

- `ui/src/slots/root.jsx`, `tokens.css`, `Canvas.jsx`, `Inspector.jsx`
- `src/electrical_engineer/circuit/graph.py` (RLC seed layout)
- `scripts/capture_readme_ui_screenshots.py` (Pillow required, shape + ink gates)
- `docs/media/ui-*-full.png`, `README.md`, `docs/planning/README_IITR_UG_REVIEW.md`

## Non-goals

- React Flow for study diagrams (keep `StaticStudyDiagram` SVG)
- Merge PR #41

## Approach

1. **Circuit layout** — `lab-surface` stacks canvas full width; `.inspector` is `position: absolute` bottom-right with panel chrome. Raise React Flow height; RLC seed on 16px grid with horizontal series + ground return.
2. **Study diagrams** — Confirm `seed_run_visuals` → `control_diagram.json` → `/api/runs/{id}` → `Canvas` chooses `StaticStudyDiagram` when `nodes.length > 0` (not `ControlDiagram.jsx`).
3. **Capture** — Viewport 1280×900 only; clear `runs/` per shot; wait ≥2 SVG shapes or ≥2 `.part-node`; `_diagram_has_ink` **requires** Pillow (fail fast); commit five PNGs.
4. **Docs** — Refresh README media table; IITR note that diagrams render in UI.

## Acceptance (per domain)

| Domain | Recipe | Assert | PNG |
|--------|--------|--------|-----|
| RLC | `simulate-circuit` | ≥2 `.part-node` | `ui-rlc-full.png` |
| Control | `control-diagram-to-model` | ≥2 SVG shapes | `ui-control-bode-full.png` |
| Power | `simulate-power-fault` | ≥2 SVG shapes | `ui-power-fault-full.png` |
| Protection | `study-protection-setting` | ≥2 SVG shapes | `ui-protection-full.png` |
| Drives | `solve-drives-problem` | ≥2 SVG shapes | `ui-drives-full.png` |

Each PNG: height ≤1000px; center diagram band dark-pixel fraction ≥0.2% (Pillow).

## Risks

- Stale `ui/dist` → always `npm run build` before capture.
- Port 8765 busy → `fuser -k` in script.

## Commits (target)

1. `fix(ui): circuit canvas layout`
2. `fix(ui): render study/control diagrams` (if seed/API tweaks needed)
3. `fix(ui): capture + ink gate`
4. `docs: refresh README media and IITR note`

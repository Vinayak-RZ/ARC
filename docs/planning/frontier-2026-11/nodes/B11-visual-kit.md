# Node plan: B11: Arc Visual Kit

| Field | Value |
|-------|-------|
| **Node id** | `B11` |
| **Job** | Engine-driven, agent-assemblable EE visual component library with registry, MCP, goldens, visual regression |
| **Wave** | 3 (parallel with B2 to B5, B8; after A1) |
| **Depends on (data)** | `capability_delta_spec`; engine outputs from B2/B3 (PSA, control); research `05-visual-components-for-agents.md` |
| **Write paths** | `packages/visual-kit/**` or `src/electrical_engineer/visual/**`, `skills/visual-kit/`, `src/electrical_engineer/mcp/**`, `ui/src/**`, `artifacts/visual-goldens/**`, `tests/visual/**` |
| **Model** | inherit |

## Objective

Agents (and students) assemble **professional** lab figures by naming registry components and passing **engine-sourced props only**. Numbers on diagrams trace to `evidentiary.json`, never prompts. Covers schematics, block diagrams, one-line diagrams, phasors, Bode/Nyquist/root-locus, swing/equal-area, AGC traces, dispatch curves, scopes, Remotion explainer clips, optional CircuitJS embeds.

## Non-goals

- Gen-AI video (Sora/Veo/Kling) for graded labels (research #05)
- Hand-typed numeric labels in props
- Full Penrose/lcapy in CI without TeX (P2)
- Replacing ngspice truth layer

## Component catalog (P0)

| Component id | Backend | Engine binding |
|--------------|---------|----------------|
| `schematic.divider` | schemdraw | spice_runner / algebraic-check |
| `control.block_diagram` | React Flow | control_runner |
| `control.bode` | matplotlib / python-control | control_runner |
| `power.swing_equal_area` | matplotlib | smib_swing |
| `power.agc_trace` | matplotlib | agc_two_area |
| `power.dispatch_curve` | matplotlib | ed_lambda |
| `power.oneline_bus` | React Flow / custom SVG | power_runner |
| `waveform.scope` | matplotlib / Vega-Lite | signal-analysis |
| `explain.trap_callout` | Remotion still/short MP4 | trap + PSA props |
| `sim.circuitjs_embed` | CircuitJS iframe | ngspice netlist export (optional) |

Each export: `VisualSpec` JSON schema (Zod/JSON Schema), `render(props) -> { png, svg, meta }`, Storybook or preview route.

## Registry and MCP

- `visual-kit/manifest.json`: ids, description, props schema path, example props, pack tags
- Skill: `skills/visual-kit/SKILL.md` (progressive disclosure: list, schema, render)
- MCP kinds (thin): `list_visual_components`, `render_visual` (props JSON in, artifact paths out)

## Quality bar

1. **Engine bind:** 100% of numeric props in goldens from engine replay scripts (CI fails on free-text numbers).
2. **Reference parity:** Side-by-side panels vs license-clean textbook and IITR lab-sheet reconstructions (min 12 component types); max layout delta documented.
3. **Blind review:** P1 pilot 20 panels, instructor rubric "looks professional" ≥4/5 median (Gate 0 optional 15).
4. **Visual regression:** Chromatic or Playwright screenshot per component variant; ≤0.1% pixel diff vs baseline unless golden bump in PR.
5. **Cut criterion:** If a component cannot pass visual regression without flake for 3 consecutive CI runs, demote to `preview` (not advertised in registry).

## Contract

**Input:** `{ "manifest_version": "0.1", "design_tokens": "DESIGN-coinbase" }`

**Output:** `{ "visual_registry_ready": true, "golden_count": number, "mcp_smoke": true, "regression_pass": true }`

## Commits (slice of parent matrix)

| # | Commit | Gate |
|---|--------|------|
| 1 | `feat(visual): scaffold manifest and schemas` | jsonschema validate |
| 2 | `feat(visual): PSA swing and AGC components` | engine bind tests |
| 3 | `feat(visual): control bode and block diagram` | visual goldens |
| 4 | `feat(visual): mcp list/render visual` | MCP smoke |
| 5 | `test(visual): regression suite` | CI green |

May coalesce with U1 commits to honor 36 budget.

## Return to graph

Feeds **U1** (scorecard + gallery), **B9** (tutoring figures), **B10** (benchmark screenshots), **D1** (README media), **B2/B3** (data contracts).

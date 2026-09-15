# UI information architecture

Persistent localhost workspace. Not KiCad. Not a second agent. WCAG AA.

## Slots

| Slot | Role |
|------|------|
| `root` | Shell: skip-link, header with **Arc icon** (`/arc-icon.png`), engines chips (Numeric / SPICE / MATLAB · via Arc) |
| `sidebar` | Runs / Books switch. Named runs (`asset-row`) or library hint. Collapses under 640px |
| `workspace` | Selected run lab, or Books (`?view=library`) |
| `run.result` | Coinbase asset-row: title, mono value or token `unchecked`, verifier caption. Not a hero metric |
| `run.canvas` | Capped place-and-wire confirm surface (`@xyflow/react`). Palette R L C V I Gnd. Orthogonal (smoothstep) wires, 16px snap, optional 90° rotate. Writes `graph.json`. Confirm does not simulate |
| `run.inspector` | Keyboard path for refdes/value/orientation. Equal to pointer on the canvas |
| `run.argument` | Host `argument.md` as readable prose (~75ch). Must not flip `unchecked` |
| `run.more` | Closed-by-default disclosures: evidentiary JSON, plan, observation, raw graph, artifacts |
| `photo.confirm` | Confirm topology (merged into the canvas Confirm). `simulate: false` |
| `rag.inventory` | Books: ingest, tags, retrieve. `?view=library` |
| `memory.excerpt` | ≤800 char excerpt + path |
| `gates.prompt` | Ask payload; MCP never waits here |

## States

`empty` · `running` · `waiting-human` · `failed` · `done`

| State | Slot behaviour |
|-------|----------------|
| `empty` | Run list and bands show an honest empty message; no fake numbers |
| `running` | Live region announces progress; bands stay previous-or-empty |
| `failed` | Result strip uses semantic-down text; canvas stays editable |
| `waiting-human` | Live region "Waiting for topology confirm"; Confirm enabled; no modal |
| `done` | Result strip + canvas + argument; JSON/plan/observation stay in disclosures |

The canvas is **confirm only**: 16 parts / 24 wires, allowlisted R L C V I Gnd. Students place premade parts; the kernel compiles `netlist.cir`. Wires are orthogonal segments (not bezier). This window is not a schematic editor (CD-KICAD). Engines chip: MATLAB is **optional, via Arc** when the MCP binary is installed. Do not tell students to add MATLAB MCP in the host.

## Token map (DESIGN-coinbase)

| Token | CSS variable | Use |
|-------|----------------|-----|
| canvas | `--ee-color-canvas: #ffffff` | page |
| ink | `--ee-color-ink: #0a0b0d` | text |
| primary | `--ee-color-primary: #0052ff` | pills, 2px focus, links |
| unchecked | `--ee-color-surface-strong` + ink | exact token, never primary fill |
| checked | `--ee-semantic-up` | text only |
| failed number | `--ee-semantic-down` | text only |
| radius card | `--ee-radius-xl: 24px` | cards |
| radius CTA | `--ee-radius-pill` | 44px-tall CTAs |
| fonts | Inter, JetBrains Mono | never Coinbase fonts |

## A11y

Keyboard operable (tab order: skip-link → Runs/Books → run list → result → palette → inspector → Save graph → Confirm topology → disclosures). Visible focus (2px primary). Skip link. `aria-live` for run state including `waiting-human`. Contrast **WCAG AA** on blue-on-white and white-on-blue. Logo `alt` is “Arc”. Empty and failed states are text, not colour-only. Inspector is the keyboard path for topology; the XYFlow pane may be pointer-first.

## Must not

Cordis/DSH dependency, `0.0.0.0`, image generation, LLM client in the browser, Coinbase wordmark, plaintext-only product identity in the header.

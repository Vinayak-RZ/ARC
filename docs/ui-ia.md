# UI information architecture

Persistent localhost workspace. Not KiCad. Not a second agent. WCAG AA.

## Slots

| Slot | Role |
|------|------|
| `root` | Shell: skip-link, header with **Arc icon** (`assets/brand/arc-icon.png` → `/arc-icon.png`), live region |
| `sidebar` | Run list (`asset-row`) |
| `workspace` | Current view |
| `run.detail` | Recipe id, state, `unchecked` badge-pill |
| `run.evidentiary` | `evidentiary.json` (alias `summary.json`): values, verifier, citations, artifact paths |
| `run.argument` | Host (or local fallback) `argument.md`. Must not flip `unchecked`. |
| `run.plan` | Large-job `plan.md` (Given/Find, packs, capability ids). Not a numeric band. |
| `run.observation` | Kernel `observation.json`: capability/provider ids, node ok, `unchecked_reason` |
| `run.artifacts` | Library SVG/PNG + paths |
| `photo.confirm` | Draft netlist + confirm (no sim) |
| `rag.inventory` | Book/chapter/folder tags |
| `memory.excerpt` | ≤800 char excerpt + path |
| `gates.prompt` | Ask payload; MCP never waits here |

## States

`empty` · `running` · `waiting-human` · `failed` · `done`

| State | Slot behaviour |
|-------|----------------|
| `empty` | Run list and bands show an honest empty message; no fake numbers |
| `running` | Live region announces progress; bands stay previous-or-empty |
| `waiting-human` | Photo confirm / gate prompt; MCP never waits here |
| `failed` | Error text in `run.detail`; evidentiary `unchecked` stays honest |
| `done` | Two bands + plan + observation readable |

## Token map (DESIGN-coinbase)

| Token | CSS variable | Use |
|-------|----------------|-----|
| canvas | `--ee-color-canvas: #ffffff` | page |
| ink | `--ee-color-ink: #0a0b0d` | text |
| primary | `--ee-color-primary: #0052ff` | pills, 2px focus, links |
| unchecked | `--ee-badge-pill` | exact token, not a red button |
| checked | `--ee-semantic-up` | text only |
| failed number | `--ee-semantic-down` | text only |
| radius card | `--ee-radius-xl: 24px` | cards |
| radius CTA | `--ee-radius-pill` | 44px-tall CTAs |
| fonts | Inter, JetBrains Mono | never Coinbase fonts |

## A11y

Keyboard operable (tab order: skip-link → sidebar → workspace bands → photo confirm). Visible focus (2px primary). Skip link. `aria-live` for run state including `waiting-human`. Contrast **WCAG AA** on blue-on-white and white-on-blue. Logo `alt` is “Arc” (or the README alt); decorative parts of the SVG use the SVG `<title>`. Empty and failed states are text, not colour-only.

## Must not

Cordis/DSH dependency, `0.0.0.0`, image generation, LLM client in the browser, Coinbase wordmark, plaintext-only product identity in the header.

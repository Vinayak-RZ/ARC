# UI information architecture (as-built freeze)

**Student-facing pages:** [`UI.md`](UI.md) (accepted). Implement that workbook, not this slot list.

This file is the **as-built** FastAPI + Vite slot register from the H1 graph. Keep it only so implementers can map old slot names while rewriting `ui/`. Do not add pages here.

## As-built slots

| Slot | Role today | Maps toward ([`UI.md`](UI.md)) |
|------|------------|--------------------------------|
| `root` | Shell: header, skip-link, live region | chrome |
| `sidebar` | Run list (`asset-row`) | **Past work** |
| `workspace` | Current view | **This problem** |
| `run.detail` | Recipe id, state, `unchecked` badge-pill | Answer card + status |
| `run.artifacts` | Library SVG/PNG + paths | Figure grid |
| `photo.confirm` | Draft netlist + confirm (no sim) | **Confirm diagram** overlay |
| `rag.inventory` | Book/chapter/folder tags | **Books** |
| `memory.excerpt` | ≤800 char excerpt + path | **Notes** |
| `gates.prompt` | Ask payload; MCP never waits here | **The lab needs a value** |

As-built still dumps `summary.json`. That fails [`UI.md`](UI.md).

## States

`empty` · `running` · `waiting-human` · `failed` · `done`

Student-facing copy uses: working / needs your check / done / not verified.

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

Keyboard, visible focus (2px primary), skip link, `aria-live` for run state, contrast AA on blue-on-white and white-on-blue.

## Must not

Cordis/DSH dependency, `0.0.0.0`, image generation, LLM client in the browser, presenting `.md` / `.json` as the product.

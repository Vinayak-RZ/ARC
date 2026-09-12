# Frontend architecture — Electrical Engineer

**Status:** As-built freeze (H1 graph). **Student IA:** [`UI.md`](UI.md). Slot names that exist in `ui/` today: [`ui-ia.md`](ui-ia.md).  
**Visual:** [`design/DESIGN-coinbase.md`](design/DESIGN-coinbase.md).

Filling the lab workbook pages is a later UI code plan. Do not treat the JSON dump as the product.

## Layout

```text
src/electrical_engineer/     # CLI, runner, ui_server
ui/                          # Vite React CSR (slots, zustand, CSS variables)
```

## Stack

- FastAPI serves the SPA and JSON for runs. Bind `127.0.0.1` only.
- Vite + React + Zustand (layout + current run). No Cordis, no DSH runtime.
- Thin slot registry (~50 lines). As-built names: `root`, `sidebar`, `workspace`, `run.detail`, `run.artifacts`, `photo.confirm`, `rag.inventory`, `memory.excerpt`, `gates.prompt`.
- CSS variables + CSS modules. Inter + JetBrains Mono (or Geist Mono). Never Coinbase fonts/wordmark.

## Slot register API (ours, ~50 lines)

```ts
register(name: SlotName, Component: React.FC)
render(name: SlotName): ReactNode
```

Plugins live in `ui/src/slots/<name>/`. Shell renders `root` only.

## States

empty, running, waiting-human, failed, done — as-built FSM. Student copy: [`UI.md`](UI.md).

## Must not

- Second agent loop in the UI
- WAN / `0.0.0.0` bind
- Tailwind-as-architecture, MUI, Ant
- Image-generation canvas
- Shipping `.md` / `.json` dumps as the student product

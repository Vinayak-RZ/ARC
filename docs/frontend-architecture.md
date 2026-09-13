# Frontend architecture — Arc

**Status:** Layout contract (A1). IA detail: [`ui-ia.md`](ui-ia.md) (U1).  
**Visual:** [`design/DESIGN-coinbase.md`](design/DESIGN-coinbase.md).

## Layout

```text
src/electrical_engineer/     # CLI, runner, ui_server
ui/                          # Vite React CSR (slots, zustand, CSS variables)
```

## Stack

- FastAPI serves the SPA and JSON for runs. Bind `127.0.0.1` only.
- Vite + React + Zustand (layout + current run). No Cordis, no DSH runtime.
- Thin slot registry (~50 lines): `root`, `sidebar`, `workspace`, `run.detail`, `run.artifacts`, `photo.confirm`, `rag.inventory`, `memory.excerpt`, `gates.prompt`.
- CSS variables + CSS modules. Inter + JetBrains Mono (or Geist Mono). Never Coinbase fonts/wordmark.
- Header identity is the Arc logo at `assets/electrical-engineer-logo.svg` (same SVG as the README). Do not ship plaintext-only “Electrical Engineer” as chrome. As-built `ui/src/slots/root.jsx` is still text; wiring the SVG is a later UI pass.

## Slot register API (ours, ~50 lines)

```ts
register(name: SlotName, Component: React.FC)
render(name: SlotName): ReactNode
```

Plugins live in `ui/src/slots/<name>/`. Shell renders `root` only.

## States

empty, running, waiting-human, failed, done — see [`ui-ia.md`](ui-ia.md).

- Second agent loop in the UI
- WAN / `0.0.0.0` bind
- Tailwind-as-architecture, MUI, Ant
- Image-generation canvas

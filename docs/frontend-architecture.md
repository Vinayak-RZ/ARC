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
- Vite + React + Zustand (layout, current run, graph dirty). No Cordis, no DSH runtime.
- Thin slot registry: `root`, `sidebar`, `workspace`, `run.result`, `run.canvas`, `run.inspector`, `run.argument`, `run.more`, `photo.confirm`, `rag.inventory`, `memory.excerpt`, `gates.prompt`.
- `@xyflow/react` (MIT) only in `ui/src/slots/canvas/`. Kernel never imports it. Graph contract: `arc.circuit.v1` → `graph.json` → `netlist.cir`.
- CSS variables + CSS modules. Inter + JetBrains Mono (or Geist Mono). Never Coinbase fonts/wordmark.
- Header identity is the Arc icon at `assets/brand/arc-icon.png` (served as `/arc-icon.png`). README lockup is `assets/brand/arc-lockup.png`. Do not ship Coinbase wordmark.
- Color strategy: **Committed chrome, Restrained lab surface**. Header/focus/Confirm use `#0052ff`. Canvas + inspector stay white/ink/hairline.
- MATLAB chip: "Coming next: Arc will call it." OSS simulators stay first-class. Product works with zero MATLAB.
- **CD-KICAD:** capped composition canvas, not CAD. Keep the cannot-do row.

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
- Full schematic editor / KiCad clone (CD-KICAD)
- Hero-metric result dashboard
- In-window chat or pack-helper spawn

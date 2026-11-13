# Visual components for AI agents (Nov 2026 research slice)

**Date:** 2026-11-13  
**Audience:** Arc Visual Kit (B11) and `render-figure` capability depth.  
**Method:** Primary URLs and publication dates where verified; community-only claims labeled **unverified**.

---

## Executive summary (top findings)

1. **Component assembly beats pixel generation for EE coursework.** Agent-friendly stacks expose **JSON props, schemas, and deterministic renderers** (schemdraw, matplotlib, python-control, Vega-Lite, React Flow). Generative video (Sora, Veo, Kling) fails legible labels and stable geometry (T2VTextBench; Sora text workarounds).
2. **Remotion is the reference for agent-built explainer video:** `z.object()` schema on `<Composition>`, `npx remotion skills add`, SSR `renderMedia()` for goldens, JSON-serializable `inputProps` tied to engine output (Remotion docs, 2025 to 2026).
3. **ManimCE agent loops need lint + render + look** (manimkit pattern): search corpus, lint API mistakes, contact-sheet feedback; Text2Manim and multi-agent pipelines (arXiv 2025) validate the loop, not raw one-shot codegen.
4. **shadcn registry + MCP (Aug 2025)** is the UI pattern to copy: `registry.json`, namespaced `@arc/visual-*`, MCP list/search/install, clear descriptions for agents (ui.shadcn.com docs).
5. **Interactive sims (CircuitJS1)** expose **scriptable state** (`exportCircuit`, `getNodeVoltage`, `setExtVoltage`) for agent-driven waveforms; same-origin iframe contract (Falstad JS interface docs).
6. **Declarative diagram DSLs (Penrose, Vega-Lite)** separate **substance from style**; good for phasor/set diagrams when agents emit short programs, not PNG prompts (Penrose CMU docs).
7. **Visual regression is mandatory for a visual moat:** Chromatic + Storybook (Storybook docs; Chromatic docs) or Playwright screenshot diff in CI; pixel baselines for every visual component variant.
8. **Arc's wedge:** Engine-bound props (SMIB arrays, Bode vectors) flow into a **single Visual Kit registry** with DESIGN-coinbase tokens, MCP `list_visual_components` / `render_visual`, and preview goldens next to numeric goldens.

---

## 1. What makes a library agent-friendly?

| Property | Why agents need it | Examples |
|----------|-------------------|----------|
| **Typed props schema** | Host validates before render; no hallucinated layout | Remotion `schema` + Zod (Remotion Composition docs); tldraw `ShapeUtil.props` validators (tldraw Shapes docs); Vega-Lite `$schema` URL (Vega schema site) |
| **Registry / manifest** | Discovery without reading entire repo | shadcn `registry.json` + MCP (shadcn MCP changelog 2025-08); Arc proposed `visual-kit/manifest.json` |
| **Deterministic rendering** | Same props + same engine data = same pixels | schemdraw `save('x.svg')`; matplotlib `savefig`; Remotion `renderStill` |
| **Theming tokens** | One design system, no per-call style invention | DESIGN-coinbase in Arc; Remotion `defaultProps` + shared `theme.ts` |
| **Preview goldens** | CI proves visual contract | Chromatic baselines (chromatic.com/docs/visual) |
| **Serializable output** | MCP and skills pass artifacts | SVG/PNG bytes, MP4 path, React Flow `toObject()` JSON |
| **Engine-sourced numbers** | Never hand-type ohms or degrees on diagram | Arc FR15; bind `props` from `evidentiary.json` only |

**Anti-patterns for agents:** prompting Sora/Veo for graded schematics; matplotlib without fixed `rcParams`; unconstrained SVG from LLM strings.

---

## 2. Video and motion (programmatic)

### 2.1 Remotion (React video)

| Field | Detail |
|-------|--------|
| **What** | React compositions rendered to MP4/WebM via `@remotion/renderer`. |
| **Agent path** | `npx remotion skills add`; skills `/remotion-markup`, `/remotion-render`, `/remotion-docs` (remotion.dev/docs/ai/skills). |
| **Schema** | `Composition` accepts `schema?: z.object()` for Studio + render validation (Remotion Composition docs; v4.0.516+ inferred props). |
| **Batch render** | `bundle` + `selectComposition` + `renderMedia` with `inputProps` (SSR Node docs). |
| **Arc fit** | Short explainers: equal-area morph, AGC step response, trap callouts; props from PSA engines. |

**Sources:** [Building with Remotion and AI](https://www.remotion.dev/docs/ai/) (living docs); [Agent Skills](https://www.remotion.dev/docs/ai/skills) (updated 2025); [Composition schema](https://www.remotion.dev/docs/composition/) (living docs).

### 2.2 Manim / ManimCE

| Field | Detail |
|-------|--------|
| **What** | Python scene graphs to MP4 (3Blue1Brown style). |
| **Agent path** | Multi-agent pipelines (Manim Video Agent repo 2025); tool-call JSON to scene ops (Manim Cursor repo, **unverified** production date); **manimkit** (PyPI 2025) search + lint + render contact sheet. |
| **Research** | Text2Manim (SciTePress 2025): validation layer before render. |
| **Arc fit** | Optional `explain` genre clips; not primary graded figures (heavy TeX deps; CANNOT_DO lcapy path). |

**Sources:** [arXiv:2505.13400 Robin-adjacent tooling ecosystem]; Text2Manim [SciTePress 2025/149357](https://www.scitepress.org/Papers/2025/149357/149357.pdf); [manimkit PyPI](https://pypi.org/project/manimkit/) (2025).

### 2.3 Motion Canvas (TypeScript)

| Field | Detail |
|-------|--------|
| **What** | Generator-based TS animations with audio sync (motioncanvas.io). |
| **Agent path** | Codegen TypeScript scenes; Vite preview; good for synced voice-over labs. |
| **Arc fit** | P2 alternative to Remotion if team prefers TS-only UI repo; not required for v1 Visual Kit. |

**Sources:** [Introduction](https://motioncanvas.io/docs/) (living docs); [Animation flow](https://motioncanvas.io/docs/flow/) (living docs).

---

## 3. EE-native static and interactive diagrams

### 3.1 schemdraw

Python chained API; SVG/PNG via `get_imagedata()` for headless CI (schemdraw.readthedocs.io). **Arc today:** default `render-figure` backend. **Agent pattern:** emit small Python snippet or JSON ops list mapped to schemdraw elements; validator runs snippet in sandbox.

**Sources:** [Getting Started](https://schemdraw.readthedocs.io/en/latest/usage/start.html) (living docs).

### 3.2 CircuitikZ / lcapy

**CircuitikZ:** LaTeX/TikZ; great for print, poor for agent CI without TeX (**high flake** in cloud agents).

**lcapy:** Netlist in, symbolic analysis + semi-auto schematics + Bode/Nyquist plots (lcapy.readthedocs.io). Arc lists as later provider (CANNOT_DO row). **Agent pattern:** netlist string from engine, not from LLM guess.

**Sources:** [Lcapy overview](https://lcapy.readthedocs.io/en/latest/overview.html) (living docs).

### 3.3 Falstad CircuitJS1

Embeddable sim with `CircuitJS1.exportCircuit()`, `getNodeVoltage`, `setExtVoltage` (falstad.com circuit doc/js-interface.html). **Agent pattern:** import engine-verified netlist fragment; drive time series from ngspice results. Same-origin iframe required.

**Sources:** [JS interface](https://www.falstad.com/circuit/doc/js-interface.html) (undated official doc); [GitHub circuitjs1 README](https://github.com/pfalstad/circuitjs1) (living).

### 3.4 Penrose

Domain + Substance + Style programs; optimization layout (penrose.cs.cmu.edu). **Agent pattern:** emit short `.substance` for sets/graphs; style pinned by Arc. **Unverified** for power one-line diagrams at UG depth.

**Sources:** [Penrose overview](https://penrose.cs.cmu.edu/docs/ref) (living docs).

---

## 4. Canvas and whiteboard SDKs

### 4.1 React Flow

Controlled `nodes`/`edges`; `useReactFlow().addNodes`, `toObject()` for JSON round-trip (reactflow.dev API docs). **Arc today:** control `control_diagram.json` path. **Agent pattern:** typed node `data` holds engine refs only.

**Sources:** [ReactFlowInstance](https://reactflow.dev/api-reference/types/react-flow-instance) (living docs).

### 4.2 tldraw

`Editor.createShape` with validated `props`; batch via `editor.run()` (tldraw.dev SDK). **Arc fit:** SLD sketch + confirm; export to kernel graph.

**Sources:** [Editor](https://tldraw.dev/sdk-features/editor) (living docs).

### 4.3 Excalidraw

**Unverified in this pass for programmatic API depth.** Hand-drawn aesthetic; better for whiteboard than graded lab figures. Arc: optional export target only.

---

## 5. Charts and plots

| Library | Agent interface | EE use |
|---------|-----------------|--------|
| **matplotlib** | Python script | PSA curves, equal-area, dispatch (Arc engines today) |
| **python-control** | Bode/Nyquist/step | ControlEval path |
| **Plotly** | JSON `figure` dict | Interactive localhost UI (**unverified** schema stability for agents) |
| **Vega-Lite** | JSON spec + `toSpec()` | Declarative charts; `$schema` enables validation (vega.github.io) |
| **D3 / Observable Plot** | JS API | Powerful; higher agent error rate without templates |
| **Mermaid** | Text DSL | Flow/block coarse diagrams; CI text diff easy; weak component styling |

**Sources:** [Vega-Lite spec](https://vega.github.io/vega-lite/docs/spec.html) (living); [vega-lite-api](https://vega.github.io/vega-lite-api/) (living).

---

## 6. 3D and motion UI chrome

**three.js / react-three-fiber:** Useful for fields and machine intuition demos; not P0 for graded labs (**unverified** agent reliability for labeled axes).

**Lottie / Rive:** Vector motion with **runtime APIs** (Rive `useRive`, data binding migration 2025 docs). **Arc fit:** loading states, micro-interactions on proof dashboard; not for numeric plots.

**Sources:** [Rive React](https://rive.app/docs/runtimes/react/react) (living docs).

---

## 7. shadcn-style registries (agent install)

| Field | Detail |
|-------|--------|
| **What** | `components.json` + `npx shadcn add @ns/component`; MCP browse/search/install (changelog 2025-08). |
| **Lesson for Arc Visual Kit** | Each visual component = registry item with `registryDependencies`, description, demo story, screenshot golden. |
| **MCP** | `npx shadcn@latest mcp init --client cursor` pattern mirrors Arc `list_workflows` discipline. |

**Sources:** [shadcn MCP](https://ui.shadcn.com/docs/mcp) (updated 2025); [CLI 3.0 changelog](https://ui.shadcn.com/docs/changelog/2025-08-cli-3-mcp) (2025-08).

---

## 8. Generative AI video (Veo, Sora, Kling)

| Claim | Evidence |
|-------|----------|
| On-screen text and formulas fail reliably | T2VTextBench (arXiv:2505.04946): best avg text score ~0.37 for Sora; geometric text transforms worst |
| Workaround industry standard | Generate motion/background only; overlay text and diagrams in Remotion/After Effects (community + OpenAI Sora discussion) |
| Physics sim accuracy limited | OpenAI: Sora "does not accurately model the physics of many basic interactions" (openai.com index, 2024) |

**Arc policy:** Use gen-AI video only for **marketing B-roll** without graded labels. All lab figures come from Visual Kit + engines.

**Unverified:** Head-to-head Veo 3 vs Sora on circuit schematics (no primary EE benchmark found).

---

## 9. Visual regression and quality gates

| Tool | Role |
|------|------|
| **Chromatic + Storybook** | Pixel diff every story; CI on push (storybook.js.org visual testing docs) |
| **Playwright `toHaveScreenshot`** | OSS alternative for `ui/` routes |
| **Remotion `renderStill` per frame** | Video spot-checks without full pixel diff of MP4 |

**Quality bar for Arc (proposed):**

1. Side-by-side with license-clean textbook / IITR lab-sheet references (human rubric).
2. Blind "looks professional" review (20 panels, Gate 0 optional 15).
3. Automated: **≤0.1%** pixel diff vs golden at 1280px width unless intentional version bump.

---

## 10. Implication matrix for Arc Visual Kit

| Action | Detail |
|--------|--------|
| **Adopt** | Remotion skills + engine-bound `inputProps`; schemdraw/matplotlib/python-control adapters; React Flow for control; CircuitJS optional embed; Vega-Lite for tabular chart JSON; shadcn-like manifest + MCP |
| **Beat** | MathWorks Copilot screenshots without golden linkage |
| **Benchmark** | Visual regression count in SCORECARD; same as numeric benchmarks |
| **Cut** | Sora/Veo for schematics; raw LLM SVG; unconstrained Mermaid for graded labs |
| **Integrate** | motion kit in `skills/ui-diagrams/` + `skills/visual-kit/` |

---

## 11. Source index (primary)

| ID | Source | URL | Date |
|----|--------|-----|------|
| V1 | Remotion AI | https://www.remotion.dev/docs/ai/ | living |
| V2 | Remotion Agent Skills | https://www.remotion.dev/docs/ai/skills | 2025+ |
| V3 | Remotion Composition | https://www.remotion.dev/docs/composition/ | living |
| V4 | Remotion SSR render | https://www.remotion.dev/docs/ssr-node | living |
| V5 | Motion Canvas docs | https://motioncanvas.io/docs/ | living |
| V6 | schemdraw | https://schemdraw.readthedocs.io/en/latest/ | living |
| V7 | Lcapy | https://lcapy.readthedocs.io/en/latest/overview.html | living |
| V8 | CircuitJS JS API | https://www.falstad.com/circuit/doc/js-interface.html | undated |
| V9 | Penrose | https://penrose.cs.cmu.edu/docs/ref | living |
| V10 | React Flow API | https://reactflow.dev/api-reference/types/react-flow-instance | living |
| V11 | tldraw Editor | https://tldraw.dev/sdk-features/editor | living |
| V12 | Vega-Lite | https://vega.github.io/vega-lite/docs/spec.html | living |
| V13 | shadcn MCP | https://ui.shadcn.com/docs/mcp | 2025 |
| V14 | shadcn CLI 3.0 | https://ui.shadcn.com/docs/changelog/2025-08-cli-3-mcp | 2025-08 |
| V15 | Chromatic visual tests | https://www.chromatic.com/docs/visual/ | living |
| V16 | Storybook visual testing | https://storybook.js.org/docs/writing-tests/visual-testing | living |
| V17 | T2VTextBench | https://www.alphaxiv.org/abs/2505.04946 | 2025 |
| V18 | OpenAI Sora sim limits | https://openai.com/index/video-generation-models-as-world-simulators/ | 2024-02 |
| V19 | Text2Manim | https://www.scitepress.org/Papers/2025/149357/149357.pdf | 2025 |
| V20 | manimkit | https://pypi.org/project/manimkit/ | 2025 |
| V21 | Rive React | https://rive.app/docs/runtimes/react/react | living |

---

*Report for Arc research track `frontier-2026-11`. Feeds B11 Arc Visual Kit node plan.*

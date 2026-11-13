# Arc UX audit (Nov 2026)

Source inputs: `uploads/UX_BRIEF.md`, screenshots of Control Studio and app shell (Nov 2026), `docs/design/DESIGN.md` (Learning Lab / Cobalt UI).

Judgement sections are labelled. Facts cite repo paths or the brief.

## 1. Facts and constraints

| Fact | Source |
|------|--------|
| Primary users: undergrad EE (IIT Roorkee coursework) plus coding agents on MCP/CLI | UX brief |
| Core loop: pose problem, agent solves with engines, verified answer + visuals + trail, human tweaks and re-runs | UX brief |
| Design language: Learning Lab tokens (canvas `#FAFAF9`, cobalt `#2F6FEB`, copper `#E07A3F`, Geist/Inter) | `docs/design/DESIGN.md` |
| UI is Vite + React, slot registry, Zustand layout, FastAPI on localhost | `ui/src/`, `AGENTS.md` |
| Run list API: `id`, `title`, `unchecked`, `recipe_id` | `ui_server/app.py` `_run_list_item` |
| Another agent owns Control Studio canvas wiring on `cursor/control-studio-6ef3` | Coordination note |

## 2. Users and jobs

**Student (human)**

- When I finish a lab problem set, I want to ask an agent to solve and verify a circuit or control problem, so I can trust the numbers and learn from the explanation.
- When I open Arc after class, I want to see my recent work with plain names and verification status, so I can pick up where I left off without decoding session IDs.
- When I disagree with a parameter, I want to edit the diagram or value and re-run, so I can explore "what if" without leaving the tool.

**Coding agent (via MCP/CLI)**

- When the student assigns a recipe, I want Arc to persist a run with evidentiary JSON and artifacts, so the human can inspect the same live object in the UI.
- When verification is incomplete, I want `unchecked` to be visible and explained, so nobody treats a symbolic-only result as checked simulation.

## 3. Journeys (core loop)

1. Trigger: new problem (CLI, agent, or "Try a problem" from home).
2. Run executes: engines produce answer, plots, observation/trace.
3. Human opens run: **answer and verification first**, then large plots, then explanation and diagnostics.
4. Human edits (graph, Control Studio, parameter): live or saved state, re-run/simulate.
5. Human understands and files work (or starts next problem).

**Moments of doubt today:** opaque run IDs in sidebar; tiny plot thumbnails; header engine chips imply products that may not be installed; no home explaining first step; developer JSON buried next to student-facing content without hierarchy.

## 4. Opportunities (outcome-led)

| Outcome | Opportunity | Screen/feature |
|---------|-------------|----------------|
| Trust the answer | Verification badge + one-line meaning of checked vs unchecked | Run result header |
| Resume work fast | Named runs, recipe grouping, search, recency | Sidebar / runs |
| Onboard in one glance | What Arc is + primary CTA | Home |
| Learn from visuals | Full-width plots, not 240px thumbs | Run result / engine panel |
| Collaborate with agent | Author badges on edits (Control Studio, op log) | Control Studio (peer agent) |
| Calm professional feel | One token set across UI and matplotlib | Tokens + Visual Kit |

## 5. Structure (navigation)

**Chosen model (judgement):** Left sidebar = workspace switcher (Home, Runs, Books, Visuals, Control) + contextual list (runs when on Runs). Main column = content. Header = brand only + optional compact status (not four engine chips).

**Progressive disclosure:** Run view = summary card, plots, explanation; Observation/trace/plan in collapsed "Diagnostics" region.

**Cut from primary nav:** Engine name chips in header (move to diagnostics tooltip or docs).

## 6. Screens

| Screen | Purpose | Primary action | Empty / loading / error |
|--------|---------|----------------|-------------------------|
| Home | Orient and start | Try a problem (CLI hint) | N/A |
| Runs list | Pick a run | Open run | "No runs yet" + CTA |
| Run result | Trust and inspect | Re-run via agent (external) / edit canvas | Loading skeleton; failed banner |
| Visuals | Gallery of kit figures | Browse | Empty fetch message |
| Books | RAG inventory | Ingest (existing) | Existing copy |
| Control Studio | Live block diagram | Simulate | Peer-owned layout |

## 7. Heuristics check (failures and fixes)

| Heuristic | Failure | Fix |
|-----------|---------|-----|
| Visibility of status | `unchecked` badge without explanation | Add helper text + link to diagnostics |
| Match real world | Session IDs as titles | Prefer `title` from evidentiary; hide raw id behind mono secondary line |
| Aesthetic/minimal | Header chips, duplicate title lines | Remove chips; one title line in list |
| Recognition over recall | No search on long run lists | Client-side search filter |
| Help users recover | Generic "failed" on fetch | Distinct error state with retry |
| HAX: show confidence | Verifier string opaque | Map to "Checked simulation" vs "Unchecked (reason)" |
| WCAG | Focus on sidebar buttons | Keep 44px targets; cobalt focus ring |

## 8. Appetite and scope (this pass)

**In:** Design docs + skills in repo; UX audit; HTML prototypes; shared tokens (CSS + JS + Python); app shell (home, runs UX, header), run result card, gallery/books polish, matplotlib theme alignment, golden regen if needed, screenshots.

**Cut (judgement):**

- Full run rename UI (needs API; defer)
- Server-side run grouping beyond recipe_id (defer folders)
- Replacing Control Studio canvas layout (owned by peer branch)
- Invented metrics, fake counts, or marketing hero numbers

**Risks:** Visual golden drift after palette change; merge conflicts on `tokens.css` with Control Studio branch.

## 9. Open questions

| Question | Default |
|----------|---------|
| Default landing: Home or last run? | Home when no `?run=` query |
| Show MATLAB/Simulink anywhere? | One line in diagnostics only, not header |

## Top findings (summary for report)

1. Sidebar is a flat ID dump with weak hierarchy and no search.
2. Header engine chips add noise and imply unavailable products.
3. No home screen; empty state is a CLI error message.
4. Results bury the answer; plots are too small.
5. Verification status is not explained to students.
6. Visual system is ad hoc (`#0052ff` blue) vs product-grade Learning Lab tokens.

**What we cut:** Header engine chips; duplicate run title rows; exposing raw JSON before student-facing summary; card shadows per DESIGN.md (sections with hairlines instead).

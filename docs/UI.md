# Student-facing lab UI

**Status:** Proposed (2026-09-12). No product code in this pass.  
**Audience of this doc:** implementers. **Audience of the product:** a UG electrical-engineering student who may not be software-fluent.  
**Visual tokens:** [`design/DESIGN-coinbase.md`](design/DESIGN-coinbase.md) (Inter + JetBrains/Geist Mono; never Coinbase fonts or wordmark).  
**Authority:** [`PID.md`](PID.md), [`PRD.md`](PRD.md) FR11, [`ARCHITECTURE.md`](ARCHITECTURE.md) §9.

The localhost UI is a **lab workbook**, not a developer console, not a file browser, and not a ChatGPT clone. The kernel still writes `summary.json`, `argument.md`, `plan.md`, and `observation.json`. The student must never be asked to read those files as files.

---

## 1. Who it is for

A second-year EE student opening a homework check: they know ohms, phasors, and lab reports. They do not need to know JSON, Markdown, YAML, MCP, DAGs, slots, FastAPI, or React. If a label only makes sense to the people who built Electrical Engineer, it does not belong on screen.

The host agent may use the same UI to confirm a photo or show results. That does not license IDE chrome.

## 2. Presentation law

| Do | Do not |
|----|--------|
| Cards, tables, figure grids, pill buttons, checklists | A `<pre>` dump of JSON, Markdown source, YAML, or TOML |
| Quantity · value · unit in a results table (mono numbers) | Filename as the title (`summary.json`, `argument.md`, `plan.md`) |
| Captioned SVG/PNG schematics and plots | Raw JSON graphs, spice log bodies, or “artifact.svg” as the heading |
| Method as formatted prose (headings, paragraphs, math) | A Markdown editor or a `.md` preview chrome |
| Plan as Given / Find / steps the student can tick mentally | A code diff or a DAG of node ids |
| Book · chapter · page on a quote card | Chunk ids, BM25 scores, index paths |
| Exact token **unchecked** plus a plain gloss (“Not verified by the lab”) | Jargon synonyms, or hiding the token (FR2) |
| Status in EE language: working, needs your check, done, not verified | Internal FSM names (`waiting-human`, `apply: true`) |
| Circuit listing titled **Circuit** when a netlist is the *electrical* artifact | Leading with `.cir` / `confirmed.json` |
| DESIGN-coinbase: white canvas, scarce blue CTAs, 24px cards, pill buttons | VS Code / ChatGPT / KiCad / trading-terminal chrome |

**On-disk vs on-screen.** Files remain the kernel contract (Layer 3 artifacts). The UI **maps** them to lab surfaces. A later “Show files” debug switch is **out of v1** — the owner asked for a non-technical product, not a dual-mode IDE.

**Still EE, not dumbed down.** Netlists, phasor tables, Bode plots, per-unit, and LaTeX-looking math are in-bounds. Software implementation is not.

## 3. Pages (v1)

Four **nav** pages. Two **overlays** (not in the sidebar). Nothing else in v1.

```text
Electrical Engineer          127.0.0.1 · this computer only
  This problem   Past work   Books   Notes
```

| Page | Student job | Reads (implementer) | Must not |
|------|-------------|---------------------|----------|
| **This problem** | See the current check: question, answer, figures, method, plan | evidentiary band, argument, plan, observation *mapped*, plots | Dump `summary.json`; title the page with a run UUID |
| **Past work** | Reopen an earlier homework check | run list + titles from `problem.json` / first line of the prompt | A sidebar of opaque ids as the only label |
| **Books** | See which textbooks they added; read a cited passage | RAG inventory + retrieve hits | Chunk JSON, licence-tag dumps, folder paths as the hero |
| **Notes** | Course notebook: units, course, facts, mistakes, lessons | memory files **as forms/cards** | Filenames (`preferences.md`) as headings |

Overlays (open from This problem when the kernel needs the student):

| Overlay | Student job | Must not |
|---------|-------------|----------|
| **Confirm diagram** | Photo vs library schematic, side by side. Confirm or fix. Does not simulate. | Show `confirmed.json`; auto-run SPICE |
| **The lab needs a value** | One missing number or a yes/no (MATLAB licence, allow this check). Counts toward the two-ask budget, in human words. | MCP wait spinner; “interrupt 1/2” as the only copy |

**Default route.** Open `electrical-engineer ui --run <id>` → **This problem** for that check. Open with no id → **Past work** if any exist, else an empty **This problem**.

Empty **This problem** copy (host-skip): “No lab check is open. Numbers an assistant typed in chat are not checked here. Run a check, or ask it to use Electrical Engineer tools; then they appear on this page.”

### 3.1 This problem (primary)

Desktop: **12-column grid**.

1. **Header band** — problem title in plain language (from the assignment prompt, truncated). Status pill. Do not lead with the run id; a small caption may keep it for support.
2. **Answer card** (span 12, or 8+4 with status) — the unknown: name, value, unit, **unchecked** or “Checked by the lab.” One quantity is the hero; extras go in the table.
3. **Results table** (span 7) — rows: quantity, value, unit, checked?. Plots and schematics as a **figure grid** under the table (2-up desktop, 1-up mobile), each with a caption (“Load voltage”, “Bode magnitude”).
4. **Method** (span 5) — engineering argument as **rendered prose**, not a file. Read-only for checked numbers (FR18): the student cannot type a fluent `Vout` here and make it checked.
5. **Plan** (full width, only if a plan exists) — Given / Find / steps. Checklist look. Looking at it is not running a simulator.
6. **Citations** — quote cards: book, chapter, page. Empty search: a visible empty state (“No passage found in the books you added”), never a blank pane.
7. **What the lab did** (optional footer, not a page) — plain sentences mapped from observation: which kind of check ran, whether a book search was empty, why something stayed **unchecked**. No `unchecked_reason` enum strings (`no-provider` → “No checker is installed for this kind of problem”).

### 3.2 Past work

Card grid (3-up desktop, 1-up mobile). Each card: title, date, course chip if known, status pill. Click → This problem. Empty: “Checks you run will show up here.”

### 3.3 Books

List of books the student added (title, chapters). Filter: this book, this chapter. Passage results as quote cards. Adding a PDF stays **CLI this graph** (`rag add`); the page may say “Add books with the Electrical Engineer command on your computer” without dumping flags. Inventory empty: explain they can add a book they have rights to.

### 3.4 Notes

Four (or five) **cards**, not five files:

| Card title | Maps from |
|------------|-----------|
| How I like answers | `preferences.md` |
| This course | `course.md` |
| Facts to reuse | `facts.md` |
| Mistakes to watch | `errors.md` |
| Lessons | `lessons.md` |

Edit = the same explicit write law (FR13). Do not silent-append. A proposed lesson after **unchecked** appears as a **draft card** (“Save this lesson?”), not an auto-edit.

## 4. What is not a page

| Idea | Why not |
|------|---------|
| Chat / prompt box | The UI is not an agent loop |
| DAG / workflow editor | Host composes; student sees results |
| Eval / gold dashboard | Implementer surface, not UG homework |
| MCP / CLI status / “slots” | How we were built |
| Raw run-directory browser | Files are not the product |
| Settings dump of `gates.toml` | Gates appear as Confirm / Ask overlays in human language |

Compose allowlist (when the student must agree to a proposed check) is the **Confirm** overlay with EE wording (“Run a circuit simulation on this netlist?”), not a graph widget.

## 5. Copy dictionary (on-screen)

| Internal | Student-facing |
|----------|----------------|
| run | problem / this check |
| `argument.md` | Method |
| `plan.md` | Plan |
| evidentiary / `summary.json` | Results |
| `observation.json` | What the lab did (sentences) |
| capability / provider / node id | omit, or “Checked by the lab” |
| `waiting-human` | Needs your check |
| `label-unchecked` | **unchecked** — Not verified by the lab |
| RAG / BM25 / chunk | Books / passage |
| memory file | Notes card title above |

Keep the exact token **unchecked** visible whenever FR2 requires it. The gloss does not replace the token.

## 6. Visual bar

Tokens: [`design/DESIGN-coinbase.md`](design/DESIGN-coinbase.md). Scene: a student at a bright desk with a lab report, not a dim IDE at 2am → **light canvas**, not a dark “hacker” theme as the default.

- White page floor, ink text, scarce `#0052ff` pills.
- Result numbers in mono (`number-display`).
- Cards `{rounded.xl}` (24px), hairline borders, one shadow on hover.
- Feature grids 2-up / 3-up as in the token doc; This problem uses the 7+5 split in §3.1.
- Mobile `<640px`: stack Answer → Results → Figures → Method → Plan. Nav collapses. Touch targets ≥44px.
- Keyboard: skip link, semantic headings, visible focus. WCAG AA contrast on body and pills.

Do not ship Coinbase wordmarks or licensed Coinbase fonts.

## 7. As-built vs this target

As-built `ui/` is a single-band viewer: run ids in a sidebar, `<pre>` of `summary.json`, a bare SVG, a Confirm button that prints JSON. That **fails** this doc. Filling the pages above is a **later UI code plan**. This overlay specifies the product; it does not implement React.

Photo confirm and gates still need the HTTP UI (do not replace the SPA with a static file dump). Do not grow an in-UI agent loop.

## 8. Non-goals (this overlay)

- Implementing the pages in `ui/`.
- A marketing landing page.
- In-browser chat, crash-resume, WAN bind, KiCad clone.
- Showing implementation files because “power users might want them.”

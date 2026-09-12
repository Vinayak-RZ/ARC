# Architecture Q&A gate — owner answers (2026-09-10)

## Purpose

Record the owner’s answers that authorized [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) and [`docs/WORKFLOWS.md`](../../docs/WORKFLOWS.md). Those docs are now **Accepted**. This sheet is historical.

## Findings

Claim | Evidence | Confidence
--- | --- | ---
Identity locks stay closed: H3 thin CLI, not H4/H5; tools own numbers or the output says exactly `unchecked`; UG bound; GATE eval overlay; local-first; no commercial PDFs in git | owner instruction 2026-09-10; `docs/PID.md` | high
Q1–Q9 locks (hybrid router, light DAG+FSM, DSH paradigm-only, photo stub, Cursor-like gates, files not DB, CLI+stdio MCP, extensive catalog) are confirmed | owner voice + written table | high
Q17–Q64 are frozen in the pick table below | owner written instruction | high
Persistent localhost UI is a **critical** product surface, not a diagram popup | owner addendum | high

### Q1–Q9 identity (confirmed)

Hybrid router; not LangGraph; light DAG+FSM; Cordis/DSH paradigm only; photo stub; gates default on, max 1–2 interrupts, allow-all globally or per-run; per-run files; `electrical-engineer run <workflow>` plus optional stateless stdio MCP (`list_workflows`, `run_workflow`); extensive student-readable catalog; H3.

### Language and install (Q10–Q16 + Q64)

| Topic | Decision |
|-------|----------|
| Nodes | In-process **Python 3.11+ functions** only |
| CLI + runner this pass | **Python 3.11+**, `pip` install, Linux + macOS + Windows |
| Later CLI skin (not this freeze) | Owner also allowed a Go or Rust CLI wrapping the same Python runner; not the Proposed stack |
| LLM | Runner is deterministic. No hidden agent loop. Model calls only through registered nodes, or the **host coding agent**. Classifier (when workflow id omitted) is one structured call **before** the runner, not a DAG node |
| Offline | Fully offline CLI is required when a local model is configured. Deterministic nodes (spice, control, load-flow) work without any model |
| MATLAB | Optional. The whole product must work without MATLAB. CI must not require MATLAB |

### Final pick table (Q17–Q64)

| Q | Decision |
|---|----------|
| 17 | Mix: YAML recipes + tiny in-process DAG runner/FSM; node implementations are registered Python functions. Do not embed Treadle / Ordius / Tasked |
| 18 | YAML |
| 19 | Parallel when ports allow. Independent ready nodes run concurrently. Deterministic start-order (sorted node id) |
| 20 | No crash-resume. Run dir is audit only. Process death ⇒ new run. UI/TTY gates are live waits, not resume |
| 21 | `./runs/<id>/` |
| 22 | Gitignore `runs/` by default |
| 23 | `{short-suffix}-{timestamp}` suffix first, e.g. `k7m2-20260910T162148Z` |
| 24 | Recipe-as-node via `run-recipe`. Cycle detection. Max nesting depth 3 |
| 25 | 2 automatic sim-repair retries; they do not count as human interrupts. After exhaustion: `label-unchecked` or `ask-human`, never a fake pass |
| 26 | 2 min default timeout; recipe may override; 10 min hard ceiling |
| 27 | Unlimited parallel runs. Each CLI invocation is an isolated process + its own `runs/<id>/` |
| 28 | Typed ports + cap: max 16 nodes / 24 edges on a composed DAG. Invalid DAG rejected before any sim |
| 29 | Only `compose-from-parts` may emit a new DAG. Router never invents one |
| 30 | `compose-from-parts` listed but `--advanced` |
| 31 | Small classifier LLM when id omitted; explicit id skips classify |
| 32 | Ask the student if top-1 and top-2 are within 0.15 |
| 33 | Always `unmatched-cosolver`: no auto-simulate; label `unchecked` |
| 34 | MCP `run_workflow` never waits. Gate would fire ⇒ fail closed + UI URL or CLI hint |
| 35 | Two MCP tools now: `list_workflows`, `run_workflow`. `resume_*` later |
| 36 | CLI now: `run`, `workflows`, `mcp`, `eval`, `ui`, `rag` (add/list/tag). Later: `resume`. Never: faculty/LMS |
| 37 | stdio now; HTTP/SSE later |
| 38 | Global `~/.config/electrical-engineer/gates.toml` + project `.electrical-engineer/gates.toml` |
| 39 | TOML |
| 40 | Most-restrictive wins |
| 41 | Allow-all: file flag, `EE_ALLOW_ALL`, CLI `--allow-all` |
| 42 | Gate table in ARCHITECTURE (local sim auto; MATLAB ask; photo ask; compose ask; outside writes deny; package install deny) |
| 43 | Abort on a would-be 3rd interrupt. Do not auto-allow the rest |
| 44 | Keep per-pack `explain-*`. Author WORKFLOWS.md from taxonomy + owner catalog list. Do not freeze the research catalog draft as API |
| 45 | `list-workflows` = CLI/MCP discovery only, not a runnable recipe |
| 46 | Specify circuits + control in full; other packs as one-liners; mark v1 / stub / later |
| 47 | Ids renamable until the first CLI ships |
| 48 | Photo stub: phone + textbook screenshot; detect → connect → OCR → draft netlist → one UI confirm; `.cir` + JSON graph; localhost viewer; after confirm stop (no sim); low-confidence OCR always flagged |
| 49 | `control-diagram-to-model`: stub. Do not drop |
| 50 | Accept listed activities. Add `run-recipe`. Classifier is not a node. Photo stages stay named |
| 51 | Separate `run-spice` / `run-matlab-if-present` / `run-load-flow` |
| 52 | MATLAB if present else OSS (PRD P1). Do not invent a third rule |
| 53 | `skills/<pack>/SKILL.md` in this repo; CLI and hosts read the same files |
| 54 | Context + retrieval numbers in ARCHITECTURE. RAG quality is first-class |
| 55 | Both: exact token `unchecked` in the answer **and** field + sentence in `summary.json`. Synonyms: no |
| 56 | Specify eval now. Gold path `eval/gold/`. Thin runner layout + `electrical-engineer eval`. No hosted leaderboard |
| 57 | BYO PDFs, photos, folder tags, and memory files are untrusted. They cannot override gates, `--allow-all`, or the `unchecked` rule |
| 58 | Run dir: node JSON, artifact paths, spice **log path** (not body). No API keys. Redact `*_KEY`, `*_TOKEN`, `*_SECRET`, `sk-`, `Bearer`, MATLAB licence strings |
| 59 | Plots/diagrams via code libraries, not generated bitmaps. Default export png + svg |
| 60 | Both LaTeX and plaintext. Invalid delimiters are a quality defect |
| 61 | Architecture **Proposed** until owner says accepted |
| 62 | This file is the answer list. Keep ADRs. Do not delete this sheet |
| 63 | Medium freeze: system diagram, catalog, gates, CLI/MCP, compose, photo stub, RAG tags, memory, localhost UI, eval layout. No per-field JSON Schema |
| 64 | Extra locks: recipe path `workflows/<pack>/<id>.yaml`; runner law; interrupt budget 2 including children; project root rule; memory/RAG/UI/eval as in ARCHITECTURE |

### Product purpose (owner)

Named workflows exist so the agent gives **better answers** — better RAG, citations, verified numbers, explanations — not only so a graph runs. The agent may orchestrate **inside** a named recipe (branching, which child recipe, which book/chapter). The router must **not** invent a new DAG. New DAGs only via `compose-from-parts --advanced`.

### Persistent UI (owner addendum)

The localhost UI is a **critical** part of the product. It is a **persistent** local workspace that helps the **agent and the student** see and understand runs, artifacts, diagrams, plots, and citations — not a one-shot “pretty schematic” dialog.

## Open questions

None remaining for the architecture answers on this sheet. Product code for MCP verb splits, UI pages, and RAG extract/chunk is a later plan, not a reopen of this Q&A.

## Sources

- Owner architecture answers (voice Q1–Q16 + written Q17–Q64 + UI addendum) — retrieved 2026-09-10 — reliability: primary
- [PID](../../docs/PID.md) — retrieved 2026-09-10 — reliability: primary
- [PRD](../../docs/PRD.md) — retrieved 2026-09-10 — reliability: primary
- [spatiotemporal-composability.md](spatiotemporal-composability.md) — retrieved 2026-09-10 — reliability: primary
- [light-dag-fsm-and-language.md](light-dag-fsm-and-language.md) — retrieved 2026-09-10 — reliability: primary
- [rag-chunking-and-retrieval.md](rag-chunking-and-retrieval.md) — retrieved 2026-09-10 — reliability: primary
- [photo-to-schematic-to-simulink.md](photo-to-schematic-to-simulink.md) — retrieved 2026-09-10 — reliability: primary

## Confidence

Overall confidence for this note: high that these are the owner’s locks for the architecture pass. Medium that ids in WORKFLOWS.md will survive until the first CLI (Q47: renamable until ship).

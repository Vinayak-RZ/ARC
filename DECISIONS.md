# DECISIONS

ADR seeds from the research phase, plus owner-accepted product locks (2026-09-09). Status values: `proposed` | `accepted` | `superseded`.

Research memo [`research/synthesis/recommendation.md`](research/synthesis/recommendation.md) remains **historical advice**. Product identity is [`docs/PID.md`](docs/PID.md) (Accepted). Requirements: [`docs/PRD.md`](docs/PRD.md).

---

## ADR-0001 — Harness base

- **Status:** accepted (product lock 2026-09-09)
- **Context:** Need a place to run EE skills, RAG, and verifiers while remaining usable from Cursor, Claude Code, and OpenAI, and also as a local CLI without those hosts.
- **Decision:** **H3** — branded CLI (`electrical-engineer`) wrapping portable skills + MCP + local RAG (**H1 layer**). The CLI is glue, ug policy, co-solver defaults, and an eval runner. It must not grow a unique agent loop (that would be H5).
- **Historical research advice:** O1 / H2 (package-first, optional Pi package) scored highest in `recommendation.md`. That advice is **superseded as the product choice**. Do not treat O1 as the locked harness.
- **Consequences:** Skills + MCP stay portable; three model paths (host subscription, BYO key, local LLM); H3 falsifier = CLI diverges from hosts.
- **Alternatives:** H1 skills-only (no branded CLI); H2 optional Pi package; **H4** Electric Pi fork (rejected); **H5** greenfield harness (rejected).
- **Sources:** owner P0; `docs/PID.md`; `docs/PRD.md`; scoring history in `research/synthesis/option-scoring.md`

---

## ADR-0002 — Knowledge grounding (RAG spine)

- **Status:** proposed
- **Context:** Undergrad EE knowledge is dense with formulae and worked examples; model priors alone are insufficient.
- **Decision:** Ground concepts via **BYO textbook RAG** (MCP tools + structure-aware hybrid retrieval); use skills for pedagogy; never commit commercial book text.
- **Consequences:** Ingestion quality becomes a core engineering problem; licence-safe by default.
- **Alternatives:** Skills-only; fine-tune; redistributed corpus (rejected).
- **Sources:** `research/notes/ee-corpus-and-licensing.md`, `research/notes/rag-*.md`

---

## ADR-0003 — Verification tier

- **Status:** proposed
- **Context:** Numeric EE answers must not be invented.
- **Decision:** **MATLAB/Simulink MCP when a licence is present**; OSS SPICE/Python stack is **first-class** otherwise (P1 default in the PRD, not a PID lock).
- **Consequences:** Mixed-licence audience. Unverified numbers are **labelled unchecked** — they are allowed, but must never be presented as simulation or lab results. (Research-era “refuse unverified simulation” is replaced by this label policy.)
- **Alternatives:** OSS-only; MATLAB-only; hard-refuse any number without a tool.
- **Sources:** `research/notes/matlab-simulink-surface.md`, `research/notes/open-source-verification.md`

---

## ADR-0004 — Multimodal RAG ingest engine

- **Status:** proposed (engine undecided until spike)
- **Context:** EE textbooks mix text, equations, tables, figures, and multi-column layout; text-only RAG fails. RAG-Anything is unmaintained risk.
- **Decision:** **Spike LightRAG 1.5** vs Docling vs BM25+dense. Facade + inventory + book/chapter/folder filters ship regardless. Do **not** adopt any engine as the agent harness. Decide after measured numbers (QUALITY then SPEED).
- **Consequences:** No engine pin in Wave 0. B_RAG_SPIKE writes the note. Fallback: BM25+dense + cannot-do row if all heavy engines fail.
- **Alternatives:** RAG-Anything/MinerU as locked default (deferred); VLM-only chunking; commercial parsers.
- **Sources:** `research/notes/rag-anything-evaluation.md`, Gate 0 owner answers, `IMPLEMENTATION_PLAN.md` §11

---

## ADR-0005 — UG coursework bound, GATE as eval, single repo

- **Status:** accepted (product lock 2026-09-09; supersedes the research-era “UG/PG + later fork” wording)
- **Context:** The project needs a public definition of success that matches a student-first vision without claiming a shipped agent, and without competing with licence-locked plant-floor or EDA copilots.
- **Decision:** Public promise = **union of representative UG EE programmes** (Indian institutes + global institutes). See `docs/curriculum-map.md`. **GATE EE is an eval overlay / capability check**, not the syllabus bound. **PG is not a public promise.** **One git repository only** — later unpublished `--profile` flags may exist; do not fork UG vs lab. C1–C8 remain the success bar; C8 is not a student UX promise. Reliability = tools own numbers **or** the output says **unchecked**; vision drafts are not truth until the student confirms.
- **Consequences:** Eval may tag GATE sections; missing a taught UG core is a product gap even if GATE omits it. No second repo. README must not promise PG or a research fork as the public line.
- **Alternatives:** GATE-only bound (rejected); public PG promise (rejected); two-repo UG-freeze vs lab fork (rejected).
- **Sources:** owner P0; `docs/PID.md`; `docs/curriculum-map.md`; `docs/PRD.md`; historical `research/notes/ee-task-taxonomy-draft.md`

---

## ADR-0006 — Apache-2.0, forever OSS, co-solver default

- **Status:** accepted (product lock 2026-09-09)
- **Context:** Licence, commercial model, and default student interaction were OPEN in the research PID draft.
- **Decision:** *Our* code is **Apache License 2.0**. This repository is **forever OSS**; no paid tier here. Default student mode is **co-solver** (full working + answer + assumptions). No faculty/TA/LMS features in v1. Civil, mechanical, and manufacturing are never this product.
- **Consequences:** `LICENSE` is Apache-2.0. Hosted paid tutors are out of this repo’s promise. Integrity is “show the work”; institutions own cheating policy.
- **Alternatives:** MIT; AGPL; dual-licence paid tier; tutor-default; faculty v1.
- **Sources:** owner P0; `LICENSE`; `docs/PID.md`; `docs/PRD.md`

---

## ADR-0007 — Orchestrator, recipes, gates, UI, eval

- **Status:** accepted (A1, 2026-09-10)
- **Context:** Need a local-first way to run named UG EE workflows, compose advanced DAGs, retrieve tagged textbooks, confirm diagrams, and score gold tasks — without LangGraph, a Temporal cluster, or a DeepSeek Harness fork (those would be H5 or H4).
- **Decision:** Tiny **Python 3.11+** in-process DAG runner of checked-in **YAML** recipes (`workflows/<pack>/<id>.yaml`) whose nodes are registered Python functions (including nested `run-recipe`, depth ≤ 3). Hybrid router **selects** a named recipe (classifier when id omitted); it **never invents** a DAG. New graphs only via `compose-from-parts --advanced` (typed ports, 16/24 cap). Per-run **files** under `./runs/{suffix}-{timestamp}/` are **audit only** (no crash-resume). Cursor-like TOML gates; MCP `run_workflow` never waits. **Persistent localhost UI** (`127.0.0.1`) is a critical shared workspace. RAG is a facade after a LightRAG 1.5 spike. Memory is capped markdown in two scopes. Eval layout is `eval/gold/` + `electrical-engineer eval`. Exact token `unchecked`.
- **Consequences:** Implementers must not add an agent loop, crash-resume, or router-authored graphs. Hosts keep LLM loops; CLI is deterministic glue plus registered LLM nodes. MATLAB remains optional.
- **Alternatives:** LangGraph (rejected); Temporal cluster (rejected); DSH/Cordis runtime (rejected, H4/H5); embed Treadle/Ordius/Tasked (rejected); Python-function-only catalog with no YAML (rejected); crash-resume from run dir (rejected); MCP allow-all (rejected).
- **Sources:** owner Q17–Q64 + UI addendum; `research/notes/architecture-qa-gate.md`; `research/notes/spatiotemporal-composability.md`; `research/notes/light-dag-fsm-and-language.md`

---

## ADR-0008 — Persistent UI stack + DESIGN-coinbase visual system

- **Status:** accepted (design lock 2026-09-10; A1)
- **Context:** The student and the host agent share a persistent localhost workspace. Slots may *inspire* DeepSeek Harness register-into-named-holes, but Cordis/DSH as a runtime is H4/H5. The owner supplied a Coinbase marketing-surface analysis as the visual system.
- **Decision:** FastAPI + Vite/React + Zustand + a **thin** in-repo slot registry. Bind `127.0.0.1` only. Visual tokens come only from [`docs/design/DESIGN-coinbase.md`](docs/design/DESIGN-coinbase.md). Fonts: Inter + JetBrains Mono or Geist Mono. Product name is **Arc**. Header chrome uses the Arc icon (`assets/brand/arc-icon.png`, served as `/arc-icon.png`). Exact token `unchecked` is a `badge-pill`. Semantic green/red are text-only. Styling is CSS variables + CSS modules. Closed log: [`docs/planning/DESIGN_LOCK.md`](docs/planning/DESIGN_LOCK.md).
- **Consequences:** U1 publishes the token map; B_UI implements CSS variables (no raw hex in components); T1 checks chrome; D1/H1 forbid Coinbase fonts/wordmark. Do not invent a second palette or run `impeccable teach` to replace this system.
- **Alternatives:** HTMX (rejected); Tailwind-as-architecture (rejected); MUI/Ant (rejected); Coinbase licensed fonts (rejected); global dark mode (rejected); Cordis/DSH dependency (rejected).
- **Sources:** owner design upload; `docs/design/DESIGN-coinbase.md`; `docs/planning/DESIGN_LOCK.md`

---

## ADR-0009 — Hybrid engine composition (host path)

- **Status:** accepted (this graph, 2026-09-13)
- **Context:** Long YAML that includes `solve-explain` starves the host viva (FR21). Unconstrained on-the-fly tool graphs (ToolWeave) would let fluent `Vout` become SPICE. D13 froze “router never invents a DAG.”
- **Decision:** **Hybrid quality.** Host + on-demand pack skills compose the job. Large jobs **write `plan.md` then execute**. Typed engines own numbers. Short physics attachments (`simulate-circuit`) stay as YAML replay. Host may `propose_composition` of **registered** engines (`apply: false` validates; `apply: true` runs). Mega `solve-*` YAML is CLI/gold rollback. Four layers 0–3; no Layer 4. Python multi-turn composition dialog remains the H3 falsifier.
- **Consequences:** Reopens D13 only into allowlisted engine graphs. MCP target verbs include `propose_composition` (still 5–7). `solve-explain` is not on the host-path allowlist. Unmatched still cannot auto-spice (netlist-port predicate). Files: `plan.md` + `evidentiary.json` seed + `argument.md`. Root skill `skills/SKILL.md` teaches plan-then-execute.
- **Alternatives:** Keep long YAML as the host-path brain (rejected); OpenMontage markdown-physics (rejected); unconstrained on-the-fly spice (rejected); add Layer 4 (rejected); eighth MCP `plan` verb (rejected — `apply: false` on the same verb).
- **Sources:** `research/notes/hybrid-engine-composition.md`; `docs/ARCHITECTURE.md`; `docs/ARCHITECTURE_CRITIQUE.md`; `docs/PRD.md` FR10/FR17/FR21/FR23

---

## ADR-0010 — Capability-first domain kernel (D19)

- **Status:** accepted (this graph, 2026-09-13)
- **Context:** Hybrid composition (ADR-0009) still named *providers* (`run-spice`, YAML, FastAPI, LightRAG) as if they were the product. That cannot express “any in-bound UG EE question”: signals/EM/measurements look like missing SPICE recipes. The owner asked to refine architecture so it is general enough for the UG bound and not heavily reliant on one stack, while staying domain-specific.
- **Decision:** **Capability registry is the domain contract.** Fourteen allowlisted capabilities cover the curriculum-map packs and seven task genres. Providers (ngspice, python-control, pandapower, sympy, MATLAB-if-present, RAG facade, figure libraries) and encodings (YAML attachments, Python CLI, FastAPI+React) are **this-pass freezes**. Coverage law: every in-bound question has a complete path (provider check **or** exact token `unchecked` + cannot-do). `propose_composition` may name capability ids; the kernel binds an installed provider or `CD-NO-PROVIDER`. Does not reopen H3/H5, `unchecked`, UG bound, or validate-then-apply.
- **Consequences:** Pack skills teach method + which capability to request, not “always SPICE.” Missing YAML is `CD-YAML-GAP`, not out-of-product. Runner still uses today’s Python activity keys until a code plan maps capability→provider. Gold depth may stay circuits-first.
- **Alternatives:** Keep engine ids as the architecture vocabulary (rejected — circuits-shaped hole); one mega “solve any EE” LLM node (rejected — FR2/`unchecked`); add a capability per GATE trick question (rejected — bound is curriculum-map); lock ngspice/MATLAB as identity (rejected).
- **Sources:** `docs/ARCHITECTURE.md` §0; `docs/curriculum-map.md`; `research/notes/ee-task-taxonomy-draft.md`; `docs/PRD.md` FR10/FR19; `DECISIONS.md` ADR-0005/0009

---

## ADR-0011 — Harness persist, observe, spawn (D20)

- **Status:** accepted (this graph, 2026-09-13)
- **Context:** Context and ACI kinds were specified; as-built persist (memory list-only, RAG inventory-only), observation (summary without reason enums), kernel hooks vs host compaction, and pack-specialist spawn files were thin. Owner asked to specify the rest of a harness without becoming H5.
- **Decision:** **Split the harness.** Layer 0 owns loop, compaction, continuation, model routing, and **host-native** specialist spawn. Layer 2 owns run audit, named memory files (explicit write; `lessons.md` proposed not silent), BYO RAG ingest pipeline, `observation.json`, and deterministic hooks (ingest, validate-then-apply, repair, observe, lesson-propose, eval). Adapter markdown lives in `hosts/adapters/` for the student host to copy. Local-only: no fleet learning, no chat dumps.
- **Consequences:** Extract/chunk remains `CD-RAG-PARSE` until a code plan. Observation may seed on `summary.json`. Chat/Work still does not claim spawn. A Python specialist orchestrator remains the H3/H5 falsifier.
- **Alternatives:** Python multi-agent runtime (rejected, H5); silent memory append every turn (rejected); cloud telemetry (rejected, FR6); treating host compaction as our middleware (rejected).
- **Sources:** `docs/ARCHITECTURE.md` §0.3 §2.5 §10–§11; `docs/PRD.md` FR13/FR19/FR24; `hosts/adapters/README.md`

---

## ADR-0012 — Public name Arc

- **Status:** accepted (owner 2026-09-13, docs pass)
- **Context:** PID Q1 and research D14 kept the job title **Electrical Engineer** as the product name, with public category **lab** and analog “turn your AI coding assistant into an undergraduate electrical-engineering lab.” The owner asked for a short public name **Arc**, a README first line without “lab,” and the same logo in UI chrome.
- **Decision:** Public name is **Arc**. README first line: **turn your AI coding assistant into an undergraduate electrical engineer** (not “UG Electrical Engineer” — UG is insider; “an UG” is ungrammatical). CLI `electrical-engineer` and GitHub repo `Electrical-Engineer` stay until a code rename. Header chrome uses `assets/brand/arc-icon.png` (as-built topbar). README lockup is `assets/brand/arc-lockup.png`. “Lab” is not the README first line.
- **Consequences:** Product docs (README, PID, PRD, AGENTS, extensive, design lock) say Arc. Python package and binary names are unchanged this pass. UI topbar already shows the Arc icon from main.
- **Alternatives:** Keep Electrical Engineer (research default, rejected by owner); “an UG Electrical Engineer” (rejected — jargon + grammar); coined lab/bench names (still collided).
- **Sources:** owner request 2026-09-13; `research/notes/naming-and-positioning.md`; `README.md`; `docs/PID.md`

---

## ADR-0013 — Artifact names, ACI, src ownership, run, fail-closed

- **Status:** accepted (this graph)
- **Context:** D19/D20 code waves need frozen file names, MCP verbs, and write-path ownership so parallel makers do not collide. Stack change is not required (system-design-tradeoffs default: SIMPLICITY). Host owns the inner loop (`agentic-system-design`); kernel is tools + gates. Source of truth is run-dir files, not a new database (`backend-architecture`).

### Trust

- UI binds `127.0.0.1` only. No product cloud. Secrets via env / host stores. MCP never waits. Peer MATLAB/Copilot scalars are not providers. Unverified numbers use the exact token `unchecked`. Student data stays local.

### Fail closed

- Unknown capability or provider id → reject
- No installed provider → `CD-NO-PROVIDER` + `unchecked`
- Photo / compose / control-diagram on MCP → fail with `ui_url`, never hang
- Invented session verbs (`lookup_vout_guess`) → reject
- Missing spice/tool → `unchecked`, never a fake pass

### Decision

**Artifacts** under `./runs/<id>/`: `evidentiary.json` (seed/alias `summary.json`), `argument.md`, `observation.json`, `plan.md` (large host jobs).

**ACI (5–7):** `list_workflows`, `retrieve`, `open_ui`/`clarify`, `simulate_attachment`, `propose_composition` (`apply: false|true`), `label`/`summary`. `run_workflow` = short-attachment / eval rollback. `eval_run` is CLI-equivalent.

**Src ownership (this graph):**

- Kernel: `nodes/`, `runner/`, `compose/`, `gates/`, `unchecked.py`, `capabilities.py`
- ACI: `mcp/`, `cli.py`, `router/`
- RAG: `rag/`
- UI: `ui/`, `ui_server/`
- Host docs: `docs/hosts/`, `hosts/`, `skills/SKILL.md`
- Workflows: `workflows/`
- Packs: `skills/<pack>/`

**Run:** `electrical-engineer --help`; `electrical-engineer run simulate-circuit`; `electrical-engineer ui` (127.0.0.1); `electrical-engineer mcp`.

- **Consequences:** B* makers must not write outside those globs. No H5 Python orchestrator. No new DB.
- **Alternatives:** HTTP MCP this graph (rejected — Later); Next.js SSR (rejected — keep Vite CSR); extra MCP tools per provider (rejected — FR17).
- **Sources:** `docs/ARCHITECTURE.md` §0–§2; `docs/PRODUCT.md`; `LOOP_GRAPH.md`

---

## ADR-0014 — UG EE knowledge corpus layout (not RAG)

- **Status:** accepted (this graph)
- **Context:** Maintainers need a licence-clean, nested teaching corpus for later retrieval. ADR-0002 already forbids commercial book bytes in git and keeps BYO RAG on the student machine. Dumping notes into `research/` or auto-ingesting into the RAG facade would mix product ingest with authorial handbooks.

### Trust

- Git may hold original pedagogical text and SPDX-clean CC BY / CC BY-SA / CC0 files only.
- No commercial textbooks, no third-party exam PDFs, no NC licences (`CC-BY-NC`).
- This tree is untrusted as a number authority: it does not mint checked ohms; `unchecked` and providers stay in the kernel.
- No auth, no secrets, no product cloud.

### Fail closed

- `oer/` file without `SPDX-License-Identifier: CC-BY-4.0` or `CC-BY-SA-4.0` or `CC0-1.0` → checker fail
- NC or commercial-book verbatim markers → checker fail
- Missing COVERAGE unit path → checker fail
- Stub unit (under word/question floors) → checker fail unless `--allow-empty` (scaffold only)

### Decision

**Layout:** `knowledge/ug-ee/<pack>/<unit>/{notes,questions,sources}.md` plus optional `oer/`. Manifest `knowledge/COVERAGE.yaml` is checker truth. Run: `python scripts/check_knowledge_tree.py`.

**Not wired to RAG.** `electrical-engineer rag add` is not pointed at `knowledge/` this graph.

**Exam items:** original reconstructions (exam-*style*). Never GATE or university paper text.

**D19 graph:** archived at `docs/planning/LOOP_GRAPH_D19.md`; this graph’s loop plans live in `plans/knowledge-loops/`.

- **Consequences:** Pack makers write only their glob. Retrieval is a later graph. Product `src/` stays untouched.
- **Alternatives:** Link-only syllabus map (rejected — owner chose original+CC-BY); store under `.electrical-engineer/corpus/` (rejected — that path is gitignored BYO); auto-ingest into LightRAG (rejected — Later).
- **Sources:** `docs/planning/GATE_0_UG_EE_KNOWLEDGE.md`; `knowledge/PRODUCT.md`; `research/notes/ee-corpus-and-licensing.md`; constitution V

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
- **Decision:** FastAPI + Vite/React + Zustand + a **thin** in-repo slot registry. Bind `127.0.0.1` only. Visual tokens come only from [`docs/design/DESIGN-coinbase.md`](docs/design/DESIGN-coinbase.md). Fonts: Inter + JetBrains Mono or Geist Mono. Product name remains Electrical Engineer. Exact token `unchecked` is a `badge-pill`. Semantic green/red are text-only. Styling is CSS variables + CSS modules. Closed log: [`docs/planning/DESIGN_LOCK.md`](docs/planning/DESIGN_LOCK.md).
- **Consequences:** U1 publishes the token map; B_UI implements CSS variables (no raw hex in components); T1 checks chrome; D1/H1 forbid Coinbase fonts/wordmark. Do not invent a second palette or run `impeccable teach` to replace this system.
- **Alternatives:** HTMX (rejected); Tailwind-as-architecture (rejected); MUI/Ant (rejected); Coinbase licensed fonts (rejected); global dark mode (rejected); Cordis/DSH dependency (rejected).
- **Sources:** owner design upload; `docs/design/DESIGN-coinbase.md`; `docs/planning/DESIGN_LOCK.md`

---

## ADR-0009 — Hybrid engine composition (host path)

- **Status:** proposed (not owner-Accepted)
- **Context:** Long YAML that includes `solve-explain` starves the host viva (FR21). Unconstrained on-the-fly tool graphs (ToolWeave) would let fluent `Vout` become SPICE. D13 froze “router never invents a DAG.”
- **Decision:** **Hybrid quality.** Host + on-demand pack skills compose the job. Large jobs **write `plan.md` then execute**. Typed engines own numbers. Short physics attachments (`simulate-circuit`) stay as YAML replay. Host may `propose_composition` of **registered** engines (`apply: false` validates; `apply: true` runs). Mega `solve-*` YAML is CLI/gold rollback. Four layers 0–3; no Layer 4. Python multi-turn composition dialog remains the H3 falsifier.
- **Consequences:** Reopens D13 only into allowlisted engine graphs. MCP target verbs include `propose_composition` (still 5–7). `solve-explain` is not on the host-path allowlist. Unmatched still cannot auto-spice (netlist-port predicate). Files: `plan.md` + `evidentiary.json` seed + `argument.md`. Root skill `skills/SKILL.md` teaches plan-then-execute.
- **Alternatives:** Keep long YAML as the host-path brain (rejected); OpenMontage markdown-physics (rejected); unconstrained on-the-fly spice (rejected); add Layer 4 (rejected); eighth MCP `plan` verb (rejected — `apply: false` on the same verb).
- **Sources:** `research/notes/hybrid-engine-composition.md`; `docs/ARCHITECTURE.md`; `docs/ARCHITECTURE_CRITIQUE.md`; `docs/PRD.md` FR10/FR17/FR21/FR23

# Question bank

Every open research question for this phase. Status: `open` | `answered` | `deferred`.

| ID | Question | Owner WS | Status | Answer / deferral pointer |
|----|----------|----------|--------|---------------------------|
| Q1 | Is a Pi **package** enough for EE specialization, or is a **fork** required? | WS-A | answered | Package-first hybrid; fork only if extension APIs fail — `notes/pi-feasibility.md` |
| Q2 | Can RAG plug into Pi without forking? | WS-A | answered | Yes — Pi documents dynamic context RAG via extensions — `notes/harness-landscape.md` |
| Q3 | How portable are Pi skills to Claude Code / Codex / Cursor? | WS-A | answered | Skill formats converging; treat MCP+skills as portable core — `notes/harness-landscape.md` |
| Q4 | Which EE textbooks can we legally index? | WS-B | deferred | Intended: curator-licensed **embedding packs**; until licence review, **BYO + OER** — `notes/ee-corpus-and-licensing.md`, `notes/local-package-and-embedding-release.md` |
| Q5 | How should formulae and circuit figures be preserved? | WS-B | answered | Layout/formula-aware parse; LaTeX/MathML preferred; figures via caption+image — `notes/rag-parsing-formulae-figures.md` |
| Q6 | What chunking/retrieval design fits EE? | WS-B | answered | Structure-aware + parent-child + hybrid dense/BM25 — `notes/rag-chunking-and-retrieval.md` |
| Q7 | Should RAG enter as MCP, middleware, or multi-hop? | WS-B | answered | MCP portable core + skill multi-hop; optional Pi middleware — `notes/rag-agent-integration.md` |
| Q8 | How do we evaluate EE RAG? | WS-B | answered | Retrieval/faithfulness/citation/EE failure taxonomy + 20 case titles — `notes/rag-eval-methodology.md` |
| Q9 | Is MATLAB/Simulink the primary verifier? | WS-C | deferred | Intended primary; CP-2 licence pending — `notes/matlab-simulink-surface.md` |
| Q10 | What OSS verification covers which domains? | WS-C | answered | Coverage matrix in `notes/open-source-verification.md` |
| Q11 | What task genres define undergrad-EE-capable? | WS-D | answered | Seven genres × GATE sections — `notes/ee-task-taxonomy-draft.md` |
| Q12 | How to measure capability without a PRD? | WS-D | answered | Rubrics + verified/judgement split — `notes/capability-eval-design.md` |
| Q13 | Among O1–O4, which path? | WS-E | answered | O1 hybrid; runner-up O3 — `synthesis/recommendation.md` |
| Q14 | Local/offline models first-class? | WS-E | answered | Yes — local-first package + local vector store; API optional — `notes/local-package-and-embedding-release.md` |
| Q15 | Map PG/PhD genres now? | WS-D | deferred | Light stretch map only; undergrad primary |
| Q16 | Ship curated embeddings via GitHub Release into local Chroma? | WS-B | answered | Feasible; Chroma default; split packs &lt;2 GiB; licence review required — `notes/local-package-and-embedding-release.md` |
| Q17 | Photo of circuit → editable UI → Simulink sim? | WS-C | answered | Feasible via netlist intermediate + UI gate; Simulink/SPICE backends — `notes/photo-to-schematic-to-simulink.md` |
| Q18 | How far has AI come in core engineering (EE, manufacturing, civil), and what success bar should this OSS student project claim? | WS-D | answered | Tool-using verify loops are the real progress; UG-bounded tutor + later research fork — `notes/ai-core-engineering-landscape.md`, root `README.md` |
| Q19 | Steal Cordis/DSH spatiotemporal composability how, without forking DSH? | WS-A | answered | Paradigm only: node plugins in space, DAG recipes in time; do not run Cordis/DSH — `notes/spatiotemporal-composability.md` |
| Q20 | Map Temporal child-workflow vs activity without a Temporal cluster? | WS-A | answered | Node = activity; `run-recipe` = nested named YAML (depth ≤ 3, cycle check) — `notes/architecture-qa-gate.md` |
| Q21 | Light DAG vs FSM vs code-as-workflow vs embeddable library? | WS-A | answered | Custom in-process DAG + tiny FSM; YAML recipes; Python node functions; not LangGraph/Temporal/Treadle — `notes/architecture-qa-gate.md` |
| Q22 | CLI/runner language: Python-only vs Rust/Go CLI + Python nodes? | WS-A | answered | Python 3.11+ CLI/runner/nodes via pip this pass; Go/Rust CLI skin later allowed — `notes/architecture-qa-gate.md` |
| Q23 | How strict is dynamic-compose allowlisting? | WS-A | answered | Typed ports + 16 nodes / 24 edges; only `compose-from-parts`; fail closed — `notes/architecture-qa-gate.md` |
| Q24 | Freeze catalog ids and human titles? | WS-D | answered | Author `docs/WORKFLOWS.md` from owner list; ids renamable until CLI ships; do not freeze the research draft as API — `notes/architecture-qa-gate.md` |
| Q25 | Collapse per-pack explain-* into one workflow? | WS-D | answered | Keep per-pack explain titles — `notes/architecture-qa-gate.md` |
| Q26 | Gate policy file shape (global vs project, allow-all)? | WS-A | answered | Global + project TOML; most-restrictive wins; file + `EE_ALLOW_ALL` + `--allow-all` — `notes/architecture-qa-gate.md` |
| Q27 | Unmatched-intent path details? | WS-A | answered | Always `unmatched-cosolver`; no auto-simulate; exact token `unchecked` — `notes/architecture-qa-gate.md` |
| Q28 | Photo stub contract (C4 still P1)? | WS-C | answered | Detect → connect → OCR → draft netlist → persistent UI confirm; `.cir` + JSON; no sim after confirm — `notes/architecture-qa-gate.md` |
| Q29 | Resume-after-crash via run-dir vs always restart? | WS-A | answered | No crash-resume. Run dir is audit only. New run after process death — `notes/architecture-qa-gate.md` |
| Q30 | May a node invoke another named recipe (child)? | WS-A | answered | Yes: `run-recipe`, max depth 3, cycles rejected — `notes/architecture-qa-gate.md` |
| Q31 | What product *class* is Electrical Engineer relative to OpenMontage (not MCP/CLI/plugin/harness)? | WS-G | answered | Same class: harness-native domain system. Vertical: undergraduate EE lab. — `notes/similar-agentic-domain-systems.md`, `notes/naming-and-positioning.md` |
| Q32 | Reopen PID Q1 — rename the product off Electrical Engineer? | WS-G | answered | No. Keep Electrical Engineer. Coined lab/bench names collide (EEBench, CircuitLab, Fuse). — `notes/naming-and-positioning.md` |
| Q33 | What category noun replaces the rejected “Agentic UG EE Studio”? | WS-G | answered | Public: **lab**. Internal: harness-native domain system. Mode stays co-solver. — `notes/naming-and-positioning.md` |
| Q34 | Topology A (markdown control plane) vs B (YAML as brain) vs C (hybrid)? | WS-G | answered | C. Host agent orchestrates the work; Python owns physics. — `notes/domain-system-architecture-patterns.md` |
| Q35 | Does C reopen H3 or drop the YAML runner? | WS-G | answered | No. H3 stays. Runner remains the deterministic backbone and genre contract. Host must not invent spice DAGs. — `notes/domain-system-architecture-patterns.md`; D16 |
| Q36 | GTM: GATE homepage vs host clubs vs CLI-only? | WS-G | answered | Host clubs first; divider eval as demo; GATE stays eval overlay; CLI-only remains a complete path. — `notes/student-gtm-ug-ee.md` |
| Q37 | Internal class: harness-native domain system vs **domain kernel** vs executive kernel vs studio? | WS-G | answered | Domain kernel. Host owns the loop. Steal no-bypass writes, not KAIJU’s runtime. Public noun stays lab. — `notes/agentic-kernel-2026.md` |
| Q38 | Attach order: MCP-first vs CLI-first vs Code Mode first? | WS-G | answered | CLI inner, MCP outer, PTC/Code Mode later on reads only. — `notes/domain-kernel-layering.md` |
| Q39 | Keep mega `run_workflow` (YAML DAG including `solve-explain`) as the host’s only write? | WS-G | answered | No on the host path (starves the viva). Yes as headless eval rollback and one-command CLI. — `notes/domain-kernel-layering.md` |
| Q40 | One artifact blob vs two bands (evidentiary vs engineering argument)? | WS-G | answered | Two bands. Host explanation cannot mint checked scalars. — `notes/agentic-kernel-2026.md` |

## Sources

- Research notes under `research/notes/` and `research/synthesis/` — retrieved 2026-09-07 — reliability: primary
- User instructions — retrieved 2026-09-07 — reliability: primary

## Confidence

Overall confidence for this register: high

Deferred rows wait on user CP-1/CP-2 or later product choices.

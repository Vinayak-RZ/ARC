# PROGRESS

Live status. Research phase completed on `cursor/ee-research-phase-7e0c`. Product identity + PRD work is on `cursor/product-identity-draft-82c4`. Technical architecture is on `cursor/tech-architecture-82c4`.

| Phase | Status | Notes |
|-------|--------|-------|
| 0 Scaffold | done | Validator + registers |
| A Harness | done | D6/D7 notes |
| B RAG | done | D8–D12 notes |
| C Verification | done | D13/D14 notes |
| D Capability | done | D15/D16 notes |
| E Synthesis | done | Scoring + memo + ADR seeds |
| F README | done | readable + extensive; 2026-09-10 aligned to architecture |
| S Spikes | skipped | No user approval |
| N Hardening | done | validate --full PASS; see PHASE_N_COMPLETION.md |
| R RAG-Anything eval | done | `rag-anything-evaluation.md`, `rag-stack-recommendation.md`, ADR-0004 |
| G Core-EE landscape + success bar | done | `ai-core-engineering-landscape.md`, README capabilities C1–C8 |
| P Product identity | done (P0) | `docs/PID.md` **Accepted**; shape note 2026-09-10 (workflows, UI) |
| Curriculum map | done | `docs/curriculum-map.md` — UG India+global; GATE = eval overlay |
| PRD | **accepted (this graph)** | FR10–FR16; §10/§11 closed D0 |
| Architecture research | done | composability, DAG/language, catalog draft |
| Technical architecture | **accepted (this graph) + Proposed D19/D20 overlays** | `docs/ARCHITECTURE.md` §0 capabilities; §0.3 harness; ADR-0010/0011 |
| Pack skills | **Proposed D19 method bodies** | `skills/<pack>/SKILL.md` — UG method + capability ids |
| Harness persist/observe/spawn | **Proposed D20** | named memory, `observation.json`, kernel hooks, `hosts/adapters/` |
| Product execution plan | **H1 complete; D19/D20 complete (archived)** | D19 archive [`docs/planning/LOOP_GRAPH_D19.md`](docs/planning/LOOP_GRAPH_D19.md); H1 [`EXECUTION_GRAPH.md`](EXECUTION_GRAPH.md) |
| UG EE knowledge corpus | **archived** | [`docs/planning/LOOP_GRAPH_KNOWLEDGE.md`](docs/planning/LOOP_GRAPH_KNOWLEDGE.md) |
| Pack skills + MATLAB MCP | **complete (H1)** | [`LOOP_GRAPH.md`](LOOP_GRAPH.md); branch `cursor/ee-skills-matlab-mcp-37b3` |
| UI design lock | **closed** | DESIGN-coinbase; ADR-0008 accepted |
| Validator | PASS | `./scripts/research/validate-research.sh --full` |

## Assumptions

- CP-1: No commercial PDFs in git; BYO + licence-clean reconstructions; exam-style items in-scope without committing third-party papers.
- CP-2: MATLAB if present; OSS first-class. Entire product must work without MATLAB.
- Phase S cancelled until explicitly approved.
- Research `recommendation.md` O1/H2 is historical advice; product harness is H3.
- Architecture Q&A answers shape the accepted docs and the PRD FRs.

## Refinement log

| Date | Change |
|------|--------|
| 2026-09-08 | Local-first package + GitHub embedding packs (Chroma) + photo→schematic→Simulink research notes; Q16–Q17, D9–D10 |
| 2026-09-08 | RAG-Anything evaluation + ADR-0004; D11 multimodal ingest engine |
| 2026-09-08 | AI-in-core-engineering landscape + README success-bar capabilities; Q18, D12, ADR-0005 seed |
| 2026-09-09 | Draft PID + decision sheet; harness H1–H5 left OPEN for owner |
| 2026-09-09 | P0 locks accepted: H3 CLI, Apache-2.0, UG coursework bound, co-solver, label-unchecked, one repo |
| 2026-09-09 | PRD written; ADRs 0001/0005/0006 accepted; README identity aligned |
| 2026-09-10 | Proposed architecture: YAML DAG runner, persistent localhost UI, tagged RAG, markdown memory, `eval/gold/` |
| 2026-09-10 | PID/PRD/README upgraded to that architecture (exact `unchecked`, named workflows, UI, FR10–FR16) |
| 2026-09-10 | Vendored `cursor-config-coding` @ `280dbc5` (nawab lite default, Spec Kit v1.0.6, opt-in graph-engineering) |
| 2026-09-10 | Gate 0 research for product nawab+graph plan; compile blocked on owner answers |
| 2026-09-10 | Compiled nawab project plan + execution graph + 25 node plans; Gate 0 closed |
| 2026-09-10 | DESIGN-coinbase locked as UI visual system; ADR-0008 seeded; Wave 0 waits on owner start |
| 2026-09-10 | Owner start: D0+A1 executed; Spec Kit scaffolded; product `src/` begins Wave 1 |
| 2026-09-12 | D19 capability-first overlay: coverage law, 14 capabilities, pack method skills; providers/YAML/UI are this-pass freezes |
| 2026-09-13 | D19/D20 graph-of-loops compiled: `LOOP_GRAPH.md` + `plans/loops/`; XOR graph-engineering |

## Handoff

PID: [`docs/PID.md`](docs/PID.md) (Accepted)  
PRD: [`docs/PRD.md`](docs/PRD.md) (Accepted for this graph)  
Architecture: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) (Accepted A1 + **Proposed D19/D20** overlays)  
ADRs: [`DECISIONS.md`](DECISIONS.md) (ADR-0010, ADR-0011 proposed)  
Curriculum: [`docs/curriculum-map.md`](docs/curriculum-map.md)

**Next:** none on this graph. PR `cursor/ee-skills-matlab-mcp-37b3`.

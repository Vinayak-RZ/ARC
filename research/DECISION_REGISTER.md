# Decision register

Stances for this research phase. Status: `open` | `leaning` | `proposed` | `deferred`.

| ID | Decision | Options | Stance | Decide-by phase | Notes |
|----|----------|---------|--------|-----------------|-------|
| D1 | Harness base | O1–O4 | **proposed: O1 hybrid** | Phase E | ADR-0001 |
| D2 | Knowledge grounding | priors / skills / RAG / fine-tune | **proposed: RAG + skills + tool verify** | Phase B/E | ADR-0002 |
| D3 | Corpus rights | owned / library / OER / BYO | **leaning: curator-licensed embedding packs + BYO** | CP-1 | Embeddings release ≠ PDF redistribute; still needs licence review |
| D4 | RAG insertion | MCP / middleware / multi-hop | **proposed: MCP + multi-hop skills** | Phase B | Local store behind MCP |
| D5 | Primary verifier | MATLAB / OSS / hybrid | **proposed: MATLAB primary, OSS fallback** | Phase C | ADR-0003; CP-2 |
| D6 | Distribution | sealed app / multi-agent | **proposed: local package + multi-host skills** | Phase A | Local-first install |
| D7 | Capability framing | exams / task genres | **proposed: task genres × verification** | Phase D | |
| D8 | Recommended build path | O1–O4 | **proposed: O1 (runner-up O3)** | Phase E | `synthesis/recommendation.md` |
| D9 | Vector store | Chroma / sqlite-vec / LanceDB | **leaning: Chroma default, sqlite-vec optional** | 2026-09-08 | `notes/local-package-and-embedding-release.md` |
| D10 | Circuit vision pipeline | VLM-only / structured detect+netlist / hybrid | **leaning: structured netlist + UI edit gate** | 2026-09-08 | `notes/photo-to-schematic-to-simulink.md` |
| D11 | Multimodal RAG engine | RAG-Anything / thin MinerU+MCP / commercial | **proposed: RAG-Anything behind MCP** | Spike gate | ADR-0004; `rag-stack-recommendation.md` |
| D12 | Success bar / product promise | vibe / exam-only / verified capability list | **proposed: UG-bounded verified capabilities + later research fork** | 2026-09-08 | ADR-0005; landscape note + README |
| D13 | Orchestrator / recipes / UI / eval | LangGraph / Temporal / DSH / custom YAML DAG | **proposed: Python YAML DAG + persistent localhost UI + eval/gold** | 2026-09-10 | ADR-0007; `docs/ARCHITECTURE.md`. Runner freeze stands. Who *drives* the work is D16. |
| D14 | Product name (PID Q1) | Electrical Engineer / coined lab-bench names / ChemCrow-style | **proposed: keep Electrical Engineer** | WS-G lock sheet | `notes/naming-and-positioning.md`. Zero rename cost; collisions kill EEBench/CircuitLab/Fuse. |
| D15 | Category noun | studio / lab / bench / system / co-solver / MCP / domain kernel | **proposed: lab (public); domain kernel (internal); co-solver (mode)** | WS-G lock sheet | Reject “Agentic UG EE Studio”. Kill bench (EEBench.org). Domain kernel supersedes “harness-native domain system” as the internal name. |
| D16 | Who orchestrates the professional workflow | A markdown control plane / B YAML FSM as brain / C hybrid | **proposed: C hybrid** | WS-G lock sheet | Host agent plans and explains; Python owns verifiers, gates, eval. Does not reopen H4/H5. Does not supersede D13’s YAML runner as the physics backbone. |
| D17 | Domain-kernel layers and host ACI | mega `run_workflow` / 1:1 node MCP / 5–7 verbs + two-band + spend/clamp | **proposed: four layers; CLI inner MCP outer; spend host on viva; clamp numbers; two-band artifacts** | WS-G lock sheet | `notes/domain-kernel-layering.md`. Does not ship code in this pass. |

## Sources

- `research/synthesis/recommendation.md` — retrieved 2026-09-07 — reliability: primary
- `DECISIONS.md` ADR seeds — retrieved 2026-09-07 — reliability: primary
- `research/notes/naming-and-positioning.md` — retrieved 2026-09-12 — reliability: primary
- `research/notes/domain-system-architecture-patterns.md` — retrieved 2026-09-12 — reliability: primary
- `research/notes/agentic-kernel-2026.md` — retrieved 2026-09-12 — reliability: primary
- `research/notes/domain-kernel-layering.md` — retrieved 2026-09-12 — reliability: primary

## Confidence

Overall confidence for this register: high

`proposed` stances await your acceptance; `deferred` await CP-1/CP-2.

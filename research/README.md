# Research phase — map

This directory holds the **research-only** phase of Electrical-Engineer.
Nothing here is product code. The goal is to decide *what to build* (harness base,
EE textbook RAG, verification surface, capability framing, and — in WS-G — product
class, names, orchestrator split, and domain-kernel layering) and write recommendation memos.

> Full internals of the repo (every folder and important file): see the eventual
> companion at [`docs/EXTENSIVE.md`](../docs/EXTENSIVE.md) after Phase F.

## How to read these notes

1. Start with [`question-bank.md`](question-bank.md) — every open research question.
2. Check [`DECISION_REGISTER.md`](DECISION_REGISTER.md) — options and current stances.
3. Read domain notes under [`notes/`](notes/).
4. End with [`synthesis/recommendation.md`](synthesis/recommendation.md) (historical O1 harness) and [`synthesis/rag-stack-recommendation.md`](synthesis/rag-stack-recommendation.md) when evaluating RAG engine choice.
5. For class, names, hybrid architecture, and layering: [`synthesis/domain-system-recommendation.md`](synthesis/domain-system-recommendation.md) then [`synthesis/vision-lock-sheet.md`](synthesis/vision-lock-sheet.md). Kernel harvest: [`notes/agentic-kernel-2026.md`](notes/agentic-kernel-2026.md), [`notes/domain-kernel-layering.md`](notes/domain-kernel-layering.md).
6. Sources are catalogued in [`source-ledger.md`](source-ledger.md).

## Note shape

Copy [`NOTE.template.md`](NOTE.template.md). Every committed note must include
`## Sources` and `## Confidence`. The gate
[`scripts/research/validate-research.sh`](../scripts/research/validate-research.sh)
rejects unfinished-work tokens, missing sections, PRD language in the
memo, and (heuristically) verbatim book text.

## Workstreams

| ID | Topic | Primary artifacts |
|----|-------|-------------------|
| WS-A | Harness base | `notes/harness-landscape.md`, `notes/pi-feasibility.md` |
| WS-B | EE textbook RAG | `notes/ee-corpus-and-licensing.md`, `notes/rag-*.md`, `notes/local-package-and-embedding-release.md`, `notes/rag-anything-evaluation.md` |
| WS-C | Verification | `notes/matlab-simulink-surface.md`, `notes/open-source-verification.md`, `notes/photo-to-schematic-to-simulink.md` |
| WS-D | Capability & evals | `notes/ee-task-taxonomy-draft.md`, `notes/capability-eval-design.md`, `notes/ai-core-engineering-landscape.md` |
| WS-E | Synthesis | `synthesis/option-scoring.md`, `synthesis/recommendation.md`, `synthesis/rag-stack-recommendation.md` |
| WS-F | README compilation | root `README.md`, `docs/EXTENSIVE.md` |
| WS-Arch | Technical architecture | `notes/spatiotemporal-composability.md`, `notes/light-dag-fsm-and-language.md`, `notes/architecture-qa-gate.md`, `docs/ARCHITECTURE.md`, `docs/WORKFLOWS.md` |
| WS-G | Domain kernel, names, GTM | `notes/domain-system-architecture-patterns.md`, `notes/similar-agentic-domain-systems.md`, `notes/naming-and-positioning.md`, `notes/student-gtm-ug-ee.md`, `notes/agentic-kernel-2026.md`, `notes/domain-kernel-layering.md`, `synthesis/domain-system-recommendation.md`, `synthesis/vision-lock-sheet.md` |

## Assumptions while blockers are open

- **Textbook rights (CP-1):** default remains **no commercial PDFs in git**. Intended delivery is **curator-licensed embedding packs** via GitHub Release into a local vector store; until each title’s licence is reviewed, treat packs as blocked and fall back to BYO + OER.
- **MATLAB licence (CP-2):** research covers MathWorks MCP as the *intended* primary verifier; open-source verification is researched in parallel in case a licence is unavailable.
- **agent-patterns MCP:** unreachable in this cloud environment; architecture pattern IDs are marked `MCP-PENDING` where relevant.

## What you learned (scaffold)

- A research phase needs a failable gate, not just good intentions.
- Separating question bank, decision register, and source ledger keeps notes from becoming the only source of truth.
- Core-engineering AI progress is real but lives in verify-loops and vendor toolchains; an open student EE harness is still the gap.
- OpenMontage’s class is right; “studio” is the wrong noun. Public category is **lab**; internal class is **domain kernel**; the host agent plans; code owns numbers. Mega `run_workflow` starves the viva.

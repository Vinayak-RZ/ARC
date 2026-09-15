# RAG stack recommendation — RAG-Anything vs alternatives

## Purpose

Answer whether [RAG-Anything](https://github.com/HKUDS/RAG-Anything) should be the primary RAG stack for Electrical-Engineer, and how it fits local distribution via GitHub Releases.

## Recommendation

**Primary path (proposed): RAG-Anything as the multimodal ingest + index engine, wrapped in a portable EE RAG MCP server — not as a replacement for the O1 harness.**

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Harness | O1 hybrid (unchanged) | Pi package + skills + MCP portability (`recommendation.md`) |
| Parse + index | **RAG-Anything** (MinerU default) | Matches EE PDF modality mix; avoids rebuilding modal pipelines |
| Agent interface | **MCP tools** | Cross-host; explicit citations (`rag-agent-integration.md`) |
| Models (local default) | **Ollama** or **LM Studio** | Upstream examples; injectable funcs |
| Verification | MATLAB MCP + OSS fallback | Unchanged (ADR-0003) |
| Corpus | BYO PDF + OER | Unchanged (ADR-0002) |

**Not recommended as sole stack:** RAG-Anything alone — it does not provide MCP, EE metadata, eval harness, or MATLAB verification.

**Runner-up:** MinerU (or Docling) + **thin custom MCP** with explicit BM25+dense fusion and EE chunk schema — choose if the spike shows LightRAG graph weight or dependency cost is unjustified.

**Not recommended now:** VLM-only chunking, commercial-only parsers, or Microsoft GraphRAG as the primary EE spine.

## Why RAG-Anything fits this project

1. **Document type match** — EE textbooks are exactly the multimodal, layout-heavy case RAG-Anything targets (text + equations + tables + figures + columns).
2. **Parser alignment** — Default MinerU path matches our prior research lean for formula-aware extraction.
3. **Integration cost** — Modal processors, context windows, parse cache, and batch ingest are weeks of glue we avoid writing.
4. **Local path exists** — Ollama/LM Studio/vLLM examples prove injectable backends; release install scripts can pin models.
5. **Upstream momentum** — LightRAG native integration reduces orphan-framework risk.

## Why not “RAG-Anything only”

1. **No MCP** — Our cross-agent strategy requires a tool server wrapper.
2. **EE schema** — `domain_tag`, `chunk_type`, prerequisite edges need a mapping layer on top of LightRAG entities.
3. **Heavy footprint** — MinerU models + optional VLM + LibreOffice; GitHub Release must be an installer, not a single binary.
4. **Unproven on EE PDFs** — Parser ranking in earlier notes was med confidence until a chapter spike.
5. **Graph complexity** — LightRAG entity extraction may help multi-hop concept queries but adds LLM cost and tuning surface.

## Local operation via GitHub Releases

Electrical-Engineer should treat RAG as a **release-packaged sidecar**, not repo-bundled runtime code in v1 research.

### Release contents (proposed)

| Asset | Role |
|-------|------|
| `ee-rag-mcp-{version}-py3-none-any.whl` (or platform wheel set) | MCP server + RAG-Anything dependency closure |
| `manifest.json` | Pinned versions, MinerU model URIs, optional Ollama model list |
| `install.sh` / `install.ps1` | venv, HF/MinerU cache, Ollama pulls, MCP host snippet |
| `.env.example` | `WORKING_DIR`, `OLLAMA_HOST`, `PARSER`, processing toggles |
| `SHA256SUMS` | Integrity for assets |

### Stays user-local (never in release)

- Textbook PDFs (BYO licence)
- Vector/graph stores under `~/.electrical-engineer/rag_storage/`
- Parse output under `~/.electrical-engineer/output/`
- API keys (if user opts into cloud models)

### Runtime topology (local)

```text
[Cursor / Claude / Pi+MCP bridge]
        │ stdio MCP
        ▼
  ee-rag-mcp (GitHub Release install)
        │ Python
        ▼
  RAG-Anything → MinerU parse → LightRAG index
        │
        ├── Ollama :11434 (LLM + embeddings)
        └── optional VLM (figure understanding)
```

### Modes

| Mode | Models | Image processing | Use case |
|------|--------|------------------|----------|
| **Local text-first** | Ollama llama3.2 + nomic-embed-text | Off (caption search only) | Privacy, laptops, fastest path |
| **Local full multimodal** | Above + vision model | On | Diagram-heavy power/machines texts |
| **Hybrid cloud** | Cloud LLM/VLM + local index | On | Quality when offline GPU insufficient |

## Ingest vs query (2026-09-15 overlay)

Do not treat “RAG-Anything” as both parser and online search. Split is pinned in [`../notes/rag-ingest-query-architecture.md`](../notes/rag-ingest-query-architecture.md):

| Side | Engine | Constraint |
|------|--------|------------|
| Ingest | RAG-Anything (MinerU) + EE ontology write | OCR, VLM captions, `illustrated_by` / `belongs_to` figure links |
| Query | Hybrid BM25+dense on **propositions**, then **1–2 deterministic hops** (GRASP-RAG graph, not GRASP agent loops) | p95 retrieve ≤ 7 s; 3 × 1500 char citations |

Eval bank: 12 lanes × 10 packs in [`../notes/rag-eval-pack-stack.md`](../notes/rag-eval-pack-stack.md). Decision **D21**.

## Spike gate (before ADR acceptance)

Run only on **one user-owned EE chapter** (no corpus in git):

1. Parse with RAG-Anything (`parser=mineru`, equations+tables on).
2. Measure: equation LaTeX usability, example boundary integrity, citation page error, retrieval@5 on 10 gold questions.
3. Compare wall time and disk vs thin MinerU+MCP baseline.
4. **Pass:** adopt RAG-Anything as index engine. **Fail:** MinerU-only thin MCP.

## Open questions

- Pin `lightrag-hku<1.5` vs track LightRAG 1.5+ multimodal API?
- Ship MinerU weights in release vs download-on-first-run?
- Required minimum hardware for acceptable ingest on a full textbook?
- Does BM25 need to be added beside LightRAG for symbol-heavy queries?

## What this memo does NOT decide

- MCP tool names and JSON schemas (implementation phase).
- Exact Ollama model pins per hardware tier.
- Whether Pi middleware duplicates MCP for sugar.

## Confidence

Overall confidence for this memo: med-high

Strategic fit is strong; lock-in awaits EE-chapter spike and MCP wrapper feasibility.

## Sources

- [rag-anything-evaluation.md](../notes/rag-anything-evaluation.md) — retrieved 2026-09-08 — reliability: primary
- [recommendation.md](recommendation.md) — retrieved 2026-09-08 — reliability: primary
- [option-scoring.md](option-scoring.md) — retrieved 2026-09-08 — reliability: primary
- [RAG-Anything](https://github.com/HKUDS/RAG-Anything) — retrieved 2026-09-08 — reliability: primary (S43)
- [rag-ingest-query-architecture.md](../notes/rag-ingest-query-architecture.md) — retrieved 2026-09-15 — reliability: primary
- [rag-eval-pack-stack.md](../notes/rag-eval-pack-stack.md) — retrieved 2026-09-15 — reliability: primary

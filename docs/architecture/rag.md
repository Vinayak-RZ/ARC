# Local textbook RAG — ingest and query

**Normative freeze** (citations, filters, 3 × 1500 chars, BYO, untrusted ingest): [`ARCHITECTURE.md`](../ARCHITECTURE.md) §10.  
**Harness vs kernel (plain language):** [`ON_THE_HARNESS.md`](../ON_THE_HARNESS.md).  
**This page:** the **graphs** the kernel runs on ingest vs query, and links to the approach (RAG-Anything ingest, GRASP-style proposition graph, hybrid then hops).

As-built today: `rag add` is inventory-only; retrieve is BM25 over a file prefix (`CD-RAG-PARSE`). The diagrams are the **target kernel contract**, not a claim that LightRAG or MinerU already shipped.

Engine pin remains ADR-0004 (QUALITY then SPEED). Identity is **tagged, citable, local RAG**, not a vendor library.

---

## Kernel vs harness

The **rented harness** (Cursor, Claude Code, Codex, ChatGPT desktop) owns the chat loop. It may call `retrieve` and write `argument.md`. It does **not** own the textbook index, OCR, or graph hops.

The **domain kernel** owns persist and the RAG sidecar: `rag add` ingest, the index, hybrid retrieve, bounded hops, inventory, and citation packing. It does **not** compact context, run GRASP agent rewrite loops, or mint ohms from a PDF.

```mermaid
flowchart LR
  subgraph harness ["Harness — Layer 0 host"]
    Loop[Chat loop and compaction]
    Call["MCP retrieve / CLI rag"]
  end
  subgraph kernel ["Kernel — Layer 2"]
    Add["rag add ingest"]
    Store[Filesystem tree plus graph]
    Qry["retrieve-citation"]
    Pack["3 passages times 1500 chars"]
  end
  Loop --> Call
  Call --> Qry
  Add --> Store
  Store --> Qry
  Qry --> Pack
  Pack --> Loop
```

| Job | Kernel | Host / harness |
|-----|--------|----------------|
| `rag add` (OCR, figures, propositions, index write) | Yes — ask gate | May invoke CLI; must not skip the gate |
| Filters, hybrid search, 1–2 hops, RankVote to pages | Yes | Passes query + tags only |
| Multi-hop **viva** (decompose the homework) | Hop cap inside `retrieve-passage` | Host may plan extra `retrieve` calls |
| Agentic GRASP planner / sub-agents | No | Optional in the host, not in the runner |
| Citation in evidentiary band | Yes | Host must not invent page numbers |
| Homework photo → netlist | `ingest-figure`, not this RAG path | UI confirm stays Layer 3 |

---

## Ingest graph (offline)

`electrical-engineer rag add`. Minutes per chapter are allowed. Fail closed on unreadable PDF (`CD-RAG-PARSE`).

**Approach:** [RAG-Anything](https://github.com/HKUDS/RAG-Anything) (MinerU parse, context-aware figures/tables/equations, multimodal `belongs_to` anchors) writing into an Arc-typed graph. Parser fallback: Docling or PaddleOCR. Circuit **simulation** photos do not use this path.

```mermaid
flowchart TB
  Drop["BYO PDF or scan\nlibrary / book / chapter tags"]
  Gate["Ask gate\npersistent index"]
  Parse["RAG-Anything parser\nMinerU default"]
  Split["Content list\ntext / image / table / equation + page"]
  Tree["Filesystem tree\nlibrary → book → chapter → section → passage"]
  Modal["Modal processors\ncaption + entity summary + crop"]
  Prop["Joint proposition + entity extract"]
  Graph["EE graph write"]
  Idx["BM25 + dense on propositions"]

  Drop --> Gate --> Parse --> Split
  Split --> Tree
  Split --> Modal
  Tree --> Prop
  Modal --> Prop
  Prop --> Graph --> Idx
```

Student-facing drop folder: [`rag-byo.md`](../rag-byo.md).

---

## Query graph (online, p95 ≤ 7 s)

`retrieve-citation` / MCP `retrieve`. Filters first. Empty retrieval is visible. Target wall clock **≤ 6 s**, hard cap **7 s**. Skip rerank if the clock already passed 4 s. If hops would overrun, return hybrid passages and mark the retrieve truncated.

**Approach:** hybrid BM25 + dense on **propositions**, then **deterministic hops** (GRASP-RAG index shape, not GRASP agent loops). Passages are what you cite.

```mermaid
flowchart TB
  Q["Query + tag filters"]
  F["Filter cone\nbook / chapter / folder / domain"]
  H["Hybrid retrieve on propositions\nBM25 + dense"]
  Hop1["Hop 1\nentities, example siblings, linked figures"]
  Hop2["Hop 2 only if multi_hop lane"]
  Vote["RankVote propositions → passages"]
  Pack["Pack 3 × 1500 chars\nbook + chapter + page + figure ids"]

  Q --> F --> H --> Hop1
  Hop1 --> Hop2 --> Vote --> Pack
  Hop1 --> Vote
```

Host-path multi-hop in [`ARCHITECTURE.md`](../ARCHITECTURE.md) §4 stays a **hop cap** on `retrieve-passage`, not a second agent loop in Python.

---

## Graph of node types

Three GRASP layers, plus assets and a worked-example bundle so problem, solution, and figures stay linked.

```mermaid
flowchart TB
  subgraph entityLayer ["Entity layer"]
    Concept[Concept]
    Symbol[Symbol]
    Device[Device]
    Law[Law]
  end
  subgraph propLayer ["Proposition layer"]
    Prop[Proposition]
  end
  subgraph passLayer ["Passage layer"]
    Passage[Passage]
  end
  subgraph assets ["Assets"]
    Figure[FigureAsset]
    Table[TableAsset]
    Eq[EquationAsset]
  end
  subgraph bundle ["Academic bundle"]
    Ex[WorkedExample]
  end
  Concept -->|mentions| Prop
  Symbol -->|mentions| Prop
  Prop -->|extracted_from| Passage
  Passage -->|part_of| Ex
  Figure -->|part_of| Ex
  Passage -->|follows| Passage
  Prop -->|illustrated_by| Figure
  Figure -->|depicts| Concept
  Law -->|mentions| Prop
```

Intra-image labels use RAG-Anything `belongs_to` into the `FigureAsset` anchor. Optional `prerequisite` edges between concepts stay a P1 overlay.

---

## Approach links

| What | Link |
|------|------|
| Product freeze (filters, citations, untrusted ingest) | [`ARCHITECTURE.md`](../ARCHITECTURE.md) §10 |
| Research: ingest vs query, latency budget, ontology | [`research/notes/rag-ingest-query-architecture.md`](../../research/notes/rag-ingest-query-architecture.md) |
| Research: 120-item pack eval bank | [`research/notes/rag-eval-pack-stack.md`](../../research/notes/rag-eval-pack-stack.md) |
| Research: RAG-Anything as ingest engine | [`research/notes/rag-anything-evaluation.md`](../../research/notes/rag-anything-evaluation.md) |
| Stack memo (D11 / D21) | [`research/synthesis/rag-stack-recommendation.md`](../../research/synthesis/rag-stack-recommendation.md) |
| Spike ADR | [`DECISIONS.md`](../../DECISIONS.md) ADR-0004 |
| RAG-Anything (ingest, images, dual graph) | https://github.com/HKUDS/RAG-Anything — paper https://arxiv.org/abs/2510.12323 |
| GRASP-RAG (entities, propositions, passages) | https://arxiv.org/abs/2605.16598 |
| Dense X Retrieval (proposition unit) | https://aclanthology.org/2024.emnlp-main.845/ |
| Hybrid + rerank (production pattern) | https://docs.databricks.com/aws/en/ai-search/retrieval-quality |
| Contextual prefixes at index time | https://www.anthropic.com/engineering/contextual-retrieval |

Do not confuse **GRASP-RAG** (this retrieval graph) with kernel **GraSP** (pack-skill loading in [`ARCHITECTURE.md`](../ARCHITECTURE.md) §6).

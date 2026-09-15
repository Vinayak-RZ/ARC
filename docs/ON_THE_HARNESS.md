# What Arc puts on the coding assistant

Cursor, Claude Code, Codex, and ChatGPT desktop already chat, call tools, and manage context. Arc does not rebuild that. Arc is the undergraduate electrical-engineering lab those assistants load: course method, simulators, safety gates, saved runs, and a local window you can look at.

If Arc did not actually check a number, it labels that number **unverified**. It never presents a guess as a lab result. In the saved run files that label is the word `unchecked`, so a fluent paragraph cannot hide it.

> Arc is the electrical-engineering expertise a general coding assistant loads. It is not a second Cursor, and it is not a public website API.
> You talk to Cursor (or the other assistants), or you type `electrical-engineer` yourself.
> Rule: an unverified number is labeled. It is never called a simulation.

A **domain kernel** is a short name for that idea: the expertise a general coding assistant loads so it can do one subject well. Arc is that kernel for undergraduate electrical engineering.

File maps: [`EXTENSIVE.md`](EXTENSIVE.md). Engineer contract: [`ARCHITECTURE.md`](ARCHITECTURE.md).

## Contents

- [Words this page uses](#words-this-page-uses)
- [The split in one picture](#the-split-in-one-picture)
- [Determinism, accuracy, reliability](#determinism-accuracy-reliability)
- [Named workflows, and when none fits](#named-workflows-and-when-none-fits)
- [Why a generic command line, API, or MCP is not the product](#why-a-generic-command-line-api-or-mcp-is-not-the-product)
- [What Arc already does](#what-arc-already-does)
- [Books and RAG — kernel, not the chat loop](#books-and-rag--kernel-not-the-chat-loop)
- [When a number was not verified](#when-a-number-was-not-verified)
- [How homework actually runs](#how-homework-actually-runs)
- [How Arc mediates MATLAB](#how-arc-mediates-matlab)
- [What ships in this checkout](#what-ships-in-this-checkout)
- [What we do not ship](#what-we-do-not-ship)
- [Where to go next](#where-to-go-next)

## Words this page uses

| Phrase | Meaning |
|--------|---------|
| Coding assistant | Cursor, Claude Code, Codex, or ChatGPT desktop. The chat loop you already use. |
| Tool | Something that assistant can call. People also say MCP tool. This page does not say "verb". |
| Simulator | A program that computes a number: SPICE for circuits, python-control for Bode plots, pandapower for load flow, algebra when that is enough. |
| Gate | A local rule that says auto, ask you, or refuse. The chat never hangs waiting. If you must confirm a photo, you get a link to the local window. |
| Unverified | Arc did not check this number. Saved as the word `unchecked`. |
| Deterministic | Same inputs, same number. The recipe runner and the simulators do not sample. |
| Named lab recipe | A saved sequence of steps (a workflow) checked into `workflows/`. Example: load netlist, simulate, label, write summary. |
| Compose | Build a one-off sequence from *allowed* kinds of check only. Arc validates the graph, then runs it. |
| Saved run | A folder under `./runs/` with the evidence, the observation log, and (when the assistant is driving) the explanation. |

## The split in one picture

The coding assistant keeps the chat loop, the context window, and its own permission prompts. Arc owns almost everything else a lab needs: method, tools, simulators, gates, books you add, local notes, an observation log, known-answer tests, and a window on this machine.

```mermaid
flowchart TB
  You[You]
  subgraph host["Coding assistant keeps"]
    Loop[Chat loop]
    Ctx[Context window]
    Loop --- Ctx
  end
  subgraph arc["Arc already ships, on this machine"]
    Method[Course method]
    Tools[Tools the assistant can call]
    Recipes[27 named lab recipes]
    Runner[Deterministic recipe runner]
    Sims[Simulators]
    Gates[Gates: auto, ask, or refuse]
    Books[Retrieve from your books]
    Notes[Local notes]
    Observe[Observation log]
    Tests[Known-answer tests]
    Folder[Saved run folder]
    Window[Local window on 127.0.0.1]
  end
  subgraph matlab["Shipped: Arc mediates MATLAB"]
    Other[Arc calls MATLAB MCP when installed]
  end
  You --> Loop
  You --> Window
  Loop --> Tools
  Tools --> Recipes
  Recipes --> Gates
  Tools --> Gates
  Gates --> Runner
  Runner --> Sims
  Sims --> Observe
  Observe --> Folder
  Folder --> Window
  Tools --> Books
  Tools --> Notes
  Tools --> Tests
  Method --> Loop
  Other -.-> Tools
```

The assistant talks. Arc checks. You can open both the numbers and the explanation in the local window.

## Determinism, accuracy, reliability

A chat model samples text. Ask it for `Vout` twice and you can get two fluent answers. That is fine for a draft email. It is a bad fit for core engineering.

In a lot of domains, especially engineering, the same inputs must produce the same number, the number must be accurate, and you must be able to trust the run after it happened. A wrong value is not a typo. On a homework sheet it fails a viva. Later it is a wrong design. That gap (a loop that talks vs a calculator that repeats) is a common reason people will not hand real engineering work to an unconstrained assistant.

Arc does not make the assistant's prose deterministic. The viva can still vary. It puts a **deterministic, accurate, replayable check** under the chat, which the chat does not have on its own:

| Need | What the chat loop does | What Arc does |
|------|-------------------------|---------------|
| Determinism | Samples a next token | The recipe runner has no model inside it. Same YAML plus same netlist, same path |
| Accuracy | Sounds confident | ngspice, python-control, pandapower, or algebra compute the number. Gold `divider-dc-01` expects `Vout = 5.0` |
| Reliability | A wrong ohm can vanish into the transcript | Gates, an observation log, a saved run you can reopen, and an unverified label when the check did not run |

```mermaid
flowchart LR
  subgraph alone["Assistant alone"]
    Q1[Same homework] --> M[Chat model]
    M --> N1[Fluent Vout, maybe different next time]
  end
  subgraph witharc["Assistant plus Arc"]
    Q2[Same homework] --> A[Assistant]
    A --> R[Deterministic runner]
    R --> S[Simulator]
    S --> O[Same Vout, or labeled unverified]
  end
  alone ~~~ witharc
```

Limit: Arc is an undergraduate lab, not a plant controller. It does not make every numeral tool-checked. It does make this promise: a number presented as verified came from a simulator or a numeric check, and you can open the run that produced it.

## Named workflows, and when none fits

A general assistant in a loop invents the next step as it goes. That is a poor fit when the next step is "run SPICE, then label anything that did not compute." The model can skip the simulator, reorder the work, or call a tool that does not exist.

A **named lab recipe** is a saved path the runner will not improvise. This checkout has **27** of them across **10** packs (circuits, control, signals, machines, power, and the rest). `simulate-circuit` is four steps: load the netlist, simulate, label unverified leftovers, write the summary. Ask twice, get the same path.

The combination is the product: the assistant **selects** a recipe (or proposes an allowed graph). Arc **runs** it. The assistant does not learn Kirchhoff by trial and error inside the loop.

```mermaid
flowchart LR
  subgraph free["General agent loop"]
    H1[Homework] --> M[Model picks the next tool]
    M --> G[Fluent answer, steps may change]
  end
  subgraph combo["Arc combination"]
    H2[Homework] --> Pick[Assistant picks a saved recipe]
    H2 --> Comp[Or proposes allowed checks]
    Pick --> Run[Deterministic runner]
    Comp --> Val[Validator: allowlist, size, no cycles]
    Val --> Run
    Run --> Out[Same path, or labeled unverified]
  end
  free ~~~ combo
```

**How the assistant selects.** It lists the recipes, matches the homework, and runs a short saved one (`simulate-circuit`, `derive-circuit`, review this solution, explain this idea). If you type `electrical-engineer run` with no name, Arc classifies the `problem.json` text, asks when two recipes are close, or uses `unmatched-cosolver` (answer, and label anything not checked). It never invents a new recipe id.

**When no saved recipe fits: compose.** The assistant names a graph of *already allowed* kinds of check (simulate this circuit, then check this algebra). Arc validates first: known ids only, at most 16 steps and 24 edges, no cycles, photos still need the local window. Record the plan without physics, or apply and run. On the command line the same job is `compose-from-parts` (asks you first). Invalid graphs fail before a simulator starts.

A generic command line runs one flag. A generic MCP dumps tools into the chat. Neither ships 27 named lab recipes plus a validator that will only run allowed checks.

Limit: the catalog is not the whole subject. A signals question with no YAML row is still in-bound: compose allowed checks, or unmatched plus an unverified label. Long `solve-*` recipes that include an essay step are the command-line / test path, not the assistant's chat brain. Full list: [`WORKFLOWS.md`](WORKFLOWS.md).

## Why a generic command line, API, or MCP is not the product

People map Arc onto the nearest object: "it is a command line", "it is an MCP server", "it is an API for circuits". Those objects exist here. None of them is the product.

| Shape | What you get | What you still miss |
|-------|----------------|---------------------|
| Generic command line | You type a flag, you get text back | Course method, gates, a window that shows the run |
| Generic website API | You POST JSON | Arc does not ship this. The HTTP server here is a local window on `127.0.0.1` only |
| Generic MCP | Extra tools on the assistant | The assistant often calls SPICE or MATLAB directly. The number appears in chat. MATLAB's own MCP also dumps a huge tool list into context |
| Arc | Command line + local MCP + local window, sharing one lab | A second Cursor. Missing simulators still produce an unverified label, not a fake lab result |

```mermaid
flowchart LR
  subgraph generic["Generic MCP"]
    G1["run_spice"]
    G2["run_matlab"]
    G1 --> Chat["Number appears in chat"]
    G2 --> Chat
  end
  subgraph arcway["Arc"]
    A1["Run a short simulation"]
    A2["Propose allowed checks"]
    A1 --> Val["Gates and allowlist"]
    A2 --> Val
    Val --> Sim["Simulator or algebra"]
    Sim --> Out["Saved evidence: number or unverified"]
  end
  generic ~~~ arcway
```

The assistant does not get a new `run_ngspice` tool for every engine. It asks Arc for a *kind of check* (simulate this circuit, check this algebra). Arc picks an installed simulator or labels the number unverified.

There is no public website API. `electrical-engineer ui` binds `127.0.0.1:8765` only.

## What Arc already does

A coding harness is usually: chat loop, tools, files, hooks, memory, evals, a UI, and safety. Arc does not rebuild the chat loop or the assistant's own permission UI. It does ship the rest for this lab.

### Course method

Pack files under [`skills/`](../skills/SKILL.md) teach how to solve circuits, machines, power, and the other undergraduate packs. The assistant loads the root file plus at most two packs for the assignment. It does not load every pack at once.

Limit: those files teach method. They do not mint ohms.

### Tools the assistant can call

Your coding assistant talks to Arc through a local MCP connection (`electrical-engineer mcp`). The tools, in plain language:

| The assistant can | What that means |
|-------------------|-----------------|
| List lab recipes | See the named workflows in this checkout |
| Look up a citation | Retrieve from books you have rights to. Empty is visible |
| Open the local window | Get a link. The chat never waits on you |
| Run a short simulation | Known small jobs such as simulate this circuit |
| Propose a combination of allowed checks | Record a plan, then run it if you said so |
| Read the labeled result | What was verified vs unverified |
| Replay a named recipe | The command-line / test path |

You can do the same jobs without an assistant: `electrical-engineer run`, `workflows`, `eval`, `ui`, `rag`, `memory`, `hosts install`.

Limit: Arc does not wrap each simulator as its own MCP tool. Confirming a photo happens in the local window, not inside the chat.

### Simulators

When they are installed, Arc can run ngspice (circuits), python-control (Bode, step, root locus), pandapower (study-level load flow), and algebra / last-line checks. MATLAB is optional. The product works with none of it: then the number is labeled unverified.

Limit: a missing simulator is not a fake SPICE pass.

### Gates

Local rules say auto, ask you, or refuse. The strictest rule wins. The chat never hangs. If you must confirm a circuit photo, Arc returns a link to the local window. Three asks in one run abort.

Limit: turning off asks does not turn off the unverified label.

### Saved runs, observations, notes, books, tests

Each run writes:

- evidence: numbers, plots, citations, unverified labels
- `observation.json`: what ran, what failed, why something was unverified
- explanation (`argument.md`) when the assistant is driving the viva
- a plan (`plan.md`) on a large assignment, written before tools that change physics

You can add licence-clean notes and books on the machine (`electrical-engineer memory`, `electrical-engineer rag add`). Known-answer tests live under `eval/gold/` (`electrical-engineer eval --pack circuits`). Diagrams of ingest vs retrieve: [`architecture/rag.md`](architecture/rag.md).

Limit: a dead run does not resume. Notes cannot flip unverified to verified. The browser is not a second chat loop.

## Books and RAG — kernel, not the chat loop

The coding assistant does not hold your textbooks in its context window. It **calls** Arc. Arc **stores** the index and **returns** three short cited passages (`engine=hybrid-graph`).

| Who | Does | Does not |
|-----|------|----------|
| Harness (the assistant) | Ask for a citation; put book/chapter filters in the plan; use the passages in the viva | OCR a PDF, own the graph, invent a page number |
| Kernel (Arc) | `rag add` ingest, optional OCR/figures, hybrid search, 1–2 hops, pack citations | Compact the chat, run a multi-agent GRASP planner, treat a PDF as a new capability |

```mermaid
flowchart LR
  subgraph harness ["Harness — assistant"]
    Ask["Look up a citation"]
  end
  subgraph kernel ["Kernel — Arc"]
    Ingest["rag add"]
    Query["rag query / MCP retrieve"]
    Cite["book + chapter + page"]
  end
  Ask --> Query
  Ingest --> Query
  Query --> Cite
```

### Ingest pipeline (offline, kernel-owned)

```mermaid
flowchart TB
  Drop["BYO text, PDF, or scan"]
  Gate["Ask gate"]
  Parse["Parse text / PDF / optional OCR"]
  Chunk["Chunk with page tags"]
  Graph["Write graph.json T0-T4"]
  Idx["BM25 + dense indexes"]
  Drop --> Gate --> Parse --> Chunk --> Graph --> Idx
```

### Query pipeline (online, p95 ≤ 7 s)

```mermaid
flowchart TB
  Q["Query + book/chapter filters"]
  F["Apply filters first"]
  H["BM25 parallel dense"]
  RRF["RRF fuse"]
  Hyd["Parent hydrate worked example / figure"]
  Hop["Typed hops k at most 2"]
  Pack["Pack 3 x 1500 chars; empty visible"]
  Q --> F --> H --> RRF --> Hyd --> Hop --> Pack
```

**Why this shape:** filter-first hybrid lexical+dense plus a small typed graph is a proven production RAG pattern for textbooks; it keeps interactive lookup under about seven seconds without GraphRAG map-reduce or agent rewrite loops in the runner. Full approach notes and ontology: [`architecture/rag.md`](architecture/rag.md). Student add-book steps: [`rag-byo.md`](rag-byo.md).

Limit: commercial-scan **layout** fidelity is still `CD-RAG-PARSE` (MinerU/RAG-Anything stay optional adapters). Empty lookup stays visible. Homework circuit **photos** for simulation still go through the photo confirm path, not this book index.

## When a number was not verified

A checked number comes from a simulator or a numeric check Arc ran. If that did not happen, Arc still answers the assignment as far as method goes, and it **labels the number unverified**.

In the run folder that label is the word `unchecked`. Gold test `eval/gold/circuits/divider-dc-01` expects divider `Vout = 5.0` from `Vin=10`, `R1=R2=1k` when the check actually ran. That eval is the product check.

A paragraph that sounds confident is not a check. A MATLAB Copilot scalar is not a check until Arc recomputes it.

## How homework actually runs

Same lab, two doors.

```mermaid
sequenceDiagram
  actor You
  participant Assistant as Coding assistant
  participant Arc as Arc
  participant UI as Local window
  You->>Assistant: circuit, viva, or assignment in plain language
  Assistant->>Assistant: load course method for at most two packs
  opt large assignment
    Assistant->>Arc: write the plan first
  end
  Assistant->>Arc: look up, simulate, or propose checks
  Arc->>Arc: gates, then simulator
  Arc-->>Assistant: saved run, never wait
  Assistant->>UI: you confirm a photo if needed
  Assistant->>Arc: write the explanation
  Arc-->>You: a checked number, or labeled unverified
```

**With a coding assistant.** It plans, calls the tools above, writes the explanation, and may start at most two pack helpers using that assistant's own Task UI. Helpers share the same Arc tools and the same run folder. Arc never starts those helpers itself.

```mermaid
flowchart LR
  Main["Main assistant"]
  S1["Pack helper 1"]
  S2["Pack helper 2"]
  Arc["Same Arc tools"]
  Run["Saved run folder"]
  Main -->|"at most two"| S1
  Main -->|"at most two"| S2
  Main --> Arc
  S1 --> Arc
  S2 --> Arc
  Arc --> Run
  Main -->|"explanation"| Run
```

**Without a coding assistant.** `electrical-engineer run` plus the local window is enough for numbers. A viva still needs an assistant or a local model you configure. ChatGPT in the browser is not a supported assistant.

## How Arc mediates MATLAB

Do **not** turn on MathWorks' MATLAB MCP next to Arc. That side-by-side setup dumps on the order of 10,000 tokens of tool description into the assistant's context window. The chat gets slower and noisier, and it is still allowed to treat a MATLAB scalar as if it were a lab result unless Arc stops it.

**Shipped path:** Arc calls MATLAB MCP itself when `matlab-mcp-server` is on the machine (`run-matlab-if-present`). The coding assistant talks only to Arc. Arc decides when MATLAB is needed, runs that call, and returns a short labeled result: verified, or unverified, with the observation log. The 10k-token tool dump never lands in your homework chat.

If a student attaches MATLAB MCP anyway, those peer scalars stay unverified until Arc recomputes them (FR20 clamp). That is not the install.

```mermaid
flowchart TB
  subgraph wrong["Do not: peer MATLAB MCP"]
    H1[Coding assistant]
    M1[MATLAB MCP]
    A1[Arc]
    H1 --> M1
    H1 --> A1
    M1 -->|"huge tool list into context"| H1
  end
  subgraph shipped["Shipped"]
    H2[Coding assistant]
    A2[Arc]
    M2[MATLAB MCP]
    H2 -->|"one lab connection"| A2
    A2 -->|"Arc calls them"| M2
    M2 -->|"short result"| A2
    A2 -->|"labeled number"| H2
  end
```

The product and CI already work with zero MATLAB. OSS simulators stay first-class. Simulink Agentic Toolkit is kernel-mediated the same way: set `EE_SIMULINK_TOOLS_JSON` to the toolkit `tools.json`. Do **not** attach the toolkit to the coding assistant. Missing toolkit stays unverified (`CD-SIMULINK-PLANT`). On a licensed desktop, run `satk_initialize` once per MATLAB session. Live `.slx` gold is later; this checkout’s CI has no Simulink.

## What ships in this checkout

Counts you can reproduce from the files.

| What | Count | In plain language |
|------|-------|-------------------|
| Undergraduate packs | 10 | Circuits, signals, electronics, machines, power, control, power electronics, measurements, electromagnetic fields, maths-for-EE |
| Spawnable EE specialists | 12 | Host Task/subagent cards in `hosts/agents/` (11 packs + `ee-simulink`). Install into homework; never this product `.cursor/` |
| Named lab recipes | 27 | Saved workflows under `workflows/` |
| Kinds of check | 14 | Algebra, lumped-circuit sim, LTI, power network, machines, converters, signals, fields, measurements, citations, figures, photo ingest, unverified label, ask you |
| Tools the assistant can call | 7 | List, look up, open window, simulate, propose checks, read result, replay recipe |
| Commands you can type | 8 | `run`, `workflows`, `mcp`, `eval`, `ui`, `rag`, `memory`, `hosts` |
| Supported assistants | 4 | Cursor, Claude Code, Codex, ChatGPT desktop |

Every pack covers seven homework shapes: solve, derive, design, simulate, review, explain, report. Known-answer tests are still deepest on circuits. Other packs may finish with an unverified label. That is a legal outcome.

Commercial textbooks are not in git. You add files you have rights to.

## What we do not ship

- A second Cursor (our own chat loop, specialist orchestrator, or token bill)
- A public website MCP or a UI bound to the internet
- New kinds of check invented in a chat session
- Faculty LMS, postgraduate as a public promise, civil or mechanical packs
- Live plant control, chip tape-out, a full schematic editor
- ChatGPT in the browser, Claude Desktop, GitHub Copilot, Gemini CLI as v1 assistants

Honest holes stay in [`CANNOT_DO.md`](CANNOT_DO.md). Prefer a row there over a fluent fake number.

## Where to go next

| If you want | Open |
|-------------|------|
| Paste a prompt and run | [README](../README.md) |
| Hook up Cursor or another assistant | [`hosts/README.md`](hosts/README.md) |
| Named lab recipes | [`WORKFLOWS.md`](WORKFLOWS.md) |
| Engineer tables | [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| RAG ingest and query graphs | [`architecture/rag.md`](architecture/rag.md) |
| Every package and file | [`EXTENSIVE.md`](EXTENSIVE.md) |
| Identity and non-goals | [`PID.md`](PID.md), [`PRODUCT.md`](PRODUCT.md) |

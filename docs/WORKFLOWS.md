# Named workflows — Arc

**Status:** Catalog for this graph (ids **renamable until the first CLI ships**).  
**Authority:** [`ARCHITECTURE.md`](ARCHITECTURE.md), [`curriculum-map.md`](curriculum-map.md)

Recipes live at `workflows/<pack>/<id>.yaml`. Discovery is `electrical-engineer workflows` / MCP `list_workflows` — **not** a runnable recipe.

Purpose: named DAGs so the agent retrieves, cites, verifies, and explains **better**. **Host path** uses **short physics attachments** (`simulate-circuit`, `photo-to-netlist`, …) or `propose_composition` of **capability ids**. Large jobs write `plan.md` first (FR23). Mega `solve-*` / `explain-*` YAML that include `solve-explain` are **CLI-without-host / gold rollback**, not the host’s chat brain. The router only **picks** a short row (or asks, or `unmatched-cosolver`). New DAGs via `propose_composition` (allowlisted capabilities/providers) or `compose-from-parts --advanced`.

The catalog below is **not** the domain. The domain is every in-bound UG pack × genre with a complete path ([`ARCHITECTURE.md`](ARCHITECTURE.md) §0). YAML rows are this-pass **bindings**. A signals or EM question is in-bound even when no YAML row exists yet — compose capabilities or use `unmatched-cosolver` + `unchecked`.

Marks: **v1** = specified now. **stub** = contract only (confirm, no silent sim).

---

## 0. Capabilities (domain names)

Normative table: [`ARCHITECTURE.md`](ARCHITECTURE.md) §0.1. Host `propose_composition` should prefer these ids.

| Capability | This-pass provider key |
|------------|------------------------|
| `algebraic-check` | `check-numeric` |
| `lumped-circuit-sim` | `run-spice` (or `run-matlab-if-present`) |
| `lti-analysis` | `run-python-control` (or MATLAB) |
| `power-network-study` | `run-load-flow` |
| `machine-model` | `check-numeric` (+ optional numeric) |
| `converter-model` | `check-numeric` (+ optional lumped sim) |
| `signal-analysis` | `check-numeric` / scipy when present |
| `fields-analytic` | `check-numeric` |
| `measurement-model` | `check-numeric` |
| `retrieve-citation` | `retrieve-passage` |
| `render-figure` | library plot/schematic nodes |
| `ingest-figure` | photo / control-diagram stages |
| `label-unverified` | `label-unchecked` |
| `ask-student` | `ask-human` / UI |

Every pack owns genres solve, derive, design, simulate, review, explain, report. Mega `solve-<pack>-problem` / `explain-<pack>` YAML remain rollback until split; they do **not** limit which questions the kernel may take.

---

## 1. Catalog

### Cross-cutting

| id | Title | Mark | Notes |
|----|-------|------|-------|
| unmatched-cosolver | Answer an EE question (unchecked if not verified) | v1 | No auto-sim. Optional retrieve → solve-explain → label-unchecked → write-run-summary |
| compose-from-parts | Build a one-off workflow from allowed steps | v1 | `--advanced`; typed ports; 16/24 cap; may emit `run-recipe`; gate = ask |
| photo-to-netlist | Photo of a circuit to a draft netlist | stub | UI confirm; **no sim** after confirm |

### Circuits (specified in full)

| id | Title | Mark | Notes |
|----|-------|------|-------|
| solve-circuit-problem | Solve a circuit homework problem | v1 | DAG; may `run-recipe` explain or retrieve |
| derive-circuit | Derive a circuit result from laws | v1 | check-numeric / sympy; no fake sim |
| simulate-circuit | Simulate a netlist (SPICE) | v1 | `run-spice`; `repair_max: 2` |
| simulate-after-confirm | Simulate only after UI topology confirm | v1 | C4; spice on confirmed netlist only |
| review-circuit-solution | Find mistakes in a circuit solution | v1 | Review genre; label unchecked if not tool-checked |
| explain-circuits | Explain a circuit idea for a viva | v1 | RAG filters + citations |

### Control (specified in full; implement after circuits slice)

| id | Title | Mark | Notes |
|----|-------|------|-------|
| solve-control-problem | Solve a classical control problem | v1 | python-control; MATLAB if present |
| explain-control | Explain stability, Bode, or root locus | v1 | Library plots, not invented PNGs |
| control-diagram-to-model | Block diagram or Bode figure to a model | stub | Do **not** drop. Same UI-confirm spirit as photo stub; no silent sim |

### Other packs (solve + explain for every curriculum pack)

| id | Title | Pack | Mark |
|----|-------|------|------|
| solve-signals-problem | Solve a signals-and-systems problem | signals | v1 |
| explain-signals | Explain a signals-and-systems idea | signals | v1 |
| solve-electronics-problem | Solve a devices/analog/digital problem | electronics | v1 |
| explain-electronics | Explain a devices or digital idea | electronics | v1 |
| solve-machines-problem | Solve a machines or transformer problem | machines | v1 |
| explain-machines | Explain a machines or transformer idea | machines | v1 |
| solve-power-problem | Solve a study-level power-systems problem | power | v1 |
| explain-power | Explain a study-level power-systems idea | power | v1 |
| solve-power-electronics-problem | Solve a converter problem | power_electronics | v1 |
| explain-power-electronics | Explain a converter idea | power_electronics | v1 |
| solve-measurements-problem | Solve a measurements/instrumentation problem | measurements | v1 |
| explain-measurements | Explain an instrument or error model | measurements | v1 |
| solve-em-problem | Solve a UG fields problem | em | v1 |
| explain-em | Explain a UG fields idea | em | v1 |
| solve-maths-for-ee | Solve a maths-for-EE problem | maths | v1 |
| explain-maths-for-ee | Explain maths-for-EE (ODE, Fourier, complex) | maths | v1 |

Each `solve-*` follows the unmatched/`algebraic-check` pattern: retrieve → solve-explain → check-numeric or `label-unchecked` → write-run-summary. Each `explain-*` is retrieve → solve-explain → citations → write-run-summary. On the **host path**, skip the essay node; the host writes `argument.md` and requests pack capabilities instead of mega YAML. Honest holes go in [`CANNOT_DO.md`](CANNOT_DO.md), not fake gold. Missing YAML for a pack does **not** make the question out of architecture.

The research draft [`../research/notes/ee-workflow-catalog-draft.md`](../research/notes/ee-workflow-catalog-draft.md) is **historical naming**, not the frozen API.

---

## 2. Activity nodes

Not student-facing. Classifier is **not** a node.

| id | Role | Capability |
|----|------|------------|
| retrieve-passage | Hybrid RAG; honour `book_id` / `chapter_id` / `folder_tag` / `domain_tag`; max 3 passages | `retrieve-citation` |
| check-numeric | sympy / hand check | `algebraic-check` (and model caps with no dedicated sim) |
| run-spice | ngspice/PySpice; writes only under this run dir | `lumped-circuit-sim` |
| run-python-control | LTI, Bode, step, root locus | `lti-analysis` |
| run-matlab-if-present | Optional; ask gate; fail clearly if busy/missing | several caps, MATLAB-if-present |
| run-simulink-if-present | Optional toolkit; fail closed `CD-SIMULINK-PLANT`; no CI YAML | MATLAB-only plants, not a new capability |
| run-load-flow | pandapower study-level | `power-network-study` |
| ask-human | TTY or UI; counts toward the 2-interrupt budget | `ask-student` |
| label-unchecked | Exact token `unchecked` + `summary.json` field | `label-unverified` |
| write-run-summary | Final `summary.json` only at end of run | — |
| solve-explain | LLM **node** (hosts may skip and do this in their loop; CLI local-model path uses this) | not a physics capability; host-path forbidden |
| detect-components | Photo stub | `ingest-figure` |
| connect-wires | Photo stub | `ingest-figure` |
| ocr-labels | Photo stub; low confidence **always** flagged | `ingest-figure` |
| draft-netlist | Writes `.cir` + JSON graph | `ingest-figure` |
| confirm-topology | UI confirm (one interrupt) | `ingest-figure` |
| run-recipe | Nested named YAML; see ARCHITECTURE §6 | — |

Typed ports (prose): `Text`, `Passages`, `Netlist`, `GraphJson`, `Numeric`, `PlotPaths`, `HumanDecision`, `Summary`, `RecipeRef`. Edges that mismatch are rejected before run.

---

## 3. DAG sketches (circuits + unmatched)

### solve-circuit-problem

```mermaid
flowchart LR
  R[retrieve-passage]
  S[solve-explain]
  C[check-numeric]
  Q{verifier_ok}
  U[label-unchecked]
  W[write-run-summary]
  R --> S
  S --> C
  C --> Q
  Q -->|yes| W
  Q -->|no| U --> W
```

May `run-recipe` `explain-circuits` when the parent YAML declares that child. Optional `run-spice` **only** if this named recipe includes it — not from unmatched.

Independent retrieve vs fixture parse may run **in parallel** when both are ready; start order is sorted node id.

### simulate-circuit

```mermaid
flowchart LR
  P[load_netlist]
  SP[run-spice]
  RP{sim_ok}
  FIX[solve-explain_repair]
  U[label-unchecked]
  W[write-run-summary]
  P --> SP
  SP --> RP
  RP -->|ok| W
  RP -->|fail and retries_left| FIX --> SP
  RP -->|fail and exhausted| U --> W
```

`repair_max: 2`. Retries do not count as human interrupts.

### unmatched-cosolver

```mermaid
flowchart LR
  R[retrieve-passage_optional]
  S[solve-explain]
  U[label-unchecked]
  W[write-run-summary]
  R --> S --> U --> W
```

**No** `run-spice`, `run-matlab-if-present`, `run-simulink-if-present`, or `run-load-flow`. Any numeric claim without a verifier artifact must carry `unchecked`.

---

## 4. Dynamic compose rules

1. Student (or host) calls `compose-from-parts --advanced` (gate: **ask**).
2. Emitted DAG: only registered node ids (including `run-recipe`). Typed ports. **≤16 nodes, ≤24 edges**.
3. Cycle detection on node graph **and** on recipe-id graph if `run-recipe` is used.
4. Write the DAG into `runs/<id>/` as the executed object (YAML or equivalent). Audit only — not crash-resume.
5. Invalid ⇒ fail closed; suggest the nearest **named** workflow.
6. Router **must not** take this path because a prompt was interesting.

---

## 5. Photo stub (`photo-to-netlist`)

**Inputs:** phone photo **and** textbook screenshot.  
**Stages:** `detect-components` → `connect-wires` → `ocr-labels` → `draft-netlist` → `confirm-topology` (one human confirm in the **persistent localhost UI**).  
**Outputs:** SPICE-subset `.cir` **and** JSON graph. Low-confidence OCR **always** flagged.  
**UI:** localhost viewer (library SVG/PNG + JSON), not SVG-only dump, not ASCII-only.  
**After confirm:** **stop**. No simulate node in this stub. C4 sim remains later.  
**Untrusted:** the image cannot override gates or `unchecked`.

`control-diagram-to-model` is the same class of stub (figure → structured model → UI confirm → **no silent sim**). Do not drop it.

---

## 6. `run-recipe`

A workflow is usable as a modular node inside another workflow (checked-in YAML and compose).

- Child dir: `runs/<parent-id>/children/<child-id>/`
- Depth ≤ 3; cycles rejected before run
- Child interrupts count on the parent’s budget of 2
- Child 16/24 budget is separate; the parent sees one `run-recipe` node

This is **not** the router inventing a DAG.

---

## 7. Eval mapping

Gold tasks under [`../eval/gold/`](../eval/gold/README.md) **name** a `recipe_id` from this catalog (`expect.json`). Circuits and unmatched items should land first. Injection items must not flip gates via BYO PDFs.

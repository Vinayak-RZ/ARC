# Per-pack retrieval eval stack

## Purpose

Define a **retrieval-only** eval bank covering every public UG pack, so ingest (OCR, figures, example bundles) and query (hybrid + hops, ≤ 7 s) can be measured before locking ADR-0004. Items are **query templates** with gold *roles* (section type, figure link, hop depth). Page numbers and book titles are **curator-bound** after a licensed or BYO chapter is ingested — no commercial book text lives here.

This extends [`rag-eval-methodology.md`](rag-eval-methodology.md) (failure taxonomy, twenty case *titles*) into a pack × lane matrix. It is not a product SLA and not a GATE exam.

## Findings

Claim | Evidence (URL or ledger ID) | Confidence
--- | --- | ---
Retrieval eval needs page/section gold and Recall@k, separate from EE-correctness of generated answers | rag-eval-methodology.md; RAG4Reports (S16) | high
Every pack × genre is in-bound; eval tags may use GATE overlay without making GATE the ceiling | curriculum-map.md; ARCHITECTURE.md §0 | high
EE retrieval fails in characteristic ways: formula variants, dropped assumptions, orphaned solutions, bad figure links, fake pages | rag-eval-methodology.md failure taxonomy | high
Figure and worked-example items must assert **graph links**, not only bag-of-chunks overlap | rag-ingest-query-architecture.md; RAG-Anything `belongs_to` (S44) | high

### Item schema

Each item is a YAML-shaped record (implement later as `eval/rag/*.yaml` if a code plan lands). Fields:

| Field | Meaning |
|-------|---------|
| `id` | `ret.<pack>.<lane>.<nn>` |
| `pack` | curriculum pack id |
| `lane` | `exact` `concept` `figure` `example` `equation` `table` `multi_hop` `adversarial` `filter` |
| `query` | student-like question (no copyrighted stem) |
| `expect_node_types` | ontology types that must appear in the hit set |
| `hop_depth` | 0, 1, or 2 |
| `needs_figure` | true if a `FigureAsset` must be retrieved or linked |
| `needs_bundle` | true if problem and solution passages must co-occur |
| `must_not` | confusion class (peak vs RMS, line vs phase, …) |
| `bind` | curator fills `book_id`, `chapter_id`, `page`, `figure_id` after ingest |
| `metrics` | always Recall@3 / Recall@5 on bound pages; plus lane-specific checks below |

**Scoring (retrieval layer only).** Do not LLM-judge EE truth here. That is capability eval (`capability-eval-design.md`).

| Check | Pass |
|-------|------|
| Page recall | Gold page in top 3 (primary) / top 5 (secondary) |
| Citation | Returned page equals bound page (no fabricated page) |
| Bundle | If `needs_bundle`, both problem and solution passage ids present |
| Figure link | If `needs_figure`, `FigureAsset` shares `illustrated_by` or `part_of` with a hit passage |
| Filter | `filter` lane: hits only from the tagged chapter |
| Adversarial | `must_not` page/section not in top 3 |
| Latency | Wall time for retrieve ≤ 7 s (log p50/p95 per pack) |
| Empty | Intentionally unanswerable query returns empty, not a confident wrong chapter |

**Corpus for a run.** OER (e.g. Kuphaldt ModEL, S29) plus the student’s BYO chapter. Gold `bind` is per corpus; the **query text** stays stable.

**Size.** 12 items × 10 packs = **120 retrieval items**. That is the v1 bank. Add more only when a lane’s CI is noisy.

---

### Shared lane recipe (every pack)

Use this mix so packs are comparable:

| # | Lane | What it probes |
|---|------|----------------|
| 01 | `exact` | Symbol / acronym lexical hit |
| 02 | `exact` | Numbered problem or example id |
| 03 | `concept` | Definition / “explain X” |
| 04 | `figure` | Caption or “what does the diagram show” |
| 05 | `figure` | Image–text link (retrieve figure given a law, or prose given a figure ask) |
| 06 | `example` | Worked example bundle (problem + solution) |
| 07 | `equation` | Identity / transfer function / LaTeX-ish query |
| 08 | `table` | Numeric table or datasheet-like block |
| 09 | `multi_hop` | Prerequisite in an earlier section of the same book |
| 10 | `concept` | Assumption-sensitive (must keep the caveat) |
| 11 | `adversarial` | Common variant confusion |
| 12 | `filter` | Same wording as 03 but **wrong chapter tag** must not leak |

---

## Pack banks

Queries are original. Bind them to whatever licensed/OER/BYO book the spike uses.

### circuits

| id | lane | query | expect | hop | figure | bundle | must_not |
|----|------|-------|--------|-----|--------|--------|----------|
| ret.circuits.exact.01 | exact | Find the section that defines `R_th` for a Thevenin equivalent. | Symbol, Passage | 0 | no | no | Norton `R_n` only page |
| ret.circuits.exact.02 | exact | Worked example labelled 3.12 (or the bound example id) on dependent-source Thevenin. | WorkedExample | 1 | no | yes | unrelated mesh example |
| ret.circuits.concept.03 | concept | Explain source transformation and when it is valid. | Concept, Proposition | 0 | no | no | — |
| ret.circuits.figure.04 | figure | Which figure shows the Thevenin equivalent looking into terminals a-b? | FigureAsset | 0 | yes | no | Norton drawing |
| ret.circuits.figure.05 | figure | From the dependent-source circuit diagram, retrieve the matching solution prose. | FigureAsset, Passage | 1 | yes | yes | — |
| ret.circuits.example.06 | example | Solution steps for finding `V_th` with a dependent source. | WorkedExample | 1 | no | yes | problem without solution |
| ret.circuits.equation.07 | equation | Natural response of a series RLC: form of `v_C(t)` in the overdamped case. | EquationAsset | 0 | no | no | underdamped form |
| ret.circuits.table.08 | table | Table of initial conditions `v_C(0)`, `i_L(0)` for the transient example. | TableAsset | 0 | no | no | — |
| ret.circuits.multi_hop.09 | multi_hop | Use KCL at a supernode to justify the mesh setup in the later example. | Law, Passage | 2 | no | no | — |
| ret.circuits.concept.10 | concept | Passive sign convention when writing element voltages for KVL. | Proposition with `assumes` | 1 | no | no | active-sign page |
| ret.circuits.adversarial.11 | adversarial | Peak versus RMS value of a sinusoidal source in phasor analysis. | Passage | 0 | no | no | peak formula page as if RMS |
| ret.circuits.filter.12 | filter | Same as 03 with `chapter_id` set to a magnetics chapter. | empty or off-pack | 0 | no | no | circuits explanation |

### signals

| id | lane | query | expect | hop | figure | bundle | must_not |
|----|------|-------|--------|-----|--------|--------|----------|
| ret.signals.exact.01 | exact | Section defining the Dirichlet conditions for Fourier series. | Concept | 0 | no | no | DTFT page |
| ret.signals.exact.02 | exact | Example on sampling a sinusoid at a given `f_s`. | WorkedExample | 1 | no | yes | continuous-time only example |
| ret.signals.concept.03 | concept | Explain aliasing in uniform sampling. | Concept | 0 | no | no | — |
| ret.signals.figure.04 | figure | Figure of a two-sided line spectrum for a periodic pulse train. | FigureAsset | 0 | yes | no | one-sided magnitude plot only |
| ret.signals.figure.05 | figure | Retrieve the sampling-theorem statement that the spectrum figure is illustrating. | Passage, FigureAsset | 1 | yes | no | — |
| ret.signals.example.06 | example | Worked convolution of a rectangular pulse with itself. | WorkedExample | 1 | no | yes | — |
| ret.signals.equation.07 | equation | Laplace transform of `e^{-at}u(t)` and ROC. | EquationAsset | 0 | no | no | Fourier-only pair |
| ret.signals.table.08 | table | Common Fourier transform pairs table: rect and sinc. | TableAsset | 0 | no | no | Laplace pair table |
| ret.signals.multi_hop.09 | multi_hop | Use LTI convolution properties to justify the Fourier transform of a delayed pulse. | Proposition | 2 | no | no | — |
| ret.signals.concept.10 | concept | Region of convergence must be stated with a unilateral Laplace pair. | Proposition | 0 | no | no | ROC omitted page |
| ret.signals.adversarial.11 | adversarial | Hz versus rad/s in the sampling theorem formula. | Passage | 0 | no | no | wrong unit form |
| ret.signals.filter.12 | filter | Alias query with a power-systems chapter filter. | empty | 0 | no | no | — |

### electronics

| id | lane | query | expect | hop | figure | bundle | must_not |
|----|------|-------|--------|-----|--------|--------|----------|
| ret.electronics.exact.01 | exact | Definition of `g_m` for a MOSFET in saturation. | Symbol | 0 | no | no | BJT `g_m` only |
| ret.electronics.exact.02 | exact | Numbered op-amp example on inverting amplifier finite gain. | WorkedExample | 1 | no | yes | ideal infinite-gain only |
| ret.electronics.concept.03 | concept | Explain Early effect and output resistance in a MOSFET. | Concept | 0 | no | no | — |
| ret.electronics.figure.04 | figure | Small-signal hybrid-π figure for a BJT. | FigureAsset | 0 | yes | no | MOSFET T-model figure |
| ret.electronics.figure.05 | figure | From the inverting-op-amp schematic, retrieve the closed-loop gain derivation. | FigureAsset, Passage | 1 | yes | yes | — |
| ret.electronics.example.06 | example | Worked bias-point calculation for a MOSFET CS amplifier. | WorkedExample | 1 | no | yes | — |
| ret.electronics.equation.07 | equation | Gain-bandwidth product constraint for a voltage-feedback op-amp. | EquationAsset | 0 | no | no | current-feedback amp |
| ret.electronics.table.08 | table | Device parameter table: `V_t`, `k_n`, `λ` for the example MOSFET. | TableAsset | 0 | no | no | — |
| ret.electronics.multi_hop.09 | multi_hop | Use KCL at the op-amp input node to finish the finite-gain example. | Law, Passage | 2 | no | yes | — |
| ret.electronics.concept.10 | concept | Saturation region inequalities that must hold for the MOSFET `g_m` formula. | Proposition | 0 | no | no | triode-region page |
| ret.electronics.adversarial.11 | adversarial | Inverting versus non-inverting closed-loop gain sign. | Passage | 0 | no | no | wrong topology page |
| ret.electronics.filter.12 | filter | `g_m` query filtered to a machines chapter. | empty | 0 | no | no | — |

### machines

| id | lane | query | expect | hop | figure | bundle | must_not |
|----|------|-------|--------|-----|--------|--------|----------|
| ret.machines.exact.01 | exact | Open-circuit test of a transformer: which winding is excited. | Concept | 0 | no | no | SC test page |
| ret.machines.exact.02 | exact | Example extracting `R_c` and `X_m` from OC/SC data. | WorkedExample | 1 | no | yes | — |
| ret.machines.concept.03 | concept | Explain slip of an induction motor and its sign in motoring. | Concept | 0 | no | no | generating slip only |
| ret.machines.figure.04 | figure | Approximate equivalent circuit of a transformer referred to the primary. | FigureAsset | 0 | yes | no | exact circuit with both leakage on both sides unreferred |
| ret.machines.figure.05 | figure | From the equivalent-circuit diagram, retrieve the OC-test interpretation paragraph. | FigureAsset, Passage | 1 | yes | no | — |
| ret.machines.example.06 | example | Worked efficiency at a given load and pf from equivalent-circuit parameters. | WorkedExample | 1 | no | yes | — |
| ret.machines.equation.07 | equation | Induced torque of an induction machine in terms of Thevenin quantities and slip. | EquationAsset | 0 | no | no | sync-machine torque angle formula |
| ret.machines.table.08 | table | Nameplate / test-data table used in the OC/SC example. | TableAsset | 0 | no | yes | — |
| ret.machines.multi_hop.09 | multi_hop | Use per-unit on the transformer base before the load-flow-style numerical in the same chapter. | Concept, Passage | 2 | no | no | SI-only page |
| ret.machines.concept.10 | concept | Neglecting magnetizing branch: when the book says it is allowed. | Proposition `assumes` | 1 | no | no | — |
| ret.machines.adversarial.11 | adversarial | Line-to-line versus phase voltage on a Y-connected stator. | Passage | 0 | no | no | delta page treated as Y |
| ret.machines.filter.12 | filter | Slip query with a signals chapter filter. | empty | 0 | no | no | — |

### power

| id | lane | query | expect | hop | figure | bundle | must_not |
|----|------|-------|--------|-----|--------|--------|----------|
| ret.power.exact.01 | exact | Assembly of `Y_bus` for a three-bus network. | Symbol, Passage | 0 | no | no | `Z_bus` building |
| ret.power.exact.02 | exact | First Newton–Raphson iteration residual example. | WorkedExample | 1 | no | yes | Gauss-Seidel example |
| ret.power.concept.03 | concept | Explain per-unit conversion across a transformer boundary. | Concept | 0 | no | no | — |
| ret.power.figure.04 | figure | One-line diagram for the three-bus study. | FigureAsset | 0 | yes | no | — |
| ret.power.figure.05 | figure | From the one-line diagram, retrieve the `Y_bus` construction steps. | FigureAsset, Passage | 1 | yes | yes | — |
| ret.power.example.06 | example | Worked symmetrical fault current at a bus using `Z_bus`. | WorkedExample | 1 | no | yes | unsymmetrical-fault only |
| ret.power.equation.07 | equation | Equal-area criterion: critical clearing angle expression. | EquationAsset | 0 | no | no | swing-equation setup only |
| ret.power.table.08 | table | Line data table: R, X, B for the study network. | TableAsset | 0 | no | no | — |
| ret.power.multi_hop.09 | multi_hop | Use the pu section to justify the base change before the load-flow numerical. | Passage | 2 | no | no | — |
| ret.power.concept.10 | concept | Slack-bus assumptions in a load-flow example. | Proposition | 0 | no | no | — |
| ret.power.adversarial.11 | adversarial | Three-phase versus single-line-to-ground fault current formula. | Passage | 0 | no | no | LG page as 3Φ |
| ret.power.filter.12 | filter | `Y_bus` query filtered to electronics. | empty | 0 | no | no | — |

### control

| id | lane | query | expect | hop | figure | bundle | must_not |
|----|------|-------|--------|-----|--------|--------|----------|
| ret.control.exact.01 | exact | Routh–Hurwitz array for a quartic characteristic polynomial. | Concept | 0 | no | no | Nyquist only |
| ret.control.exact.02 | exact | Numbered lead-compensator design example from phase-margin specs. | WorkedExample | 1 | no | yes | lag-only example |
| ret.control.concept.03 | concept | Explain gain and phase margin on a Bode plot. | Concept | 0 | no | no | — |
| ret.control.figure.04 | figure | Bode magnitude and phase plots for the uncompensated plant. | FigureAsset | 0 | yes | no | Nyquist plot |
| ret.control.figure.05 | figure | From the Bode figure, retrieve the numerical gain-margin reading. | FigureAsset, Passage | 1 | yes | yes | — |
| ret.control.example.06 | example | Worked PID (or lead) gain selection to a settling-time spec. | WorkedExample | 1 | no | yes | — |
| ret.control.equation.07 | equation | Closed-loop transfer function for unity feedback `G/(1+G)`. | EquationAsset | 0 | no | no | — |
| ret.control.table.08 | table | Routh array numerical table for the quartic example. | TableAsset | 0 | no | yes | — |
| ret.control.multi_hop.09 | multi_hop | Use final-value theorem to check the step-error claim in the later design example. | Passage | 2 | no | no | — |
| ret.control.concept.10 | concept | Linear time-invariant assumption before applying Laplace-domain Bode. | Proposition | 0 | no | no | nonlinear describing-function page |
| ret.control.adversarial.11 | adversarial | Degrees versus radians in phase-margin arithmetic. | Passage | 0 | no | no | — |
| ret.control.filter.12 | filter | Routh query with a machines chapter filter. | empty | 0 | no | no | — |

### power_electronics

| id | lane | query | expect | hop | figure | bundle | must_not |
|----|------|-------|--------|-----|--------|--------|----------|
| ret.power_electronics.exact.01 | exact | CCM voltage conversion ratio of a buck converter. | EquationAsset, Concept | 0 | no | no | DCM formula |
| ret.power_electronics.exact.02 | exact | Example computing inductor current ripple for given `L`, `D`, `V_g`. | WorkedExample | 1 | no | yes | — |
| ret.power_electronics.concept.03 | concept | Explain continuous versus discontinuous conduction in a buck. | Concept | 0 | no | no | — |
| ret.power_electronics.figure.04 | figure | Buck converter waveforms: inductor current and switch voltage. | FigureAsset | 0 | yes | no | boost waveforms |
| ret.power_electronics.figure.05 | figure | From the waveform figure, retrieve the volt-second balance paragraph. | FigureAsset, Passage | 1 | yes | no | — |
| ret.power_electronics.example.06 | example | Worked SPWM inverter modulation index and fundamental component. | WorkedExample | 1 | no | yes | six-step only |
| ret.power_electronics.equation.07 | equation | Average switch model duty-cycle constraint `0 < D < 1`. | EquationAsset | 0 | no | no | — |
| ret.power_electronics.table.08 | table | Device voltage/current stress table for the converter example. | TableAsset | 0 | no | no | — |
| ret.power_electronics.multi_hop.09 | multi_hop | Use Faraday’s law (volt-second) to justify the CCM buck ratio in the example. | Law, Passage | 2 | no | yes | — |
| ret.power_electronics.concept.10 | concept | Ideal-switch and lossless-inductor assumptions in the CCM derivation. | Proposition | 1 | no | no | — |
| ret.power_electronics.adversarial.11 | adversarial | Buck versus boost conversion ratio (duty in numerator vs denominator). | Passage | 0 | no | no | boost page as buck |
| ret.power_electronics.filter.12 | filter | CCM buck query filtered to signals. | empty | 0 | no | no | — |

### measurements

| id | lane | query | expect | hop | figure | bundle | must_not |
|----|------|-------|--------|-----|--------|--------|----------|
| ret.measurements.exact.01 | exact | CT ratio error and phase-angle error definitions. | Concept | 0 | no | no | PT/VT only |
| ret.measurements.exact.02 | exact | Example computing burden for a specified CT class. | WorkedExample | 1 | no | yes | — |
| ret.measurements.concept.03 | concept | Explain a Wheatstone bridge balance condition. | Concept | 0 | no | no | Kelvin bridge only |
| ret.measurements.figure.04 | figure | Phasor diagram of CT errors (ratio and phase). | FigureAsset | 0 | yes | no | — |
| ret.measurements.figure.05 | figure | From the CT phasor diagram, retrieve the ratio-error formula prose. | FigureAsset, Passage | 1 | yes | no | — |
| ret.measurements.example.06 | example | Worked Maxwell inductance-bridge numerical. | WorkedExample | 1 | no | yes | — |
| ret.measurements.equation.07 | equation | Instrument transformer composite error bound used in the text. | EquationAsset | 0 | no | no | — |
| ret.measurements.table.08 | table | Accuracy-class table for CTs (0.2, 0.5, 5P, …). | TableAsset | 0 | no | no | — |
| ret.measurements.multi_hop.09 | multi_hop | Use burden definition to interpret the nameplate VA in the CT example. | Passage | 2 | no | yes | — |
| ret.measurements.concept.10 | concept | Frequency and waveform assumptions for a given meter constant. | Proposition | 0 | no | no | — |
| ret.measurements.adversarial.11 | adversarial | Percent ratio error versus phase-angle error (minutes). | Passage | 0 | no | no | swapped definitions |
| ret.measurements.filter.12 | filter | CT query filtered to power electronics. | empty | 0 | no | no | — |

### em

| id | lane | query | expect | hop | figure | bundle | must_not |
|----|------|-------|--------|-----|--------|--------|----------|
| ret.em.exact.01 | exact | Boundary conditions on tangential **H** at a current sheet. | Law | 0 | no | no | dielectric-only boundary |
| ret.em.exact.02 | exact | Example: capacitance of a coaxial pair from Gauss’s law. | WorkedExample | 1 | no | yes | two-wire capacitance only |
| ret.em.concept.03 | concept | Explain skin depth in a good conductor at a given frequency. | Concept | 0 | no | no | — |
| ret.em.figure.04 | figure | Field sketch for a coaxial capacitor or infinite line charge. | FigureAsset | 0 | yes | no | — |
| ret.em.figure.05 | figure | From the coaxial figure, retrieve the Gauss-surface argument. | FigureAsset, Passage | 1 | yes | yes | — |
| ret.em.example.06 | example | Worked lossless-line input impedance at a given electrical length. | WorkedExample | 1 | no | yes | lossy-line example |
| ret.em.equation.07 | equation | Plane-wave intrinsic impedance of free space in the book’s units. | EquationAsset | 0 | no | no | — |
| ret.em.table.08 | table | Constitutive parameters table (`ε_r`, `σ`) for the example media. | TableAsset | 0 | no | no | — |
| ret.em.multi_hop.09 | multi_hop | Use Faraday’s law in integral form to set up the transformer-like loop example if present, else the induction example. | Law, Passage | 2 | no | no | — |
| ret.em.concept.10 | concept | Quasi-static assumption stated before lumped RLC extraction. | Proposition | 0 | no | no | full-wave page |
| ret.em.adversarial.11 | adversarial | SI versus cgs in Coulomb’s constant for a numerical. | Passage | 0 | no | no | mixed-unit page |
| ret.em.filter.12 | filter | Skin-depth query filtered to control. | empty | 0 | no | no | — |

### maths

| id | lane | query | expect | hop | figure | bundle | must_not |
|----|------|-------|--------|-----|--------|--------|----------|
| ret.maths.exact.01 | exact | Cauchy–Riemann equations in Cartesian form. | EquationAsset | 0 | no | no | polar form only |
| ret.maths.exact.02 | exact | Example solving a linear constant-coefficient ODE with Laplace. | WorkedExample | 1 | no | yes | — |
| ret.maths.concept.03 | concept | Explain analyticity versus differentiability at a point in the complex plane. | Concept | 0 | no | no | — |
| ret.maths.figure.04 | figure | Pole-zero plot used in an EE-oriented residue example. | FigureAsset | 0 | yes | no | — |
| ret.maths.figure.05 | figure | From the pole-zero figure, retrieve the inverse-Laplace partial-fraction steps. | FigureAsset, Passage | 1 | yes | yes | — |
| ret.maths.example.06 | example | Worked contour-integral / residue evaluation the text uses for an inverse transform. | WorkedExample | 1 | no | yes | — |
| ret.maths.equation.07 | equation | Fourier inversion integral as printed (sign convention in the exponent). | EquationAsset | 0 | no | no | opposite-sign convention page |
| ret.maths.table.08 | table | Laplace transform pair table used in the ODE example. | TableAsset | 0 | no | no | — |
| ret.maths.multi_hop.09 | multi_hop | Use Euler’s formula from an earlier section in a later phasor-style example. | Passage | 2 | no | no | — |
| ret.maths.concept.10 | concept | Region of convergence or existence conditions on a unilateral Laplace pair. | Proposition | 0 | no | no | — |
| ret.maths.adversarial.11 | adversarial | Degrees versus radians in a complex-exponential numerical. | Passage | 0 | no | no | — |
| ret.maths.filter.12 | filter | Cauchy–Riemann query filtered to machines. | empty | 0 | no | no | — |

---

## How to run (design)

1. Ingest one OER chapter **or** one BYO chapter per pack under test (circuits-first is enough for the first spike).
2. Curator fills `bind` (pages, figure ids) by hand once — that is the gold, not an LLM.
3. Run retrieve with filters on; log hits, latency, bundle/figure link checks.
4. Report per lane, then micro-average. Do not hide `filter` and `adversarial` in a single Recall@k.

Host generation quality is **out of this stack**. If retrieve is right and the host still invents ohms, that is a kernel/host eval, not a RAG miss.

## Open questions

- Human time to bind 120 items against a real Hayt/Chapman/Glover chapter versus OER-only first pass.
- Whether `filter` items should use a held-out chapter of the **same** book (harder negatives) once a full book is ingested.
- Judge-model use for “assumption present in passage” if string match on `assumes` edges is too brittle.

## Sources

- [rag-eval-methodology.md](rag-eval-methodology.md) — retrieved 2026-09-15 — reliability: primary
- [rag-ingest-query-architecture.md](rag-ingest-query-architecture.md) — retrieved 2026-09-15 — reliability: primary
- [ee-task-taxonomy-draft.md](ee-task-taxonomy-draft.md) — retrieved 2026-09-15 — reliability: primary
- [`docs/curriculum-map.md`](../../docs/curriculum-map.md) — retrieved 2026-09-15 — reliability: primary
- [Kuphaldt ModEL](https://ibiblio.org/kuphaldt/socratic/model/index.html) — retrieved 2026-09-07 — reliability: primary (S29)
- [RAG4Reports](https://aclanthology.org/2026.rag4reports-1.4.pdf) — retrieved 2026-09-07 — reliability: paper (S16)
- [GATE EE syllabus mirror](https://static.collegedekho.com/media/uploads/2024/07/01/gate-_ee_2025_syllabus.pdf) — retrieved 2026-09-07 — reliability: secondary (S11)

## Confidence

Overall confidence for this note: high

The lane mix and pack coverage are enough to spike ingest+retrieve. Gold page binds and latency numbers remain corpus-dependent until a chapter is actually indexed.

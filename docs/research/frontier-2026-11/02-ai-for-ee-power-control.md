# AI / LLM agents for electrical engineering (power & control)

**Research slice:** state of the art, May 2024 – Nov 2026 (weighted toward 2025–2026).  
**Audience:** Arc domain-kernel planning — verified engines, traps, goldens, evals.  
**Method:** claims tied to primary sources (paper, repo, official post) with URL and publication/submission date; items without a checked primary source are marked **unverified**.

---

## Top 10 findings (executive summary)

| # | Finding | Primary source (date) | Implication for Arc |
|---|---------|------------------------|---------------------|
| 1 | **Solver-in-the-loop agents** (MCP / function tools + deterministic power-flow, OPF, contingency, SPICE, `python-control`) are the only pattern that reliably hits engineering numbers; bare LLMs fail complex power-simulation tasks (~28% vs ~0% on complex cases for GPT-4o/o1). | Jia et al., arXiv:2411.16707 (2024-11-21); GridMind, arXiv:2509.02494 (2025-09-02) | **Adopt** — Arc’s kernel model is validated industry-wide; extend MCP provider surface (ANDES, MATPOWER/Daline, ngspice, SymPy/RK). |
| 2 | **GridMind (ANL)** and **PowerAgent (Harvard/EPRI ecosystem)** converge on multi-agent orchestration + deterministic solvers for OPF/N-1; GridMind reports correct IEEE-case results when tools are wired. | GridMind SC Workshops ’25 (2025-11); PowerAgent IEEE P&E Mag (2025-08-20) | **Beat on pedagogy** — they target operators/researchers, not UG lab law (CCT signs, λ-ED limits, trap T1–T10). |
| 3 | **EPRI sector LLM benchmark (2,100+ SME questions)** shows **83–86% MCQ** but **~27 pt drop** open-ended; expert-level open answers **46–71%** for best models (Dec 2025). | EPRI press (2025-12-09); white paper product page (2025-11-26) | **Benchmark against** — publish Arc + host on EPRI-style open QA, not just MCQ. |
| 4 | **EEE-Bench (CVPR 2025):** best model **GPT-4o 46.78%** on 2,860 multimodal EEE problems; models “lazy” on diagrams. | CVPR 2025 OA (2025) | **Report** multimodal subset; Arc advantage is checked numbers on power/control subsets. |
| 5 | **ControlAgent + ControlEval (500 tasks):** agent + Python `control` feedback ~**100% ASR** on most classical SISO tasks vs weak GPT-4o prompting baselines. | arXiv:2410.19811 (2024-10); GitHub ControlAgent | **Integrate** ControlEval as external regression; **beat** with state-space / Simulink lab paths. |
| 6 | **ControlBench (147 UG problems):** even best model (Claude 3 Opus) struggles on design (**33% ACC**, **63% ACC-s**); Bode/Nyquist/visual tasks near **0–13%**. | arXiv:2404.03647 (2024-04-04) | **Frontier claim** via trap goldens + engine-verified plots — gap competitors do not close. |
| 7 | **SPICE agents (AnalogCoder, SPICEPilot, AITEE):** feedback + simulation lifts analog/circuit success (e.g. **20/24** AnalogCoder; AITEE 1-Shot-CoT+MRI+Sim near-tutor on harder netlists). | arXiv:2405.14918 (2024-05); arXiv:2505.21582 (2025-05-27) | **Adopt** same loop; **differentiate** with course packs + checked BOM/spec labels. |
| 8 | **CIRCUIT benchmark:** GPT-4o **48%** final answer, **27.45%** unit-test pass; topology reasoning still weak. | arXiv:2502.07980 (2025-02-11) | **Benchmark against** for circuit theory; pair with ngspice oracle. |
| 9 | **NREL eGridGPT / MCP co-simulation (2024–2025):** trustworthy control-room GenAI = digital twins + human-in-loop; not end-to-end autonomy. | NREL TP report DOI 10.2172/2352232 (2024); MCP presentation (2025-07) | **Align** — Arc stays augmentation + `unchecked` token, not autonomous switching. |
| 10 | **MathWorks MATLAB/Simulink Copilot + official MCP Server (2025–2026):** commoditized “run MATLAB” tool surface for any host agent. | MathWorks newsroom (2025-10-07); GitHub `matlab-mcp-server` (2025-10-22) | **Integrate** as optional provider; open-path remains SymPy/Python/ANDES. |

---

## 1. Scope and verification note

This document covers LLM **agents** and closely related **benchmarks** for:

- Power systems (power flow, OPF, stability, operator copilots)
- Control design
- Analog/digital circuits (SPICE-in-the-loop)
- Power electronics & drives (where published)
- Protection
- EE education / tutoring
- Physics-informed and neural grid surrogates callable by agents

**Not claimed without source:** utility production deployments beyond published pilots/reports; exact ISO control-room rollouts; unified “EE agent” products beating human experts on graded coursework.

---

## 2. Cross-cutting pattern: what works vs what fails

### 2.1 Verification approaches that worked (evidence-backed)

| Approach | Reported effect | Sources |
|----------|-----------------|--------|
| **Structured tool / MCP calls** to MATPOWER, Daline, Pandapower, ANDES, MATLAB | High task success when orchestrated (93–97% on simulation task suites vs ~28% bare LLM) | arXiv:2411.16707; NREL MCP talk 2025; PowerAgent roadmap |
| **Closed-loop feedback** (run code → measure → revise) | ControlAgent ~100% ASR on many categories; AnalogCoder 20/24 circuits | arXiv:2410.19811; arXiv:2405.14918 |
| **SPICE / numeric oracle** for tutoring | AITEE: simulation-backed arithmetic; EPRI relay tests emphasize text/grid models over SLDs | arXiv:2505.21582; PAC World 2024 |
| **Deterministic benchmark harness** (no LLM-as-judge) | EEBench (atopile), ControlEval env, Arc-style goldens | eebench.org; EnvCommons/ControlEval |
| **Human-in-the-loop + digital twin** for grid ops | eGridGPT design philosophy | NREL 2024 report |
| **Domain-specific RAG / graph similarity** (not naive chunk RAG) | AITEE MRI netlist-indexing; PowerAgent PowerSkills | arXiv:2505.21582 |

### 2.2 Where frontier models still fail (published failure analyses)

| Failure mode | Evidence |
|--------------|----------|
| **Open-ended utility Q&A** vs structured MCQ | −27 pp average accuracy (EPRI, 2025-12-09) |
| **Multimodal EEE diagrams** | EEE-Bench best 46.78%; visual neglect (“laziness”) | CVPR 2025 |
| **Symbolic equation from schematics** | CircuitSense: >85% perception but **<19%** symbolic derivation | arXiv:2509.22339 |
| **Classical control design & frequency-domain plots** | ControlBench: Bode 6.66–13.3% ACC; Nyquist often 0% | arXiv:2404.03647 |
| **Circuit topology unit tests** | CIRCUIT: 27.45% pass@unit-test | arXiv:2502.07980 |
| **College science (incl. physics math)** | SciBench best ~43% text / 13.8% multimodal | ICML 2024 / arXiv:2307.10635 |
| **Protection SLD interpretation** | Mixed; text/grid strong, SLD weak (EPRI/PAC World) | pacw.org 2024 |
| **Subtle power-system procedure law** (signs, limits, segment models) | Arc trap ablation (internal goldens) — **see repo** `test_trap_ablation.py`; external analog: EPRI open-ended gap | Arc repo + EPRI 2025 |

---

## 3. Power systems agents & grid copilots

### 3.1 GridMind (Argonne)

| Field | Detail |
|-------|--------|
| **What** | Multi-agent LLM system for conversational ACOPF and N-1 contingency on IEEE cases. |
| **Method** | Specialized agents (ACOPF, contingency, planner/coordinator) + **function calls** to deterministic solvers; LangGraph-style orchestration per GridAI site. |
| **Results** | Paper claims framework delivers **correct solutions** across tested LLMs on IEEE cases; smaller LLMs match accuracy with lower latency. |
| **Limits** | Prototype scope (OPF + contingency); not UG transient stability pedagogy; no public trap-level regression cited. |
| **Arc** | **Benchmark against** OPF/contingency orchestration; **beat** on SMIB/CCT/AGC/ED with verified undergraduate kernels. |

**Sources:** [arXiv:2509.02494](https://arxiv.org/abs/2509.02494) (2025-09-02); [ACM SC Workshops ’25](https://doi.org/10.1145/3731599.3767409) (2025-11); [GridAI](https://argonne-gridfm.github.io/) (2025).

### 3.2 PowerAgent (open community)

| Field | Detail |
|-------|--------|
| **What** | Roadmap and repos for **PowerFM**, **PowerMCP**, **PowerWF**, **PowerSkills**. |
| **Method** | Foundation models + MCP tool bridge + modular workflows; co-pilot not end-to-end optimizer. |
| **Results** | Magazine article defines architecture; GitHub hosts PowerFM collection (e.g. PriceFM arXiv:2508.04875 cited on site). |
| **Limits** | Ecosystem early; eval harness less mature than EE education goldens. |
| **Arc** | **Integrate** MCP patterns; **differentiate** with course-aligned capability registry. |

**Sources:** [IEEE P&E Magazine](https://doi.org/10.1109/mpe.2025.3579718) (2025-08-20); [poweragent.seas.harvard.edu](https://poweragent.seas.harvard.edu/) (2025-06 launch); [TechRxiv preprint](https://doi.org/10.36227/techrxiv.174918210.07854858/v1) (2025-06-05).

### 3.3 Feedback-driven simulation agents (Daline / MATPOWER)

| Field | Detail |
|-------|--------|
| **What** | Multi-agent RAG + CoT + environment feedback for power-system simulation code generation. |
| **Method** | Triple-store RAG, reasoning prompts, error feedback loop; 69 tasks Daline + MATPOWER. |
| **Results** | **93.13%** (Daline) and **96.85%** (MATPOWER) success; GPT-4o/o1 **27.77%** standard / **0%** complex; ~30 s & ~$0.014 USD per task. |
| **Limits** | Simulation **setup** not graded coursework; may not enforce equal-area/CCT sign conventions. |
| **Arc** | **Adopt** feedback architecture; **beat** by binding named recipes + trap catalog. |

**Sources:** [arXiv:2411.16707](https://arxiv.org/abs/2411.16707) (v3 2025-05-19); precursor [arXiv:2406.17215](https://arxiv.org/abs/2406.17215) (2024-06-18).

### 3.4 NREL eGridGPT & generative AI for operations

| Field | Detail |
|-------|--------|
| **What** | Control-room-oriented GenAI: procedures, suggestions, digital-twin simulation. |
| **Method** | LLM + SCADA/state estimation/contingency context; cybersecurity & NERC CIP framing. |
| **Results** | Conceptual architecture; benchmarking against operator exams cited in third-party summary of NREL report (**interpret cautiously** — not independent lab metrics in excerpt). |
| **Limits** | Research report, not product; validation burden on utilities. |
| **Arc** | **Align** trust model; **ignore** becoming control-room OS; optional cite for MCP co-simulation. |

**Sources:** [NREL/TP eGridGPT](https://research-hub.nrel.gov/en/publications/egridgpt-trustworthy-ai-in-the-control-room) (2024); [Generative AI for Grid Operations PDF](https://docs.nlr.gov/docs/fy25osti/91176.pdf) (2024-11); [MCP-driven analysis presentation](https://research-hub.nrel.gov/en/publications/co-simulation-meets-ai-mcp-driven-power-system-analysis/) (2025-07).

### 3.5 EPRI Open Power AI Consortium & LLM benchmarking

| Field | Detail |
|-------|--------|
| **What** | Domain-specific GenAI models + **2,100+** utility SME Q&A benchmark. |
| **Method** | MCQ, web-augmented, open-ended phases; GPT-5, Grok 4, Gemini 2.5 Pro tested (per press). |
| **Results** | MCQ **83–86%** frontier; open-ended **~27 pp** drop; expert open **46–71%**; web search **+2–4%** with retrieval risk. |
| **Limits** | MCQ overstates readiness; not laboratory-style numeric grading. |
| **Arc** | **Benchmark against** EPRI open-ended power topics; publish **checked** numeric deltas. |

**Sources:** [EPRI press 2025-12-09](https://www.epri.com/about/media-resources/press-release/i6nJ8So7cP6QhiYtwvF5labVsGqpi2xj); [NVIDIA/EPRI consortium blog](https://blogs.nvidia.com/blog/open-power-ai-consortium/) (2025-03-20); [Benchmark product page](https://www.epri.com/research/products/000000003002034347) (2025-11-26).

### 3.6 LLM-driven transient stability workflow (research)

| Field | Detail |
|-------|--------|
| **What** | Agent automates ANDES scenarios + NAS for TSA classifiers. |
| **Method** | RAG + CoT + self-correction; IEEE 39 & 118 bus studies. |
| **Results** | Claims superior accuracy vs hand-designed NN baselines (see paper tables). |
| **Limits** | Research automation for **ML TSA**, not student equal-area/CCT grading. |
| **Arc** | **Integrate** ANDES provider optional; **beat** on UG swing/CCT with deterministic goldens. |

**Sources:** [arXiv:2511.20276](https://arxiv.org/html/2511.20276v2) (v2 2025; check version date on arXiv).

### 3.7 Neural / differentiable grid surrogates (agent-callable)

| Field | Detail |
|-------|--------|
| **What** | **LUMINA** GNN foundation model for fast ACOPF prediction; GridMind can call neural solvers. |
| **Method** | Heterogeneous GNN, physics-informed / augmented Lagrangian training, topology transfer. |
| **Results** | Model card: 3.8M params; trained multi-case up to 13,659 bus; GridAI cites LUMINA-Bench. |
| **Limits** | Surrogate feasibility ≠ optimality proof; Mar 2026 formal paper emphasizes constraint satisfaction trade-offs. |
| **Arc** | **Integrate** as optional fast provider with **fallback** to full solver + `unchecked` labeling. |

**Sources:** [GridAI / LUMINA](https://argonne-gridfm.github.io/); [Hugging Face argonne/LUMINA](https://huggingface.co/argonne/LUMINA/blob/main/README.md); [arXiv:2603.04300](https://arxiv.org/abs/2603.04300) (2026-03-04).

---

## 4. Control design agents

### 4.1 ControlAgent & ControlEval

| Field | Detail |
|-------|--------|
| **What** | Multi-agent LLM + **Python computation agent** (`python-control`) for classical loop shaping. |
| **Method** | Task-specific agents, memory, iterative tuning vs stability/settling/PM specs. |
| **Results** | **~100% ASR** most categories; near **96%** higher-order; GPT-4o few-shot baselines far lower. |
| **Limits** | Transfer-function SISO textbook tasks; no Simulink/state-space course quirks. |
| **Arc** | **Benchmark against** ControlEval; extend to **discrete** labs & block-diagram traps. |

**Sources:** [arXiv:2410.19811](https://arxiv.org/pdf/2410.19811) (2024-10); [github.com/ControlAgent/ControlAgent](https://github.com/ControlAgent/ControlAgent); [EnvCommons/ControlEval](https://github.com/EnvCommons/ControlEval).

### 4.2 ControlBench (bare LLM baseline)

| Field | Detail |
|-------|--------|
| **What** | 147 undergraduate control problems, expert-graded. |
| **Method** | Zero-shot + self-check (ACC / ACC-s). |
| **Results** | Claude 3 Opus best but **Control System Design 33.3% ACC**; **Bode 13.3%**; calculation & plot-reading dominant errors. |
| **Limits** | 2024 models; sampling variance high. |
| **Arc** | **Beat** with tool-augmented host + kernel; publish head-to-head on overlapping topics. |

**Sources:** [arXiv:2404.03647](https://arxiv.org/abs/2404.03647) (2024-04-04).

---

## 5. Circuits & chip-adjacent agents

### 5.1 AnalogCoder & SPICEPilot

| Field | Detail |
|-------|--------|
| **What** | Training-free LLM → **PySpice/ngspice** code with feedback & skill library. |
| **Method** | Domain prompts, OP/DC checks, modular subcircuits. |
| **Results** | **20/24** tasks vs GPT-4o **15/24**; SPICEPilot reports **24/24** with prompt engineering on same benchmark. |
| **Limits** | Functional correctness focus, not full PDK optimization / tape-out. |
| **Arc** | **Adopt** pattern; bind to Arc ngspice capability + student trap checks. |

**Sources:** [arXiv:2405.14918](https://arxiv.org/abs/2405.14918) (2024-05-23); [SPICEPilot](https://arxiv.org/html/2410.20553) (2024-10).

### 5.2 EEBench (atopile) — agent hardware design

| Field | Detail |
|-------|--------|
| **What** | Simulation-graded **agent** benchmark (13 tasks v1). |
| **Method** | atopile bundles → SPICE + BOM cost score (0.65 technical + 0.35 economics). |
| **Results** | Public leaderboard (dynamic); methodology stresses deterministic checks. |
| **Limits** | Small task count; vendor-maintained; no manufacture. |
| **Arc** | **Benchmark against** for design agents; Arc focuses broader UG coursework coverage. |

**Sources:** [eebench.org](https://www.eebench.org/); [methodology](https://eebench.org/methodology.html).

### 5.3 CIRCUIT, AMSbench, CircuitSense

| Field | Detail |
|-------|--------|
| **What** | Reasoning / MLLM benchmarks for analog & mixed-signal. |
| **Method** | Unit-test grouping; hierarchical perception → analysis → design. |
| **Results** | CIRCUIT: **48.04%** / **27.45%** unit pass; CircuitSense symbolic **<19%**; AMSbench ~8k Qs with large MLLM gaps (per abstracts). |
| **Limits** | Mostly QA, not full lab notebooks. |
| **Arc** | **Report** subset scores; **beat** with SPICE-backed homework paths. |

**Sources:** [arXiv:2502.07980](https://arxiv.org/abs/2502.07980) (2025-02-11); [arXiv:2509.22339](https://arxiv.org/abs/2509.22339) (2025-09-26); [arXiv:2505.24138](https://arxiv.org/abs/2505.24138) (2025-05-30).

---

## 6. Power electronics, drives, protection

### 6.1 PHIA / PE-GPT (modulation & converter design)

| Field | Detail |
|-------|--------|
| **What** | LLM planners + physics-informed surrogates for converter modulation. |
| **Method** | Chat requirements → simulation/optimization loop. |
| **Results** | PHIA: **63.2%** lower MAE vs next benchmark; **33×** faster (user study n=20 experts). |
| **Limits** | Narrow task (modulation); not full UG drives set. |
| **Arc** | **Integrate** pattern for power-electronics capabilities; golden-switching waveforms. |

**Sources:** [arXiv:2411.14214](https://arxiv.org/abs/2411.14214) (2024-11-21); [arXiv:2403.14059](https://arxiv.org/abs/2403.14059) (2024-03-21).

### 6.2 Multi-agent PE control design

| Field | Detail |
|-------|--------|
| **What** | LLM agents decompose PE controller design (plan → model → simulate → verify). |
| **Method** | Multi-agent workflow (paper is conceptual + case-oriented). |
| **Results** | Claims efficient autonomous pipeline; quantitative table limited in abstract. |
| **Limits** | Few public benchmarks. |
| **Arc** | **Ignore** until reproducible eval; reuse architecture ideas only. |

**Sources:** [arXiv:2406.12628](https://arxiv.org/abs/2406.12628) (2024-06-18).

### 6.3 Protection & relay settings (LLM trials)

| Field | Detail |
|-------|--------|
| **What** | Off-the-shelf LLMs for relay setting workflows from grid models + guides. |
| **Method** | EPRI/PAC structured tests on distance/OC/differential settings. |
| **Results** | Strong on **text/grid**; **mixed on SLDs**; some models progressed mid-2024 → late-2024. |
| **Limits** | Not safety-certified; ambiguous guideline handling fails. |
| **Arc** | **White space** for UG protection numbering; optional future capability. |

**Sources:** [PAC World article](https://www.pacw.org/practical-application-of-ai-llms-for-calculating-relay-settings) (2024); [IET 2025 paper DOI](https://digital-library.theiet.org/doi/10.1049/icp.2025.1040); [arXiv:2403.09125](https://arxiv.org/html/2403.09125v2) (energy sector limitations).

**Note:** TechRxiv “LLM-OS relaying” with 15% faster detection is **single preprint** — treat as **unverified** for production claims until peer-reviewed replication.

---

## 7. MATLAB / Simulink copilots & open alternatives

### 7.1 MathWorks Copilot + MCP

| Field | Detail |
|-------|--------|
| **What** | **MATLAB Copilot** (R2025b+), **Simulink Copilot** (R2026a), **MATLAB MCP Server** on GitHub. |
| **Method** | Cloud LLM + local MATLAB execution tools (`evaluate_matlab_code`, `run_matlab_file`, etc.). |
| **Results** | Official product scope: explain, generate, test MATLAB; Simulink model search & error help. |
| **Limits** | Subscription, network, regional limits; not deterministic grader. |
| **Arc** | **Integrate** as provider; keep SymPy/Python/ANDES open path. |

**Sources:** [MathWorks MATLAB Copilot news](https://www.mathworks.com/company/newsroom/mathworks-launches-generative-ai-powered-matlab-copilot-to-boost-productivity-and-accelerate-development-for-engineers-scientists-and-researchers.html) (2025-10-07); [Simulink Copilot product](https://www.mathworks.com/products/simulink-copilot.html); [github.com/matlab/matlab-mcp-server](https://github.com/matlab/matlab-mcp-server/) (2025-10-22).

### 7.2 Open stacks agents already use

Julia `PowerModels.jl`, Python `andes`, `pandapower`, `ngspice`, `Daline` — surfaced in papers above as **tool targets**, not student-facing products. Arc already aligns with **provider-swappable** architecture (`docs/ARCHITECTURE.md`).

---

## 8. AI tutoring for engineering students

### 8.1 AITEE (EE-specific agentic tutor)

| Field | Detail |
|-------|--------|
| **What** | Circuit image → netlist, GNN similarity RAG, **SPICE**, Socratic dialogue. |
| **Method** | 1-Shot-CoT + MRI indexing + optional Sim verification. |
| **Results** | Large gains on complex classes; Claude 3.5 near-flawless on dataset with Sim; arithmetic/superposition limits remain. |
| **Limits** | First-year DC circuits focus; didactic metrics partial. |
| **Arc** | **Beat** via full UG EE coverage + traps; **adopt** MRI+Sim pattern. |

**Sources:** [arXiv:2505.21582](https://arxiv.org/abs/2505.21582) (2025-05-27).

### 8.2 SocraticLM (math) & circuit homework grading

| Field | Detail |
|-------|--------|
| **What** | Socratic fine-tuning (SocraTeach 35K dialogues); circuit homework **assessment** benchmark. |
| **Method** | Multi-agent dataset construction; LaTeX solutions, five rubric metrics. |
| **Results** | SocraticLM **+12%** vs GPT-4 on pedagogy dims; grading: GPT-4o/Llama 70B > GPT-3.5 on circuit HW. |
| **Limits** | Math-centric tutoring; not power/control labs. |
| **Arc** | **Integrate** Socratic host policy; kernel supplies **correctness** oracle. |

**Sources:** [NeurIPS 2024 SocraticLM](https://proceedings.neurips.cc/paper_files/paper/2024/file/9bae399d1f34b8650351c1bd3692aeae-Paper-Conference.pdf); [arXiv:2506.06390](https://arxiv.org/abs/2506.06390) (2025-06-05).

---

## 9. Implication matrix (Arc actions)

| Action | Targets |
|--------|---------|
| **Adopt** | Solver-in-the-loop MCP; SPICE feedback; ControlEval-style binary specs; EPRI-style open-ended reporting; `unchecked` token discipline. |
| **Beat** | UG power lab law (CCT, AGC signs, λ-ED limits); multimodal diagram + **checked** numeric; ControlBench weakness areas with tools. |
| **Benchmark against** | EEE-Bench, EPRI 2.1k, ControlEval, CIRCUIT, EEBench, internal `test_trap_ablation.py` / PSA evals. |
| **Integrate** | MATLAB MCP, ANDES/MATPOWER, GridMind-style multi-agent **recipes** (not ANL stack). |
| **Ignore** | Domain FM training races, autonomous relay LLM-OS preprints, operator-only copilots without student goldens. |

---

## 10. Public benchmarks Arc should report (frontier status)

| Benchmark | Why | Metric to publish |
|-----------|-----|-------------------|
| **Arc trap ablation** (`tests/integration/test_trap_ablation.py`) | Unique UG power proof; large bare-agent errors | Pass rate bare vs Arc; numeric delta on T1/T6/T4–T5 |
| **PSA / scripts checks** (`scripts/check_psa_evals.py`) | Repo-native regression | CI pass + scorecard |
| **ControlEval** | External credibility for control | ASR vs ControlAgent paper baseline |
| **ControlBench** (subset) | Shows frequency-domain gap closure | ACC with SymPy/MATLAB tools enabled |
| **EEE-Bench** (power + control + PE tags) | Multimodal EE visibility | % by subdomain vs GPT-4o 46.78% ceiling |
| **EPRI-style open-ended** (sample or licensed mirror) | Utility-grade honesty | Open accuracy + **verified** subscore |
| **CIRCUIT** (level 1–3 + power category) | Circuit reasoning | Unit-test pass % with ngspice |
| **EEBench** (optional) | Agentic design league | Task pass if atopile in scope |

**Reporting format suggestion:** always pair **host-only** vs **Arc kernel** on the same items; cite primary benchmark date; store JSON artifacts under `artifacts/evals/` (future).

---

## 11. White space (no one is reliably good yet)

1. **Undergraduate power-system laboratory law** — multi-segment equal-area/CCT, clearing-time grids, primary vs AGC transients, economic dispatch with binding limits — with **published** head-to-head vs frontier host (Arc goldens exist; sector agents do not publish this layer).
2. **Multimodal → symbolic → numeric** single pipeline for coursework (CircuitSense gap: high perception, **<19%** symbolic derivation).
3. **Open-ended utility engineering answers** with automatic **physics verification** (EPRI shows 27+ pp MCQ/open gap; few verify numbers).
4. **Protection & relay coordination** from SLDs + ambiguous utility guides (PAC/EPRI: SLD remains weak).
5. **Frequency-domain control courseware** (Bode/Nyquist/loop shaping) at **>80%** verified without human grader (ControlBench: often **<15%**).
6. **Drives & machines labs** (vector control, torque/speed, dq frames) as agent benchmarks — sparse agent papers vs controls/PE silos.
7. **Cross-domain UG EE co-solver** spanning circuits + signals + power + control + PE in **one** trap-aware kernel (products are siloed: GridMind, AnalogCoder, AITEE, ControlAgent).
8. **Socratic tutoring that is also numerically certified** on exam-style EE (AITEE close on circuits; power/control unaddressed).
9. **Feasibility-certified fast surrogates** wired into student agents with **fallback proofs** (LUMINA-class models improve speed; constraint stories still open in 2026 paper).
10. **Reproducible “bare coding agent” failure gallery** for EE coursework (Arc ablation is a template; not yet a public standard dataset).

---

## 12. Source index (primary)

| ID | Citation | URL | Date |
|----|----------|-----|------|
| S1 | GridMind | https://arxiv.org/abs/2509.02494 | 2025-09-02 |
| S2 | PowerAgent (IEEE) | https://doi.org/10.1109/mpe.2025.3579718 | 2025-08-20 |
| S3 | Jia et al., simulation agents | https://arxiv.org/abs/2411.16707 | 2024-11-21 (v3 2025-05-19) |
| S4 | EPRI LLM benchmark press | https://www.epri.com/about/media-resources/press-release/i6nJ8So7cP6QhiYtwvF5labVsGqpi2xj | 2025-12-09 |
| S5 | EEE-Bench (CVPR) | https://openaccess.thecvf.com/content/CVPR2025/html/Li_EEE-Bench_A_Comprehensive_Multimodal_Electrical_And_Electronics_Engineering_Benchmark_CVPR_2025_paper.html | 2025 |
| S6 | ControlAgent | https://arxiv.org/pdf/2410.19811 | 2024-10 |
| S7 | ControlBench | https://arxiv.org/abs/2404.03647 | 2024-04-04 |
| S8 | AnalogCoder | https://arxiv.org/abs/2405.14918 | 2024-05-23 |
| S9 | CIRCUIT | https://arxiv.org/abs/2502.07980 | 2025-02-11 |
| S10 | AITEE | https://arxiv.org/abs/2505.21582 | 2025-05-27 |
| S11 | NREL eGridGPT report | https://research-hub.nrel.gov/en/publications/egridgpt-trustworthy-ai-in-the-control-room | 2024 |
| S12 | PHIA | https://arxiv.org/abs/2411.14214 | 2024-11-21 |
| S13 | CircuitSense | https://arxiv.org/abs/2509.22339 | 2025-09-26 |
| S14 | SciBench | https://arxiv.org/abs/2307.10635 | ICML 2024 proc. |
| S15 | MATLAB Copilot launch | https://www.mathworks.com/company/newsroom/mathworks-launches-generative-ai-powered-matlab-copilot-to-boost-productivity-and-accelerate-development-for-engineers-scientists-and-researchers.html | 2025-10-07 |
| S16 | MATLAB MCP Server | https://github.com/matlab/matlab-mcp-server | 2025-10-22 |
| S17 | PAC World relay LLM tests | https://www.pacw.org/practical-application-of-ai-llms-for-calculating-relay-settings | 2024 |
| S18 | LUMINA | https://arxiv.org/abs/2603.04300 | 2026-03-04 |
| S19 | SocraticLM | https://proceedings.neurips.cc/paper_files/paper/2024/file/9bae399d1f34b8650351c1bd3692aeae-Paper-Conference.pdf | NeurIPS 2024 |
| S20 | EEBench methodology | https://eebench.org/methodology.html | accessed 2026-11-13 |

---

*Document version: 2026-11-13. Maintainer: Arc research track `frontier-2026-11`.*

# Frontier labs and vendors: AI for science, engineering, and industry (Nov 2025–Nov 2026)

Research snapshot for Arc positioning. **Scope:** roughly the twelve months ending **13 November 2026**, plus a few **anchor releases from H1 2025** still defining the competitive frame (notably Google AI co-scientist, Sakana AI Scientist v1). Every factual claim below cites a **primary URL and publication date** where verified; unverified or secondary-only claims are labeled.

Audience: product and domain-kernel strategy for undergraduate EE (power, control, circuits, protection, drives).

---

## Executive summary: ten findings that matter for Arc

1. **Verification beats narration.** The strongest lab and industry systems treat **automated evaluators** (scorers, simulators, lab instruments) as the authority—not the LLM. Google **AlphaEvolve** (14 May 2025) pairs Gemini with code execution and quantitative metrics; OpenAI’s **FERMIACC** collider workflow uses deterministic physics checks. Arc’s trap catalog + golden JSON is the same architectural bet at undergrad scale. **Arc: beat** generic research agents on “checked or labeled unchecked” copy.

2. **Skills + MCP are the composable stack.** Anthropic shipped **Agent Skills** (Oct 2025) and published them as an **open standard** at [agentskills.io](https://agentskills.io/home) (Dec 2025), explicitly paired with **MCP connectors**. Arc already is a domain kernel in this shape (skills, recipes, MCP). **Arc: integrate** with host skills/MCP; document parity with Claude/OpenAI harnesses.

3. **Vertical “science packs” bundle connectors, skills, and benchmarks—not bigger models alone.** **Claude for Life Sciences** (20 Oct 2025; expanded 11 Jan 2026) adds Benchling/PubMed connectors, life-sciences skills, and cited evals (Protocol QA, BixBench). **Claude for Financial Services** (15 Jul 2025; 27 Oct 2025) mirrors the pattern. **Arc: copy** the packaging story for EE: named connectors (ngspice, MATLAB paths), skills, and published ablations.

4. **Hypothesis factories scale; lab law does not.** **Google AI co-scientist** (19 Feb 2025) and **Microsoft Discovery** (19 May 2025) orchestrate multi-agent literature synthesis, tournaments, and HPC loops—but validation is domain-specific and often biomedical/chemistry. They do not ship SMIB CCT sign conventions or λ-ED limit loops. **Arc: ignore** as product competitors for coursework; **beat** on verifiable undergrad EE outcomes.

5. **“AI scientist” startups prove closed loops in bio/chem, not EE homework.** **FutureHouse Robin** (May 2025) and **Edison Kosmos** (5 Nov 2025) scale literature + analysis code; **Sakana AI Scientist-v2** (Apr 2025) automates ML papers with tree search. Wins are therapeutic/ML workshop tier, not grader-aligned power labs. **Arc: differentiate** on domain traps and reproducible engine outputs.

6. **Autonomous labs are capital-intensive and physics-grounded.** **Lila Sciences** (10 Mar 2025; $350M Series A Oct 2025), **Periodic Labs** (30 Sep 2025), and **NVIDIA Physical AI** stacks close the loop with robots, twins, and surrogate sims. EE undergrad workflows are cheaper: SPICE, MATLAB, and golden regressions. **Arc: integrate** sim hooks; do not compete on robotic labs.

7. **Incumbent EDA and MBD vendors ship copilots, not graded kernels.** **MathWorks MATLAB Copilot** (7 Oct 2025), **Simulink Copilot** (beta Dec 2025 / product docs R2026a), **Ansys Engineering Copilot** (29 Jul 2025), **Siemens Industrial Copilot + agents** (Mar–May 2025), **Synopsys.ai / Cadence JedAI** (2025). These assist documentation, scripting, and in-tool Q&A; they do not prove equal-area or ACE sign. **Arc: beat** MATLAB-only paths with verified numbers; **partner** where users already live.

8. **Industrial AI targets the field, not the lecture hall.** Anthropic × **IFS Resolve** (13 Nov 2025) and Siemens **Industrial AI agents** (12 May 2025) optimize maintenance, PLCs, and twins. Valuable for “where EE graduates work,” not for EEC301-style grading. **Arc: copy** multimodal troubleshooting patterns for lab support; **ignore** as core wedge.

9. **OpenAI and Google productize research agents for developers.** **OpenAI Codex** GA (6 Oct 2025), **OpenAI for Science** + GPT‑5 case studies (20 Nov 2025), **Gemini Deep Research** via Interactions API (11 Dec 2025), distributed **GPT‑Rosalind** agents (index page, 2025). Throughput for experts with oversight; citation and numerics remain fragile. **Arc: integrate** as hosts; keep kernel authoritative for EE numbers.

10. **The frontier gap Arc can own:** no shipping product combines **undergrad EE lab law**, **trap-aware skills**, **deterministic engines**, and **published A/B vs bare agent** in one installable kernel. Labs and clouds optimize discovery velocity or tool UX; Arc optimizes **grader-aligned correctness or explicit uncertainty**.

---

## 1. Anthropic

### 1.1 Claude for Life Sciences (vertical)

| Field | Detail |
|--------|--------|
| **What** | Packaged life-sciences offering: scientific **connectors**, **Agent Skills**, prompt library, enterprise support. |
| **How it works** | Connectors (Benchling, PubMed, 10x Genomics, etc.) via MCP-style integration; skills for workflows; model evals cited (Sonnet 4.5 on Protocol QA 0.83 vs human 0.79; BixBench gains). Jan 2026 expansion adds clinical/regulatory connectors (Medidata, ClinicalTrials.gov, ToolUniverse 600+ tools). |
| **Who** | Pharma R&D, biotech, clinical ops, regulatory. |
| **What it proves** | Vertical share is won by **tool graph + skills + benchmarks**, not raw chat. |
| **Arc implication** | **Copy** GTM and architecture: EE connectors (SPICE, MATLAB sync), skills per recipe, publish trap ablation as benchmark. |

**Primary sources:** [Claude for Life Sciences](https://www.anthropic.com/news/claude-for-life-sciences) (2025-10-20); [Healthcare & life sciences expansion](https://www.anthropic.com/news/healthcare-life-sciences) (2026-01-11).

### 1.2 Claude for Financial Services (vertical template)

| Field | Detail |
|--------|--------|
| **What** | Financial Analysis Solution: connectors (S&P, PitchBook, Snowflake…), **Claude for Excel** beta, finance **Agent Skills** (DCF, comps, coverage). |
| **How it works** | MCP connectors + skills; cites Vals AI Finance Agent benchmark (Sonnet 4.5 55.3% Oct 2025). |
| **Who** | Banks, asset managers, fintech. |
| **What it proves** | Repeatable vertical pattern: data plane + skills + office add-ins. |
| **Arc implication** | **Copy** “skills for repeatable artifacts”; EE analog = λ-ED spreadsheets, load-flow summaries with citations to goldens. |

**Primary sources:** [Claude for Financial Services](https://www.anthropic.com/news/claude-for-financial-services) (2025-07-15); [Advancing Claude for FS](https://www.anthropic.com/news/advancing-claude-for-financial-services) (2025-10-27).

### 1.3 Agent Skills + MCP + plugins

| Field | Detail |
|--------|--------|
| **What** | **Agent Skills**: folders of instructions/scripts loaded on demand; **MCP** for remote tools in Messages API; **plugins** bundle skills + connectors. |
| **How it works** | Progressive disclosure; Skills API + code execution beta; MCP `mcp_servers` + `mcp_toolset` (tools only, beta). |
| **Who** | Enterprise and developers standardizing agent workflows. |
| **What it proves** | Industry settling on **MCP = data/tools, Skills = procedure**. |
| **Arc implication** | **Integrate**—Arc recipes map cleanly to Skills; engines via MCP or local CLI. |

**Primary sources:** [Equipping agents with Agent Skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills) (2025-10-16); [Introducing Agent Skills / open standard note](https://claude.com/resources/articles/skills) (updated 2025-12-18); [MCP connector docs](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector); [agentskills.io](https://agentskills.io/specification).

### 1.4 Claude Code and Claude Science (research coding)

| Field | Detail |
|--------|--------|
| **What** | **Claude Code**: agentic terminal/IDE coding; **Claude Science** (guide): local provenance-forward research app vs Code for shipping repos. |
| **How it works** | Best practices: explore → plan → implement → verify; Jupyter side-by-side; Life Sciences pushes bioinformatics through Claude Code. |
| **Who** | Scientific computing teams, platform engineers. |
| **What it proves** | Hosts separate **research analysis** from **software engineering** surfaces. |
| **Arc implication** | **Integrate** with Claude Code + `AGENTS.md`; position Arc as kernel Claude Science does not provide for EE numerics. |

**Primary sources:** [Claude Code best practices](https://www.anthropic.com/research/claude-code-best-practices); [Claude Science product guide](https://claude.com/resources/guides/claude-science-product-guide/when-to-use-which-claude-surface).

### 1.5 Industrial partnership (manufacturing vertical)

| Field | Detail |
|--------|--------|
| **What** | **IFS × Anthropic Resolve** — industrial AI for frontline workers (vision, sensors, schematics, audio). |
| **How it works** | Claude multimodal reasoning on operational data; customer case studies (William Grant & Sons). |
| **Who** | Manufacturing, utilities, A&D, energy. |
| **What it proves** | Anthropic’s “real world” push is **ops/maintenance**, not academic EE grading. |
| **Arc implication** | **Copy** multimodal troubleshooting UX for lab hardware; **ignore** as core academic wedge. |

**Primary sources:** [IFS × Anthropic](https://www.ifs.com/en/insights/news/ifs-partners-with-anthropic) (2025-11-13).

---

## 2. OpenAI

### 2.1 OpenAI for Science + GPT‑5 experiments

| Field | Detail |
|--------|--------|
| **What** | Program and case-study paper on GPT‑5 assisting expert-led science (math, physics, biology, materials, astronomy). |
| **How it works** | Frontier model + collaborations; explicit limits (hallucinated citations, need expert oversight). |
| **Who** | University and national-lab researchers. |
| **What it proves** | Acceleration is real in **expert loops**; not autonomous reliable numerics. |
| **Arc implication** | **Copy** honest limitation language; **beat** with mandatory verify-or-unchecked for EE numbers. |

**Primary sources:** [Early experiments accelerating science with GPT‑5](https://openai.com/index/accelerating-science-gpt-5/) (2025-11-20); [OpenAI Science](https://openai.com/science/).

### 2.2 Distributed research agents (biology)

| Field | Detail |
|--------|--------|
| **What** | Thousands of **GPT‑Rosalind** agents analyzing brain-cell atlas; 32-minute distributed run (blog). |
| **How it works** | Fan-out agents per gene disruption + literature linking. |
| **Who** | Computational biology partnerships. |
| **What it proves** | **Scale-out agent fleets** for evidence synthesis—not symbolic EE lab checks. |
| **Arc implication** | **Ignore** for product; optional pattern for parallel eval jobs. |

**Primary source:** [Scaling AI research for complex biological data](https://openai.com/index/scaling-ai-research-for-complex-biological-data/).

### 2.3 FERMIACC (physics agent pipeline) — _verify date on Academy post_

| Field | Detail |
|--------|--------|
| **What** | Closed-loop agents + collider tools (FeynRules, MadGraph, Pythia) for anomaly chasing. |
| **How it works** | OpenAI Agents SDK; structured outputs; **deterministic checks** on decays/interactions. |
| **Who** | Collider phenomenology researchers (UCSB/KITP). |
| **What it proves** | Domain **verifiers** make agent loops credible. |
| **Arc implication** | **Copy** verifier-first agent design—Arc engines are the verifier. |

**Primary source:** [How physicists are using AI to chase new physics](https://academy.openai.com/home/blogs/how-physicists-are-using-ai-to-chase-new-physics-2026-03-25) — **Note:** URL dated 2026-03-25; included as architecture reference; treat marketing dates cautiously.

### 2.4 Codex (software engineering agent)

| Field | Detail |
|--------|--------|
| **What** | Cloud/local **Codex** agent: sandboxes, PRs, reviews, **GPT‑5‑Codex**, SDK, Slack. |
| **How it works** | Repo sandboxes, tests/linters, AGENTS.md, MCP; GA Oct 2025. |
| **Who** | Software teams (also Arc’s host surface). |
| **What it proves** | General coding agents are table stakes; domain correctness is external. |
| **Arc implication** | **Integrate**—Arc is what Codex loads for EE verification. |

**Primary sources:** [Introducing Codex](https://openai.com/index/introducing-codex/) (2025-05-16); [Codex GA](https://openai.com/index/codex-now-generally-available/) (2025-10-06).

---

## 3. Google DeepMind / Google

### 3.1 AI co-scientist

| Field | Detail |
|--------|--------|
| **What** | Multi-agent **Gemini 2.0** system: Generation, Reflection, Ranking, Evolution, Proximity, Meta-review; tournament evolution + test-time compute. |
| **How it works** | Natural-language goals → hypotheses + protocols; biomedical validation cases in paper. |
| **Who** | Biomedical researchers (early access institutions). |
| **What it proves** | **Hypothesis throughput** can scale; wet-lab validation still human-led. |
| **Arc implication** | **Ignore** as coursework solver; **beat** on deterministic PSA/AGC/ED checks. |

**Primary sources:** [Google Research blog](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/) (2025-02-19); [arXiv:2502.18864](https://arxiv.org/abs/2502.18864).

### 3.2 AlphaEvolve

| Field | Detail |
|--------|--------|
| **What** | Evolutionary **coding agent** (Gemini Flash + Pro) with automated evaluators; production use in Google Borg scheduling (~0.7% compute recovery). |
| **How it works** | Propose code → run → score → mutate; human-readable heuristics; matrix-multiply kernel speedups for Gemini training. |
| **Who** | Google internal + planned academic early access. |
| **What it proves** | **Machine-gradable objectives** enable genuine algorithm discovery. |
| **Arc implication** | **Copy** eval-driven loops for recipe tuning; **beat** by publishing EE golden suites openly. |

**Primary source:** [AlphaEvolve blog](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) (2025-05-14).

### 3.3 Gemini Deep Research (API)

| Field | Detail |
|--------|--------|
| **What** | Long-horizon research agent via **Interactions API**; **DeepSearchQA** benchmark open-sourced. |
| **How it works** | Gemini 3 Pro core; iterative search/plan; file upload + citations; MCP planned. |
| **Who** | Developers in finance, biotech, market research. |
| **What it proves** | Report quality improving; still citation/recall tradeoffs (see ReportBench). |
| **Arc implication** | **Integrate** for literature; never substitute for engine-verified lab numbers. |

**Primary source:** [Build with Gemini Deep Research](https://blog.google/innovation-and-ai/technology/developers-tools/deep-research-agent-gemini-api/) (2025-12-11).

---

## 4. Microsoft Discovery

| Field | Detail |
|--------|--------|
| **What** | Azure **agentic R&D platform**: Discovery Engine, knowledge graph, specialized agents, HPC/quantum roadmap; local **Discovery app** (preview) with GitHub Copilot account. |
| **How it works** | Graph reasoning over internal + public science; agent workflows (e.g., PFAS-free coolant demo at Build 2025); explainable provenance. |
| **Who** | Enterprise R&D (materials, chemistry, energy). |
| **What it proves** | Enterprises buy **orchestrated discovery loops + governance**, not chatbots. |
| **Arc implication** | **Copy** provenance and graph memory ideas for saved Arc runs; **ignore** full platform build. |

**Primary sources:** [Build 2025 blog](https://azure.microsoft.com/en-us/blog/transforming-rd-with-agentic-ai-introducing-microsoft-discovery/) (2025-05-19); [Microsoft Learn overview](https://learn.microsoft.com/en-us/azure/microsoft-discovery/overview-what-is-microsoft-discovery).

---

## 5. NVIDIA (Physical AI, optimization, simulation)

### 5.1 Omniverse / digital twins / Physical AI

| Field | Detail |
|--------|--------|
| **What** | OpenUSD + Omniverse twins; Foxconn case study with **PhysicsNeMo**, **cuOpt**, Isaac Sim. |
| **How it works** | Surrogate ML for CFD/thermal (up to ~150× vs traditional in cited case); cuOpt for AGV/material flow; reinforcement learning in Isaac Lab. |
| **Who** | Electronics manufacturing, datacenter, robotics. |
| **What it proves** | **Sim + optimize + sense** loops for factories—not symbolic Laplace homework. |
| **Arc implication** | **Integrate** where Arc adds control/power didactics; **ignore** twin platform scope. |

**Primary sources:** [Omniverse Taiwan manufacturers](https://blogs.nvidia.com/blog/omniverse-digital-twins-taiwan-manufacturers-physical-ai/) (2025, COMPUTEX); [Foxconn case study](https://www.nvidia.com/en-in/case-studies/foxconn-develops-physical-ai-enabled-smart-factories-with-digital-twins/).

### 5.2 cuOpt open source

| Field | Detail |
|--------|--------|
| **What** | GPU **decision optimization** (LP/MIP/VRP) opened under Apache 2.0. |
| **How it works** | PuLP/AMPL interfaces; complements CPU solvers. |
| **Who** | Logistics, energy unit commitment, factory planning. |
| **What it proves** | Optimization AI is commoditizing; **correct formulation** still domain-hard (cf. λ-ED). |
| **Arc implication** | **Integrate** for dispatch demos; **beat** on teaching limit loops and IC units. |

**Primary sources:** [cuOpt open source](https://blogs.nvidia.com/blog/cuopt-open-source/); [Technical blog](https://developer.nvidia.com/blog/accelerate-decision-optimization-using-open-source-nvidia-cuopt/) (2025-06-11).

### 5.3 PhysicsNeMo / DoMINO NIM

| Field | Detail |
|--------|--------|
| **What** | AI physics framework and **DoMINO NIM** microservice; 500× claims with partners (Ansys Fluent path, aerospace). |
| **How it works** | Surrogate initialization + high-fidelity solver validation. |
| **Who** | Aerospace, automotive, CAE vendors. |
| **What it proves** | Surrogates must be **anchored** to trusted solvers—same as Arc’s engine story. |
| **Arc implication** | **Copy** “fast guess + deterministic check” narrative for SPICE/MATLAB. |

**Primary source:** [AI physics aerospace/automotive](https://blogs.nvidia.com/blog/ai-physics-aerospace-automotive-design-engineering/) (2025-10-28).

---

## 6. Siemens, MathWorks, Ansys, Synopsys, Cadence

### 6.1 Siemens Industrial Copilot and agents

| Field | Detail |
|--------|--------|
| **What** | Copilots across design/planning/engineering/operations; **AI agents** with orchestrator (Automate 2025); Hermes Award 2025. |
| **How it works** | Natural language → SCL/PLC code, P&ID digitalization, Senseye maintenance; on-prem option. |
| **Who** | Process and discrete manufacturing. |
| **What it proves** | Incumbents own **shop-floor** AI; education layer is separate. |
| **Arc implication** | **Copy** career narrative; **beat** on academic verification, not PLC codegen breadth. |

**Primary sources:** [AI agents press release](https://press.siemens.com/global/en/pressrelease/siemens-introduces-ai-agents-industrial-automation) (2025-05-12); [Hermes Award](https://press.siemens.com/global/en/pressrelease/bringing-generative-ai-industry-siemens-industrial-copilot-wins-hermes-award-2025).

### 6.2 MathWorks MATLAB / Simulink Copilot

| Field | Detail |
|--------|--------|
| **What** | **MATLAB Copilot** in R2025b (7 Oct 2025); **Simulink Copilot** beta (Dec 2025) / help docs; GPT‑5 mini update (13 Nov 2025 blog). |
| **How it works** | LLM grounded on MathWorks docs + editor context; explains errors, generates code/tests; probabilistic outputs with validate warnings. |
| **Who** | Engineers and students in MBD workflow. |
| **What it proves** | **Direct competition** for “AI + MATLAB” story Arc mediates. |
| **Arc implication** | **Beat** with trap-aware recipes and goldens; **integrate** where users insist on native Copilot. |

**Primary sources:** [MATLAB Copilot launch](https://www.mathworks.com/company/newsroom/mathworks-launches-generative-ai-powered-matlab-copilot-to-boost-productivity-and-accelerate-development-for-engineers-scientists-and-researchers.html) (2025-10-07); [Simulink Copilot blog](https://blogs.mathworks.com/simulink/2025/12/01/a-copilot-for-simulink/) (2025-12-01); [Copilot LLM update](https://blogs.mathworks.com/matlab/2025/11/13/matlab-copilot-gets-a-new-llm-november-2025-updates/) (2025-11-13).

### 6.3 Ansys Engineering Copilot (Synopsys portfolio)

| Field | Detail |
|--------|--------|
| **What** | In-solver assistant + **AnsysGPT** (Azure OpenAI); 2025 R2 AI+ features. |
| **How it works** | RAG over courses, forums, KB; not running verified university lab engines. |
| **Who** | FEA/CFA/EM simulation users. |
| **What it proves** | Support and onboarding AI ≠ domain grading kernel. |
| **Arc implication** | **Ignore** except shared “copilot + solver” positioning language. |

**Primary sources:** [2025 R2 press release](https://ansys.synopsys.com/news-center/press-releases/7-29-25-r2-accelerates-innovation-with-ai) (2025-07-29); [Engineering Copilot blog](https://ansys.synopsys.com/blog/work-faster-smarter-with-ansys-engineering-copilot).

### 6.4 Synopsys.ai Copilot + Cadence JedAI / agentic EDA

| Field | Detail |
|--------|--------|
| **What** | **Synopsys.ai Copilot** knowledge/workflow/creative GenAI (RTL, formal assertions); **Cadence JedAI** + agentic AI roadmap (Mar–May 2025). |
| **How it works** | RAG on EDA docs; agent frameworks across Verisium/Cerebrus/etc.; NVIDIA Nemotron collaboration. |
| **Who** | Chip and system designers. |
| **What it proves** | EE *industry* AI is chip-design-centric, not power-system labs. |
| **Arc implication** | **Ignore** for UG power labs; note for circuits/microelectronics track extensions. |

**Primary sources:** [Synopsys AI expansion](https://news.synopsys.com/2025-09-03-Synopsys-Announces-Expanding-AI-Capabilities-for-its-Leading-EDA-Solutions) (2025-09-03); [Cadence–NVIDIA PR](https://www.cadence.com/en_US/home/company/newsroom/press-releases/pr/2025/cadence-accelerates-ai-driven-engineering-design-and-science.html) (2025-03-18); [Cadence agentic AI blog](https://community.cadence.com/cadence_blogs_8/b/corporate-news/posts/agentic-ai-soc-system-engineering) (2025-05-07).

---

## 7. Startups and research labs

### 7.1 FutureHouse / Edison Scientific

| Field | Detail |
|--------|--------|
| **What** | **Platform** agents Crow/Falcon/Owl/Phoenix (May 2025); **Robin** autonomous discovery (May 2025); **Kosmos** AI Scientist + Edison spinout (Nov 2025). |
| **How it works** | Literature tools + multi-agent loops; Kosmos structured world models over huge paper/code context; claims ~80% conclusion accuracy (self-reported). |
| **Who** | Biology/chemistry pharma partners. |
| **What it proves** | Closed discovery loops work in **wet-lab verticals**; EE undergrad traps untouched. |
| **Arc implication** | **Beat** on reproducible EE goldens; **copy** transparent reasoning chains for viva. |

**Primary sources:** [FutureHouse platform](https://www.futurehouse.org/news/launching-futurehouse-platform-ai-agents) (2025-05-01); [Robin arXiv:2505.13400](https://arxiv.org/abs/2505.13400); [Kosmos](https://edisonscientific.com/news/announcing-kosmos) (2025-11-05); [Edison spinout](https://www.futurehouse.org/news/announcing-edison-scientific) (2025-11-05).

### 7.2 Periodic Labs

| Field | Detail |
|--------|--------|
| **What** | AI scientists + **autonomous materials labs**; $300M seed (Sep 2025). |
| **How it works** | Physical experiments as RL environment; agents plan/execute/analyze in powder synthesis labs. |
| **Who** | Materials, semiconductors (heat dissipation), defense/space customers. |
| **What it proves** | Next scaling axis is **private experimental data**, not textbooks. |
| **Arc implication** | **Ignore** capex race; **copy** “nature/simulator as judge” language for ngspice/MATLAB. |

**Primary source:** [Introducing Periodic Labs](https://periodic.com/news/introducing-periodic-labs) (2025-09-30).

### 7.3 Lila Sciences

| Field | Detail |
|--------|--------|
| **What** | “Scientific superintelligence” + **AI Science Factories**; $200M seed Mar 2025, **$350M Series A** Oct 2025. |
| **How it works** | Generative AI + robotic labs across life/chemical/materials science; partner platform. |
| **Who** | Pharma, sustainability, materials partners. |
| **What it proves** | Flagship-style **full-stack science factories** are fundable; not courseware. |
| **Arc implication** | **Ignore** as competitor; **copy** safety/human-gate patterns for student-facing tools. |

**Primary sources:** [Flagship unveil](https://www.flagshippioneering.com/news/press-release/flagship-pioneering-unveils-lila-sciences-to-build-superintelligence-in-science) (2025-03-10); [Series A](https://www.lila.ai/news/announcing-the-close-of-our-series-a) (2025-10-10).

### 7.4 Sakana AI Scientist

| Field | Detail |
|--------|--------|
| **What** | v1 (Aug 2024) full ML-paper automation; **v2** (Apr 2025) tree search, first AI-generated **peer-reviewed workshop** acceptance claimed. |
| **How it works** | Idea → code → experiments → paper → simulated/real peer review; VLM figure polish. |
| **Who** | ML researchers; demo domain = ML subfields. |
| **What it proves** | End-to-end automation hits **low-stakes ML workshop** bar, not ABET lab grading. |
| **Arc implication** | **Ignore** product overlap; **copy** eval harness discipline for Arc recipe regression. |

**Primary sources:** [Sakana v1 post](https://sakana.ai/ai-scientist/) (2024-08-13); [v2 arXiv:2504.08066](https://arxiv.org/abs/2504.08066); [First publication post](https://sakana.ai/ai-scientist-first-publication/) (2025-03-12).

---

## 8. Cross-cutting architecture patterns (2025–2026)

| Pattern | Who exemplifies | Verification | Arc stance |
|---------|-----------------|--------------|------------|
| MCP + Skills + plugins | Anthropic | Partial (skills run code in sandbox) | Already aligned |
| Multi-agent debate / tournament | Google co-scientist, Microsoft Discovery | Wet-lab or human expert | Ignore for grading |
| Evolution + auto-grader | AlphaEvolve | Quantitative metrics | Copy for evals |
| Copilot-in-CAD/MBD/CAE | MathWorks, Ansys, Siemens | User must validate | Beat with goldens |
| Autonomous lab loop | Lila, Periodic | Physical measurement | Integrate sim-only |
| Deep research / literature | Gemini, OpenAI | Citation audits fail often | Integrate, don’t trust numerics |
| Coding agent GA | Codex, Claude Code | Tests/CI | Host loads Arc kernel |

**Deep research caution (verified third-party evals):** JMIR and dermatology studies (2025) report citation inaccuracies and shallow synthesis—relevant when comparing Arc literature assist to Gemini/OpenAI Deep Research. **Arc: beat** by never blending unverified literature numbers into graded outputs.

---

## 9. Synthesis: implications for Arc product and messaging

### Copy (patterns worth adopting)

- Vertical packaging: **connectors + skills + benchmarks + support** (Anthropic life sciences/finance).
- **MCP + Agent Skills** open standard for portable EE recipes.
- **Verifier-first agents** (AlphaEvolve, FERMIACC, Robin’s lab loop) in marketing and architecture diagrams.
- Honest **expert-in-the-loop** and hallucination limits (OpenAI for Science).
- Provenance in saved runs (Microsoft Discovery, Claude Science guide).

### Beat (differentiation)

- **Undergrad EE lab law** (traps T1–T10, PSA/AGC/ED/circuits) with published ablation vs bare agent.
- **MATLAB Copilot / raw Codex** on numeric coursework without goldens.
- Hypothesis-only “co-scientist” tools on anything requiring **sign conventions, limits, or solver policy**.

### Integrate (hosts and adjacent tools)

- Claude Code, Codex, Cursor as harnesses; Gemini/OpenAI for literature.
- MathWorks stack where required; ngspice/MATLAB as connectors.
- NVIDIA-style **fast surrogate + deterministic check** story for simulation recipes.

### Ignore (out of Arc scope unless explicitly expanded)

- Robotic science factories (Lila, Periodic).
- Industrial field AI (IFS Resolve, Siemens shop-floor agents).
- EDA agentic chip design platforms.
- Autonomous ML paper mills (Sakana) as quality competitors for labs.

---

## 10. Source list (primary, by organization)

| Date | Source | URL |
|------|--------|-----|
| 2025-10-20 | Anthropic — Claude for Life Sciences | https://www.anthropic.com/news/claude-for-life-sciences |
| 2026-01-11 | Anthropic — Healthcare & life sciences expansion | https://www.anthropic.com/news/healthcare-life-sciences |
| 2025-07-15 | Anthropic — Claude for Financial Services | https://www.anthropic.com/news/claude-for-financial-services |
| 2025-10-27 | Anthropic — Advancing Claude for FS | https://www.anthropic.com/news/advancing-claude-for-financial-services |
| 2025-10-16 | Anthropic — Agent Skills research post | https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills |
| 2025-12-18 | Anthropic — Agent Skills article (open standard) | https://claude.com/resources/articles/skills |
| — | Agent Skills specification | https://agentskills.io/specification |
| — | Claude MCP connector docs | https://platform.claude.com/docs/en/agents-and-tools/mcp-connector |
| — | Claude Science product guide | https://claude.com/resources/guides/claude-science-product-guide/when-to-use-which-claude-surface |
| 2025-11-13 | IFS × Anthropic Resolve | https://www.ifs.com/en/insights/news/ifs-partners-with-anthropic |
| 2025-11-20 | OpenAI — GPT‑5 science experiments | https://openai.com/index/accelerating-science-gpt-5/ |
| — | OpenAI for Science | https://openai.com/science/ |
| — | OpenAI — biological data agents | https://openai.com/index/scaling-ai-research-for-complex-biological-data/ |
| 2025-05-16 | OpenAI — Introducing Codex | https://openai.com/index/introducing-codex/ |
| 2025-10-06 | OpenAI — Codex GA | https://openai.com/index/codex-now-generally-available/ |
| 2025-02-19 | Google — AI co-scientist blog | https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/ |
| — | arXiv co-scientist paper | https://arxiv.org/abs/2502.18864 |
| 2025-05-14 | Google DeepMind — AlphaEvolve | https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/ |
| 2025-12-11 | Google — Gemini Deep Research API | https://blog.google/innovation-and-ai/technology/developers-tools/deep-research-agent-gemini-api/ |
| 2025-05-19 | Microsoft — Discovery announcement | https://azure.microsoft.com/en-us/blog/transforming-rd-with-agentic-ai-introducing-microsoft-discovery/ |
| — | Microsoft Learn — Discovery | https://learn.microsoft.com/en-us/azure/microsoft-discovery/overview-what-is-microsoft-discovery |
| 2025-10-28 | NVIDIA — PhysicsNeMo / DoMINO | https://blogs.nvidia.com/blog/ai-physics-aerospace-automotive-design-engineering/ |
| 2025-06-11 | NVIDIA — cuOpt open source (technical) | https://developer.nvidia.com/blog/accelerate-decision-optimization-using-open-source-nvidia-cuopt/ |
| — | NVIDIA — cuOpt blog | https://blogs.nvidia.com/blog/cuopt-open-source/ |
| — | NVIDIA — Omniverse manufacturers | https://blogs.nvidia.com/blog/omniverse-digital-twins-taiwan-manufacturers-physical-ai/ |
| 2025-05-12 | Siemens — Industrial AI agents | https://press.siemens.com/global/en/pressrelease/siemens-introduces-ai-agents-industrial-automation |
| 2025-10-07 | MathWorks — MATLAB Copilot launch | https://www.mathworks.com/company/newsroom/mathworks-launches-generative-ai-powered-matlab-copilot-to-boost-productivity-and-accelerate-development-for-engineers-scientists-and-researchers.html |
| 2025-12-01 | MathWorks — Simulink Copilot beta | https://blogs.mathworks.com/simulink/2025/12/01/a-copilot-for-simulink/ |
| 2025-11-13 | MathWorks — Copilot LLM update | https://blogs.mathworks.com/matlab/2025/11/13/matlab-copilot-gets-a-new-llm-november-2025-updates/ |
| 2025-07-29 | Ansys/Synopsys — 2025 R2 + Copilot | https://ansys.synopsys.com/news-center/press-releases/7-29-25-r2-accelerates-innovation-with-ai |
| 2025-09-03 | Synopsys — AI Copilot expansion | https://news.synopsys.com/2025-09-03-Synopsys-Announces-Expanding-AI-Capabilities-for-its-Leading-EDA-Solutions |
| 2025-03-18 | Cadence — NVIDIA agentic AI PR | https://www.cadence.com/en_US/home/company/newsroom/press-releases/pr/2025/cadence-accelerates-ai-driven-engineering-design-and-science.html |
| 2025-05-07 | Cadence — Agentic AI blog | https://community.cadence.com/cadence_blogs_8/b/corporate-news/posts/agentic-ai-soc-system-engineering |
| 2025-05-01 | FutureHouse — Platform launch | https://www.futurehouse.org/news/launching-futurehouse-platform-ai-agents |
| — | Robin paper | https://arxiv.org/abs/2505.13400 |
| 2025-11-05 | Edison — Kosmos | https://edisonscientific.com/news/announcing-kosmos |
| 2025-09-30 | Periodic Labs — Intro | https://periodic.com/news/introducing-periodic-labs |
| 2025-03-10 | Flagship — Lila Sciences | https://www.flagshippioneering.com/news/press-release/flagship-pioneering-unveils-lila-sciences-to-build-superintelligence-in-science |
| 2025-10-10 | Lila — Series A | https://www.lila.ai/news/announcing-the-close-of-our-series-a |
| 2024-08-13 | Sakana — AI Scientist v1 | https://sakana.ai/ai-scientist/ |
| 2025-03-12 | Sakana — First peer-reviewed claim | https://sakana.ai/ai-scientist-first-publication/ |
| — | Sakana — AI Scientist v2 | https://arxiv.org/abs/2504.08066 |

### Secondary / analysis sources used with caution

- JMIR Deep Research perspective: https://www.jmir.org/2025/1/e75666
- ReportBench (deep research evaluation): https://arxiv.org/html/2508.15804

### Unverified or date-ambiguous items (not asserted as fact)

- **Claude Science** standalone product: described in Anthropic guide URLs; GA date and feature completeness **not verified** in this pass beyond the product guide.
- **OpenAI FERMIACC** Academy blog dated **2026-03-25** (future-dated URL at time of research run); architecture description treated as illustrative only.
- **CadenceLIVE video page** shows “July 06, 2026” metadata—excluded from factual claims.

---

*Document produced for Arc research track `frontier-2026-11`. No product code changes.*

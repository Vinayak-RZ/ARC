# Agent architecture, verification, and evals (Nov 2026 research slice)

**Audience:** Arc domain-kernel planning — what to adopt, slim, or cut as frontier generalists improve.  
**Scope:** Public primary sources from roughly Nov 2024–Nov 2026 (12-month window ending today, 13 Nov 2026).  
**Non-goals:** Product code changes; prescribing specific Arc PRs.  
**Arc hooks:** README domain kernel, `docs/DOMAIN_KERNEL_CAPABILITIES.md`, trap catalog T1–T10, goldens, `test_trap_ablation.py`.

---

## Top 10 (executive)

| # | Finding | Implication for Arc |
|---|---------|---------------------|
| 1 | **Agent Skills + MCP are complementary open standards** (skills = procedural expertise; MCP = tool/data reach), converging under AAIF with progressive disclosure of `SKILL.md` ([Anthropic skills/MCP article](https://claude.com/resources/articles/extending-claude-capabilities-with-skills-mcp-servers), 18 Dec 2025; [Google AAIF post](https://opensource.googleblog.com/2026/11/scaling-ai-agents-open-standards-mcp-aaif.html), Nov 2026). | **Adopt:** Ship Arc as portable skills + thin MCP (engines, goldens), not a custom harness DSL. **Cut:** Duplicate “how to do the lab” prose that belongs in skills the host already loads. |
| 2 | **Host ecosystems commoditize wiring:** Cursor Rules/`AGENTS.md`, Claude Code plugins (skills + hooks + MCP), OpenAI Agents SDK + Apps SDK on MCP ([Cursor rules docs](https://cursor.com/docs/context/rules); [Claude Code plugins](https://code.claude.com/docs/en/plugins/overview); [OpenAI Apps SDK](https://openai.com/index/introducing-apps-in-chatgpt/), 6 Oct 2025). | **Change:** Arc kernel = engines + traps + evals; hosts own loop, memory, and UI. **Cut:** Building a second chat product or visual agent builder. |
| 3 | **Frontier coding models are strong at repo-scale agentic work** (e.g. Claude Sonnet 4.5: 77.2% SWE-bench Verified, 30+ hour runs; GPT-5: 74.9% SWE-bench Verified, 88% Aider polyglot, 96.7% τ²-bench telecom — [Anthropic](https://www.anthropic.com/news/claude-sonnet-4-5), 29 Sep 2025; [OpenAI developers](https://openai.com/index/introducing-gpt-5-for-developers/), 7 Aug 2025). | **Cut/slim:** Generic coding tutorials, shallow MATLAB/Python scaffolding, “explain RK4” skills. **Keep:** Domain stage/sign/limit law models can't infer from SWE-bench. |
| 4 | **Scientific + domain numerics remain weak at research fidelity** — SciCode: best models solve single-digit % of main problems; HAL leaderboard top agent ~9.2% ([SciCode site](https://scicode-bench.github.io/); [HAL SciCode](https://hal.cs.princeton.edu/scicode), accessed Nov 2026). | **Adopt:** Simulator-in-the-loop + golden JSON as the graded truth layer. **Moat:** Verified EE engines (PSA, dispatch, AGC), not “better codegen.” |
| 5 | **RLVR (rule-based verifiable rewards) is the default post-training recipe** for reasoning models (DeepSeek-R1, RLVR theory/RISE/imperfect verifiers, Reasoning Gym envs — [DeepSeek-R1](https://arxiv.org/abs/2501.12948v1), 22 Jan 2025; [RLVR reasoning paper](https://arxiv.org/abs/2506.14245), Jun 2025; [NeurIPS RISE](https://proceedings.neurips.cc/paper_files/paper/2025/file/bd3d106d8e9789ce4fd40e1edafe71d5-Paper-Conference.pdf), 2025). | **Change:** Treat Arc goldens/traps as **RLVR environment**, not documentation. **Do not** rely on fine-tuning the frontier model on lab PDFs as the moat. |
| 6 | **Process reward / verifier loops at inference** materially improve agents (SWE-PRM +10.6 pp on SWE-bench Verified; GUI-Shepherd verifier re-ranking — [arXiv:2509.02360](https://arxiv.org/abs/2509.02360), Sep 2025; [arXiv:2509.23738](https://arxiv.org/html/2509.23738)). | **Adopt:** Arc “critic” = trap catalog + engine re-run + `unchecked` labeling; optional lightweight PRM on *procedure* steps (solver choice, sign, limits). |
| 7 | **Evolutionary / self-improving agents need user-supplied evaluators** (AlphaEvolve; Darwin Gödel Machine; AI Scientist-v2 — [DeepMind AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/), 14 May 2025; [Sakana DGM](https://sakana.ai/dgm/), 30 May 2025; [AI Scientist-v2](https://arxiv.org/html/2504.08066), Apr 2025). | **Adopt:** Use goldens + trap ablations as the **fitness function** for recipe/skill evolution, not open-ended self-modification of the host. |
| 8 | **Eval methodology shifted to contamination resistance, reliability metrics, and vertical rubrics** (LiveCodeBench time-segmentation; τ-bench pass^⌝k; Anthropic agent eval guide — [ICLR LiveCodeBench](https://proceedings.iclr.cc/paper_files/paper/2025/hash/94074dd5a072d28ff75a76dabed43767-Abstract-Conference.html); [τ-bench ICLR 2025 PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/1b126cc38b8638e07bef37e7b2bb72bf-Paper-Conference.pdf); [Anthropic demystifying evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), 9 Jan 2026). | **Adopt:** Report **pass^1 and pass^k** on trap suite; hold-out traps; dated golden sets. **Adopt:** LiveCodeBench-style **release-date** versioning for Arc eval corpora. |
| 9 | **Vertical winners prove superiority via expert rubrics + pairwise arena + retrieval goldens**, not public academic benchmarks alone (Harvey BigLaw Bench / Arena — [Harvey eval blog](https://www.harvey.ai/blog/scaling-ai-evaluation-through-expertise), 22 May 2025; [BLB Arena](https://www.harvey.ai/blog/introducing-biglaw-bench-arena), 7 Nov 2025). | **Adopt:** Arc A/B trap ablation + instructor-style rubrics is the right shape. **Change:** Publish arena-style blind preferences vs “bare Cursor” on **held-out** lab sheets. |
| 10 | **Formal / property-based verification for scientific code is emerging but narrow** (SPIRAL lifting, PBT for codegen, ProofWright for CUDA — [CMU SPIRAL HPEC 2025 PDF](https://users.ece.cmu.edu/~franzf/papers/2025_HPEC_Oschatz_Q.pdf); [Property-Generated Solver](https://arxiv.org/html/2506.18315v1), Jun 2025). | **Adopt:** Property tests on invariants (unit consistency, monotonicity, limit satisfaction). **Defer:** Full formal proofs except for tiny kernel lemmas. |

---

## 1. Agent skills, MCP, and host plugin ecosystems

### What it is

Three layers hardened in 2025–2026:

- **MCP:** Standard tool/data connectivity; official [MCP Registry preview](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/) (8 Sep 2025) at `registry.modelcontextprotocol.io`; July 2026 spec move to **stateless** transports ([Google Open Source Blog](https://opensource.googleblog.com/2026/11/scaling-ai-agents-open-standards-mcp-aaif.html), Nov 2026).
- **Agent Skills:** `SKILL.md` packages with progressive disclosure (YAML frontmatter → full instructions/scripts on demand). Anthropic published skills as an **open standard** (article update, 18 Dec 2025). Skills and MCP donated to **AAIF** alongside MCP ([same Google post](https://opensource.googleblog.com/2026/11/scaling-ai-agents-open-standards-mcp-aaif.html)).
- **Host packaging:** Claude Code **plugins** bundle skills, agents, hooks, MCP ([plugins overview](https://code.claude.com/docs/en/plugins/overview)). Cursor **Rules** + `AGENTS.md` provide repo-scoped instructions ([Cursor rules](https://cursor.com/docs/context/rules)). OpenAI **Apps SDK** (preview, 6 Oct 2025) extends MCP with app UI/logic in ChatGPT ([OpenAI Apps](https://openai.com/index/introducing-apps-in-chatgpt/)); **AgentKit** (6 Oct 2025) targets build/deploy/eval for agents ([AgentKit](https://openai.com/index/introducing-agentkit/)) with a **June 2026 wind-down notice** for Agent Builder/Evals products on the platform (noted on same page, 3 Jun 2026 update).

### Why it matters

The industry converged on **“MCP for hands, Skills for SOPs.”** Hosts duplicate loop mechanics; differentiation moves to **domain instructions + verifiable tool surfaces**.

### Evidence

| Claim | Primary source | Date |
|-------|----------------|------|
| Skills teach workflows; MCP connects systems | [Anthropic: Extending Claude with skills and MCP](https://claude.com/resources/articles/extending-claude-capabilities-with-skills-mcp-servers) | Updated 18 Dec 2025 |
| Skills vs prompts/projects/MCP table | [Skills explained](https://claude.com/resources/articles/skills-explained) | 2025 (undated on page) |
| MCP Registry preview launch | [MCP blog](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/) | 8 Sep 2025 |
| AAIF co-maintenance, stateless MCP | [Google Open Source Blog](https://opensource.googleblog.com/2026/11/scaling-ai-agents-open-standards-mcp-aaif.html) | Nov 2026 |
| Claude Code plugin anatomy | [code.claude.com plugins](https://code.claude.com/docs/en/plugins/overview) | 2025–2026 (living docs) |
| Cursor rules / AGENTS.md | [cursor.com/docs/context/rules](https://cursor.com/docs/context/rules) | 2025–2026 (living docs) |

### Implication for Arc

- **Adopt:** Standardize Arc delivery as **repo skills + MCP engines + hooks** (post-tool golden check), matching how students already attach Cursor/Claude Code.
- **Cut:** Custom skill formats that don't interoperate with Agent Skills / Claude Code / Cursor.
- **Change:** Position MCP as **narrow verbs** (`run_workflow`, `solve`, goldens) per `research/notes/agentic-kernel-2026.md` — not one tool per MATLAB function.

---

## 2. Tool-grounded and simulator-in-the-loop reasoning

### What it is

Agents that **execute** domain code (simulators, compilers, unit tests) and grade on **external state**, not self-reported reasoning. Benchmarks: τ-bench (DB end-state grading), SciCode (scientific research scripts with domain tests), AlphaEvolve (user-defined scalar metrics on code runs).

### Why it matters

Frontier models ace **software engineering** benchmarks yet remain near **floor** on authentic scientific pipelines. Arc's ngspice/YAML/PSA engines are exactly the “ground truth outside the model” pattern AlphaEvolve and τ-bench assume.

### Evidence

| Claim | Primary source | Date |
|-------|----------------|------|
| τ-bench: tool+policy+user sim; DB state grading; pass^⌝k | [ICLR 2025 τ-bench paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/1b126cc38b8638e07bef37e7b2bb72bf-Paper-Conference.pdf) | ICLR 2025 |
| SciCode: 338 subproblems, research-level; SOTA low % | [scicode-bench.github.io](https://scicode-bench.github.io/) | 2024–2025 (site); HAL Nov 2026 |
| AlphaEvolve requires automated evaluators | [DeepMind blog](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) | 14 May 2025 |
| Gemini 2.5 cites large SWE-bench gains; still not SciCode-saturating | [arXiv:2507.06261](https://arxiv.org/html/2507.06261v2) | Jul 2025 |

### Implication for Arc

- **Adopt:** Every recipe path must end in **engine execution or explicit `unchecked`** — already Arc DNA; double down.
- **Cut:** Long chain-of-thought “derivations” without simulator cross-check for numeric labs.
- **Change:** Expose **simulator-in-the-loop** as first-class MCP (batch runs, waveform diff), not optional nice-to-have.

---

## 3. Verifier, critic, and process-reward loops

### What it is

- **Evaluator–optimizer workflow** (generator + critic LLM) — [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents) (Dec 2024, still canonical).
- **Process Reward Models (PRMs)** at inference: SWE-PRM intervenes on trajectories ([arXiv:2509.02360](https://arxiv.org/abs/2509.02360), 2025).
- **RLVR + self-verification (RISE)** trains verification alongside solving ([NeurIPS 2025 PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/bd3d106d8e9789ce4fd40e1edafe71d5-Paper-Conference.pdf)).

### Why it matters

Outcome-only grading misses **procedure errors** (wrong solver, wrong sign) — Arc trap catalog T1–T10. PRMs address the same gap for SWE agents; Arc's traps are a **deterministic PRM** for EE.

### Implication for Arc

- **Adopt:** Trap-triggered **course correction** in the host loop (hook after edit: run golden delta).
- **Change:** Separate **outcome** graders (numbers match golden) from **process** graders (forbidden `ode45`, wrong ACE sign).
- **Cut:** LLM-as-judge as the *only* verifier for numeric labs (use as tie-breaker only).

---

## 4. Formal and property-based verification for scientific code

### What it is

- **Semantics lifting** (SPIRAL) to bound numerical error for PDE/FFT kernels ([CMU papers](https://users.ece.cmu.edu/~franzf/papers/2025_HPEC_Oschatz_Q.pdf), 2025).
- **Property-Based Testing (PBT)** loops for codegen ([Property-Generated Solver](https://arxiv.org/html/2506.18315v1), Jun 2025).
- **Agentic formal verification** for GPU kernels ([ProofWright](https://arxiv.org/html/2511.12294v1), Nov 2025).

### Why it matters

Undergrad EE needs **invariants** (per-unit consistency, limit satisfaction, energy balance) more than Lean proofs. PBT and golden oracles are the practical middle ground.

### Implication for Arc

- **Adopt:** Hypothesis/property tests on engine outputs (e.g., λ–P dual feasibility, equal-area segment boundaries).
- **Defer:** SPIRAL-scale formal pipelines unless Arc sells safety-critical design automation.

---

## 5. Self-improving and evolutionary agents

### What it is

- **AlphaEvolve:** LLM + evolutionary search + **user evaluators** ([blog](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/), [arXiv:2506.13131](https://arxiv.org/abs/2506.13131), Jun 2025).
- **Darwin Gödel Machine:** self-modifying coding agent validated on SWE-bench / Polyglot ([Sakana](https://sakana.ai/dgm/), [arXiv:2505.22954](https://arxiv.org/html/2505.22954v2), May 2025).
- **AI Scientist-v2:** autonomous ML experiments + peer review ([arXiv:2504.08066](https://arxiv.org/html/2504.08066), Apr 2025; [Sakana publication note](https://sakana.ai/ai-scientist-first-publication/), 12 Mar 2025).

### Why it matters

These systems **do not** trust the base model; they trust **repeatable scoring**. Arc can evolve skills/recipes against trap fitness without letting the agent rewrite PSA core unsupervised.

### Implication for Arc

- **Adopt:** Offline **evolution of YAML recipes/skills** against golden+trap fitness (AlphaEvolve-shaped, bounded scope).
- **Cut:** Autonomous self-modification of verified engine code without human gate.
- **Change:** Document lineage of golden changes (DGM-style archive) for auditability.

---

## 6. Long-horizon autonomy, memory, and harness ownership

### What it is

- Claude Sonnet 4.5: **30+ hour** multi-step coding sessions; context editing + memory tool in API ([Anthropic announcement](https://www.anthropic.com/news/claude-sonnet-4-5), 29 Sep 2025).
- GPT-5: long agentic tool chains, τ²-bench telecom 96.7% ([OpenAI for developers](https://openai.com/index/introducing-gpt-5-for-developers/), 7 Aug 2025).
- Industry pattern: **rent the harness** (Cursor, Claude Code, Codex) — aligned with Arc `research/notes/agentic-kernel-2026.md`.

### Why it matters

Long context reduces need for Arc to **re-teach** generic persistence patterns; it increases need for **stable domain state** (case JSON, lab parameters) the host can reload.

### Implication for Arc

- **Cut:** Building long-horizon memory/RAG over entire EE corpora as default attach.
- **Adopt:** Small **durable case files** + goldens per lab; let host handle conversation memory.
- **Change:** Skills should encode **what must not drift** (f0, Pm, fault type) across long sessions.

---

## 7. RAG vs fine-tune vs RLVR for vertical domains

### What it is

| Approach | 2025–2026 role | Evidence |
|----------|----------------|----------|
| **RAG** | Connectors + Apps SDK / MCP data planes | OpenAI Apps on MCP, Oct 2025 |
| **Fine-tune / distill** | Cheap specialists from R1-class teachers | [DeepSeek-R1](https://arxiv.org/abs/2501.12948v1), Jan 2025; MIT license |
| **RLVR** | Post-train on rule checkers (math, code tests) | [arXiv:2506.14245](https://arxiv.org/abs/2506.14245); [Reasoning Gym](https://proceedings.neurips.cc/paper_files/paper/2025/hash/528d56195a2c77c808494c86fa7c77ad-Abstract-Datasets_and_Benchmarks_Track.html), NeurIPS 2025 |
| **Imperfect verifiers** | De-bias FN/FP in rule rewards | [arXiv:2510.00915](https://arxiv.org/abs/2510.00915), Oct 2025 |

### Why it matters

Harvey-style verticals win on **retrieval goldens + expert rubrics**, not secret base models. EE labs are **RLVR-shaped** (numeric oracle + procedure rules) — Arc already has the verifier.

### Implication for Arc

- **Adopt:** **RLVR environment** framing for traps/goldens; optional GRPO-style training on open distill models for *routing*, not physics.
- **Cut/slim:** Large EE textbook RAG as prerequisite for labs (frontier models + skills cover most prose).
- **Change:** If fine-tuning, target **tool selection / trap awareness**, not Kirchhoff solving.

---

## 8. Eval methodology: contamination, rubrics, traps, ablations, pass^k

### What it is

- **Contamination-resistant coding evals:** LiveCodeBench time-tags problems post model cutoff ([ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/94074dd5a072d28ff75a76dabed43767-Abstract-Conference.html)).
- **Agent reliability:** pass^⌝k vs pass@k — [τ-bench](https://proceedings.iclr.cc/paper_files/paper/2025/file/1b126cc38b8638e07bef37e7b2bb72bf-Paper-Conference.pdf); [Anthropic agent evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), 9 Jan 2026.
- **Capability vs regression suites; deterministic graders; reference solutions** — same Anthropic post.
- **Vertical rubrics:** Harvey expert golden queries, auto-graders, A/B preference, Arena Elo ([Harvey](https://www.harvey.ai/blog/scaling-ai-evaluation-through-expertise), 22 May 2025; [Arena](https://www.harvey.ai/blog/introducing-biglaw-bench-arena), 7 Nov 2025).

### Arc alignment

Arc already runs **trap ablation** and goldens (`docs/DOMAIN_KERNEL_CAPABILITIES.md`). Gap vs frontier practice: publish **pass^k**, versioned hold-out traps, and contamination-aware release notes for eval JSON.

### Implication for Arc

- **Adopt:** Report pass^1, pass^8 on trap suite alongside bare-agent baseline.
- **Adopt:** **Held-out trap variants** (parameter scrub) not in skills.
- **Change:** Date-stamp golden artifacts; freeze “regression” vs “capability” eval suites per Anthropic taxonomy.

---

## 9. How vertical agent companies prove beats over generalists

### Pattern (Harvey as canonical public example)

1. **Domain retrieval goldens** (precision/recall vs expert doc sets).
2. **Rubric auto-graders** with expert-written criteria.
3. **Blind A/B and pairwise Arena** vs foundation models and humans ([Arena blog](https://www.harvey.ai/blog/introducing-biglaw-bench-arena), 7 Nov 2025).
4. **Workflow-level claims** (drafting, chronology) with lawyer preference — [Harvey Agents](https://www.harvey.ai/blog/introducing-harvey-agents) (date on page not verified in this slice).

### Arc translation

Arc's published **177° δ_cr error** vs bare agent on T1 (`docs/DOMAIN_KERNEL_CAPABILITIES.md`) is the same *class* of proof as Harvey's arena — deterministic, domain-oracle based. To match 2026 bar, add **multi-trial pass^k** and **blind** presentation.

### Implication for Arc

- **Adopt:** Public “Arc vs bare host” arena on **new** lab sheets (not in repo skills).
- **Cut:** Marketing claims tied only to SWE-bench-like proxies.

---

## 10. What frontier generalists do out of the box (Nov 2026 snapshot)

Synthesis from primary vendor pages (not independent EE lab runs on Arc sheets — **those EE-specific head-to-heads are unverified in this document**).

| Capability | Representative evidence | Arc relevance |
|------------|-------------------------|---------------|
| Long agentic coding, SWE-bench 72–77% class | [Claude Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5), 29 Sep 2025; [GPT-5 dev](https://openai.com/index/introducing-gpt-5-for-developers/), 7 Aug 2025 | Repo editing, MATLAB/Python scaffolding |
| Tool orchestration / MCP ecosystems | [Apps SDK](https://openai.com/index/introducing-apps-in-chatgpt/), Oct 2025; [MCP Registry](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/), Sep 2025 | Plug-in simulators |
| Math/code RLVR reasoning | [DeepSeek-R1](https://arxiv.org/abs/2501.12948v1), Jan 2025 | Generic derivations |
| Weak research SciCode | [SciCode](https://scicode-bench.github.io/) | Domain sim + law |
| Policy-following agents still &lt;50% τ-bench; low pass^8 | [τ-bench PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/1b126cc38b8638e07bef37e7b2bb72bf-Paper-Conference.pdf) | Lab **policy** (solver bans, signs) |

---

## Capabilities generalists now have (cut or slim in Arc)

1. **Generic multi-file coding, debugging, and refactoring** at SWE-bench-class quality — slim Arc “how to code” skills; rely on host ([Anthropic Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5), 29 Sep 2025).
2. **MCP/tool plumbing and discovery** — cut custom connector sprawl; use registry + thin Arc MCP ([MCP Registry](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/), 8 Sep 2025).
3. **Host-native skills/rules/plugins** — slim duplicate procedural markdown not specific to EE law ([Claude Code skills](https://code.claude.com/docs/en/skills/); [Cursor rules](https://cursor.com/docs/context/rules)).
4. **Long-horizon session persistence** in frontier APIs — slim Arc-built chat memory; keep case JSON ([Anthropic Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5)).
5. **Open-web / textbook-level EE prose** and standard derivations — slim large always-on RAG corpora unless citation to licensed sources is required (**EE prose uplift unverified on Arc benchmarks**).
6. **Visual studio / agent builder UIs** — cut; OpenAI itself winds down visual Agent Builder toward SDK ([AgentKit post](https://openai.com/index/introducing-agentkit/), update 3 Jun 2026).
7. **Basic numerical coding for toy problems** — slim tutorial nodes; SciCode shows models still fail research tasks but may pass course demos ([SciCode](https://scicode-bench.github.io/)).
8. **Single-turn “please solve this lab” without tools** — cut as product path; reliability requires pass^k with tools ([Anthropic evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), 9 Jan 2026).

---

## Moats that still hold for a verified domain kernel

1. **Deterministic engines with lab-law encodings** (which curve, which sign, which limit) — evidenced by Arc T1–T10 ablation story in `docs/DOMAIN_KERNEL_CAPABILITIES.md` (repo primary).
2. **Trap catalog as executable policy** — structurally similar to τ-bench domain rules + pass^⌝k gap for GPT-4o-class agents ([τ-bench](https://proceedings.iclr.cc/paper_files/paper/2025/file/1b126cc38b8638e07bef37e7b2bb72bf-Paper-Conference.pdf), ICLR 2025).
3. **Golden JSON + integration tests as RLVR oracle** — aligned with RLVR / Reasoning Gym / AlphaEvolve evaluator pattern ([RLVR](https://arxiv.org/abs/2506.14245); [Reasoning Gym](https://proceedings.neurips.cc/paper_files/paper/2025/hash/528d56195a2c77c808494c86fa7c77ad-Abstract-Datasets_and_Benchmarks_Track.html)).
4. **Simulator-in-the-loop** (ngspice, PSA, dispatch) where models lack SciCode-level fidelity ([SciCode](https://scicode-bench.github.io/); [HAL](https://hal.cs.princeton.edu/scicode)).
5. **Held-out trap variants + pass^k reporting** — vertical proof standard per Harvey + Anthropic ([Harvey Arena](https://www.harvey.ai/blog/introducing-biglaw-bench-arena), 7 Nov 2025; [Anthropic evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), 9 Jan 2026).
6. **Explicit `unchecked` semantics** when oracle missing — trust boundary generalists don't standardize (**Arc design primary**).
7. **Cross-host attach** (skills + MCP + CLI) without owning the loop — 2026 consensus ([Anthropic skills/MCP](https://claude.com/resources/articles/extending-claude-capabilities-with-skills-mcp-servers), 18 Dec 2025; `research/notes/agentic-kernel-2026.md`).
8. **Recipe/YAML DAG with no-bypass writes to engines** — executive-kernel pattern; keep gates in code, not skills alone.

---

## Unverified / needs Arc-local measurement

- Exact **pass^k** of Claude Sonnet 4.5 / GPT-5 on **Arc goldens** (no public primary source found).
- Whether frontier models **without** Arc engines now pass EEC301 traps at high rate — contradicts Arc ablation doc but **not re-run in this research task**.
- OpenAI AgentKit long-term roadmap after Jun 2026 wind-down — only vendor note on [AgentKit page](https://openai.com/index/introducing-agentkit/).
- EE-specific formal verification at production scale — academic prototypes only ([SPIRAL 2025 PDFs](https://users.ece.cmu.edu/~franzf/papers/2025_HPEC_Oschatz_Q.pdf)).

---

## Sources (primary; retrieved unless noted)

| ID | Title | URL | Date / version |
|----|-------|-----|----------------|
| S1 | Extending Claude's capabilities with skills and MCP | https://claude.com/resources/articles/extending-claude-capabilities-with-skills-mcp-servers | Updated 18 Dec 2025 |
| S2 | Skills explained (vs MCP, etc.) | https://claude.com/resources/articles/skills-explained | 2025 (undated) |
| S3 | Agent Skills (Claude API) | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | Living doc |
| S4 | Scaling AI agents — MCP & Skills in AAIF | https://opensource.googleblog.com/2026/11/scaling-ai-agents-open-standards-mcp-aaif.html | Nov 2026 |
| S5 | Introducing the MCP Registry (preview) | https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/ | 8 Sep 2025 |
| S6 | MCP Registry about | https://modelcontextprotocol.io/registry/about | Living doc |
| S7 | Build with Agent Skills (MCP dev skills) | https://modelcontextprotocol.io/docs/2025-11-25/develop/build-with-agent-skills | 25 Nov 2025 |
| S8 | Claude Code — Plugins overview | https://code.claude.com/docs/en/plugins/overview | Living doc |
| S9 | Claude Code — Hooks guide | https://code.claude.com/docs/en/hooks-guide/ | Living doc |
| S10 | Cursor — Rules | https://cursor.com/docs/context/rules | Living doc |
| S11 | Introducing AgentKit | https://openai.com/index/introducing-agentkit/ | 6 Oct 2025 (update 3 Jun 2026) |
| S12 | Introducing apps in ChatGPT / Apps SDK | https://openai.com/index/introducing-apps-in-chatgpt/ | 6 Oct 2025 |
| S13 | OpenAI Agents SDK | https://developers.openai.com/api/docs/guides/agents/sdk | Living doc |
| S14 | Introducing GPT-5 | https://openai.com/index/introducing-gpt-5/ | 7 Aug 2025 |
| S15 | Introducing GPT-5 for developers | https://openai.com/index/introducing-gpt-5-for-developers/ | 7 Aug 2025 |
| S16 | Introducing Claude Sonnet 4.5 | https://www.anthropic.com/news/claude-sonnet-4-5 | 29 Sep 2025 |
| S17 | Building effective agents | https://www.anthropic.com/research/building-effective-agents | Dec 2024 |
| S18 | Demystifying evals for AI agents | https://www.anthropic.com/research/demystifying-evals-for-ai-agents | 9 Jan 2026 |
| S19 | DeepSeek-R1 (arXiv) | https://arxiv.org/abs/2501.12948v1 | 22 Jan 2025 |
| S20 | DeepSeek-R1 release | https://www.deepseek.com/en/news/deepseek-r1/ | 20 Jan 2025 |
| S21 | RLVR incentivizes reasoning (arXiv) | https://arxiv.org/abs/2506.14245 | Jun 2025 |
| S22 | RISE — RLVR + self-verification (NeurIPS) | https://proceedings.neurips.cc/paper_files/paper/2025/file/bd3d106d8e9789ce4fd40e1edafe71d5-Paper-Conference.pdf | 2025 |
| S23 | RLVR under imperfect verifiers (arXiv) | https://arxiv.org/abs/2510.00915 | 1 Oct 2025 |
| S24 | Reasoning Gym (NeurIPS) | https://proceedings.neurips.cc/paper_files/paper/2025/hash/528d56195a2c77c808494c86fa7c77ad-Abstract-Datasets_and_Benchmarks_Track.html | 2025 |
| S25 | τ-bench (ICLR) | https://proceedings.iclr.cc/paper_files/paper/2025/file/1b126cc38b8638e07bef37e7b2bb72bf-Paper-Conference.pdf | ICLR 2025 |
| S26 | LiveCodeBench (ICLR abstract) | https://proceedings.iclr.cc/paper_files/paper/2025/hash/94074dd5a072d28ff75a76dabed43767-Abstract-Conference.html | ICLR 2025 |
| S27 | LiveCodeBench (arXiv) | https://arxiv.org/abs/2403.07974 | Mar 2024 |
| S28 | SWE-PRM (arXiv) | https://arxiv.org/abs/2509.02360 | Sep 2025 |
| S29 | GUI-Shepherd PRM (arXiv HTML) | https://arxiv.org/html/2509.23738 | 2025 |
| S30 | AlphaEvolve blog | https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/ | 14 May 2025 |
| S31 | AlphaEvolve (arXiv) | https://arxiv.org/abs/2506.13131 | 16 Jun 2025 |
| S32 | Darwin Gödel Machine | https://sakana.ai/dgm/ | 30 May 2025 |
| S33 | DGM (arXiv) | https://arxiv.org/html/2505.22954v2 | May 2025 |
| S34 | AI Scientist-v2 (arXiv) | https://arxiv.org/html/2504.08066 | Apr 2025 |
| S35 | AI Scientist first publication | https://sakana.ai/ai-scientist-first-publication/ | 12 Mar 2025 |
| S36 | SciCode benchmark | https://scicode-bench.github.io/ | 2024–2025 |
| S37 | HAL SciCode leaderboard | https://hal.cs.princeton.edu/scicode | Accessed Nov 2026 |
| S38 | Gemini 2.5 technical report (arXiv) | https://arxiv.org/html/2507.06261v2 | Jul 2025 |
| S39 | Gemini thinking update (blog) | https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-model-thinking-updates-march-2025/ | Mar 2025 |
| S40 | Harvey — Scaling AI Evaluation | https://www.harvey.ai/blog/scaling-ai-evaluation-through-expertise | 22 May 2025 |
| S41 | Harvey — BigLaw Bench Arena | https://www.harvey.ai/blog/introducing-biglaw-bench-arena | 7 Nov 2025 |
| S42 | Harvey — Introducing Agents | https://www.harvey.ai/blog/introducing-harvey-agents | Living (date not verified) |
| S43 | SPIRAL verification of LLM scientific code (PDF) | https://users.ece.cmu.edu/~franzf/papers/2025_HPEC_Oschatz_Q.pdf | 2025 |
| S44 | Semantics lifting FFT (PDF) | https://users.ece.cmu.edu/~franzf/papers/2025_TPSA_Lifting.pdf | 2025 |
| S45 | Property-Generated Solver (arXiv) | https://arxiv.org/html/2506.18315v1 | Jun 2025 |
| S46 | ProofWright (arXiv) | https://arxiv.org/html/2511.12294v1 | Nov 2025 |
| S47 | Arc domain kernel capabilities (repo) | `docs/DOMAIN_KERNEL_CAPABILITIES.md` | Repo primary |
| S48 | Arc agentic kernel note (repo) | `research/notes/agentic-kernel-2026.md` | Repo primary |

---

**Confidence:** High on ecosystem/eval trends (multiple vendor + peer-reviewed sources). Medium on exact “what to cut” weighting until Arc re-measures pass^k on current frontier models against T1–T10 hold-outs.

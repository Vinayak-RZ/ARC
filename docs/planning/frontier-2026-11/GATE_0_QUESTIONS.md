# Gate 0 questions (Arc frontier upgrade, Nov 2026)

Research for this plan is **complete** (five reports under `docs/research/frontier-2026-11/`, merged to `main`). **Gate 0 is ANSWERED** (Vinayak, 2026-11-13): all recommended defaults for must-answer 1 to 10, trade-offs T1 to T5, and optional 11 to 15.

**Owner addendum (same date):** Arc Visual Kit is a **first-class capability**, not UI polish. See research `05-visual-components-for-agents.md` and graph node **B11**.

Execution may begin after plan merge; this PR updates the plan only.

---

## Must-answer (blocks graph execution)

1. **Proof bar:** What is the minimum public evidence to claim "frontier" in 2026?
   - **Recommended default:** Publish LIVE host A/B on **8 held-out** lab sheets (not in repo skills), **pass^8 ≥ 0.75** with Arc vs **≤ 0.15** bare host on the same models, plus regression suite green on T1 to T10 scripted traps.
   - **Override:** Name a lower bar only if timeline is fixed.

2. **Benchmark scope:** Which external benchmarks are in-bound for Arc v1 frontier release?
   - **Recommended default (P0):** Arc trap ablation + PSA CI, ControlEval ASR subset (≤50 tasks), ControlBench tool-augmented subset (frequency + design, ~40 items), EPRI-style open-ended **mirror** (50 SME items we license or reconstruct), CIRCUIT L1 to L3 with ngspice oracle (100 items).
   - **Recommended default (P1):** EEE-Bench power/control/PE tags (~200 items), EEBench optional.

3. **Host models for LIVE A/B:** Which hosts and models are authoritative for the public scorecard?
   - **Recommended default:** Cursor Composer 2.5 + Claude Sonnet 4.5 + GPT-5 (API) on the **same** held-out sheets; store prompts and transcripts under `artifacts/frontier-ab/`.
   - **Trade-off:** More models = credibility; higher cost and flake.

4. **MATLAB provider:** Is MathWorks MCP a **shipped default** or optional extra?
   - **Recommended default:** Optional `engines` extra only; OSS path must score ≥95% on P0 goldens without MATLAB; Arc never mints MATLAB scalars without EE engine recompute (per FR20).

5. **Multimodal depth:** What is the first multimodal capability we ship beyond photo stub?
   - **Recommended default:** `ingest-figure` for **control block diagrams** and **lumped schematics** (16/24 UI cap) with human confirm, then SPICE or `python-control` verify; not full SLD protection in v1 frontier.

6. **Tutoring mode:** Is certified Socratic tutoring P0 or P1?
   - **Recommended default P1:** Ship proof kernel first; tutoring uses host Socratic policy + Arc numerics oracle, no fine-tune in v1 frontier.

7. **Public benchmark artifact:** Do we release a downloadable **EEE-Coursework-Trap** dataset (prompts + goldens, no copyrighted sheets)?
   - **Recommended default:** Yes, versioned under `artifacts/benchmarks/eee-coursework-trap/v0.1/` with license-clean reconstructions only.

8. **Commit budget for execution phase:** Hard conventional commit count after plan approval?
   - **Recommended default:** **36** commits (matches EEC301 lift floor culture; graph maps 34 node-owned rows + 2 lead integration).

9. **Non-goals lock:** Confirm these stay out of frontier v1?
   - **Recommended default:** H5 Python orchestrator, HTTP MCP, hosted keys, PyPI publish, industrial EMS, tape-out, live PLC, graduate optimal control as public promise.

10. **Supersedes:** Does this plan supersede `docs/planning/eec301-lift/` execution or only extend it?
    - **Recommended default:** **Extend** EEC301 lift artifacts; close eec301-lift `PROGRESS.md` as "merged to main"; frontier graph owns net-new work.

---

## Trade-off (pick PRIORITY if both valid)

### T1: Breadth vs depth across packs

**Option A:** Depth-first: power PSA trilogy + control frequency + circuits SPICE to lab grade; other packs stay homework + `unchecked` honesty.
- Pros: Provable frontier wedge fast; matches audit scorecard (PSA 5/5, others 2 to 3).
- Cons: Marketing "10 packs" story stays uneven.

**Option B:** Breadth-first: one thin gold per pack before deepening.
- Pros: Curriculum-map law looks complete in eval CLI.
- Cons: Dilutes proof; repeats shallow CANNOT_DO rows.

**Default if you skip:** **Option A** because **PRIORITY = QUALITY** (Harvey-style vertical proof beats catalog width).

### T2: Live A/B cost vs scripted regression

**Option A:** LIVE host runs in CI nightly (API spend cap).
- Pros: Credible 2026 eval bar; matches report #03 Harvey arena pattern.
- Cons: Flaky, expensive, needs secrets.

**Option B:** Scripted wrong-model regression only in CI; LIVE A/B quarterly manual.
- Pros: Cheap, stable CI.
- Cons: Weak "beats bare agent" claim vs MathWorks Copilot marketing.

**Default if you skip:** **Option A** with **nightly budget cap** ($50/day) because **PRIORITY = QUALITY**.

### T3: RAG corpus scale

**Option A:** Slim RAG: BYO ingest only, 4 eval retrievals + citation skill.
- Pros: Aligns report #03 cut list; frontier models cover prose.
- Cons: Weaker "cite your textbook page" demo.

**Option B:** Ship 500-page license-clean EE primer in repo for RAG demo.
- Pros: Vertical pack story like Claude Life Sciences connectors.
- Cons: Maintenance, copyright risk, distracts from engines.

**Default if you skip:** **Option A** because **PRIORITY = SIMPLICITY**.

### T4: UI investment for frontier proof

**Option A:** Minimal UI: eval scorecard page + arena transcript viewer.
- Pros: Small surface; proof in CLI + JSON.
- Cons: Less demo sizzle.

**Option B:** Impeccable-style proof dashboard (leaderboards, A/B replay).
- Pros: GTM artifact; Mobbin-quality demo.
- Cons: Weeks of UI work; not kernel moat.

**Default if you skip:** **Option A** for v1 frontier; **Option B** as P1 if fundraising demo date exists.

### T5: RLVR / fine-tune

**Option A:** Package goldens as open **environment** only (Gym-style); no weight training.
- Pros: Matches moat thesis (oracle not model).
- Cons: No "Arc-tuned router" story.

**Option B:** Fine-tune small router on trap awareness (tool selection only).
- Pros: Routing gains on held-out traps.
- Cons: Ops burden, model drift, contradicts "deterministic kernel" simplicity.

**Default if you skip:** **Option A** because **PRIORITY = CONSISTENCY**.

---

## Optional (defaults stated)

11. **PyPI / install friction:** Keep git-clone primary?
    - **Default:** Yes (`CD-PYPI` stays).

12. **Specialist spawn count:** Keep ≤2 pack specialists?
    - **Default:** Yes (ARCHITECTURE D20).

13. **ANDES / MATPOWER providers:** Add as optional providers in frontier v1?
    - **Default:** ANDES behind `engines` extra for one OPF gold; not P0.

14. **Protection SLD:** Research-only in frontier v1?
    - **Default:** Yes; one toy `protection_study` gold only.

15. **Arena blinding:** Human preference study on Arc vs bare?
    - **Default:** P1; 20 item pilot with EE instructor rubric.

---

## Locked answers (2026-11-13)

| # | Answer |
|---|--------|
| 1 | Held-out 8 sheets; pass^8 ≥0.75 Arc vs ≤0.15 bare; T1 to T10 regression green |
| 2 | P0 benches per defaults; P1 EEE-Bench/EEBench optional |
| 3 | Composer 2.5, Sonnet 4.5, GPT-5; artifacts under `artifacts/frontier-ab/` |
| 4 | MATLAB optional `engines` extra; OSS ≥95% P0 goldens |
| 5 | `ingest-figure` for control blocks + lumped schematics (16/24 cap) |
| 6 | Tutoring P1 |
| 7 | Public `eee-coursework-trap v0.1` |
| 8 | 36 conventional commits (B11 visual rows may coalesce into wave 3) |
| 9 | Non-goals list unchanged |
| 10 | Extend eec301-lift; frontier graph owns net-new |
| T1 | Depth-first (QUALITY) |
| T2 | LIVE AB nightly, $50/day cap (QUALITY) |
| T3 | Slim RAG/BYO (SIMPLICITY) |
| T4 | **Override:** U1 + **B11 Arc Visual Kit** are P0 presentation proof (owner addendum); not minimal-only UI |
| T5 | RLVR env only (CONSISTENCY) |
| 11 to 15 | All defaults |
| **Visual Kit** | Engine-bound props; registry + MCP; visual goldens in CI; textbook/IITR parity review |

## Approval record

| Field | Value |
|-------|-------|
| Gate 0 research | Complete 2026-11-13; report #05 added same day |
| Owner sign-off | **Vinayak, 2026-11-13** (all defaults + Visual Kit addendum) |
| Execution | **Blocked until plan PR merged** (owner kickoff) |

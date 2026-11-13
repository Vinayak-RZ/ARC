# Arc internal capability audit (Nov 2026)

**Audit date:** 2026-11-13  
**Repo snapshot:** `main` @ `d7c33ea` (merge of PR [#43](https://github.com/Vinayak-RZ/ARC/pull/43) `cursor/eec301-system-lift-b2f6`, merged 2026-09-22)  
**Scope:** Audited **`main` only** — EEC-301 lift is on `main`; the feature branch was not re-audited separately.

**Commands run (this audit):**

```text
uv sync --extra dev --extra engines
uv run ruff check .                                    → All checks passed
uv run pytest -q                                       → 232 passed, 2 warnings, ~10.7s
uv run python scripts/check_psa_evals.py               → 16 passed (~1.1s)
uv run electrical-engineer eval --pack <pack>            → see §3 and scorecard
```

---

## One-page summary

Arc today is a **clone-and-run undergraduate EE co-solver**: Python 3.11+ CLI (`electrical-engineer`), YAML DAG runner, stdio MCP, localhost UI (`127.0.0.1:8765`), pack skills, and a capability registry documented in [`docs/ARCHITECTURE.md`](../../ARCHITECTURE.md). Product identity is honest about boundaries via [`docs/CANNOT_DO.md`](../../CANNOT_DO.md) (27 rows). The **strongest verified wedge** is the **EEC-301 PSA kernel** on `main`: SMIB equal-area / CCT (`src/electrical_engineer/engines/smib_swing.py`), two-area AGC (`agc_two_area.py`), λ-ED with limits (`ed_lambda.py`), lab JSON in `artifacts/eec301-lab-goldens/exp06–08.json`, trap knowledge `knowledge/traps/T1–T10`, skills `skills/swing-equation/`, `skills/agc-two-area/`, `skills/economic-dispatch-lambda/`, and **scripted** bare-vs-Arc checks in `tests/integration/test_trap_ablation.py` (δ_cr **79.5324°** vs bare wrong path **~256°**; CCT time **0.309716 s**; ED **P₂=150 MW** at PD=500). CI enforces this via `.github/workflows/ci.yml` + `scripts/check_psa_evals.py`.

Everything else is **breadth over depth**: 10 curriculum packs (`docs/curriculum-map.md`), **31** workflow YAMLs (`src/electrical_engineer/catalog.py`), **12** host specialist cards (`hosts/agents/INDEX.md`), **448** UG note files under `knowledge/ug-ee/`, and **232** pytest tests. Default **recipe-path** providers are real but thin: ngspice (`engines/spice_runner.py`), python-control (`control_runner.py`), pandapower 3-bus template (`power_runner.py`), plus study toys for protection/drives/digital. **Gold eval** (`electrical-engineer eval`) passes **11 recipe-scored items** across circuits, control, signals, machines, RAG, explain, unmatched, injection; **power PSA gold folders exist but are not wired** to the eval runner (`eval/gold/power/*-eec301-01/expect.json` lack `recipe_id` → `KeyError` in `eval_runner/score.py`). PSA proof is therefore **unit tests + ablation**, not the public eval CLI.

**A/B evidence** is **reproducible and narrow**: three traps (T1, T2, T6) are automated; T3–T5, T7–T10 are narrative/knowledge (`docs/planning/eec301-lift/AB_REVIEW_NARRATIVE.md`). The “bare agent” baseline in tests is a **hand-authored wrong model** (`_bare_t1_wrong_delta_cr()` in `test_trap_ablation.py`), not a live LLM run — strong for regression, weak as agentic eval. PSA engines are **not on the workflow graph** (`workflows/power/solve-power-problem.yaml` uses `run-load-flow` + `check-numeric`, not `smib_swing`).

**Quality risks:** doc drift (README “27 recipes” vs 31 catalog ids; `eval/gold/README.md` stale; `hosts/agents/INDEX.md` still says 27); `check-numeric` remains a small hand-solved seam (`nodes/sim.py`); RAG is tested (14 unit tests) but not CI-gated as a heavy engine; MATLAB/Simulink paths are optional stubs. **Frontier upgrade** should **double down** on PSA + eval integration + live-agent trap eval, and **cut or freeze** surface that advertises depth without gold (duplicate host narrative, orphan planning branches, eval items that never run).

---

## 1. Capability map by EE area

Depth key: **toy** (formula demo), **homework** (structured problem), **lab** (lab-sheet parity / golden JSON), **professional** (not claimed; see CANNOT_DO).

| Area | Engines / providers | Skills / knowledge | Evals / tests | Depth | Verified numbers (examples) |
|------|---------------------|--------------------|---------------|-------|-----------------------------|
| **Circuits** | `run-spice` → `engines/spice_runner.py`; graph/netlist `circuit/` | `skills/circuits/SKILL.md`, `skills/_cross/` | Gold: `eval/gold/circuits/divider-dc-01/`; integ: `tests/integration/test_circuits_wf.py`, `test_simulate_circuit.py` | **homework** (divider); SPICE path **lab-capable** if ngspice present | **Vout = 5.0** (`eval/gold/circuits/divider-dc-01/expect.json`); photo fixture `eval/gold/circuits/photo-stub-01/` has **no** `expect.json` |
| **Signals** | `check-numeric` / scipy via `nodes/sim.py` | `skills/signals/SKILL.md` | Gold: `eval/gold/signals/lti-path-01/`; `tests/integration/test_signals_wf.py` | **homework** | LTI path scored via recipe; hole **CD-SIGNALS-MATLAB** in skills |
| **Control** | `run-python-control` → `control_runner.py`; `block_diagram.py`; `control/diagram.py` | `skills/control/SKILL.md`, `skills/ui-diagrams/` | Gold: `block-feedback-01`, `digital-pole-01`; `tests/unit/test_control_diagram.py` | **homework / lab-lite** | Eval PASS via `control-diagram-to-model`, `solve-digital-control-problem` |
| **Power / PSA** | **Lab:** `smib_swing.py`, `agc_two_area.py`, `ed_lambda.py`, `eec301_goldens.py`; **Study:** `power_runner.py` (pandapower) | PSA skills + `knowledge/traps/*`; pack `skills/power/SKILL.md` | Gold JSON: `artifacts/eec301-lab-goldens/`; eval dirs `smib/agc/ed-eec301-01` (**not CLI-runnable**); `scripts/check_psa_evals.py`; unit: `tests/unit/test_smib_*.py`, `test_agc_*.py`, `test_ed_*.py`; ablation: `tests/integration/test_trap_ablation.py` | **lab** (PSA); **toy/homework** (load flow/fault YAML) | δ_cr **79.532410°**, t_to_δ_cr **0.309716 s**, CCT **0.309688 s** (`exp06.json`); Δf **−0.16 Hz**, ΔP₁₂ **−45.07 MW** (`exp07.json`); PD=500 → **P₂=150**, λ **≈7.392308** (`exp08.json`) |
| **Protection** | `protection_study.py` | `skills/power/SKILL.md` + workflow `study-protection-setting.yaml` | Gold: `eval/gold/power/protection-oc-01/` (not run in this audit’s partial eval) | **toy** | OC pickup arithmetic, not relay coordination CAD |
| **Machines / drives** | `drives_study.py` (DC steady-state) | `skills/machines/SKILL.md` | Gold: `machines/dc-drive-speed-01` PASS; `tests/integration/test_machines_wf.py` | **toy** | Drive speed from V, R_a, k, T_load |
| **Power electronics** | `converter-model` → mostly `check-numeric` | `skills/power_electronics/SKILL.md` | WF tests only: `tests/integration/test_power_electronics_wf.py` | **homework** (algebra); **CD-PE-HIL** | No dedicated gold item |
| **Electronics** | `algebraic-check` + optional SPICE | `skills/electronics/SKILL.md` | `tests/integration/test_electronics_wf.py` | **homework** | **CD-ELEC-PDK** |
| **EM** | `fields-analytic` → `check-numeric` | `skills/em/SKILL.md` | `tests/integration/test_em_wf.py` | **homework** | **CD-EM-HFSS** |
| **Digital (within control pack)** | `digital_control.py` | control skill | `digital-pole-01` gold | **homework** | Pole plot / ZOH discretization |
| **Measurements** | `measurement-model` | `skills/measurements/SKILL.md` | `tests/integration/test_measurements_wf.py` | **homework** | **CD-MEAS-BENCH** |
| **Maths** | `algebraic-check` | `skills/maths/SKILL.md` | `tests/integration/test_maths_wf.py` | **homework** | **CD-MATHS-CAS** |
| **Cross / unmatched** | retrieve + `label-unverified` | `skills/_cross/`, `workflows/_cross/unmatched-cosolver.yaml` | `unmatched/open-ended-01` PASS; adversarial: `tests/integration/test_adversarial_host_prompts.py` | **homework** | Forces `unchecked` on open prompts |

**Pack coverage law** is enforced in code: `tests/unit/test_pack_coverage.py` ↔ `docs/CANNOT_DO.md` ↔ `skills/*/SKILL.md`.

---

## 2. Architecture

| Layer | What exists today | Key paths |
|-------|-------------------|-----------|
| **L0 Host** | Cursor / Claude Code / Codex / ChatGPT desktop adapters; spawn ≤2 specialists | `hosts/adapters/`, `hosts/agents/INDEX.md`, `docs/hosts/*.md` |
| **L1 Attach** | CLI `electrical-engineer`; MCP stdio; pack skills | `src/electrical_engineer/cli.py`, `mcp/server.py`, `.cursor/mcp.json`, `skills/` |
| **L2 Kernel** | YAML runner, capability registry, gates, RAG facade, memory, eval runner | `src/electrical_engineer/runner/`, `catalog.py`, `gates.toml`, `rag/`, `eval_runner/score.py` |
| **L3 Surfaces** | FastAPI UI + React canvas | `src/electrical_engineer/ui_server/app.py`, `ui/` |
| **Domain engines** | Typed Python (PSA + runners) | `src/electrical_engineer/engines/` (11 modules) |
| **Workflows** | 31 checked-in DAGs | `workflows/<pack>/*.yaml` |
| **Knowledge** | Traps + UG corpus (not RAG-only) | `knowledge/traps/`, `knowledge/ug-ee/` (448 markdown files) |
| **Install path** | `uv sync --extra dev --extra engines`; `npm run build --prefix ui`; `electrical-engineer hosts install` | `README.md`, `pyproject.toml`, `ui/package.json` |
| **CI** | ruff + full pytest + PSA script | `.github/workflows/ci.yml` |

**MCP tools (product):** `list_workflows`, `retrieve`, `open_ui`, `simulate_attachment`, `propose_composition`, label/summary, run helpers — `src/electrical_engineer/mcp/server.py`. **MATLAB** optional via `matlab_mcp.py` (not on default MCP surface).

**RAG:** LightRAG-style spike behind facade; 4 gold retrieval tasks under `eval/gold/rag-retrieval/`; unit suite `tests/unit/test_rag_*.py` (14 passed). Ontology contract: `docs/planning/RAG_ONTOLOGY_CONTRACT.json`. IITR trials documented in `docs/planning/IITR_RAG_TRIALS.md` — not all paths CI-required per `CANNOT_DO`.

**Authority docs:** `docs/PID.md`, `docs/PRD.md`, `docs/ARCHITECTURE.md` (D19/D20 overlay). Execution graph notes H1 complete on branch `cursor/ee-product-execution-9e9d` per `AGENTS.md` (may be ahead of this snapshot).

---

## 3. Proof: A/B, traps, reproducibility

| Claim | Evidence | Reproducibility | Weakness |
|-------|----------|-----------------|----------|
| T1 δ_cr | `test_ablation_t1_arc_beats_bare_on_delta_cr` | `pytest tests/integration/test_trap_ablation.py` | Bare side is **scripted** wrong physics, not LLM |
| T2 CCT timing | `test_ablation_t2_time_to_dcr_matches_json` | Same + `exp06.json` | RK4 step `h=1e-5`; not host-invoked |
| T6 ED limits | `test_ablation_t6_ed_limit_case` | Same + `exp08.json` | Single demand point PD=500 |
| T3–T5, T7–T10 | `knowledge/traps/`, skills | Manual / narrative | No automated pass/fail |
| PSA unit parity | `tests/unit/test_smib_swing.py` (+ integrator sweep vs `exp06.json`) | `check_psa_evals.py` | Engines disconnected from YAML power recipes |
| Eval CLI product proof | `electrical-engineer eval --pack circuits` etc. | 11/11 recipe golds PASS in isolation | **Crashes** on power pack when hitting `agc-eec301-01` (`KeyError: 'recipe_id'`) |
| Kernel harden trials | `scripts/kernel_harden/`, `artifacts/kernel-harden/` | Scenario bank + optional drivers | Separate from PSA ablation; not in default CI |

**Trap catalog source of truth:** `docs/planning/eec301-lift/TRAP_CATALOG.md`. **Runnable narrative:** `docs/planning/eec301-lift/AB_REVIEW_RUNNABLE.md`. **Prompt stubs:** `proofs/ablation/trap_prompts.yaml`.

**Contamination risk:** Gold numbers are **in-repo JSON** (`artifacts/eec301-lab-goldens/`) derived from lab sheets (`docs/planning/eec301-lift/EEC301_EXP6_GOLDEN.md`) — models can memorize paths; mitigations for frontier: held-out cases, live agent eval, no gold in prompt context.

---

## 4. Quality issues (honest)

| Issue | Severity | Paths |
|-------|----------|-------|
| PSA engines off workflow/MCP DAG | High for product story | `workflows/power/solve-power-problem.yaml`, `nodes/sim.py` (no `smib`/`agc`/`ed` activities) |
| Eval runner vs PSA gold schema split | High | `eval_runner/score.py` vs `eval/gold/power/smib-eec301-01/expect.json` |
| `electrical-engineer eval` / `eval --pack power` broken on PSA items | High | Observed 2026-11-13 on `main` |
| Marketing / index drift | Medium | `README.md` (27 recipes), `hosts/agents/INDEX.md`, `eval/gold/README.md` vs `catalog.py` (31) |
| `check-numeric` thin seam | Medium | `nodes/sim.py` — not full CAS for arbitrary EE |
| `photo-stub-01` gold incomplete | Low | `eval/gold/circuits/photo-stub-01/` missing `expect.json` |
| `ui-diagrams` eval pack empty | Low | `eval --pack ui-diagrams` → 0/0 |
| Planning doc stale branch refs | Low | `docs/planning/eec301-lift/PROGRESS.md` |
| Many planning branches on remote, not product | Low | `git branch -r` (research/agentic overlays) |
| Solve-explain mint risk | Medium (documented) | `docs/PRD.md` FR9 — gold must not score LLM numerics |

**Impressive but thin:** 10 packs × 7 genres **documented** (`ARCHITECTURE.md` §0); **18** gold items vs hundreds of corpus notes; pandapower template vs real campus models; protection/drives study functions vs settings engineering.

---

## 5. Candidate cuts vs double-downs

### Candidate cuts (maintenance ≫ proof value)

- Freeze or archive **remote-only planning branches** not merged to `main` unless actively executing a graph (reduce confusion in audit/CI narratives) — see `origin/cursor/*` list in git.
- Stop extending **31 workflows** without matching `eval/gold` rows (`CD-YAML-GAP` discipline).
- De-emphasize **screenshot/trial PNG galleries** under `docs/media/trials/` for CI — keep README subset only.
- Do not invest in **duplicate** unlock prose until eval CLI runs PSA gold (`DOMAIN_KERNEL_CAPABILITIES.md` vs broken `eval --pack power`).
- **`solve-explain` on power recipes** without engine hook — yields unchecked + narrative, not PSA proof.

### Candidate double-downs (uniquely strong)

- **EEC-301 PSA trilogy** + trap catalog T1–T10 — only place with lab-grade verified numbers and ablation story (`engines/`, `artifacts/eec301-lab-goldens/`, `knowledge/traps/`).
- **`scripts/check_psa_evals.py` + `test_trap_ablation.py`** — extend to T4–T5 (AGC) live deltas already in unit tests.
- **Capability registry + `unchecked` law** — `docs/ARCHITECTURE.md`, `tests/unit/test_pack_coverage.py`, injection gold `flip-gates-01`.
- **Host install + MCP ACI** — low-friction attach path `.cursor/mcp.json`, `electrical-engineer hosts install`.
- **RAG eval quartet** — `eval/gold/rag-retrieval/` (4/4 PASS); expand with held-out chapters before scaling ingest.
- **Wire PSA into runner** — new activities or `eval` engine mode so product CLI proves what CI proves.

---

## Scorecard (Nov 2026, `main`)

| Dimension | Score (0–5) | Evidence (this audit) |
|-----------|-------------|------------------------|
| PSA / transient stability kernel | **5** | `smib_swing.py`, `exp06.json`, ablation T1–T2, 232 pytest green |
| Power systems study (flow/fault) | **2** | `power_runner.py`, `lg-01`/`ll-01` gold exists; eval pack **broken** on PSA folders |
| Circuits (SPICE) | **3** | ngspice CI; divider gold PASS; integration tests |
| Control & digital | **3** | 2 eval golds PASS; python-control runner |
| Signals / EM / electronics / PE | **2** | WF integration tests; CANNOT_DO holes; sparse gold |
| Machines & drives | **2** | 1 drive gold PASS; FEA explicitly out |
| Protection | **2** | Toy engine + gold on disk; not re-run in eval sweep |
| RAG / knowledge | **3** | 4/4 eval; 448 ug-ee notes; 14 unit tests |
| Host + MCP productization | **4** | MCP server, 12 agent cards, adapters |
| Local UI | **3** | FastAPI + Vite; diagram trials in docs/media |
| Eval harness integrity | **2** | 11 recipe golds PASS; PSA gold **orphaned**; full `eval` crashes |
| A/B agentic proof | **2** | Strong regression; not live-agent |
| CI health | **5** | `ruff` clean; **232** pytest; PSA gate **16** tests |
| Doc truth vs tree | **3** | ARCHITECTURE/PID strong; README/recipe counts drift |

**Eval CLI summary (2026-11-13):**

| Pack | Result |
|------|--------|
| circuits | 1/1 PASS |
| control | 2/2 PASS |
| signals | 1/1 PASS |
| machines | 1/1 PASS |
| rag-retrieval | 4/4 PASS |
| explain | 1/1 PASS |
| unmatched | 1/1 PASS |
| injection | 1/1 PASS |
| power | **FAIL** (`KeyError: 'recipe_id'` on `agc-eec301-01`) |
| ui-diagrams | 0/0 (no scored items) |
| Full `electrical-engineer eval` | **6 PASS then crash** (same KeyError) |

---

## References

- Domain unlock story: [`docs/DOMAIN_KERNEL_CAPABILITIES.md`](../../DOMAIN_KERNEL_CAPABILITIES.md)
- EEC-301 merge: PR #43 → `d7c33ea`
- Trap catalog: [`docs/planning/eec301-lift/TRAP_CATALOG.md`](../../planning/eec301-lift/TRAP_CATALOG.md)
- Test log artifact: `/opt/cursor/artifacts/pytest-full.log` (232 passed)
- Eval logs: `/opt/cursor/artifacts/eval-packs.log`, `/opt/cursor/artifacts/eval-all.log`

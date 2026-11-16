# Arc independent test report

Last updated: 2026-11-16 (round 2)  
Branch: `cursor/independent-test-engineer-43f2`  
Base: `cursor/collab-loop-f29f`  
Role: independent test engineer (tests and tooling only; no `src/` or `ui/src` product edits)

## Executive summary (round 2)

| Metric | Value |
|--------|------:|
| Independent pytest functions (round 1+2) | 66 collected in this PR slice |
| Passing (with ngspice installed) | 61 |
| Skipped | 1 (`ARC_LIVE_UI` live SSE optional) |
| xfail strict (known product bugs) | 4 |
| Playwright full suite (local, UI up) | 38 passed, 13 failed, 5 did not run |
| Mutation testing (mutmut 2.5) | **No score** (0 files mutated; stats pass blocked by `test_scenario_bank` in global pytest) |
| Golden audit candidates | 70 paths (`/opt/cursor/artifacts/golden-audit.json`) |
| ngspice | Installed (`ngspice 42`); former 3 spice skips now run (2 xfails document bugs) |

Head SHA for this report: see latest push on `cursor/independent-test-engineer-43f2`.

### What we actually ran

```bash
sudo apt-get install -y ngspice
cd ui && npm install && npm run build
EE_NO_BROWSER=1 uv run electrical-engineer ui &
curl -sf http://127.0.0.1:8765/api/health
cd ui && STUDIO_URL=http://127.0.0.1:8765 npm run test:e2e   # full suite ~12.3m
uv run pytest -q tests/unit/test_*.py tests/integration/test_*independent* \
  tests/integration/test_collab_lab_semantics.py tests/integration/test_arc_lab_mcp_cli_contracts.py \
  tests/integration/test_four_sample_wiring.py tests/integration/test_sse_inprocess_ordering.py \
  tests/integration/test_live_sse_ordering.py
uv run python tests/tools/golden_audit.py
bash scripts/mutation/run_verify_path_mutmut.sh   # attempted; see mutation section
```

Artifacts: `playwright-full-suite.log`, `playwright-round2-summary.txt`, `golden-audit.json`, `mutmut-run.log` under `/opt/cursor/artifacts/`.

## Round 2 additions

| Area | New assets |
|------|------------|
| Live / in-process SSE | `tests/integration/test_live_sse_ordering.py`, `tests/integration/test_sse_inprocess_ordering.py` |
| Four sample wiring | `tests/integration/test_four_sample_wiring.py` (divider, rlc-step API, control workflow, rectifier + IDMT recipes) |
| Golden contamination | `tests/unit/test_golden_contamination.py`, `tests/tools/golden_audit.py` |
| Mutation kill-suite | `tests/unit/test_mutation_targets.py`, `mutmut.ini`, `scripts/mutation/run_verify_path_mutmut.sh` |
| Playwright | `independent-full-collab-loop.spec.ts` in `testMatch`; `ui/package-lock.json` updated for `@axe-core/playwright` |

## Capability coverage matrix (updated)

| Capability | Tested | Passing | Failing / xfail | Untested |
|------------|--------|---------|-----------------|----------|
| Lab meta, revisions, `op_log`, restore | Yes | Yes | | |
| MCP + CLI lab contracts | Yes | Yes | | |
| Verify-after-derive 2% edges | Yes | Yes | ARC-TE-003 documented | |
| Graph compile + ngspice (graph-only RLC tran) | Yes | | ARC-TE-006 xfail | |
| Derive netlist bypass on shorted graph | Yes | | ARC-TE-001 xfail | |
| Control lab mismatch (`y_ss` vs `y_final`) | Yes | | ARC-TE-005 xfail | |
| SSE live ordering | Yes | | ARC-TE-007 xfail | |
| SSE in-process (TestClient) | Yes | | ARC-TE-007 xfail | |
| Four examples E2E (API + workflows) | Yes | Yes | | |
| IDMT + rectifier solver recipes | Yes | Yes | ARC-TE-002 formula gap | UI hw3 vs Python |
| Golden perturbation (declared `value`) | Yes | Yes | | |
| Playwright collab loop spec | Yes | | 3/3 fail (studio circuit shell) | |
| Playwright full suite | Yes | 38 | 13 fail (mixed collab + studio URL bugs) | 5 not run |
| Mutation (compare_derived, netlist, IDMT, RLC) | Attempted | Partial (`test_mutation_targets` only) | mutmut blocked | cosmic-ray not run |

## Mutation testing

**Goal:** mutmut on `compare_derived`, `compile_netlist`, IDMT and RLC solvers.

**Result:** `mutmut run` with `mutmut.ini` reported **0 files mutated, 207 unmodified** on the first stats pass; a full-repo pytest runner used for statistics failed on `tests/unit/test_scenario_bank.py` import (`annotate_scenarios`). Surviving mutants were **not** enumerated.

**Mitigation in this PR:** `tests/unit/test_mutation_targets.py` (6 focused tests) targets branches in those modules. **Mutation score: N/A until** mutmut is configured with an isolated runner that only executes `test_mutation_targets.py` (or `test_scenario_bank` is fixed / excluded in CI stats).

**Better use of time vs full-repo mutmut right now:** extend `test_mutation_targets.py` after each P0 fix; or adopt `cosmic-ray` with an explicit `cosmic-ray.toml` test path list (not done in this pass).

## Playwright (real run)

- **Build:** `ui/npm run build` succeeded (Vite).
- **Server:** `electrical-engineer ui` on `127.0.0.1:8765` healthy.
- **Full suite:** 38 passed, 13 failed, 5 did not run (~12.3m). See `/opt/cursor/artifacts/playwright-round2-summary.txt`.
- **Collab-specific failures:** `collab-lab` and `independent-full-collab-loop` timeout on `.react-flow` or `.studio-circuit-app .cs-simulate-btn` / `.answer-num` (circuits lab shell with `?run=`).
- **Note:** Many failures are **pre-existing** studio/layout specs, not introduced by this PR.

## Golden audit

- Scanned 70 repo files where goldens and derive/simulate paths co-occur (`tests/tools/golden_audit.py`).
- **Known contamination pattern:** `seed-control-lab` copies upstream `value` / `y_ss` into `derived_value` without independent derive (`nodes/sim.py`).
- **Tests:** `test_circuit_derived_moves_when_declared_value_perturbed` proves `finish_circuit_lab` ignores bogus `problem["value"]` when derive succeeds; `test_injected_wrong_derived_*` flags injected wrong derive.
- **Script hazard:** `scripts/capture_collab_lab_screenshots.py` sets `summ["value"] = 11.963` (intentionally wrong Euler demo).

## Prioritized bug list (full)

### P0

**ARC-TE-001: Verify path simulates derive netlist, not drawn graph** (unchanged; `xfail` strict)

### P1

**ARC-TE-002:** Python `rectifier_3ph` vs UI hw3 discontinuous Vo (unchanged)

**ARC-TE-007: SSE `/api/runs/{id}/events` delivers no bytes to clients**

- **Repro:** `GET /events` with curl or httpx for 3s while `PUT /graph`.
- **Expected:** `data: {"type":"hello",...}` then `data: {"type":"graph","revision":N,...}`.
- **Actual:** HTTP 200 `text/event-stream`, **zero body** (see `/opt/cursor/artifacts/sse-stream-sample.txt`).
- **Suspect:** `src/electrical_engineer/collab/run_events.py` + `StreamingResponse` flush/`asyncio.to_thread` interaction.
- **Tests:** `test_live_sse_ordering` (optional `ARC_LIVE_UI=1`), `test_sse_delivers_graph_revisions_in_process` (`xfail strict`).

### P2

**ARC-TE-003:** `compare_derived(tol=)` absolute vs relative (unchanged)

**ARC-TE-004:** Learn API with empty `create_app(tmp_path)` (unchanged)

**ARC-TE-005: `finish_control_lab` reads `y_final`, simulate returns `y_ss`**

- **Repro:** `finish_control_lab(..., derived_value=wrong)` with unity golden.
- **Expected:** `mismatch=True` when `derived_value` off by 5.
- **Actual:** `simulated=None`, `mismatch=False`.
- **Suspect:** `collab/workflow.py` ~213-214 vs `control_studio/simulate.py` ~230.
- **Test:** `test_control_seed_derived_mismatch_when_derived_value_perturbed` (`xfail strict`).

**ARC-TE-006: Graph-only RLC tran peak wrong without UIC `.tran` in compiled netlist**

- **Repro:** `simulate_graph(series_rlc_graph(), {analysis: tran, ...})` without `problem["cir"]`.
- **Expected:** Vc peak ~11.63 V.
- **Actual:** ngspice returns ~10 V (DC-like).
- **Suspect:** `circuit/netlist.py` (compile only `.end`); tran setup in `spice_runner` when `cir` omitted.
- **Test:** `test_graph_only_simulation_matches_derived_rlc_peak` (`xfail strict`).

**ARC-TE-008 (e2e): Open run in studio circuits lab does not expose simulate results**

- **Repro:** Playwright `/?view=studio&tab=circuits&run={rlc-step run_id}`, click simulate.
- **Expected:** `.studio-circuit-results .answer-num` visible.
- **Actual:** timeout 45s (3 viewports).
- **Suspect:** collab branch UI routing / circuit shell (not modified in this PR).

## Is any of this pointless right now?

**Full Playwright regression (13 failures):** Low signal until collab branch stabilizes studio URLs (`studioUrl&tab=control` invalid URL) and `?run=` circuit studio shell. **Better:** gate CI on `collab-lab` + `independent-full-collab-loop` + `circuit-sandbox` only.

**Repo-wide mutmut:** Blocked and noisy on this tree. **Better:** module-scoped cosmic-ray or mutmut with runner = `pytest tests/unit/test_mutation_targets.py` only after fixing scenario_bank collection.

**Live SSE test with second server:** Redundant once ARC-TE-007 is fixed; keep in-process test only.

## Commands (CI parity)

```bash
uv sync --extra dev --extra engines --extra control
sudo apt-get install -y ngspice   # match .github/workflows/ci.yml
cd ui && npm ci && npm run build
uv run pytest -q tests/unit/test_independent_golden_numerics.py \
  tests/unit/test_graph_netlist_fidelity.py tests/unit/test_verify_after_derive_edges.py \
  tests/integration/test_collab_lab_semantics.py tests/integration/test_arc_lab_mcp_cli_contracts.py \
  tests/integration/test_independent_robustness.py tests/integration/test_independent_capability_smoke.py \
  tests/unit/test_mutation_targets.py tests/unit/test_golden_contamination.py \
  tests/integration/test_four_sample_wiring.py tests/integration/test_sse_inprocess_ordering.py
# optional: ARC_LIVE_UI=1 pytest tests/integration/test_live_sse_ordering.py
```
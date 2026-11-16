# Arc independent test report

Last run: 2026-11-16  
Branch: `cursor/independent-test-engineer-43f2`  
Base: `cursor/collab-loop-f29f`  
Role: independent test engineer (tests and fixtures only; no `src/` or `ui/src` product edits)

## Summary

| Metric | Value |
|--------|------:|
| New test modules | 8 Python + 1 Playwright spec |
| New test functions (pytest) | 47 |
| Passing (new suite) | 44 |
| Skipped (ngspice absent) | 3 |
| xfail strict (known bugs) | 1 |
| Playwright cases | 3 viewport/theme rows |

Commands:

```bash
uv sync --extra dev --extra engines --extra control
uv run pytest -q \
  tests/unit/test_independent_golden_numerics.py \
  tests/unit/test_graph_netlist_fidelity.py \
  tests/unit/test_verify_after_derive_edges.py \
  tests/integration/test_collab_lab_semantics.py \
  tests/integration/test_arc_lab_mcp_cli_contracts.py \
  tests/integration/test_independent_robustness.py \
  tests/integration/test_independent_capability_smoke.py
cd ui && npm ci && npm run test:e2e -- e2e/independent-full-collab-loop.spec.ts
```

## Capability coverage matrix

| Capability | Tested | Passing | Failing / xfail | Untested |
|------------|--------|---------|-----------------|----------|
| Lab model (`lab_meta.json`, revision, `op_log`, `actor_label`, restore) | Yes | Yes | | |
| MCP `arc_circuit_lab_*` + `arc_lab_finish_control` schemas | Yes | Yes | | Control finish not exercised end-to-end here |
| CLI `electrical-engineer lab get\|finish\|simulate\|open` | Yes | Yes | | |
| API `GET /api/runs/{id}/lab`, `POST .../lab/restore` | Yes | Yes | | |
| SSE `/api/runs/{id}/events` | Partial | Yes (publish + route wiring) | Live stream ordering not blocked in CI | Full ordering under load |
| Verify-after-derive (`needs_review` > 2%) | Yes | Yes | | |
| Circuit graph compile + ngspice simulate | Yes | Yes when ngspice present | ARC-TE-001 xfail | |
| Graph vs derive-netlist fidelity on shorts | Yes | xfail | ARC-TE-001 | |
| Control Studio goldens (unity K=10) | Yes | Yes | | Bode/locus/margins not re-goldened here |
| Rectifier hw3 closed form | Yes | Yes | | UI lab only; Python `rectifier_3ph` differs topology |
| IDMT IEC standard | Yes | Yes | | |
| Series RLC headline goldens | Yes | Yes | | |
| Problems / gallery / learn APIs | Yes | Yes | | Full Playwright learn/gallery |
| Web-verify node | Yes | Yes | | Citation workflow not replayed |
| Circuit sandbox | Existing + collab e2e | | | Dedicated sandbox fuzz |
| Playwright full collab loop | New spec | Pending CI / local UI | | |

## Prioritized bug list

### P0

**ARC-TE-001: Verify-after-derive simulates derive netlist, not compiled graph**

- **Repro**
  1. Seed headline series RLC lab via `finish_circuit_lab`.
  2. Append graph edge `vin.n1` → `c1.n2` (parallel short).
  3. Call `simulate_graph(graph, problem)` **without** `problem["cir"]`.
  4. Call `finish_circuit_lab` with the same shorted graph still seeded from problem.
- **Expected:** Simulated peak disagrees with analytic 11.630 V; `mismatch` / `needs_review`.
- **Actual:** `finish_circuit_lab` merges `derived["cir"]` into `sim_prob` (`collab/workflow.py` ~74; `circuit/simulate_graph.py` ~21-24), so ngspice runs the correct template netlist while the drawn graph is shorted.
- **Suspect:** `src/electrical_engineer/circuit/simulate_graph.py:21-24`, `src/electrical_engineer/collab/workflow.py:72-75`
- **Test:** `tests/unit/test_graph_netlist_fidelity.py::test_shorted_drawn_graph_must_not_match_analytic_peak` (`xfail strict=True`)

### P1

**ARC-TE-002: Python `rectifier_3ph` half-wave formula does not match hw3 discontinuous R-load lab**

- **Repro:** Compare `electrical_engineer.engines.solvers.power_electronics.rectifier_3ph(..., topology="half")` at 415 V, α=45° to UI `voClosedForm` hw3 discontinuous (203.7 V).
- **Expected:** Same Vo within 0.5 V for the teaching case.
- **Actual:** Python uses continuous `cos(α)` form (`power_electronics.py` ~69-70); UI uses `(3Vm/2π)(1+cos(α+30°))` when discontinuous.
- **Suspect:** `src/electrical_engineer/engines/solvers/power_electronics.py:69-70` vs `ui/src/studio-engine/labs/rectifier.js:54-60` (UI not modified by this PR)

### P2

**ARC-TE-003: `compare_derived(tol=0.02)` treats tol as absolute volts, not relative fraction**

- **Repro:** `compare_derived(100, 102, tol=0.02)` → mismatch; `compare_derived(100, 102, rel_tol=0.02)` → match.
- **Expected:** Documented `tol` on problems is relative (per PRD collab loop).
- **Actual:** `compare_derived` uses `tol` as absolute margin when set (`simulate_graph.py` ~63).
- **Suspect:** `src/electrical_engineer/circuit/simulate_graph.py:53-64`

**ARC-TE-004: Learn curriculum API returns empty shape when `create_app(tmp_path)` without repo learn files**

- **Repro:** `TestClient(create_app(tmp_path)).get("/api/learn/curriculum")` from empty tmp cwd.
- **Expected:** Stable payload or explicit error.
- **Actual:** Depends on `curriculum_payload(root)` with non-repo root.
- **Suspect:** `src/electrical_engineer/ui_server/learn_routes.py:96-99`

## Files added (test-only)

- `tests/golden_numerics_refs.py`
- `tests/__init__.py`
- `tests/unit/test_independent_golden_numerics.py`
- `tests/unit/test_graph_netlist_fidelity.py`
- `tests/unit/test_verify_after_derive_edges.py`
- `tests/integration/test_collab_lab_semantics.py`
- `tests/integration/test_arc_lab_mcp_cli_contracts.py`
- `tests/integration/test_independent_robustness.py`
- `tests/integration/test_independent_capability_smoke.py`
- `ui/e2e/independent-full-collab-loop.spec.ts`
- `pyproject.toml` (hypothesis in dev extra)
- `ui/package.json` (`@axe-core/playwright` devDependency)

## CI note

Ensure `ngspice` is on `PATH` in CI for spice-dependent tests (existing collab suite + new graph fidelity tests). Skips apply locally when simulator is missing.
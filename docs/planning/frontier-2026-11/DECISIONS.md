# Frontier upgrade decisions (Gate 0, 2026-11-13)

Locked answers from [GATE_0_QUESTIONS.md](GATE_0_QUESTIONS.md). Execution agents treat this as `capability_delta_spec`.

## Proof bar

- LIVE host A/B on **8 held-out** lab sheets, **pass^8 ≥ 0.75** Arc vs **≤ 0.15** bare host.
- Regression: T1 to T10 scripted traps stay green in CI.
- Models: Cursor Composer 2.5, Claude Sonnet 4.5, GPT-5 (API).

## Benchmark scope (P0)

Arc trap ablation + PSA CI, ControlEval subset (≤50), ControlBench subset (~40), EPRI-style mirror (50), CIRCUIT L1 to L3 with ngspice (100). P1: EEE-Bench tags, EEBench optional.

## Providers and multimodal

- MATLAB: optional `engines` extra only; OSS path must score ≥95% on P0 goldens.
- Multimodal v1: `ingest-figure` for control block diagrams and lumped schematics (16/24 UI cap), human confirm, then SPICE or python-control verify.

## Product scope

- Tutoring: **P1** (host Socratic + Arc numerics oracle).
- Public **EEE-Coursework-Trap** dataset v0.1 under `artifacts/benchmarks/`.
- **36** conventional commits after plan merge (coalesce allowed per PLAN §9).
- Non-goals: H5 orchestrator, HTTP MCP, hosted keys, PyPI, industrial EMS, tape-out, live PLC, graduate optimal control as public promise.
- Supersedes: **extends** EEC301 lift; frontier graph owns net-new work.

## Owner addendum

- **C1** repo cleanup in wave 2b (audit #04).
- **B11** Arc Visual Kit first-class (engine-sourced numbers, registry, visual goldens).
- **D2** terminal node: full README + authority docs after trials.

## Trade-offs (defaults)

| ID | Choice | Priority |
|----|--------|----------|
| T1 | Depth-first PSA + control + circuits | QUALITY |
| T2 | LIVE A/B nightly with $50/day cap | QUALITY |
| T3 | Slim BYO RAG only | SIMPLICITY |
| T4 | Minimal UI scorecard + transcript (B11 visuals for demo) | QUALITY via B11 |
| T5 | RLVR environment package only, no weight training | SIMPLICITY |

## Eval schema v2

Gold `expect.json` may be:

1. **Recipe mode:** `recipe_id` + optional numeric / unchecked / citations.
2. **Retrieval mode:** `mode: retrieval` + citations / faithfulness.
3. **Engine mode:** `schema: arc.eval.expect.v2` + `engine` key (`smib_swing`, `agc_two_area`, `ed_lambda`) for PSA CLI proof.

Implemented in `src/electrical_engineer/eval_runner/score.py` and `psa_score.py`.

# A/B review — runnable dramatic deltas (T1, T2, T6)

Harness: `tests/integration/test_trap_ablation.py` · prompts: `proofs/ablation/trap_prompts.yaml`.

## T1 — Wrong Pmax equal-area

| Path | δ_cr (deg) |
|------|------------|
| Bare (single Pmax=1.5) | ≈ 90+ (wrong) |
| Arc `critical_clearing_angle` | **79.5324** (exp06.json) |

**Unlock:** stage-aware formula + skill — not “slightly better RK4”.

## T2 — CCT / solver cheat

| Path | Outcome |
|------|---------|
| Bare | ode45 / off-grid tc → invalid lab procedure |
| Arc | `time_to_angle_during_fault` h=1e−5 → **0.309716 s**; bisection golden **0.309688 s** |

## T6 — ED limits ignored

| Path | P2 @ PD=500 |
|------|-------------|
| Bare unconstrained | >150 MW |
| Arc `solve_lambda_ed` | **150 MW**, IC2<λ |

Run: `uv run --extra dev pytest tests/integration/test_trap_ablation.py -q`

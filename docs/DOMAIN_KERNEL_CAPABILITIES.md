# Domain kernel capabilities (Arc)

Audience: you installed Arc next to Cursor or Claude and want to know what changes
compared to a **general coding agent alone**.

## What a domain kernel is

A general harness can edit files and call tools. It does not, by itself, know which
**stage** of a power-angle curve applies, which **sign** the tie flow uses in ACE,
or when a λ-ED unit is **at max**. A domain kernel adds named recipes, checked
engines, trap knowledge, and golden JSON so answers are either **verified** or
labeled `unchecked`. The chat loop stays generic; the kernel carries the lab law.

## What a bare agent still gets wrong

Typical confident failures on undergraduate power-systems labs (see trap catalog T1–T10):

- **Equal-area / CCT (SMIB):** one `Pmax` for every segment, or bolted-fault math when the sheet gives `Pmax_fault = 0.5 pu`. δ_cr can be off by **tens of degrees**.
- **CCT procedure:** `ode45` when the lab forbids it; clearing time not aligned to the RK step grid; reporting δ_cr as if it were time.
- **Two-area AGC:** `ACE = B·Δf − ΔP12` with the wrong sign; `B = 1/R` without damping; expecting AGC to erase the **first** frequency dip.
- **Economic dispatch:** ignoring `Pmax`; λ solved once with no limit loop; `IC = b + cP` (missing the factor of 2).
- **Diagrams:** pretty block diagrams with droop on the wrong block.
- **Defaults:** `Pm = 1`, `f0 = 60` in an Exp 6 sheet that specifies `Pm = 0.9`, `f0 = 50`.

## What Arc unlocks (checked numbers)

These come from `artifacts/eec301-lab-goldens/` and `tests/integration/test_trap_ablation.py`.

| Trap | Bare-style mistake | Arc (engine + traps) | Delta (order of) |
|------|-------------------|----------------------|------------------|
| **T1** | Wrong during-fault model for δ_cr | **79.5324°** (`critical_clearing_angle`, Exp 6) | Ablation wrong path ≈ **256.6°** (≈177° error) |
| **T2** | Solver / grid cheat | During-fault time to δ_cr **0.309716 s** (RK4, h = 1×10⁻⁵); bisection golden **0.309688 s** | Procedure-valid CCT, not a hand-waved table |
| **T6** | No limits at PD = 500 MW | **P2 = 150 MW** at max, **λ ≈ 7.3923**, **IC2 = 7.30 < λ** | Unconstrained dispatch would exceed 150 MW |
| **T4–T5** | ACE / primary vs AGC confusion | Primary **Δf ≈ −0.16 Hz**, **ΔP12 ≈ −45.07 MW**; AGC restores **Δf → 0**, **~100 MW** in Area 1 | `agc_two_area` + `exp07.json` |
| **T7–T10** | IC units, forbidden solvers, silent defaults | `incremental_cost`, skills, `validate_smib_case` | Knowledge + regression tests |

Arc is not “a better RK4 tutorial.” It encodes **which curve, which sign, which limit** the lab grader checks.

## Prove it yourself

```bash
uv sync --extra dev --extra engines
uv run ruff check .
uv run python scripts/check_psa_evals.py
uv run --extra dev pytest tests/integration/test_trap_ablation.py -q
```

Optional deeper reads (planning appendix, not required for the story above):

- [`docs/planning/eec301-lift/AB_REVIEW_RUNNABLE.md`](planning/eec301-lift/AB_REVIEW_RUNNABLE.md)
- [`docs/planning/eec301-lift/AB_REVIEW_NARRATIVE.md`](planning/eec301-lift/AB_REVIEW_NARRATIVE.md)
- [`docs/planning/eec301-lift/LAB_FEEDS_KERNEL.md`](planning/eec301-lift/LAB_FEEDS_KERNEL.md)

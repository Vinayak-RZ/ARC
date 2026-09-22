# T5 — Primary vs secondary (AGC) dynamics (Exp 7)

**Bare-agent failures:** Expect AGC to remove the **first dip**; claim governors
zero steady Δf with K=0; ignore that integral AGC recenters frequency slowly.

**Lab truth:**

| Run | Steady Δf1 | Steady ΔP12 | Steady Pm1 |
|-----|------------|-------------|------------|
| Primary | ≈ −0.16 Hz | ≈ −45 MW | ≈ 53 MW |
| AGC K=0.3 | ≈ 0 | ≈ 0 | ≈ 100 MW |

First dip still ≈ −0.41 Hz under AGC (`run2_agc.first_dip`).

**Arc path:** `simulate_two_area(..., run="primary"|"agc")` + this trap note.

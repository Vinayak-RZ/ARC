# T7 — IC factor 2 / fuel units (Exp 8)

**Bare-agent failures:** `IC = b + c P` (missing 2); minimize `Σ b P` only; mix
Rs/hr totals with Rs/MWh λ.

**Correct:** `IC = b + 2 c P`. Constants `a_i` affect cost totals, not λ on free set.

**Arc path:** `incremental_cost()` in `ed_lambda.py`; skill `economic-dispatch-lambda`.

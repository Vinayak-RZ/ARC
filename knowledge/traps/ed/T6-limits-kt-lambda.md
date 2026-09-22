# T6 — ED limits / KT / λ update (Exp 8)

**Bare-agent failures:** Ignore limits; PD=500 with P2>150; fix unit at max but
keep old λ; assert IC=λ always at bounds.

**Lab truth (PD=500):** P2=150 at max, λ≈7.3923, **IC2=7.30 < λ**.

**Arc path:** `solve_lambda_ed()` iterative free-set update; goldens in `exp08.json`.

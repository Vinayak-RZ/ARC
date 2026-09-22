# T4 — ACE / bias B ≠ β; tie sign (Exp 7)

See `docs/planning/eec301-lift/BARE_AGENT_FAILURE_NOTES.md` §T4.

**Bare-agent failures:** `ACE1 = B1Δf1 − ΔP12` (wrong sign); `B = 1/R` only; tie
integrator missing factor 2; Area 2 tie injection same sign as Area 1.

**Arc path:** `skills/agc-two-area/SKILL.md`, `engines/agc_two_area.py` ACE/tie signs.

**Goldens:** primary Δf = −0.160 Hz, ΔP12 = −45.07 MW (`exp07.json`).

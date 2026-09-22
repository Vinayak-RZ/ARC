# Trap catalog — EEC-301 lift (proof must hit)

| ID | Domain | Bare-agent failure | Arc unlock |
|----|--------|-------------------|------------|
| T1 | SMIB | Wrong Pmax for δ_cr / equal-area | swing-equation skill + `smib_swing` equal-area |
| T2 | SMIB | CCT clearing model / step off-by-one | CCT bisection helper + eval |
| T3 | SMIB | H↔M / f vs ω base mixup | knowledge + unit guard |
| T4 | AGC | ACE form; B≠β; tie sign | agc skill + parity notes |
| T5 | AGC | Primary vs secondary dynamics confusion | scenario knowledge |
| T6 | ED | Ignore limits; broken KT / λ update | λ-ED skill + solver |
| T7 | ED | Wrong IC / fuel units | knowledge trap |
| T8 | Diagrams | Pretty wrong signal flow | ui-diagrams rules |
| T9 | Integration | “Just use ode45 / fmincon” when forbidden | skill constraints |
| T10 | Numeric | Silent wrong defaults (Pm, Pmax stages) | engine API validation |

**A/B DoD (landing PR):** narrative for all T1–T10; scripted fail/pass for at least **T1, T2, T6**; stretch to five scripted.

**W0–W2 scope:** traps **T1–T3** encoded as knowledge; engines/evals back T1–T2 numerics.

# High-quality EE diagram patterns (PSA / control lab)

Research synthesis for Arc `ui-diagrams` upgrades (W5). Sources: IITR visual
conventions (`docs/planning/DIAGRAM_IITR_VISUAL_CONVENTIONS.md`), classic LFC block
diagrams, and trap **T8** failure catalog.

## Principles

1. **Signal direction:** left-to-right time / causality; feedback arrows return to
   summing junctions, not across unrelated blocks.
2. **Summing junctions:** label `+` / `−` inputs; ACE enters governor path **before**
   turbine, not after tie-only paths.
3. **Two-area tie:** show `ΔP12` leaving Area 1 with minus into swing, plus into Area 2.
4. **Units on axes:** pu MW vs MW vs Hz — state which; `B` in pu MW/pu Hz.
5. **Lab report:** one figure per run (primary vs AGC); annotate load step time.

## PSA figure checklist

- [ ] Governor–turbine–generator chain per area
- [ ] Tie integrator `1/(2πT12)` or equivalent label matching PDF
- [ ] ACE integrator with gain `K`
- [ ] Load step arrow on correct area bus

Fold into `skills/ui-diagrams/SKILL.md` §PSA / power LFC.

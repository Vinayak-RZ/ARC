# RAG evaluation methodology (design only)

## Purpose

Design how we would know an EE textbook RAG system is helping — without setting product SLAs or writing a PRD.

## Findings

Claim | Evidence (URL) | Confidence
--- | --- | ---
Technical RAG papers evaluate with citation correctness and structured rubrics, not only BLEU-like scores | https://aclanthology.org/2026.rag4reports-1.4.pdf | high
Agentic systems should ship with golden tasks, edge cases, and adversarial prompts before user-facing behavior | `.cursor/skills/agentic-system-design/SKILL.md` | high
EE-specific failures differ from generic QA: formula variants, dropped assumptions, units, sign conventions | domain reasoning | high

### Eval layers

| Layer | Question | Method |
|-------|----------|--------|
| Retrieval | Did we fetch the right section/page? | Page/section gold labels; Recall@k |
| Faithfulness | Does the answer stick to retrieved text? | NLI / judge vs passages |
| Citation | Are page citations real? | Exact page match |
| EE correctness | Is the engineering content right? | Expert or verified numeric check |
| Harmful fluency | Confident wrong formula? | Adversarial variants |

### EE failure taxonomy

1. **Wrong formula variant** (e.g. peak vs RMS; line vs phase).
2. **Dropped assumption** (linearity, balanced three-phase, neglecting magnetizing branch).
3. **Unit slip** (pu vs SI; degrees vs radians).
4. **Sign / reference convention** (passive sign, current direction).
5. **Orphaned example** (solution without matching problem constraints).
6. **Fabricated citation** (page does not exist).

Pack × lane retrieval items (120 queries, curator-bound pages): [`rag-eval-pack-stack.md`](rag-eval-pack-stack.md). The titles below remain a cross-pack flavour list; they are not a substitute for that bank.

### Twenty candidate eval case *titles* (design sketches — not built)

1. Series RLC transient time constant identification
2. Thevenin equivalent with dependent source
3. Three-phase power factor correction sizing
4. Per-unit conversion across transformer boundary
5. Ybus assembly for a three-bus network
6. Newton-Raphson load flow first iteration residual
7. Symmetrical fault current at a bus
8. Equal-area criterion critical clearing angle
9. Transformer OC/SC test parameter extraction
10. Induction motor torque-speed point at given slip
11. Synchronous generator capability curve reading
12. Routh-Hurwitz stability for a quartic plant
13. Bode plot gain/phase margin from TF
14. Lead compensator design sketch from specs
15. Buck converter CCM voltage relation
16. SPWM inverter modulation index and fundamental
17. CT burden and ratio error conceptual check
18. Op-amp inverting amplifier with finite GBW caveat
19. Sampling theorem aliasing example
20. Adversarial: “simulate” a circuit but no tool allowed — must refuse numeric fabrication

### Explicitly not decided here

Pass thresholds, CI gating numbers, and product launch criteria wait for a later PRD phase.

## Open questions

- Human expert budget for EE-correctness labels vs MATLAB-verified subset only.
- Whether judge models can score formula equivalence reliably.

## Sources

- [RAG4Reports](https://aclanthology.org/2026.rag4reports-1.4.pdf) — retrieved 2026-09-07 — reliability: paper (S16)
- [agentic-system-design](.cursor/skills/agentic-system-design/SKILL.md) — retrieved 2026-09-07 — reliability: primary (S3)
- [GATE EE syllabus](https://static.collegedekho.com/media/uploads/2024/07/01/gate-_ee_2025_syllabus.pdf) — retrieved 2026-09-07 — reliability: secondary (S11)
- [rag-eval-pack-stack.md](rag-eval-pack-stack.md) — retrieved 2026-09-15 — reliability: primary

## Confidence

Overall confidence for this note: high

The failure taxonomy still holds. Pack-lane gold binds live in `rag-eval-pack-stack.md`; scoring automation quality remains medium uncertainty.

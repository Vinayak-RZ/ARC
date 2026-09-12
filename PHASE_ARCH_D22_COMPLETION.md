# PHASE_ARCH_D22_COMPLETION — Host-skip, glossary, viva axis

> **Historical completion log.** Host-skip, glossary, and viva axis are Accepted in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and [`docs/GLOSSARY.md`](docs/GLOSSARY.md).

## Completed work

Docs-only response to three critics: host non-compliance, terminology density, missing pedagogical signal. No product code.

## Files modified

- `docs/GLOSSARY.md` — contributor words; how vs why
- `docs/ARCHITECTURE.md` — readable preamble; When the host does not comply; eval two axes
- `docs/PRD.md` FR25/FR26; `docs/CANNOT_DO.md`; `eval/gold/README.md`; `skills/SKILL.md`; `docs/UI.md` empty-state
- ADR-0013; critique loop 7; vision-lock D22

## Architectural changes

Lab-checked means kernel Results. Chat freelance is outside the claim. Method checklist is a second eval axis and must not flip `unchecked`.

## Validation performed

`rg` for FR25, FR26, CD-HOST-SKIP, GLOSSARY, host-skip. No `.py`/`.jsx` in the diff.

## Known issues

- D22 Proposed, not Accepted; README unchanged
- `expect-viva.json` scorer and gold items wait on an eval code plan

## Next phase objectives

Owner Accept. Then code: UI empty-state, host-skip gold fixture, method checklist scorer.

## What you learned

- Prompting is not a sandbox; the honest design is a claim boundary plus CLI backstop
- Overlay ids belong in ADRs; architecture should start with how the lab works
- Viva quality needs its own axis or it stays an unmeasured slogan

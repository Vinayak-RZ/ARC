# India-first student GTM (P1)

## Purpose

Where undergraduate EE / EEE students would actually find **Electrical Engineer**, the lab — without turning GATE into the product or inventing a new name. Positioning pair is locked to `naming-and-positioning.md`: product Electrical Engineer, category lab.

## Findings

Claim | Evidence (URL or ledger ID) | Confidence
--- | --- | ---
The first users are students who **already have** Claude Code, Cursor, or Codex, plus the CLI-only path for those who do not | `docs/PID.md` Q-S / Q-S2; Claude Builder Club IIT Madras | high
Campus builder clubs on those hosts are a real India channel, not a fantasy: IIT Madras runs a Claude Builder Club with Claude Code workshops | https://claude-builder-clubiitm.vercel.app/ | high
GDG / GDSC-style campus orgs and coding clubs remain the default OSS on-ramp at Indian engineering colleges | DSC NIT Rourkela; Coding Club RVCE | med
GATE must not be the homepage. Curriculum bound is the union of UG programmes; GATE is an eval overlay | `docs/curriculum-map.md`; `docs/PID.md` Q7 | high
The demo artifact is already in-repo: divider gold `Vout = 5.0` via `electrical-engineer eval --pack circuits` | `eval/gold/circuits/divider-dc-01`; `README.md` | high
WhatsApp / Telegram batch groups are how many Indian UG students share tools; they are not a documented official channel we can “join as a brand” without spam | industry practice; no primary census | low
README copy is hygiene. Reach (host clubs, GitHub topics, one honest demo) moves the needle more than a slogan | github-growth-kit study is one category, n≈300, treat as weak prior | low

### Who we are talking to

Primary: UG electrical / EEE students, India first, including colleges without a MATLAB-fluent TA. Same cores globally. Self-learners on those cores. GATE/IES aspirants may use exam-style items; that does not make this a GATE app (`docs/PID.md`).

They already have language for the category: **electrical lab**. Pitch: the coding assistant you use for CS assignments can run an EE lab that checks numbers.

### Channels (do, in this order)

1. **Host-native clubs.** Claude Builder Club (IIT Madras exists; Anthropic lists many campuses). Cursor / Codex user groups. The lab is *for* those hosts. A 30-minute workshop: clone, `eval --pack circuits`, open `electrical-engineer ui`, run `solve-circuit-problem`.
2. **GitHub as the landing page.** H1 Electrical Engineer, subtitle lab, invariant `unchecked`, proof command. Topics once README is allowed to change: `electrical-engineering`, `ngspice`, `claude-code`, `education`. Not this phase.
3. **Campus GDG/GDSC and coding clubs** for install help and OSS norms (Git, uv, local CLI). EE departments are the *users*; CS clubs are often the *installers*.
4. **awesome-lists and agent-skill catalogs** once the one-liner is locked — discovery for people already collecting harness-native labs.
5. **CLI-only story** for students who will not pay for Cursor: spice/control/load-flow with no model; local OpenAI-compat when configured (`docs/ARCHITECTURE.md` §3).

### Channels (do not)

- GATE coaching funnels, Unacademy-style ads, “crack GATE with AI.” Eval overlay, not the bound.
- Faculty / LMS / “hide the answer for the professor.” PID: no faculty v1.
- Plant-floor LinkedIn (Eigen, PLC, protection actuation). Never this product.
- Star-chasing README theatre (CTAs, empty Discord, fake badges). Validator already rejects product-landing language on `README.md`.
- Pretending WhatsApp forwards are a GTM plan. If a student shares the repo in a batch group, that is luck plus a working divider demo — not a campaign we operate.

### Demo, not a viral video

OpenMontage shows a finished film. We show a **checked number**.

```text
uv run electrical-engineer eval --pack circuits
```

Gold: `eval/gold/circuits/divider-dc-01` expects `Vout = 5.0` from `Vin=10`, `R1=R2=1k`. A fluent wrong voltage presented as checked fails the product. That is the GTM proof. Secondary: localhost UI on `127.0.0.1` with the `unchecked` pill on an unmatched run.

### Copy that can travel (not applied to README)

One breath: Electrical Engineer is a lab for undergraduate electrical engineering. It runs on Claude Code, Codex, or Cursor, and as a local CLI. Numbers come from simulators, or they say `unchecked`.

India-first examples should stay licence-clean (Kuphaldt / BYO), not scanned GATE papers.

## Open questions

- Whether to list specific Claude Builder campuses beyond IIT Madras after a later outreach pass.
- Whether GitHub Student / Copilot Student pauses in 2026 change host mix (Copilot new student sign-ups were reported paused). Does not change Claude Code / Cursor / CLI as first-class.

## Sources

- [`research/notes/naming-and-positioning.md`](naming-and-positioning.md) — retrieved 2026-09-12 — reliability: primary
- [`docs/PID.md`](../../docs/PID.md) — retrieved 2026-09-12 — reliability: primary
- [`docs/curriculum-map.md`](../../docs/curriculum-map.md) — retrieved 2026-09-12 — reliability: primary
- [`eval/gold/circuits/divider-dc-01`](../../eval/gold/circuits/divider-dc-01) — retrieved 2026-09-12 — reliability: primary
- [Claude Builder Club IIT Madras](https://claude-builder-clubiitm.vercel.app/) — retrieved 2026-09-12 — reliability: primary
- [Claude Builder Club IIT Madras LinkedIn](https://in.linkedin.com/company/claude-builder-club-iit-madras) — retrieved 2026-09-12 — reliability: secondary
- [DSC NIT Rourkela](https://github.com/dscnitrourkela) — retrieved 2026-09-12 — reliability: secondary
- [Coding Club RVCE](https://github.com/codingclubrvce/codingclubrvce) — retrieved 2026-09-12 — reliability: secondary
- [GitHub Copilot plans (student pause note)](https://docs.github.com/en/copilot/get-started/plans) — retrieved 2026-09-12 — reliability: vendor
- [`research/notes/ai-core-engineering-landscape.md`](ai-core-engineering-landscape.md) — retrieved 2026-09-12 — reliability: primary

## Confidence

Overall confidence for this note: med

Host-club and curriculum claims are primary. Batch-chat distribution is widely believed and weakly evidenced. This note is GTM advice, not a campaign calendar.

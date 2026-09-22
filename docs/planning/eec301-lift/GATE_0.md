# GATE_0 — EEC-301 stress-test → Arc system lift (revised)

**Date:** 2026-09-22 (rev 2 — system-first, commit floor, dramatic A/B)  
**Profile:** nawab **project** + graph-of-loops  
**Commit floor:** **≥30 conventional commits on the landing Arc PR** (hard DoD; plan targets **36** so the floor cannot be missed by squash/skip)

## Priority order (locked)

1. **P0 — Arc system** skills, knowledge traps, engines/helpers, golden evals, host/pack cards, diagram skill, CI, A/B proof harness  
2. **P0 — Dramatic proof** documented examples where Arc unlocks correct work a bare coding agent fails or botches  
3. **P1 — Lab Exps 6–8** complete solutions used as the **learning stress-test** that discovers and feeds (1)–(2)  
4. **P2 — Optional** MATLAB `.m` mirrors, extra UI panels

Solving the experiments matters because they are how we **find** system gaps. The main deliverable people care about is a **better Arc**, with evidence.

## Locked answers

| # | Topic | Answer |
|---|--------|--------|
| Runtime | No Simulink; Exp6/8 Python primary; Exp7 OSS twin + Simulink parity notes |
| Delivery | Lab pack **separate**; Arc upgrades via **PRs** |
| Commits | Floor **≥30** on landing PR; planned **36** atomic conventional commits; no squash below floor |
| Books | High-value traps now; refine when textbooks arrive |
| Proof | ≥5 trap cases in A/B review (was 3); at least 3 with runnable checks |

## Success check

- Landing Arc PR has `git rev-list --count base..HEAD` **≥ 30**
- Arc evals green for trap suite
- A/B review shows **dramatic** capability delta (not “slightly nicer RK4”)
- Lab pack reproduces Exp6–8 expected tables within documented tolerance

# Commit floor — non-negotiable

## Rule

The **landing Arc PR** for this lift must contain **≥ 30** conventional commits relative to the merge base (`main` or agreed base).

If the work is split across PRs, **the primary system PR** still must meet ≥30, **or** the set of open PRs for this lift must collectively contain ≥30 unique commits that land (tracked in PROGRESS). Prefer **one fat system PR** with ≥30 commits so auditors can count once.

## Enforcement

1. Plan lists **36** named commits (cushion above 30).
2. Each wave exits only when its commit titles are present on the branch (`git log --oneline`).
3. Before “ready to merge,” run:

```bash
git fetch origin main
git rev-list --count origin/main..HEAD   # must be >= 30
git log --oneline origin/main..HEAD
```

4. **Forbidden:** squashing the PR to “clean history” if that drops below 30; combining unrelated commits to speed up; marking DoD while count < 30.
5. If a cloud agent batches work into fewer commits, **follow-up** must split or add atomic commits until floor is met (docs-only filler commits are **not** allowed — each commit must carry real skill/knowledge/engine/eval/lab-feed value).

## What counts

- Real conventional commits: `feat:`, `fix:`, `test:`, `docs:`, `skill:`, `knowledge:`, `chore:` with substance
- Lab pack lives outside Arc; lab commits do **not** count toward the Arc PR floor unless vendored into Arc (they should not be). Lab has its own local git history optional.

## Escalation

If approaching merge with <30: **do not merge**. Add remaining planned commits from the backlog in §6 of IMPLEMENTATION_PLAN (preferred) or expand eval/knowledge coverage — never pad with empty files.

# Learning log — Kernel harden graph

## Wave 0 — Plan authoring

- **Concept:** Graph-of-loops needs extensive per-node stops before product code.
- **Pattern:** Plan-harden checker (headings + linked stops) as a first gate.
- **Trade-off:** Up-front doc cost vs thrash later — paid once.

## Wave 1 — Trace / corpus / UI

- **Concept:** Domain-kernel observability is file JSONL, not APM.
- **Pattern:** `TraceWriter` in `wrap()` + UI excerpts.
- **Trade-off:** No OTel keeps deps zero; export adapter bridges Unagent.

## Wave 2 — Validate / boot

- **Concept:** Bind greps can false-positive on regex `.` (e.g. `1_000_000`).
- **Pattern:** Prefer `1000000` literals near security greps.
- **Trade-off:** Slight readability vs CI honesty.

## Wave 3 — Host corpus

- **Concept:** Volume reveals mislabeled reasons better than intuition.
- **Pattern:** 120 scenario JSON → trial_driver → CORPUS_INDEX.
- **Trade-off:** Thin problem fixtures → many honest `labeled` unchecked.

## Wave 4 — Critique / I1

- **Concept:** Observation enums are product surface area.
- **Pattern:** Add `labeled`; never use `unmatched` as generic fallback.
- **Trade-off:** Enum growth vs lying to hosts/UI.

## Wave 5 — Advisors / I2

- **Concept:** Advisors abstaining is a valid outcome for tool kernels.
- **Pattern:** Unagent custom events; Improveness frozen-physics checklist.
- **Trade-off:** Don’t force FlipToDet to look “improved.”

## Wave 6–7 — Harden / docs-out

- **Concept:** Docs-out after evidence (case study cites corpus + boot).
- **Pattern:** H1 checklist then CASE_STUDY + integrations + LEARNING.
- **Trade-off:** Raw corpus gitignored; index committed.

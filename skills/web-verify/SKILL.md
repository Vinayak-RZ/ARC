# Web-verify and citations

Load when a solve recipe ran an engine and the answer cites datasheet constants, vendor curves, or web sources that are not in the reference library.

## When to use

| Situation | Action |
|-----------|--------|
| After `simulate-circuit`, control, power, machines, power_electronics solve | Workflow `web-verify` node lists `context_claims` from `problem.json` |
| Standard table already in reference library | `skills/reference/SKILL.md` + `arc_reference_get` instead of web |
| Host has Firecrawl or browser MCP | Gather URL + snippet; submit via `arc_web_evidence_submit` |
| No web tool or empty retrieval | Answer cites **unverified (from memory)**; do not fake `Web-verify:` |

## Provenance honesty (mandatory)

Never write `Web-verify:`, `web-verified`, or similar in answers or notes unless the same run has `evidence/web_sources.json` (or `host_submit.json`) with **URL + quoted snippet + timestamp** per claim. CLI gate: `electrical-engineer provenance audit <file>`.

Reference library rows are not automatic web proof. Distinct paths:

- **Reference:** `arc_reference_search` / `arc_reference_get` / `reference engine`
- **Web:** workflow `web-verify` or MCP evidence submit after live fetch

## Engines

Web-verify does not replace EE engines. Checked scalars still need `run-spice`, `check-numeric`, `run-python-control`, `run-load-flow`, or other FR20 allowlist providers. Web evidence only supports constant labels and citations. Missing engine output → exact token `unchecked`.

## Benchmarks

Eval items with `web-verify` in graph: `eval/gold/`. Trap: claiming web-verified without evidence file.

# Node plan: D2: final README and documentation refresh

| Field | Value |
|-------|-------|
| **Node id** | `D2` |
| **Job** | Rewrite README and sync all shipped behavior in authority docs after build completes |
| **Wave** | **10 (last)** |
| **Depends on (data)** | **All build nodes:** B2, B3, B4, B5, B6, B7, B8, B9 (if shipped), B10, B11, U1, M1, E1, R1, T1 outputs |
| **Write paths** | `README.md`, `docs/ARCHITECTURE.md` (delta appendix only), `docs/DOMAIN_KERNEL_CAPABILITIES.md`, `docs/CANNOT_DO.md`, `docs/visual-kit/**`, `artifacts/benchmarks/**` companion docs, `docs/hosts/README.md` |
| **Model** | inherit |

## Objective

User-facing story matches **what actually shipped**: pip-first install (`uv` alternate), frontier scorecard numbers, Visual Kit screenshots and short clips, problem-solving tone, impressive unlocks with verified commands. No em dashes in prose.

## README requirements (owner)

1. **Install:** `pip install -e ".[dev]"` primary; `uv sync` as alternate; Python 3.11+.
2. **Tone:** Problem-solving for undergrad EE; not hype without numbers.
3. **Media:** Window-sized screenshots and Visual Kit gallery stills; optional Remotion clip paths from B11.
4. **Unlocks:** Short table (PSA, traps, eval packs) with one command each.
5. **Scorecard:** Embed actuals from `artifacts/benchmarks/SCORECARD.md` (not targets).
6. **Style:** No em dashes.

## Authority docs to refresh

| Doc | Must reflect |
|-----|----------------|
| `ARCHITECTURE.md` | Visual Kit registry, MCP `render_visual`, eval schema v2 |
| `DOMAIN_KERNEL_CAPABILITIES.md` | LIVE AB + visual regression metrics |
| `CANNOT_DO.md` | Close rows opened by shipping; no false promises |
| Visual Kit | `docs/visual-kit/README.md` manifest, agent skill, MCP usage |
| Benchmarks | `artifacts/benchmarks/README.md` how to reproduce |

## Contract

**Input:** `{ "scorecard": path, "visual_manifest": path, "integrated_manifest": from M1, "proof_artifacts_bundle": from T1 }`

**Output:** `{ "readme_rewritten": true, "docs_sync_checklist": "all green" }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 1 | `docs: frontier README rewrite with scorecard and visuals` | readme smoke, no em dash lint |
| 2 | `docs: sync ARCHITECTURE DOMAIN_KERNEL CANNOT_DO visual-kit benchmarks` | manual review + link check |

**D1** may land SCORECARD-only earlier; **D2** is the full user-facing pass and **must not** run until wave 8 trials pass.

## Non-goals

- Rewriting `docs/PID.md` / `PRD.md` thesis
- Marketing site off-repo
- Re-opening Gate 0 trade-offs

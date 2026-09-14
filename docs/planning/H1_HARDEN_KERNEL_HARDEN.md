# H1 harden — Kernel harden

## Checklist

| Check | Result |
|-------|--------|
| `./scripts/validate.sh` | PASS |
| No `0.0.0.0` bind in src/ui | PASS (grep) |
| Raw corpus gitignored | PASS (`artifacts/kernel-harden/raw/`) |
| Secrets in committed artifacts | PASS (no keys in reports) |
| Held-out ids not in IMPROVE_LOG prompts | PASS |
| Trace schema_version on spans | PASS (`schema_version: 1`) |
| MCP/ASK fail-closed still | PASS (gate-closed / unmatched tests) |
| Scorer untouched without ADR | PASS (I1 only observation enum + reason helper) |

## Residual risk

- Host corpus problem fixtures remain thin outside circuits; many runs are honestly `labeled` unchecked.
- Unagent ABSTAIN is expected for tool-shaped graphs; do not force FlipToDet.

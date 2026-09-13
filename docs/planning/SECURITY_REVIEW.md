# Security review — D19/D20 graph

Readonly. Bind, secrets, MCP wait, RAG path, PII in run dirs.

## Bind

UI and CLI bind **127.0.0.1** only (`BIND_HOST`). `0.0.0.0` is refused by `scripts/validate.sh`. MCP stdio never waits; photo/compose/control-diagram return `ui_url`.

## Secrets

No API keys in git. `.env` / `*_KEY` / `*_TOKEN` / `*_SECRET` / `sk-` / `Bearer` stay out of run dirs (ARCHITECTURE §13). BYOK is Later. Local LLM URL is env-only.

## RAG

Ingest is untrusted. BYO paths cannot override gates or `unchecked`. CI fixture is licence-clean markdown, not a commercial PDF.

## PII

Run dirs are local audit, not a product cloud. Memory writes are explicit. Observation does not store token/cost.

## Findings

No P0 rewrite this loop. Keep fail-closed MCP and loopback bind.

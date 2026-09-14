# Licence rules for `knowledge/`

This tree is Apache-2.0 as part of the Arc repository, plus third-party OER that we **copy** only when redistribution is allowed in an OSS repo.

## Allowed in git

- Original notes and original worked examples authored for this corpus
- Files under `oer/` that include `SPDX-License-Identifier: CC-BY-4.0`, `CC-BY-SA-4.0`, or `CC0-1.0`

## Forbidden in git

- Commercial textbook text (Hayt, Nilsson, Chapman, Ogata, Oppenheim, Grainger, Rashid, …)
- Third-party exam PDFs or verbatim GATE / university question papers
- NC licences (`CC-BY-NC`, `CC-BY-NC-SA`, `CC-BY-NC-ND`) — link only
- Institute library scrapes

## Link-only until SPDX is recorded

- Åström / Murray, *Feedback Systems* (authors host a free PDF; Princeton print rights — do not copy yet)
- Steven W. Smith, *The Scientist and Engineer’s Guide to DSP* (site grant — record before bundling)
- MIT OCW (typically CC BY-NC-SA)
- NPTEL course video/transcript dumps

## OER copy header

Every copied file starts with:

```text
<!--
SPDX-License-Identifier: CC-BY-4.0
Source: <url>
Retrieved: <ISO date>
-->
```

Adjust SPDX to match the upstream licence. Keep the upstream copyright line.

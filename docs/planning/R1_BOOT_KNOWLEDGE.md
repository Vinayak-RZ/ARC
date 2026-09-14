# R1 — knowledge corpus inventory boot

**Date:** 2026-09-14  
**Graph:** UG EE knowledge corpus (`LOOP_GRAPH.md`)

## Command

```text
python scripts/check_knowledge_tree.py
```

Working directory: repository root.

## Exit

exit code: 0

## Observed

```text
packs=19 units=134 questions=748 allow_empty=False
```

`knowledge/GLOSSARY.md` exists. This graph does not boot the Arc CLI; inventory of the markdown tree is the run target.

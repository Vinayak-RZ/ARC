# UG EE knowledge corpus

Persistent nested markdown for undergraduate electrical engineering. **Not** the RAG index. Do not `electrical-engineer rag add` this tree until a later graph.

## Browse

Start at [`ug-ee/INDEX.md`](ug-ee/INDEX.md) or [`GLOSSARY.md`](GLOSSARY.md). Each unit has `notes.md`, `questions.md` (original worked examples), and `sources.md`.

## Inventory / boot command

From the repo root:

```text
python scripts/check_knowledge_tree.py
```

Prints pack, unit, and question counts. Exit 0 means every `COVERAGE.yaml` unit meets the handbook floors (headings, ≥1500-word notes, ≥5 worked questions, SPDX on any `oer/` file).

Floors only (manifest):

```text
python scripts/check_coverage_floors.py
```

One pack:

```text
python scripts/check_knowledge_tree.py --pack circuits
```

## Licence

[`LICENCE.md`](LICENCE.md). Original notes plus CC BY / CC BY-SA / CC0 copies with SPDX. No commercial textbooks, GATE papers, or NC OER.

## Product lock (this graph)

[`PRODUCT.md`](PRODUCT.md). Arc product lock remains [`docs/PRODUCT.md`](../docs/PRODUCT.md).

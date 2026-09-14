# Knowledge tree schema

Each pack listed in [`COVERAGE.yaml`](COVERAGE.yaml) has `INDEX.md`, `SYLLABUS.md`, and unit folders.

## Unit folder

Required files:

- `notes.md` — teaching handbook
- `questions.md` — original worked set
- `sources.md` — syllabus bullets + OER URLs

Optional: `oer/` — SPDX-copied CC BY / CC BY-SA / CC0 excerpts only.

## `notes.md` headings (required)

```markdown
## Concepts
## Equations
## Methods
## Mistakes
```

Floor: **1500** whitespace-separated words (strict mode).

## `questions.md` items (required)

At least **five** items. Each item:

```markdown
## Q1
### Given
### Find
### Solution
### Answer
```

Numbering `## Q1` … `## Qn` (digits). Original numbers only. Never paste GATE or university papers.

## `oer/` SPDX

First 40 lines of each file must contain one of:

```text
SPDX-License-Identifier: CC-BY-4.0
SPDX-License-Identifier: CC-BY-SA-4.0
SPDX-License-Identifier: CC0-1.0
```

Forbidden: `CC-BY-NC`, commercial-book dump markers listed in the checker.

## Checker

```text
python scripts/check_knowledge_tree.py --allow-empty   # scaffold
python scripts/check_knowledge_tree.py                 # strict
python scripts/check_knowledge_tree.py --pack circuits
python scripts/check_coverage_floors.py                # D0 unit-count floors
```

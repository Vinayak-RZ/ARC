# Optional host hooks (copy-paste)

Not kernel middleware. Compaction and continuation stay the **host**.

After a write-verb returns `run_id`, the main host should:

1. Read `./runs/<id>/` evidentiary seed and `observation.json` (or summary fields).
2. Write `argument.md` if missing (FR21).
3. If `unchecked: true`, show the reason and **ask** before `memory write lessons.md`.

Do not auto-append memory. Do not treat Copilot scalars as checked. Stop if a
gate returned `ui_url`.

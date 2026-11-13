# EEE-Coursework-Trap v0.1

Rebuild: `uv run python scripts/build_benchmark_v01.py`

| Artifact | Contents |
|----------|----------|
| `eee-coursework-trap-v0.1-questions.tar.gz` | Public questions only (`questions.json`, datasheet) |
| `_key/answer_key.json` | Private references (not in questions tarball) |
| `manifest.json` | Questions SHA-256 and task counts |

Grade: `uv run python scripts/grade_benchmark_v01.py answers.json`  
Naive baseline: `uv run python scripts/grade_benchmark_v01.py --naive`

Circuits are picked up automatically from `eval/gold/circuits/*/expect.json`.

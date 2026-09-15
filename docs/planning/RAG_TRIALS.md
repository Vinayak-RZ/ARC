# RAG trials (T1)

Commands run on branch `cursor/rag-hybrid-pipeline-78c0`:

| Trial | Command / check | Result |
|-------|-----------------|--------|
| Happy OER Ohm | `electrical-engineer rag query --book-id kuphaldt-dc --query "Ohm's law"` | non-empty, ch2 first, `engine=hybrid-graph`, ~2ms |
| Empty filter | gold `empty-chapter` | `empty: true` visible |
| Hop + figure | `tests/unit/test_rag_hybrid_hops.py` | worked_example + figure + illustrates |
| Latency | `tests/unit/test_rag_latency.py` | elapsed_ms ≪ 7000 |
| Eval pack | `electrical-engineer eval --pack rag-retrieval` | 4/4 PASS |
| Unit suite | `pytest tests/unit/test_rag_*.py` | all PASS |

OCR: provider path exists (`ocrmypdf`); CI skips when binary missing. Multimodal MinerU/RAG-Anything remains optional adapter (not required in CI).

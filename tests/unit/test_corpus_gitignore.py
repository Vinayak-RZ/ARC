from pathlib import Path


def test_gitignore_excludes_corpus_and_index() -> None:
    text = Path(".gitignore").read_text(encoding="utf-8")
    assert ".electrical-engineer/corpus/" in text
    assert ".electrical-engineer/rag/" in text

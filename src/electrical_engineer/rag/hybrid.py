"""BM25 + dense scoring helpers and RRF fusion (stdlib; optional ST embed)."""

from __future__ import annotations

import math
import re
from collections import Counter

_TOKEN = re.compile(r"[a-z0-9]+")


def tokens(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def bm25_scores(
    query: str,
    docs: list[str],
    *,
    k1: float = 1.5,
    b: float = 0.75,
) -> list[float]:
    """Classic BM25 over an in-memory corpus."""
    q = tokens(query)
    if not q or not docs:
        return [0.0] * len(docs)
    tokenized = [tokens(d) for d in docs]
    N = len(tokenized)
    avgdl = sum(len(t) for t in tokenized) / max(N, 1)
    df: Counter[str] = Counter()
    for toks in tokenized:
        df.update(set(toks))
    scores: list[float] = []
    for toks in tokenized:
        tf = Counter(toks)
        dl = len(toks) or 1
        s = 0.0
        for term in q:
            n_q = df.get(term, 0)
            if n_q == 0:
                continue
            idf = math.log(1 + (N - n_q + 0.5) / (n_q + 0.5))
            freq = tf.get(term, 0)
            s += idf * (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * dl / avgdl))
        scores.append(s)
    return scores


def _hash_embed(text: str, dim: int = 64) -> list[float]:
    """Deterministic bag-of-tokens hash embed for CI without sentence-transformers."""
    vec = [0.0] * dim
    for t in tokens(text):
        vec[hash(t) % dim] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


_model = None


def dense_embed(texts: list[str]) -> list[list[float]]:
    global _model
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        return [_hash_embed(t) for t in texts]
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    vectors = _model.encode(texts, normalize_embeddings=True)
    return [list(map(float, row)) for row in vectors]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=False))


def dense_scores(query: str, docs: list[str]) -> list[float]:
    if not docs:
        return []
    vectors = dense_embed([query, *docs])
    qv = vectors[0]
    return [cosine(qv, v) for v in vectors[1:]]


def rrf_fuse(
    rank_lists: list[list[int]],
    *,
    k: int = 60,
) -> list[tuple[int, float]]:
    """Reciprocal rank fusion. rank_lists hold doc indices best→worst."""
    scores: dict[int, float] = {}
    for ranking in rank_lists:
        for rank, idx in enumerate(ranking, start=1):
            scores[idx] = scores.get(idx, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))

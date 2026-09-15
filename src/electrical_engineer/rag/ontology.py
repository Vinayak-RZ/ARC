"""RAG ontology: T0–T4 kinds and typed edges for hybrid-graph retrieve."""

from __future__ import annotations

from typing import Final

# Tier 0 — document spine
T0_KINDS: Final = frozenset({"library", "book", "chapter", "section"})
# Tier 1 — retrievable units
T1_KINDS: Final = frozenset(
    {"prose", "equation", "caption", "solution_step", "table_cell", "question"}
)
# Tier 2 — parents / bundles
T2_KINDS: Final = frozenset({"worked_example", "section_parent", "figure_group"})
# Tier 3 — assets
T3_KINDS: Final = frozenset({"figure"})
# Tier 4 — light concepts
T4_KINDS: Final = frozenset({"entity", "proposition"})

NODE_KINDS: Final = T0_KINDS | T1_KINDS | T2_KINDS | T3_KINDS | T4_KINDS

EDGE_TYPES: Final = frozenset(
    {
        "belongs_to",
        "part_of_example",
        "illustrates",
        "caption_of",
        "mentions",
        "states",
        "prerequisite",
    }
)

# Query may walk only these edges (k ≤ 2)
HOP_EDGES: Final = frozenset(
    {"part_of_example", "illustrates", "caption_of", "states", "mentions", "belongs_to"}
)

PASSAGE_CHARS: Final = 1500
MAX_PASSAGES: Final = 3
MAX_HOPS: Final = 2
RETRIEVE_BUDGET_S: Final = 7.0
ENGINE_ID: Final = "hybrid-graph"


def valid_node(kind: str) -> bool:
    return kind in NODE_KINDS


def valid_edge(edge_type: str) -> bool:
    return edge_type in EDGE_TYPES

"""Round public givens and format stems without float noise."""

from __future__ import annotations

import copy
from typing import Any


def _sigfig(x: float, n: int = 4) -> float:
    if x == 0.0:
        return 0.0
    return float(f"{float(x):.{n}g}")


def round_public_givens(g: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(g)

    def walk(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: walk(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [walk(v) for v in obj]
        if isinstance(obj, float):
            return _sigfig(obj)
        if isinstance(obj, int) and not isinstance(obj, bool):
            return obj
        return obj

    return walk(out)


def format_stem_number(x: float) -> str:
    return f"{_sigfig(x):g}"

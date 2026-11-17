"""Mean-vs-Vo tolerances aligned with ui/src/studio-engine/labs/rectifier.test.js."""

from __future__ import annotations


def rectifier_mean_skip(topology: str, load: str, alpha_deg: float) -> bool:
    return load in {"RL", "RLE"} and (
        (topology == "full1" and alpha_deg >= 45) or (topology == "hw3" and alpha_deg > 45)
    )


def rectifier_mean_rel_tol(topology: str, load: str, alpha_deg: float) -> float:
    if load in {"RL", "RLE"} and topology == "full1":
        return 0.085
    if load in {"RL", "RLE"} and topology == "hw3" and alpha_deg > 30:
        return 0.03
    return 0.005
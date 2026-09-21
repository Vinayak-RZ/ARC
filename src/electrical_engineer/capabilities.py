"""Allowlisted capabilities bind this-pass providers or CD-NO-PROVIDER."""

from __future__ import annotations

from dataclasses import dataclass, replace
from importlib import import_module

from electrical_engineer.runner.fsm import NodeSpec, Recipe

CAPABILITIES = frozenset(
    {
        "algebraic-check",
        "lumped-circuit-sim",
        "lti-analysis",
        "power-network-study",
        "machine-model",
        "converter-model",
        "signal-analysis",
        "fields-analytic",
        "measurement-model",
        "retrieve-citation",
        "render-figure",
        "ingest-figure",
        "label-unverified",
        "ask-student",
    }
)

PROVIDERS = frozenset(
    {
        "retrieve-passage",
        "check-numeric",
        "run-spice",
        "run-python-control",
        "run-matlab-if-present",
        "run-simulink-if-present",
        "run-load-flow",
        "ask-human",
        "label-unchecked",
        "write-run-summary",
        "solve-explain",
        "detect-components",
        "connect-wires",
        "ocr-labels",
        "draft-netlist",
        "confirm-topology",
        "run-recipe",
        "load-netlist",
        "compose-control-blocks",
        "run-digital-control",
        "run-protection-study",
        "run-drives-study",
    }
)

# ponytail: MATLAB-if-present is optional; DEFAULT_BIND stays OSS. Client is matlab_mcp.py.
DEFAULT_BIND = {
    "algebraic-check": "check-numeric",
    "lumped-circuit-sim": "run-spice",
    "lti-analysis": "run-python-control",
    "power-network-study": "run-load-flow",
    "machine-model": "check-numeric",
    "converter-model": "check-numeric",
    "signal-analysis": "check-numeric",
    "fields-analytic": "check-numeric",
    "measurement-model": "check-numeric",
    "retrieve-citation": "retrieve-passage",
    "render-figure": "label-unchecked",
    "ingest-figure": "confirm-topology",
    "label-unverified": "label-unchecked",
    "ask-student": "ask-human",
}

_OPTIONAL_IMPORT = {
    "run-spice": "PySpice",
    "run-python-control": "control",
    "run-load-flow": "pandapower",
}

ALWAYS_INSTALLED = PROVIDERS - frozenset(_OPTIONAL_IMPORT) - {
    "run-matlab-if-present",
    "run-simulink-if-present",
}

CD_NO_PROVIDER = "CD-NO-PROVIDER"


class CapabilityError(ValueError):
    pass


@dataclass(frozen=True)
class Bind:
    capability: str | None
    provider: str
    no_provider: bool
    cannot_do: str | None


def provider_installed(activity: str) -> bool:
    if activity in ALWAYS_INSTALLED:
        return True
    mod = _OPTIONAL_IMPORT.get(activity)
    if mod is None:
        return False
    try:
        import_module(mod)
    except ImportError:
        return False
    return True


def bind(name: str) -> Bind:
    """Map a capability or provider id. Unknown ids reject."""
    if name in CAPABILITIES:
        provider = DEFAULT_BIND[name]
        if name == "render-figure" or not provider_installed(provider):
            return Bind(name, "label-unchecked", True, CD_NO_PROVIDER)
        return Bind(name, provider, False, None)
    if name in PROVIDERS:
        return Bind(None, name, False, None)
    raise CapabilityError(f"unknown id {name}")


def rebind_recipe(recipe: Recipe) -> Recipe:
    """Resolve capability ids on a parsed recipe. Unknown provider keys pass through."""
    nodes: dict[str, NodeSpec] = {}
    for nid, spec in recipe.nodes.items():
        if spec.activity not in CAPABILITIES:
            nodes[nid] = spec
            continue
        bound = bind(spec.activity)
        extras = dict(spec.extras)
        extras["capability"] = bound.capability
        if bound.no_provider:
            extras["cannot_do"] = bound.cannot_do
        nodes[nid] = replace(spec, activity=bound.provider, extras=extras)
    return Recipe(id=recipe.id, nodes=nodes)

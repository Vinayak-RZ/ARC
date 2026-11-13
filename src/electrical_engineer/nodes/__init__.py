from electrical_engineer.nodes import photo as _photo  # noqa: F401
from electrical_engineer.nodes import sim as _sim  # noqa: F401
from electrical_engineer.nodes import study as _study  # noqa: F401
from electrical_engineer.nodes import web_verify as _web_verify  # noqa: F401
from electrical_engineer.nodes.registry import REGISTRY, names

__all__ = ["REGISTRY", "names"]

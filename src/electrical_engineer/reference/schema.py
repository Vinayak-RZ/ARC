"""Reference record schema validation."""

from __future__ import annotations

from typing import Any

REQUIRED_TOP = (
    "id",
    "domain",
    "title",
    "values",
    "source",
    "source_secondary",
    "url",
    "license",
    "verification",
    "confidence",
    "value_conditions",
)
REQUIRED_SOURCE = ("title", "edition", "clause")
CONFIDENCE_VALUES = frozenset({"verified_dual", "single_source"})


class SchemaError(ValueError):
    pass


def _validate_source(src: Any, path: str) -> None:
    if not isinstance(src, dict):
        raise SchemaError(f"{path}: source must be a mapping")
    for key in REQUIRED_SOURCE:
        if key not in src:
            raise SchemaError(f"{path}: source missing {key}")


def validate_record(rec: dict[str, Any], *, path: str = "") -> None:
    if not isinstance(rec, dict):
        raise SchemaError(f"{path}: record must be a mapping")
    for key in REQUIRED_TOP:
        if key not in rec:
            raise SchemaError(f"{path}: missing {key}")
        if key == "value_conditions":
            if rec[key] is None:
                raise SchemaError(f"{path}: missing value_conditions")
            continue
        if rec[key] in (None, ""):
            raise SchemaError(f"{path}: missing {key}")
    conf = str(rec["confidence"])
    if conf not in CONFIDENCE_VALUES:
        raise SchemaError(f"{path}: invalid confidence {conf}")
    _validate_source(rec["source"], f"{path}.source")
    _validate_source(rec.get("source_secondary") or {}, f"{path}.source_secondary")
    if not isinstance(rec["values"], dict):
        raise SchemaError(f"{path}: values must be a mapping")
    vcond = rec.get("value_conditions")
    if vcond is not None and not isinstance(vcond, dict):
        raise SchemaError(f"{path}: value_conditions must be a mapping")
    aliases = rec.get("aliases", [])
    if aliases is not None and not isinstance(aliases, list):
        raise SchemaError(f"{path}: aliases must be a list")

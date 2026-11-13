"""Reference record schema validation."""

from __future__ import annotations

from typing import Any

REQUIRED_TOP = ("id", "domain", "title", "values", "source", "url", "license", "verification")
REQUIRED_SOURCE = ("title", "edition", "clause")


class SchemaError(ValueError):
    pass


def validate_record(rec: dict[str, Any], *, path: str = "") -> None:
    if not isinstance(rec, dict):
        raise SchemaError(f"{path}: record must be a mapping")
    for key in REQUIRED_TOP:
        if key not in rec or rec[key] in (None, ""):
            raise SchemaError(f"{path}: missing {key}")
    src = rec["source"]
    if not isinstance(src, dict):
        raise SchemaError(f"{path}: source must be a mapping")
    for key in REQUIRED_SOURCE:
        if key not in src:
            raise SchemaError(f"{path}: source missing {key}")
    if not isinstance(rec["values"], dict):
        raise SchemaError(f"{path}: values must be a mapping")
    aliases = rec.get("aliases", [])
    if aliases is not None and not isinstance(aliases, list):
        raise SchemaError(f"{path}: aliases must be a list")

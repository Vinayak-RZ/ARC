"""Curated EE reference library (open/factual records + engines)."""

from electrical_engineer.reference.catalog import (
    get_record,
    list_domains,
    load_catalog,
    search_records,
)

__all__ = ["get_record", "list_domains", "load_catalog", "search_records"]

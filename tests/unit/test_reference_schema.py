from electrical_engineer.reference.catalog import clear_catalog_cache, load_catalog, search_records


def setup_function() -> None:
    clear_catalog_cache()
from electrical_engineer.reference.schema import validate_record


def test_all_reference_records_validate() -> None:
    catalog = load_catalog()
    assert len(catalog) >= 40
    for rec in catalog.values():
        assert rec["confidence"] in ("verified_dual", "single_source")
        assert rec.get("source_secondary")
    for rid, rec in catalog.items():
        validate_record(rec, path=rid)
        assert rec["id"] == rid


def test_search_aliases() -> None:
    hits = search_records("Zebra")
    ids = {h["id"] for h in hits}
    assert "ACSR_ZEBRA" in ids
    iec = search_records("IEC SI")
    assert any(h["id"] == "IEC_SI" for h in iec)

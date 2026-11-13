from electrical_engineer.reference.catalog import load_catalog, search_records
from electrical_engineer.reference.schema import validate_record


def test_all_reference_records_validate() -> None:
    catalog = load_catalog()
    assert len(catalog) >= 30
    for rid, rec in catalog.items():
        validate_record(rec, path=rid)
        assert rec["id"] == rid


def test_search_aliases() -> None:
    hits = search_records("Zebra")
    ids = {h["id"] for h in hits}
    assert "ACSR_ZEBRA" in ids
    iec = search_records("IEC SI")
    assert any(h["id"] == "IEC_SI" for h in iec)

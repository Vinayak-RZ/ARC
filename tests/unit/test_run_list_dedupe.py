from electrical_engineer.ui_server.app import _dedupe_run_items


def test_dedupe_keeps_newest_title() -> None:
    items = [
        {"id": "a", "display_title": "Voltage divider · Vout", "modified_at": 100.0},
        {"id": "b", "display_title": "Voltage divider · Vout", "modified_at": 200.0},
        {"id": "c", "display_title": "Other", "modified_at": 50.0},
    ]
    out = _dedupe_run_items(items)
    assert len(out) == 2
    assert out[0]["id"] == "b"
    assert out[1]["id"] == "c"

"""PACKS single source and pack_for_recipe."""

from __future__ import annotations

from electrical_engineer.catalog import PACKS, pack_for_recipe, pack_recipe_counts


def test_packs_has_ten() -> None:
    assert len(PACKS) == 10
    ids = [p.id for p in PACKS]
    assert ids[0] == "circuits"
    assert "power_electronics" in ids
    assert "maths" in ids


def test_pack_for_known_recipe() -> None:
    assert pack_for_recipe("smib-swing-study") == "power"
    assert pack_for_recipe("solve-circuit-problem") == "circuits"
    assert pack_for_recipe("photo-to-netlist") is None


def test_pack_recipe_counts_ten() -> None:
    packs = pack_recipe_counts()
    assert len(packs) == 10
    by_id = {p["id"]: p for p in packs}
    assert by_id["circuits"]["recipe_count"] >= 1
    assert by_id["power"]["label"] == "Power"

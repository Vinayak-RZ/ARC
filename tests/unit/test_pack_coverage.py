"""Every curriculum pack has a complete co-solver path (capability or cannot-do)."""

from pathlib import Path

PACK_DEFAULT = {
    "circuits": "lumped-circuit-sim",
    "signals": "signal-analysis",
    "electronics": "algebraic-check",
    "machines": "machine-model",
    "power": "power-network-study",
    "control": "lti-analysis",
    "power_electronics": "converter-model",
    "measurements": "measurement-model",
    "em": "fields-analytic",
    "maths": "algebraic-check",
}

PACK_HOLE = {
    "signals": "CD-SIGNALS-MATLAB",
    "machines": "CD-MACHINES-FEA",
    "power": "CD-POWER-EMS",
    "electronics": "CD-ELEC-PDK",
    "measurements": "CD-MEAS-BENCH",
    "em": "CD-EM-HFSS",
    "power_electronics": "CD-PE-HIL",
    "maths": "CD-MATHS-CAS",
    "circuits": "CD-NO-PROVIDER",
    "control": "CD-NO-PROVIDER",
}


def test_pack_coverage_paths() -> None:
    cannot = Path("docs/CANNOT_DO.md").read_text()
    assert "CD-NO-PROVIDER" in cannot
    assert "CD-YAML-GAP" in cannot
    for pack, cap in PACK_DEFAULT.items():
        text = Path(f"skills/{pack}/SKILL.md").read_text()
        assert cap in text, pack
        assert "unchecked" in text, pack
        hole = PACK_HOLE[pack]
        assert hole in cannot, hole
        if hole != "CD-NO-PROVIDER":
            assert hole in text, pack
    cross = Path("skills/_cross/SKILL.md").read_text()
    assert "label-unverified" in cross
    assert "unchecked" in cross

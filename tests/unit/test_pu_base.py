from __future__ import annotations

from electrical_engineer.engines.pu_base import aggregate_fault_impedance, impedance_pu_on_new_base


def test_impedance_base_change_50_to_100_mva() -> None:
    x50 = 0.15j
    x100 = impedance_pu_on_new_base(x50, s_old_mva=50, s_new_mva=100, v_old_kv=13.8, v_new_kv=13.8)
    assert abs(x100 - 0.075j) < 1e-12


def test_aggregate_includes_gen_and_xfmr() -> None:
    out = aggregate_fault_impedance(
        [
            {"id": "gen", "z_pu": 0.2j, "s_base_mva": 50, "sequence": "1"},
            {"id": "xf", "z_pu": 0.1j, "s_base_mva": 100, "sequence": "1"},
        ],
        s_system_mva=100,
        v_system_kv=13.8,
    )
    assert abs(out["z1_pu"] - (0.1j + 0.1j)) < 1e-9
    assert len(out["table"]) == 2

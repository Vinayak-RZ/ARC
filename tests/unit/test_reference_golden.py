"""Golden tests tied to published worked examples (sources cited in assertions)."""

import math

import pytest

from electrical_engineer.reference.catalog import clear_catalog_cache
from electrical_engineer.reference.engines.economic_dispatch import economic_dispatch
from electrical_engineer.reference.engines.iec60909 import initial_symmetrical_ka
from electrical_engineer.reference.engines.iec60909_peak import peak_short_circuit_ka
from electrical_engineer.reference.engines.ieee80 import tolerable_voltages
from electrical_engineer.reference.engines.ieee519 import tdd_compliance
from electrical_engineer.reference.engines.nema_locked_rotor import locked_rotor_current_a


@pytest.fixture(autouse=True)
def _fresh_catalog() -> None:
    clear_catalog_cache()


def test_ieee80_eq32_touch_annex_style() -> None:
    """IEEE Std 80-2013 Eq. 32 style: (1000+1.5*Cs*rho)*k_touch/sqrt(t)."""
    out = tolerable_voltages(
        kind="touch",
        body_mass_kg=70,
        rho_s_ohm_m=200.0,
        cs=1.0,
        t_s=0.4,
    )
    expected = (1000.0 + 1.5 * 1.0 * 200.0) * 0.157 / math.sqrt(0.4)
    assert out["e_v"] == pytest.approx(322.71, rel=1e-3)
    assert out["e_v"] == pytest.approx(expected, rel=1e-6)
    step = tolerable_voltages(
        kind="step", body_mass_kg=70, rho_s_ohm_m=200.0, cs=1.0, t_s=0.4
    )
    assert step["e_v"] > out["e_v"]


def test_matpower_case9_economic_dispatch_golden() -> None:
    """MATPOWER case9.m gencost; gen3 out of service -> lambda 33.06 MW/MW."""
    out = economic_dispatch(
        "IEEE_CASE_9_GENCOST",
        total_load_mw=315.0,
        out_of_service_buses=[3],
    )
    assert out["lambda_mw_per_mw"] == pytest.approx(33.064, rel=1e-3)
    by_bus = {g["bus"]: g["p_mw"] for g in out["generators"]}
    assert by_bus[1] == pytest.approx(127.564, rel=1e-3)
    assert by_bus[2] == pytest.approx(187.436, rel=1e-3)


def test_iec60909_peak_factor_chain() -> None:
    """IEC 60909-0 ip = kappa * sqrt(2) * Ik'' (TR 60909-4 equation chain)."""
    z = 0.05 + 0.5j
    sym = initial_symmetrical_ka(voltage_kv=11.0, z_ohm=z)
    peak = peak_short_circuit_ka(voltage_kv=11.0, z_ohm=z)
    assert peak["ip_ka"] == pytest.approx(
        peak["kappa"] * math.sqrt(2) * sym["ik_ka"],
        rel=1e-9,
    )


def test_ieee519_2022_table2_tdd_compliance() -> None:
    out = tdd_compliance(isc_il_ratio=35.0, measured_tdd_percent=7.5)
    assert "IEEE Std 519-2022" in out["edition_label"]
    assert out["limit_tdd_percent"] == 8.0
    assert out["compliant"] is True


def test_nema_code_g_locked_rotor_current() -> None:
    """NEMA MG1 Table 11-1 code G band mid kVA/hp."""
    out = locked_rotor_current_a(code_id="NEMA_CODE_G", hp=10.0, line_voltage_v=460.0, use="mid")
    kva_mid = (5.6 + 6.29) / 2.0 * 10.0
    i_exp = kva_mid * 1000.0 / (math.sqrt(3) * 460.0)
    assert out["i_lr_a"] == pytest.approx(i_exp, rel=1e-6)

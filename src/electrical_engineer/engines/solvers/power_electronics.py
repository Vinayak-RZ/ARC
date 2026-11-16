"""Power electronics SolverSpec table."""

from __future__ import annotations

import math

from electrical_engineer.engines.solvers.spec import Param, SolverSpec

_SQRT6 = math.sqrt(6.0)
_SQRT2 = math.sqrt(2.0)
_SQRT3 = math.sqrt(3.0)
_PI = math.pi


def _deg(rad: float) -> float:
    return math.degrees(rad)


def _mu_deg(cos_alpha: float, w_ls_io: float, vm_pk: float, alpha_rad: float) -> float:
    rhs = cos_alpha - w_ls_io / vm_pk
    rhs = max(-1.0, min(1.0, rhs))
    mu_rad = math.acos(rhs) - alpha_rad
    return _deg(mu_rad) if mu_rad >= 0 else 0.0


def rectifier_1ph(
    v_rms: float,
    alpha_deg: float,
    topology: str,
    load: str,
    io_a: float = 0.0,
    ls_h: float = 0.0,
    f_hz: float = 50.0,
) -> dict:
    alpha = math.radians(alpha_deg)
    cos_a = math.cos(alpha)
    vm = _SQRT2 * v_rms
    w = 2.0 * _PI * f_hz
    if topology == "half":
        vo = (vm / (2.0 * _PI)) * (1.0 + cos_a)
    elif topology == "semi":
        vo = (vm / _PI) * (1.0 + cos_a) - (w * ls_h * io_a) / _PI
    elif topology == "full":
        if load == "continuous":
            vo = (2.0 * vm / _PI) * cos_a - (2.0 * w * ls_h * io_a) / _PI
        else:
            vo = (vm / _PI) * (1.0 + cos_a)
    else:
        raise ValueError(f"topology must be half, semi, or full, got {topology!r}")
    out: dict = {"Vo_V": vo, "topology": topology, "load": load}
    if topology == "full" and load == "continuous":
        out["mu_deg"] = _mu_deg(cos_a, 2.0 * w * ls_h * io_a, vm, alpha)
    return out


def rectifier_3ph(
    v_ll_rms: float,
    alpha_deg: float,
    topology: str,
    io_a: float = 0.0,
    ls_h: float = 0.0,
    f_hz: float = 50.0,
    *,
    load: str = "R",
) -> dict:
    alpha = math.radians(alpha_deg)
    cos_a = math.cos(alpha)
    vll_pk = _SQRT2 * v_ll_rms
    w = 2.0 * _PI * f_hz
    vm_ph = vll_pk / _SQRT3
    if topology == "half":
        continuous = load != "R" or alpha_deg <= 30.0
        if continuous:
            vo = (3.0 * _SQRT3 * vm_ph / (2.0 * _PI)) * cos_a - (3.0 * w * ls_h * io_a) / (2.0 * _PI)
        else:
            vo = (3.0 * vm_ph / (2.0 * _PI)) * (1.0 + math.cos(alpha + _PI / 6.0))
            vo -= (3.0 * w * ls_h * io_a) / (2.0 * _PI)
    elif topology == "full":
        vo = (3.0 * vll_pk / _PI) * cos_a - (3.0 * w * ls_h * io_a) / _PI
    else:
        raise ValueError(f"topology must be half or full, got {topology!r}")
    pf = (3.0 / _PI) * cos_a if topology == "full" else None
    is_rms = math.sqrt(2.0 / 3.0) * io_a if io_a else 0.0
    out = {
        "Vo_V": vo,
        "PF": pf,
        "Is_rms_A": is_rms,
        "topology": topology,
    }
    if topology == "full":
        out["mu_deg"] = _mu_deg(cos_a, 2.0 * w * ls_h * io_a, vll_pk, alpha)
    return out


def boost_ccm(vin: float, d: float, l: float, c: float, fs: float, r: float) -> dict:
    if d >= 1.0 or d < 0:
        raise ValueError("duty d must be in [0, 1)")
    vo = vin / (1.0 - d)
    di_l = vin * d / (l * fs)
    dvo = (vo / r) * d / (c * fs)
    l_crit = d * (1.0 - d) ** 2 * r / (2.0 * fs)
    return {"Vo_V": vo, "delta_iL_A": di_l, "delta_Vo_V": dvo, "L_crit_H": l_crit}


def buck_boost_ccm(vin: float, d: float, l: float, c: float, fs: float, r: float) -> dict:
    if d >= 1.0 or d <= 0:
        raise ValueError("duty d must be in (0, 1)")
    vo = -vin * d / (1.0 - d)
    di_l = vin * d / (l * fs)
    dvo = abs(vo) / r * d / (c * fs)
    return {"Vo_V": vo, "delta_iL_A": di_l, "delta_Vo_V": dvo}


def inverter_six_step(vdc: float) -> dict:
    v_ll1 = (_SQRT6 / _PI) * vdc
    v_ph1 = (_SQRT2 / _PI) * vdc
    v_ll = math.sqrt(2.0 / 3.0) * vdc
    harmonics = {n: 1.0 / n for n in (5, 7, 11, 13)}
    return {
        "V_LL1_rms_V": v_ll1,
        "V_ph1_rms_V": v_ph1,
        "V_LL_rms_V": v_ll,
        "harmonics_V_rel": harmonics,
    }


def spwm_inverter(vdc: float, ma: float, mf: float, phases: str) -> dict:
    del mf  # teaching harmonic index; not needed for RMS closed form
    if ma > 1.0:
        raise ValueError("overmodulation not supported")
    if phases == "3":
        v_ll1 = 0.6124 * ma * vdc
        return {"V_LL1_rms_V": v_ll1, "phases": phases, "ma": ma}
    if phases == "1":
        v1 = ma * vdc / _SQRT2
        return {"V1_rms_V": v1, "phases": phases, "ma": ma}
    raise ValueError(f"phases must be '1' or '3', got {phases!r}")


SPECS: dict[str, SolverSpec] = {
    "rectifier_1ph": SolverSpec(
        fn=rectifier_1ph,
        params=(
            Param("v_rms"),
            Param("alpha_deg"),
            Param("topology", kind="str", choices=("half", "semi", "full")),
            Param("load", kind="str", choices=("R", "continuous")),
            Param("io_a", default=0.0),
            Param("ls_h", default=0.0),
            Param("f_hz", default=50.0),
        ),
        value_key="Vo_V",
        unit="V",
    ),
    "rectifier_3ph": SolverSpec(
        fn=rectifier_3ph,
        params=(
            Param("v_ll_rms"),
            Param("alpha_deg"),
            Param("topology", kind="str", choices=("half", "full")),
            Param("io_a", default=0.0),
            Param("ls_h", default=0.0),
            Param("f_hz", default=50.0),
        ),
        value_key="Vo_V",
        unit="V",
    ),
    "boost_ccm": SolverSpec(
        fn=boost_ccm,
        params=(
            Param("vin"),
            Param("d"),
            Param("l"),
            Param("c"),
            Param("fs"),
            Param("r"),
        ),
        value_key="Vo_V",
        unit="V",
    ),
    "buck_boost_ccm": SolverSpec(
        fn=buck_boost_ccm,
        params=(
            Param("vin"),
            Param("d"),
            Param("l"),
            Param("c"),
            Param("fs"),
            Param("r"),
        ),
        value_key="Vo_V",
        unit="V",
    ),
    "inverter_six_step": SolverSpec(
        fn=inverter_six_step,
        params=(Param("vdc"),),
        value_key="V_LL1_rms_V",
        unit="V",
    ),
    "spwm_inverter": SolverSpec(
        fn=spwm_inverter,
        params=(
            Param("vdc"),
            Param("ma"),
            Param("mf"),
            Param("phases", kind="str", choices=("1", "3")),
        ),
        value_key="V_LL1_rms_V",
        unit="V",
    ),
}
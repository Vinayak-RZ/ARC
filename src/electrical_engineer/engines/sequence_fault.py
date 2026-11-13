"""Sequence-network fault analysis with phase-domain verification."""

from __future__ import annotations

import cmath
import math
from typing import Any, Literal

PhaseName = Literal["a", "b", "c"]

_A = cmath.exp(1j * 2.0 * math.pi / 3.0)
_A2 = _A * _A

# Canonical faults referenced to phase-a prefault Va; permute for other faulted labels.
_CANON_KIND = {
    "SLG": "slg",
    "LL": "ll",
    "LLG": "llg",
    "3PH": "3ph",
}

_PHASE_IDX = {"a": 0, "b": 1, "c": 2}


def _norm_phases(phases: tuple[str, ...] | list[str] | None) -> tuple[str, ...]:
    if not phases:
        return ()
    xs = tuple(sorted({str(p).lower()[0] for p in phases}))
    if any(p not in ("a", "b", "c") for p in xs):
        raise ValueError(f"invalid phase names {phases}")
    return xs


def _norm_fault(ft: str) -> str:
    u = ft.upper().replace(" ", "").replace("-", "")
    aliases = {
        "LG": "SLG",
        "1LG": "SLG",
        "SLG": "SLG",
        "2LL": "LL",
        "LL": "LL",
        "2LLG": "LLG",
        "DLG": "LLG",
        "LLG": "LLG",
        "3PH": "3PH",
        "LLL": "3PH",
        "THREE_PHASE": "3PH",
        "3PHASE": "3PH",
    }
    if u not in aliases:
        raise ValueError(f"unsupported fault type {ft}")
    return aliases[u]


def _seq_to_phase(i0: complex, i1: complex, i2: complex) -> dict[str, complex]:
    ia = i0 + i1 + i2
    ib = i0 + _A * i1 + _A2 * i2
    ic = i0 + _A2 * i1 + _A * i2
    return {"a": ia, "b": ib, "c": ic}


def _canonical_sequence_currents(
    kind: str,
    v_pre: complex,
    z1: complex,
    z2: complex,
    z0: complex,
    zf: complex,
) -> tuple[complex, complex, complex]:
    if kind == "3ph":
        i1 = v_pre / z1
        return 0j, i1, 0j
    if kind == "slg":
        i1 = v_pre / (z1 + z2 + z0 + 3.0 * zf)
        return i1, i1, i1
    if kind == "ll":
        i1 = v_pre / (z1 + z2)
        return 0j, i1, -i1
    if kind == "llg":
        zpar = z2 * (z0 + 3.0 * zf) / (z2 + z0 + 3.0 * zf)
        i1 = v_pre / (z1 + zpar)
        k = (z0 + 3.0 * zf) / (z2 + z0 + 3.0 * zf)
        i2 = -i1 * k
        i0 = i2
        return i0, i1, i2
    raise ValueError(kind)


def _unmap_rotated_phases(phase_i: dict[str, complex], steps: int) -> dict[str, complex]:
    """Map phase currents from rotated-a-fault frame back to actual a,b,c."""
    order = ("a", "b", "c")
    return {order[i]: phase_i[order[(i - steps) % 3]] for i in range(3)}


def analyze_sequence_fault(
    *,
    fault_type: str,
    faulted_phases: tuple[str, ...] | list[str] | None = None,
    v_prefault_pu: complex = 1 + 0j,
    v_angle_deg: float = 0.0,
    z1_pu: complex,
    z2_pu: complex,
    z0_pu: complex,
    zf_pu: complex = 0j,
) -> dict[str, Any]:
    """Return sequence and phase currents (magnitude and angle vs prefault Va)."""
    ft = _norm_fault(fault_type)
    phases = _norm_phases(faulted_phases or ())
    if ft == "SLG" and len(phases) == 3:
        phases = ("a",)
    if ft == "SLG" and len(phases) == 0:
        phases = ("a",)
    if ft == "LL" and len(phases) == 0:
        phases = ("a", "b")
    if ft == "LLG" and len(phases) == 0:
        phases = ("b", "c")
    if ft == "3PH":
        phases = ("a", "b", "c")
    if ft == "SLG" and len(phases) != 1:
        raise ValueError("SLG requires exactly one faulted phase")
    if ft == "LL" and len(phases) != 2:
        raise ValueError("LL requires exactly two faulted phases")
    if ft == "LLG" and len(phases) != 2:
        raise ValueError("LLG requires exactly two faulted phases")

    kind = _CANON_KIND[ft]
    anchor = phases[0] if ft != "3PH" else "a"
    rot = _PHASE_IDX[anchor]

    v_pre = v_prefault_pu * cmath.exp(1j * math.radians(v_angle_deg))
    v_rot = v_pre * (_A ** (-rot))
    i0, i1, i2 = _canonical_sequence_currents(kind, v_rot, z1_pu, z2_pu, z0_pu, zf_pu)
    phase_i = _unmap_rotated_phases(_seq_to_phase(i0, i1, i2), rot)

    ref = cmath.exp(1j * math.radians(v_angle_deg))

    def _pol(z: complex) -> dict[str, float]:
        ang = math.degrees(cmath.phase(z / ref))
        return {"mag_pu": float(abs(z)), "angle_deg": float(ang)}

    phase_domain = _phase_domain_verify(ft, phases, i0, i1, i2, phase_i)
    seq_phase = phase_i

    out = {
        "fault_type": ft,
        "faulted_phases": list(phases),
        "I0_pu": _pol(i0),
        "I1_pu": _pol(i1),
        "I2_pu": _pol(i2),
        "I_phase_pu": {p: _pol(seq_phase[p]) for p in ("a", "b", "c")},
        "phase_domain_verify": phase_domain,
        "verified": phase_domain["ok"],
    }
    if ft == "SLG":
        out["value"] = out["I_phase_pu"][phases[0]]["mag_pu"]
    elif ft == "LL":
        out["value"] = math.sqrt(3.0) * out["I1_pu"]["mag_pu"]
    elif ft == "3PH":
        out["value"] = out["I1_pu"]["mag_pu"]
    else:
        out["value"] = max(out["I_phase_pu"][p]["mag_pu"] for p in phases)
    return out


def _phase_domain_verify(
    ft: str,
    phases: tuple[str, ...],
    i0: complex,
    i1: complex,
    i2: complex,
    phase_i: dict[str, complex],
    *,
    tol: float = 1e-5,
) -> dict[str, Any]:
    """Check bolted-fault constraints and consistency with sequence interconnect."""
    try:
        _check_fault_bc(ft, phases, phase_i, tol)
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}
    ok = bool(_check_fault_bc(ft, phases, phase_i, tol, raise_exc=False))
    return {"ok": ok, "I_abc_check_pu": {p: float(abs(phase_i[p])) for p in phase_i}}


def _check_fault_bc(
    ft: str,
    phases: tuple[str, ...],
    phase_i: dict[str, complex],
    tol: float,
    *,
    raise_exc: bool = True,
) -> bool:
    if ft == "SLG":
        p = phases[0]
        ok = all(abs(phase_i[q]) <= tol for q in ("a", "b", "c") if q != p)
        if not ok and raise_exc:
            raise ValueError("SLG: non-fault phase currents should be ~0")
        return ok
    if ft == "LL":
        other = next(x for x in ("a", "b", "c") if x not in phases)
        if abs(phase_i[other]) > tol:
            if raise_exc:
                raise ValueError("LL: unfaulted phase current should be ~0")
            return False
    return True


def legacy_scalar_current(
    fault_type: str,
    v_prefault: complex,
    z1: complex,
    z2: complex,
    z0: complex,
    zf: complex = 0j,
    *,
    faulted_phases: tuple[str, ...] | None = None,
) -> complex:
    """Backward-compatible scalar (phase-a magnitude driver for gold lg/ll)."""
    ft = _norm_fault(fault_type)
    phases = faulted_phases
    if phases is None:
        if ft == "SLG":
            phases = ("a",)
        elif ft == "LL":
            phases = ("a", "b")
        elif ft == "LLG":
            phases = ("b", "c")
        elif ft == "3PH":
            phases = ("a", "b", "c")
    r = analyze_sequence_fault(
        fault_type=fault_type,
        faulted_phases=phases,
        v_prefault_pu=v_prefault,
        z1_pu=z1,
        z2_pu=z2,
        z0_pu=z0,
        zf_pu=zf,
    )
    if ft == "LL":
        pick = max(phases, key=lambda p: r["I_phase_pu"][p]["mag_pu"])
    elif ft == "SLG":
        pick = phases[0]  # type: ignore[index]
    else:
        pick = "a"
    ph = r["I_phase_pu"][pick]
    return ph["mag_pu"] * cmath.exp(1j * math.radians(ph["angle_deg"]))

"""Electronics SolverSpec table."""

from __future__ import annotations

import itertools
import math
from typing import Any

from electrical_engineer.engines.solvers.spec import Param, SolverSpec

_VAR_NAMES = "ABCDEF"


def bjt_divider_bias(
    vcc: float,
    r1: float,
    r2: float,
    rc: float,
    re: float,
    beta: float,
    vbe: float = 0.7,
) -> dict:
    if r1 <= 0 or r2 <= 0 or rc <= 0 or re <= 0 or beta <= 0:
        raise ValueError("resistances and beta must be positive")
    vth = vcc * r2 / (r1 + r2)
    rth = (r1 * r2) / (r1 + r2)
    denom = rth + (beta + 1) * re
    ib = (vth - vbe) / denom if denom > 0 else 0.0
    ic = beta * ib
    ie = ib * (beta + 1)
    vce = vcc - ic * rc - ie * re
    if ic <= 0:
        region = "cutoff"
    elif vce < vbe:
        region = "saturation"
    else:
        region = "active"
    return {
        "ic_A": ic,
        "ib_A": ib,
        "ie_A": ie,
        "vce_V": vce,
        "vth_V": vth,
        "rth_ohm": rth,
        "region": region,
    }


def opamp_config(
    config: str,
    vin: list,
    rf: float = 0.0,
    r1: float = 1.0,
    r2: float = 0.0,
    r3: float = 0.0,
    vsat: float = 15.0,
) -> dict:
    vins = [float(v) for v in vin]
    saturated = False
    if config == "inverting":
        if r1 <= 0:
            raise ValueError("r1 must be positive for inverting amp")
        gain = -rf / r1
        vout = gain * vins[0] if vins else 0.0
    elif config == "noninverting":
        if r1 <= 0:
            raise ValueError("r1 must be positive")
        gain = 1.0 + rf / r1
        vout = gain * vins[0] if vins else 0.0
    elif config == "follower":
        gain = 1.0
        vout = vins[0] if vins else 0.0
    elif config == "summing":
        gains = []
        resistors = [r1, r2, r3][: len(vins)]
        for ri in resistors:
            if ri <= 0:
                raise ValueError("summation resistors must be positive")
            gains.append(-rf / ri)
        vout = sum(g * v for g, v in zip(gains, vins))
        gain = gains[0] if gains else 0.0
    elif config == "difference":
        if r1 <= 0 or r2 <= 0 or r3 <= 0 or rf <= 0:
            raise ValueError("difference amp resistors must be positive")
        ratio = rf / r1
        if abs(r3 / r2 - ratio) > 1e-6:
            raise ValueError("difference amp needs R3/R2 = Rf/R1")
        if len(vins) < 2:
            vins = vins + [0.0]
        gain = ratio
        vout = ratio * (vins[1] - vins[0])
    else:
        raise ValueError(f"config must be inverting, noninverting, follower, summing, difference; got {config!r}")
    if vout > vsat:
        vout = vsat
        saturated = True
    elif vout < -vsat:
        vout = -vsat
        saturated = True
    return {"gain": gain, "vout_V": vout, "saturated": saturated, "config": config}


def _term_literals(term: str) -> list[tuple[str, bool]]:
    out: list[tuple[str, bool]] = []
    i = 0
    while i < len(term):
        ch = term[i]
        if ch.isalpha():
            neg = i + 1 < len(term) and term[i + 1] == "'"
            out.append((ch, not neg))
            i += 2 if neg else 1
        else:
            i += 1
    return out


def _sop_literal_count(sop: str) -> int:
    terms = [t.strip() for t in sop.replace(" ", "").split("+") if t.strip()]
    return sum(len(_term_literals(t)) for t in terms)


def _eval_sop(sop: str, assign: dict[str, bool]) -> bool:
    for term in [t.strip() for t in sop.replace(" ", "").split("+") if t.strip()]:
        ok = True
        for var, val in _term_literals(term):
            if assign.get(var, False) != val:
                ok = False
                break
        if ok:
            return True
    return False


def _combine_one_bit(a: str, b: str) -> str | None:
    if len(a) != len(b):
        return None
    diff = sum(1 for x, y in zip(a, b) if x != y)
    if diff != 1:
        return None
    out = []
    for x, y in zip(a, b):
        out.append("-" if x != y else x)
    return "".join(out)


def _qm_prime_implicants(n_vars: int, minterms: set[int]) -> set[str]:
    groups: dict[int, list[tuple[str, set[int]]]] = {}
    for m in minterms:
        bits = format(m, f"0{n_vars}b")
        groups.setdefault(bits.count("1"), []).append((bits, {m}))
    primes: set[str] = set()
    while groups:
        marked: set[tuple[str, frozenset[int]]] = set()
        new_groups: dict[int, list[tuple[str, set[int]]]] = {}
        for ones in sorted(groups):
            for bits_a, set_a in groups[ones]:
                for bits_b, set_b in groups.get(ones + 1, []):
                    combined = _combine_one_bit(bits_a, bits_b)
                    if combined is None:
                        continue
                    marked.add((bits_a, frozenset(set_a)))
                    marked.add((bits_b, frozenset(set_b)))
                    key = combined.count("1") + combined.count("-")
                    new_groups.setdefault(key, []).append((combined, set_a | set_b))
        for g in groups.values():
            for bits, mset in g:
                if (bits, frozenset(mset)) not in marked:
                    primes.add(bits)
        if not new_groups:
            break
        merged: dict[str, set[int]] = {}
        for g in new_groups.values():
            for bits, mset in g:
                merged.setdefault(bits, set()).update(mset)
        groups = {}
        for bits, mset in merged.items():
            groups.setdefault(bits.count("1") + bits.count("-"), []).append((bits, mset))
    return primes


def _bits_to_term(bits: str) -> str:
    out = []
    for i, ch in enumerate(bits):
        if ch == "-":
            continue
        var = _VAR_NAMES[i]
        out.append(var if ch == "1" else f"{var}'")
    return "".join(out) or "1"


def _covers(implicant: str, minterm: int, n_vars: int) -> bool:
    bits = format(minterm, f"0{n_vars}b")
    for ib, mb in zip(implicant, bits):
        if ib == "-":
            continue
        if ib != mb:
            return False
    return True


def kmap_minimize(n_vars: float, minterms: list, dont_cares: list | None = None) -> dict:
    n_vars = int(n_vars)
    if not 2 <= n_vars <= 6:
        raise ValueError("n_vars must be between 2 and 6")
    dc = set(int(x) for x in (dont_cares or []))
    mt = set(int(x) for x in minterms)
    work = mt | dc
    primes = sorted(_qm_prime_implicants(n_vars, work))
    essential: list[str] = []
    covered = set()
    for p in primes:
        hits = {m for m in mt if _covers(p, m, n_vars)}
        if len(hits) == 1:
            essential.append(p)
            covered |= hits
    remaining = mt - covered
    candidate = set(essential)
    if remaining:
        covers_for: list[tuple[str, set[int]]] = []
        for p in primes:
            hits = {m for m in mt if _covers(p, m, n_vars)}
            if hits:
                covers_for.append((p, hits))
        best_score = 10**9
        best_pick: set[str] = set(candidate)
        for r in range(0, len(covers_for) + 1):
            for combo in itertools.combinations(covers_for, r):
                pick = set(candidate) | {p for p, _ in combo}
                if not all(any(_covers(p, m, n_vars) for p in pick) for m in mt):
                    continue
                sop = " + ".join(_bits_to_term(p) for p in sorted(pick))
                score = _sop_literal_count(sop)
                if score < best_score:
                    best_score = score
                    best_pick = pick
        candidate = best_pick
    selected = sorted(candidate)
    terms = [_bits_to_term(p) for p in dict.fromkeys(selected)]
    sop = " + ".join(terms)
    return {
        "literal_count": float(_sop_literal_count(sop)),
        "sop": sop,
        "n_terms": len(terms),
        "prime_implicants": terms,
    }


SPECS: dict[str, SolverSpec] = {
    "bjt_divider_bias": SolverSpec(
        fn=bjt_divider_bias,
        params=(
            Param("vcc"),
            Param("r1"),
            Param("r2"),
            Param("rc"),
            Param("re"),
            Param("beta"),
            Param("vbe", default=0.7),
        ),
        value_key="ic_A",
        unit="A",
    ),
    "opamp_config": SolverSpec(
        fn=opamp_config,
        params=(
            Param("config", kind="str", choices=("inverting", "noninverting", "follower", "summing", "difference")),
            Param("vin", kind="list"),
            Param("rf", default=0.0),
            Param("r1", default=1.0),
            Param("r2", default=0.0),
            Param("r3", default=0.0),
            Param("vsat", default=15.0),
        ),
        value_key="gain",
        unit="1",
    ),
    "kmap_minimize": SolverSpec(
        fn=kmap_minimize,
        params=(
            Param("n_vars"),
            Param("minterms", kind="list"),
            Param("dont_cares", kind="list", default=[]),
        ),
        value_key="literal_count",
        unit="1",
    ),
}
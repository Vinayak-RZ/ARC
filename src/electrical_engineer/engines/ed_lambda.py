"""N-unit economic dispatch by λ-iteration with limits (EEC-301 Exp 8)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

UnitStatus = Literal["free", "at_min", "at_max"]


@dataclass(frozen=True)
class EdUnit:
    a: float
    b: float
    c: float
    pmin: float
    pmax: float


@dataclass(frozen=True)
class EdCase:
    units: tuple[EdUnit, ...]

    @classmethod
    def from_coeff_lists(
        self,
        a: list[float],
        b: list[float],
        c: list[float],
        pmin: list[float],
        pmax: list[float],
    ) -> EdCase:
        return EdCase(
            units=tuple(EdUnit(a[i], b[i], c[i], pmin[i], pmax[i]) for i in range(len(a)))
        )

    @classmethod
    def eec301_default(cls) -> EdCase:
        return cls.from_coeff_lists(
            a=[500.0, 400.0, 200.0],
            b=[5.3, 5.5, 5.8],
            c=[0.004, 0.006, 0.009],
            pmin=[50.0, 30.0, 20.0],
            pmax=[300.0, 150.0, 120.0],
        )


def incremental_cost(p: float, unit: EdUnit) -> float:
    return unit.b + 2.0 * unit.c * p


def fuel_cost(p: float, unit: EdUnit) -> float:
    return unit.a + unit.b * p + unit.c * p * p


def _dispatch_free_lambda(lam: float, free: list[int], case: EdCase) -> list[float]:
    p = [0.0] * len(case.units)
    for i in free:
        u = case.units[i]
        if u.c <= 0:
            raise ValueError("positive quadratic c required for λ dispatch")
        p[i] = (lam - u.b) / (2.0 * u.c)
    return p


def solve_lambda_ed(case: EdCase, pd_mw: float, *, max_iter: int = 50) -> dict[str, Any]:
    """Iterative λ on free set with limit fixing (Kuhn–Tucker)."""
    n = len(case.units)
    status: list[UnitStatus] = ["free"] * n
    p = [0.0] * n

    for _ in range(max_iter):
        free = [i for i in range(n) if status[i] == "free"]
        fixed_sum = sum(p[i] for i in range(n) if status[i] != "free")
        demand = pd_mw - fixed_sum
        if not free:
            break
        inv_2c = sum(1.0 / (2.0 * case.units[i].c) for i in free)
        sum_b_2c = sum(case.units[i].b / (2.0 * case.units[i].c) for i in free)
        lam = (demand + sum_b_2c) / inv_2c
        p_try = _dispatch_free_lambda(lam, free, case)
        changed = False
        for i in free:
            u = case.units[i]
            if p_try[i] < u.pmin:
                p[i] = u.pmin
                status[i] = "at_min"
                changed = True
            elif p_try[i] > u.pmax:
                p[i] = u.pmax
                status[i] = "at_max"
                changed = True
            else:
                p[i] = p_try[i]
        if not changed:
            lam = incremental_cost(p[free[0]], case.units[free[0]])
            break

    ic = [incremental_cost(p[i], case.units[i]) for i in range(n)]
    costs = [fuel_cost(p[i], case.units[i]) for i in range(n)]
    return {
        "PD": pd_mw,
        "lam": lam,
        "P": p,
        "IC": ic,
        "C": costs,
        "total_cost": sum(costs),
        "status": status,
        "sum_P": sum(p),
    }

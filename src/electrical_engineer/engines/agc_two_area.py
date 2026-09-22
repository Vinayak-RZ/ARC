"""Two-area primary / AGC linear OSS twin (EEC-301 Exp 7, Simulink Fig. 1 parity)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Literal

RunKind = Literal["primary", "agc", "area2_disturbance"]


@dataclass(frozen=True)
class AreaParams:
    tg: float
    tt: float
    m: float
    d: float
    r: float
    b: float
    k: float


@dataclass(frozen=True)
class TwoAreaAgcCase:
    area1: AreaParams
    area2: AreaParams
    tie_sync_gain: float = 2.0
    f0_hz: float = 60.0
    base_mva: float = 1000.0

    @classmethod
    def eec301_default(cls) -> TwoAreaAgcCase:
        return cls(
            area1=AreaParams(tg=0.2, tt=0.5, m=10.0, d=0.6, r=0.05, b=20.6, k=0.0),
            area2=AreaParams(tg=0.3, tt=0.6, m=8.0, d=0.9, r=0.0625, b=16.9, k=0.0),
            tie_sync_gain=2.0,
            f0_hz=60.0,
            base_mva=1000.0,
        )

    def with_k(self, k: float) -> TwoAreaAgcCase:
        a1 = self.area1
        a2 = self.area2
        return TwoAreaAgcCase(
            area1=AreaParams(a1.tg, a1.tt, a1.m, a1.d, a1.r, a1.b, k),
            area2=AreaParams(a2.tg, a2.tt, a2.m, a2.d, a2.r, a2.b, k),
            tie_sync_gain=self.tie_sync_gain,
            f0_hz=self.f0_hz,
            base_mva=self.base_mva,
        )

    def with_bias_b1(self, b1: float) -> TwoAreaAgcCase:
        a1 = self.area1
        return TwoAreaAgcCase(
            area1=AreaParams(a1.tg, a1.tt, a1.m, a1.d, a1.r, b1, a1.k),
            area2=self.area2,
            tie_sync_gain=self.tie_sync_gain,
            f0_hz=self.f0_hz,
            base_mva=self.base_mva,
        )


def _derivatives(
    state: list[float],
    pl1: float,
    pl2: float,
    case: TwoAreaAgcCase,
) -> list[float]:
    df1, df2, xg1, xm1, xg2, xm2, p12, xi1, xi2 = state
    a1, a2 = case.area1, case.area2
    ace1 = a1.b * df1 + p12
    ace2 = a2.b * df2 - p12
    u1 = a1.k * xi1
    u2 = a2.k * xi2
    dxg1 = (-df1 / a1.r - u1 - xg1) / a1.tg
    dxm1 = (xg1 - xm1) / a1.tt
    dxg2 = (-df2 / a2.r - u2 - xg2) / a2.tg
    dxm2 = (xg2 - xm2) / a2.tt
    ddf1 = (xm1 - pl1 - a1.d * df1 - p12) / a1.m
    ddf2 = (xm2 - pl2 - a2.d * df2 + p12) / a2.m
    dp12 = case.tie_sync_gain * (df1 - df2)
    dxi1 = ace1
    dxi2 = ace2
    return [ddf1, ddf2, dxg1, dxm1, dxg2, dxm2, dp12, dxi1, dxi2]


def _rk4_step(state: list[float], h: float, pl1: float, pl2: float, case: TwoAreaAgcCase) -> list[float]:
    def f(s: list[float]) -> list[float]:
        return _derivatives(s, pl1, pl2, case)

    k1 = f(state)
    s2 = [state[i] + 0.5 * h * k1[i] for i in range(len(state))]
    k2 = f(s2)
    s3 = [state[i] + 0.5 * h * k2[i] for i in range(len(state))]
    k3 = f(s3)
    s4 = [state[i] + h * k3[i] for i in range(len(state))]
    k4 = f(s4)
    return [
        state[i] + (h / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i])
        for i in range(len(state))
    ]


def simulate_two_area(
    case: TwoAreaAgcCase,
    *,
    h_s: float = 0.001,
    t_end_s: float = 50.0,
    step_time_s: float = 1.0,
    dpl1_pu: float = 0.1,
    dpl2_pu: float = 0.0,
    run: RunKind = "primary",
) -> dict[str, Any]:
    """Load step in area 1 by default (Exp 7 Run 1/2)."""
    if run == "area2_disturbance":
        dpl1_pu, dpl2_pu = 0.0, 0.1
    k = 0.0 if run == "primary" else case.area1.k
    if run == "agc":
        k = case.area1.k if case.area1.k > 0 else 0.3
    sim_case = case.with_k(k)

    state = [0.0] * 9
    t = 0.0
    trail: list[tuple[float, list[float]]] = [(0.0, state.copy())]
    min_f1_hz = 0.0
    min_t_after = 0.0
    max_p12_pu = 0.0
    max_p12_t = 0.0
    diverged = False

    while t < t_end_s:
        pl1 = dpl1_pu if t >= step_time_s else 0.0
        pl2 = dpl2_pu if t >= step_time_s else 0.0
        state = _rk4_step(state, h_s, pl1, pl2, sim_case)
        t += h_s
        trail.append((t, state.copy()))
        df1, df2, _, xm1, _, xm2, p12, _, _ = state
        f1_hz = df1 * sim_case.f0_hz
        if t >= step_time_s and f1_hz < min_f1_hz:
            min_f1_hz = f1_hz
            min_t_after = t - step_time_s
        if abs(p12) > abs(max_p12_pu):
            max_p12_pu = p12
            max_p12_t = t
        if abs(df1) > 0.5 or abs(df2) > 0.5 or abs(p12) > 2.0:
            diverged = True
            break

    df1, df2, _, xm1, _, xm2, p12, _, _ = state
    mva = sim_case.base_mva
    return {
        "steady": {
            "df1_pu": df1,
            "df2_pu": df2,
            "df1_hz": df1 * sim_case.f0_hz,
            "df2_hz": df2 * sim_case.f0_hz,
            "P12_pu": p12,
            "P12_MW": p12 * mva,
            "Pm1_pu": xm1,
            "Pm2_pu": xm2,
            "Pm1_MW": xm1 * mva,
            "Pm2_MW": xm2 * mva,
        },
        "first_dip": {"f1_Hz": min_f1_hz, "t_after_step": min_t_after},
        "peak_P12": {"P12_MW": max_p12_pu * mva, "P12_pu": max_p12_pu, "t": max_p12_t},
        "diverged": diverged,
        "trail": trail,
    }


def analytic_primary_steady(dpl1_pu: float, beta1: float = 20.6, beta2: float = 16.9) -> dict[str, float]:
    df = -dpl1_pu / (beta1 + beta2)
    p12 = -beta2 / (beta1 + beta2) * dpl1_pu
    pm1 = dpl1_pu + p12
    pm2 = -p12
    return {"df_pu": df, "df_hz": df * 60.0, "P12_pu": p12, "Pm1_pu": pm1, "Pm2_pu": pm2}


def gain_sweep(
    case: TwoAreaAgcCase,
    gains: list[float],
    *,
    h_s: float = 0.001,
    t_end_s: float = 60.0,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for k in gains:
        out = simulate_two_area(case.with_k(k), h_s=h_s, t_end_s=t_end_s, run="agc")
        st = out["steady"]
        rows.append(
            {
                "K": k,
                "peak_df1_Hz": out["first_dip"]["f1_Hz"],
                "peak_P12_MW": out["peak_P12"]["P12_MW"],
                "diverged": out["diverged"],
                "ss_df1_Hz": st["df1_hz"] if not out["diverged"] else None,
                "ss_P12_MW": st["P12_MW"] if not out["diverged"] else None,
            }
        )
    return rows

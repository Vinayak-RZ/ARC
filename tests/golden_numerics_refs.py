"""Checked headline numerics for independent test engineer goldens."""

from __future__ import annotations

import math

HEADLINE_RLC_R_OHM = 10.0
HEADLINE_RLC_L_H = 0.01
HEADLINE_RLC_C_F = 100e-6
HEADLINE_RLC_VIN = 10.0
HEADLINE_RLC_ZETA = 0.5
HEADLINE_RLC_WN_RAD_S = 1000.0
HEADLINE_RLC_VC_PEAK_V = 11.630
HEADLINE_RLC_T_PEAK_S = 3.628e-3


def hw3_discontinuous_vo_v(v_ll_rms: float, alpha_deg: float) -> float:
    vm = math.sqrt(2) * v_ll_rms / math.sqrt(3)
    alpha = math.radians(alpha_deg)
    return (3.0 * vm / (2.0 * math.pi)) * (1.0 + math.cos(alpha + math.pi / 6))


HEADLINE_RECTIFIER_VO_V = 203.7
HEADLINE_CONTROL_Y_SS = 10.0 / 11.0
HEADLINE_CONTROL_TS_S = math.log(50.0) / 11.0
HEADLINE_IDMT_T_S = 2.971
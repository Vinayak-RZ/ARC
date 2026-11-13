"""Equal-area analytics for SMIB plots (engine-sourced angles)."""

from __future__ import annotations

import numpy as np

from electrical_engineer.engines.smib_swing import SmibCase, eec301_reference


def equal_area_energies(case: SmibCase) -> dict[str, float]:
    ref = eec301_reference(case)
    d0 = ref["delta0_rad"]
    dcr = ref["delta_cr_rad"]
    dmax = ref["delta_max_rad"]
    n = 400
    d1 = np.linspace(d0, dcr, n)
    pe_f = case.pmax_fault_pu * np.sin(d1)
    trap = np.trapezoid
    a1 = float(trap(np.maximum(case.pm_pu - pe_f, 0.0), d1))
    d2 = np.linspace(dcr, dmax, n)
    pe_p = case.pmax_post_pu * np.sin(d2)
    a2 = float(trap(np.maximum(pe_p - case.pm_pu, 0.0), d2))
    return {
        **ref,
        "A1_accel_rad": a1,
        "A2_decel_rad": a2,
        "delta0_deg": ref["delta0_deg"],
        "delta_cr_deg": ref["delta_cr_deg"],
        "delta_max_deg": ref["delta_max_deg"],
    }

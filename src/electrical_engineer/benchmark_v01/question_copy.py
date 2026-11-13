"""Textbook-style benchmark questions from givens (no repo coupling)."""

from __future__ import annotations

from typing import Any

from electrical_engineer.benchmark_v01.sanitize import clean_question_text


def _fmt_task_dir(name: str) -> str:
    return name.replace("-", " ").replace("_", " ")


def _template_question(item_name: str, pack: str, givens: dict[str, Any]) -> str | None:
    if item_name == "rc-step-01":
        return (
            f"A series RC circuit has V={givens['v']} V, R={givens['r']} ohm, "
            f"C={givens['c']} F. Find the capacitor voltage (V) at t={givens['t']} s."
        )
    if item_name == "divider-dc-01":
        return (
            f"A DC voltage divider has Vin={givens.get('vin_V', 10)} V, "
            f"R1={givens.get('r1_ohm', 1000)} ohm, R2={givens.get('r2_ohm', 1000)} ohm. "
            "Find Vout at the R1-R2 junction (V)."
        )
    if item_name == "breakaway-3pole-01":
        poles = givens.get("poles", [])
        return (
            f"Unity-feedback system: open-loop poles at {poles} on the real axis. "
            "Find the breakaway point coordinate sigma on the real axis."
        )
    if item_name == "margin-40-01":
        num = givens.get("num", [])
        den = givens.get("den", [])
        return (
            f"Plant G(s) has numerator coeffs {num} and denominator coeffs {den} (s-domain). "
            "Report gain margin in dB for the unity-feedback loop."
        )
    if item_name == "smib-eec301-01":
        return (
            "Single-machine-infinite-bus equal-area: from the SMIB parameters in givens "
            "(H, f0, Pm, Pmax pre/fault/post in pu), find delta0 (deg), delta_cr (deg), "
            "and critical clearing time tcr (s) using handwritten RK4 (no ode45)."
        )
    if item_name == "agc-eec301-01":
        return (
            "Two-area primary-frequency and AGC twin: using area parameters, tie gain, "
            "and load step in givens, report primary steady-state Area-1 frequency (Hz) and "
            "AGC steady-state Area-1 frequency (Hz) after load step."
        )
    if item_name == "ed-eec301-01":
        return (
            "Three-unit economic dispatch with quadratic costs and limits in givens: "
            "for each PD (MW) case listed, report lambda (Rs/MWh) and unit MW allocations."
        )
    if item_name == "ed-penalty-t13-01":
        return (
            f"Three generators with quadratic costs and loss matrix B; total demand "
            f"Pd={givens.get('pd_mw')} MW. Run λ-iteration with B-based penalty factors "
            "until MW balance converges. Report converged λ (Rs/MWh)."
        )
    if item_name in ("lg-01", "ll-01", "llg-bc-01"):
        return (
            f"Sequence-network fault: type {givens.get('fault_type', 'LG')}, "
            f"V_pre={givens.get('v_prefault_pu', 1.0)} pu, "
            f"Z1={givens.get('z1_pu', 0.1)} pu, Z2={givens.get('z2_pu', 0.1)} pu, "
            f"Z0={givens.get('z0_pu', 0.3)} pu. Report |Ifault| (pu)."
        )
    if item_name == "protection-oc-01":
        return (
            f"OC relay: CT {givens.get('ct_primary_a')} A : {givens.get('ct_secondary_a')} A, "
            f"pickup {givens.get('relay_pickup_a')} A secondary, "
            f"fault current {givens.get('fault_current_a')} A primary. "
            "Does the relay trip? Answer 1 if yes, 0 if no."
        )
    if item_name == "pu-base-12-01":
        return (
            "Aggregate positive-sequence fault impedance at the fault bus from the "
            "per-unit element data and system base in givens. Report |Z1| (pu)."
        )
    if item_name == "steady-state-type1-01":
        return (
            f"Type-{givens.get('system_type', 1)} unity-feedback loop with gain "
            f"K={givens.get('gain')}. Find ramp-error coefficient ess (dimensionless)."
        )
    if item_name == "block-feedback-01":
        return (
            "Unity negative feedback: forward path G(s)=10/(s+1), feedback H(s)=1. "
            "Find closed-loop DC gain (value of C/R with unit step reference)."
        )
    if item_name == "digital-pole-01":
        return (
            f"Discrete plant G(z) with num={givens.get('num')} den={givens.get('den')} "
            f"and sample time Ts={givens.get('ts', 0.01)} s. "
            "Report max(|z|-plane pole|)."
        )
    return None


def eval_question(
    item_name: str,
    pack: str,
    givens: dict[str, Any],
    *,
    task_md: str = "",
) -> str:
    templated = _template_question(item_name, pack, givens)
    if templated:
        return templated
    if task_md:
        cleaned = clean_question_text(task_md)
        if cleaned and "recipe" not in cleaned.lower() and "arc " not in cleaned.lower():
            return cleaned
    return f"Undergraduate {pack} problem ({_fmt_task_dir(item_name)}). Use all numeric givens with units."

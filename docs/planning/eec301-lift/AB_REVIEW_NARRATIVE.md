# A/B review — narrative traps T3–T5, T7–T10

| Trap | Bare failure | Arc unlock |
|------|--------------|------------|
| T3 | f0 vs ω_s, H vs M mixup | `SmibCase.accel_coeff`, agc `f0=60` in exp07 |
| T4 | ACE sign, B≠β | `agc_two_area` ACE/tie signs, skill |
| T5 | AGC vs primary confusion | exp07 primary vs AGC steady table |
| T7 | IC missing 2cP | `incremental_cost()` |
| T8 | Wrong LFC diagram | ui-diagrams PSA rules + T8 knowledge |
| T9 | ode45 / fmincon | T9 knowledge + host cards |
| T10 | Wrong Pm/Pmax defaults | `validate_smib_case()` |

Scripted checks: T1, T2, T6 (`test_trap_ablation.py`). Others: knowledge + manual review prompts in `BARE_AGENT_FAILURE_NOTES.md`.

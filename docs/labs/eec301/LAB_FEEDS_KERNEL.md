# How the EEC-301 lab pack feeds Arc

```text
Lab solve (Exps 6–8) → bare-agent failure notes → trap id (T1–T10)
  → skill + knowledge/traps + engine helper + golden JSON
  → pytest + eval/gold + (W7) ablation harness
```

| Exp | Lab golden | Arc engine | Skill | Traps |
|-----|------------|------------|-------|-------|
| 6 | `exp06.json` | `smib_swing` | `swing-equation` | T1–T3, T9, T10 |
| 7 | `exp07.json` | `agc_two_area` | `agc-two-area` | T4–T5, T8–T9 |
| 8 | `exp08.json` | `ed_lambda` | `economic-dispatch-lambda` | T6–T7, T9–T10 |

Lab **source code** stays outside Arc; only JSON goldens and trap narratives are vendored.

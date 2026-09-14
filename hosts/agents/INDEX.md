# EE specialists — host-spawned catalog

Canonical cards the **rented host** (Cursor, Codex, Claude Code) can spawn.
This is not a second Arc loop. CLI / MCP / UI never start these children.

**Count: 12** spawnable specialists.

Install into a **homework** tree (never this product `.cursor/`):

```text
electrical-engineer hosts install --into <homework> --host all
```

Law: [`../adapters/specialist-body.md`](../adapters/specialist-body.md).
OpenMontage analog: domain cards live in this tree; host dirs are copies.

| File | Spawn name | Use for |
|------|------------|---------|
| [ee-circuits.md](ee-circuits.md) | `ee-circuits` | KCL/KVL, phasors, transients, Thevenin, two-ports |
| [ee-signals.md](ee-signals.md) | `ee-signals` | LTI, convolution, Fourier/Laplace/z, sampling |
| [ee-electronics.md](ee-electronics.md) | `ee-electronics` | devices, op-amps, small-signal, UG digital |
| [ee-machines.md](ee-machines.md) | `ee-machines` | transformers, DC/IM/synchronous equivalent circuits |
| [ee-power.md](ee-power.md) | `ee-power` | per-unit, load flow, faults, study-level protection |
| [ee-control.md](ee-control.md) | `ee-control` | TF/SS, Routh, Bode/Nyquist, simple compensators |
| [ee-power-electronics.md](ee-power-electronics.md) | `ee-power-electronics` | rectifiers, buck/boost, PWM, averaged models |
| [ee-measurements.md](ee-measurements.md) | `ee-measurements` | errors, bridges, instrument specs |
| [ee-em.md](ee-em.md) | `ee-em` | electrostatics, magnetostatics, TEM lines at UG |
| [ee-maths.md](ee-maths.md) | `ee-maths` | complex algebra, ODE/Laplace/Fourier as EE tools |
| [ee-cross.md](ee-cross.md) | `ee-cross` | unmatched or multi-pack; no auto-SPICE |
| [ee-simulink.md](ee-simulink.md) | `ee-simulink` | `.slx` / block-diagram labs via Arc MCP only |

Skills (method, parent window) stay under `skills/<pack>/SKILL.md`. Do not
confuse the 12 spawnable agents with 10 undergraduate packs or 27 recipes.

At most two live children. Local same-checkout only. No nested Task.

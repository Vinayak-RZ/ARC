# T1 host harness — pack specialists as the lead host

Lead acted as Cursor/Codex: load pack `SKILL.md`, call live EE MCP (`handle` / stdio), score **capability path + `unchecked` honesty**, not eloquence. MATLAB MCP was never on the host `tools/list`.

Recorded 2026-09-14. Result column uses `pass` or `fail`.

| Pack | Question | Capability | Result | Evidence |
|------|----------|------------|--------|----------|
| circuits | Find Vout of a 10 V divider R1=R2=1k. | lumped-circuit-sim | pass | Skill + retrieve called; `propose_composition` apply false wrote plan.md |
| signals | Is y[n]=x[n]+x[n-1] LTI? Convolution vs SPICE. | signal-analysis | pass | retrieve empty visible; no auto-SPICE in skill |
| electronics | Ideal op-amp inverting gain for Rf=10k Rin=1k. | algebraic-check | pass | retrieve empty; capability graph validate-only |
| machines | OC/SC test: find equivalent-circuit Rm Xm. | machine-model | pass | retrieve empty; CD-MACHINES-FEA still in skill |
| power | Three-bus study-level \|V\| at bus 2; no EMS. | power-network-study | pass | retrieve empty; no pandapower case invented |
| control | Routh for s^3+2s^2+s+k. Bode only with typed TF. | lti-analysis | pass | retrieve empty; skill forbids simulate-circuit default |
| power_electronics | Buck CCM V=D Vin. No HIL. | converter-model | pass | retrieve empty; CD-PE-HIL remains |
| measurements | Wheatstone limiting error. No live bench. | measurement-model | pass | retrieve empty; CD-MEAS-BENCH remains |
| em | E of infinite line charge. Not HFSS. | fields-analytic | pass | retrieve empty; CD-EM-HFSS remains |
| maths | Laplace of e^{-at}u(t). Not a CAS replacement. | algebraic-check | pass | retrieve empty; second-slot pack |
| _cross | Unmatched text with no netlist. | label-unverified | pass | Skill forbids auto-spice; retrieve scaffold present |

Spawn names checked on disk: `ee-circuits` … `ee-maths`, `ee-cross`. `electrical-engineer hosts install --into` temp dir; product `.cursor/agents` still absent.

Score rule: pass = pack skill names the capability, retrieve was called, composition did not wait, host tools/list has no MATLAB, specialist law forbids `evaluate_matlab_code`.

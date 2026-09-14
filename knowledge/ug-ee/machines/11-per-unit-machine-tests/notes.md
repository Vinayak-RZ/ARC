# Per-unit machines and standard tests

Per-unit (pu) notation is the natural language of machine nameplates and of power-system studies. A 0.08 pu transformer impedance and a 1.2 pu synchronous reactance mean something independent of whether the machine is 5 kVA or 500 MVA. This unit is how to pick bases, how to change base, and how the standard tests — transformer OC/SC, DC resistance, induction-machine no-load and blocked-rotor, alternator OCC/SCC/ZPF, and retardation/heat-run sketches — populate an equivalent circuit in ohms and in pu. It ties the pack together. Tests already introduced in earlier units are collected here with pu arithmetic and with the practical limits (temperature, reduced frequency, saturation).

The discipline: never add a 4 Ω rotor to a 400 V stator without a base. Convert to pu on a common VA and voltage base, or refer to one side in ohms, then proceed.

## Concepts

A base triad for a single-phase machine: \(S_b\), \(V_b\), then \(I_b=S_b/V_b\), \(Z_b=V_b/I_b=V_b^2/S_b\). Three-phase: \(S_b\) total three-phase VA, \(V_b\) line-to-line, \(I_b=S_b/(\sqrt{3}V_b)\), \(Z_b=V_{ph}/I_{ph}=V_L^2/S_{3\phi}\). The last identity is the one to memorize: \(Z_b=V_{LL}^2/S_{3\phi}\). Motor nameplates often give kW and PF, not kVA; \(S_b\) is still rated VA if you can reconstruct it, or rated kW as an approximate base when the problem says so. Do not mix.

Per-unit impedance \(Z_\mathrm{pu}=Z_\Omega/Z_b\). Per-unit current \(I_\mathrm{pu}=I/I_b\). Kirchhoff’s laws hold in pu if every quantity in an equation is pu on the same base (or you keep \(\sqrt{3}\) consistent). Transformer \(a\) disappears in pu if primary and secondary bases follow the turns ratio: \(V_{b2}=V_{b1}/a\), then a 0.05 pu series impedance is 0.05 pu on both sides.

Base change: \(Z_{\mathrm{pu,new}}=Z_{\mathrm{pu,old}}\times (S_{b,\mathrm{new}}/S_{b,\mathrm{old}})\times (V_{b,\mathrm{old}}/V_{b,\mathrm{new}})^2\). A 0.08 pu transformer on 10 MVA becomes 0.16 pu on 20 MVA at the same kV. Machine \(X_s\) from the manufacturer is on the machine’s own MVA and kV; on a system study base it must be scaled.

Standard tests, transformers: OC at rated voltage (shunt), SC at rated current (series), DC winding resistance (split \(R_1,R_2\), temperature correct to 75 °C). Turns ratio test. Polarity/vector-group. Insulation (megger, tanδ) is not an equivalent-circuit test.

Induction machines: (1) DC stator resistance per phase. (2) No-load: rated voltage, no shaft load, measure \(V,I_0,P_0\). Separates rotational loss plus core plus a little stator Cu \(3I_0^2 R_1\). Remainder assigned to \(R_c\) and \(X_m\). (3) Blocked-rotor: rotor locked, reduced voltage, rated current, \(V_\mathrm{br},I_\mathrm{br},P_\mathrm{br}\). Gives \(R_1+R_2'\) and \(X_1+X_2'\). Frequency: IEEE recommends a reduced frequency (near 25 Hz) for some designs so leakage matches running slip; many UG labs use 50 Hz and accept the error. Split of \(X_1\) and \(X_2'\) by NEMA class (A/B 50/50, C/D different). (4) Optional: no-load curve versus voltage to separate core from F&W (F&W from the intercept of \(P\) vs \(V^2\)).

Synchronous machines: OCC, SCC, armature resistance, and optionally ZPF lagging for Potier. Slip test for \(X_q\) (salient): reduced V, slip a few percent, field open, oscilloscope of \(I\) or \(V\); \(X_d\) and \(X_q\) from max/min. Maximum-lagging-current test as a \(X_q\) check. Sudden short-circuit for \(X_d',X_d'',T_d'\) (transient) is a power-system test, UG-intro only: the envelope of AC current has subtransient, transient, and synchronous periods.

DC machines: OCC at constant speed, load magnetization, brake test or Swinburne (no-load + calculated Cu) for efficiency. Hopkinson (back-to-back two machines) for a full-load heat run with a small supply. Retardation test: decelerate, \(J\omega\mathrm{d}\omega/\mathrm{d}t=-P_\mathrm{rot}(\omega)\).

Heat run: temperature rise by resistance (copper) and by thermometer/embedded detector (iron, coolant). Limits are insulation class (B, F, H). Equivalent-circuit \(R\) should be at the specified temperature.

Efficiency from tests: transformer \(\eta\) from OC and SC losses without actually loading. Induction motor: circle diagram or equivalent circuit; input-output (brake) is the ground truth. “Summation of losses” is the standard-test philosophy: measure each loss at convenient conditions, sum, rather than subtract two large powers.

Per-unit time and inertia: \(H\) in seconds is already pu energy / base VA. The swing equation in the previous unit used that. Electrical radians versus mechanical: \(\delta\) in electrical rad, \(\omega_s=2\pi f\).

Nameplate %IZ for a transformer is \(Z_\mathrm{pu}\times 100\) on the transformer base. Short-circuit current on an infinite bus is \(1/Z_\mathrm{pu}\) times rated. A motor starting current 6 pu is 6 times rated current, not 6 times magnetizing.

## Equations

Bases (3-phase):

\[
I_b=\frac{S_b}{\sqrt{3}V_b},\qquad Z_b=\frac{V_b^2}{S_b},\qquad Y_b=1/Z_b.
\]

Base change:

\[
Z_{\mathrm{pu}2}=Z_{\mathrm{pu}1}\frac{S_{b2}}{S_{b1}}\left(\frac{V_{b1}}{V_{b2}}\right)^2.
\]

Transformer SC:

\[
Z_{\mathrm{pu}}=\frac{V_\mathrm{SC}/V_\mathrm{rated}}{I_\mathrm{SC}/I_\mathrm{rated}}\approx \frac{V_\mathrm{SC}}{V_\mathrm{rated}}\quad\text{at rated current}.
\]

IM blocked-rotor:

\[
Z_\mathrm{br}=\frac{V_{\mathrm{br,ph}}}{I_{\mathrm{br,ph}}},\qquad R_\mathrm{br}=\frac{P_\mathrm{br}}{3 I_\mathrm{br,ph}^2},\qquad X_\mathrm{br}=\sqrt{Z_\mathrm{br}^2-R_\mathrm{br}^2}.
\]

IM no-load (approx., after subtracting \(3I_0^2 R_1\)):

\[
Q_0=\sqrt{(3 V_\mathrm{ph} I_0)^2-(P_0-3I_0^2 R_1)^2\ldots}\ \text{or per-phase } X_m\approx \frac{V_\mathrm{ph}}{I_{m}}.
\]

Synchronous:

\[
X_{s,\mathrm{pu}}=\frac{E_{\mathrm{OC,ph}}/V_{b,\mathrm{ph}}}{I_{\mathrm{SC}}/I_b}\quad\text{at the chosen }I_f.
\]

SCR \(= I_{f,\mathrm{OCC}(V_r)}/I_{f,\mathrm{SCC}(I_r)}\).

Retardation:

\[
P_\mathrm{rot}=-J\omega\frac{\mathrm{d}\omega}{\mathrm{d}t}.
\]

## Methods

Always write the base: “on 50 kVA, 400 V.” Convert every given ohm to pu or every pu to ohms before mixing. For a transformer with OC on LV and SC on HV, convert both to one side, then to pu on nameplate.

IM parameter recipe: DC \(R_1\) (×1.2 if AC factor specified). From BR, \(R_2'=R_\mathrm{br}-R_1\), \(X_1=X_2'=X_\mathrm{br}/2\) unless class given. From NL, \(I_c=(P_0-3I_0^2 R_1)/(3V_\mathrm{ph})\), \(I_m=\sqrt{I_0^2-I_c^2}\), \(X_m=V_\mathrm{ph}/I_m\). Build the circuit, then a load point is a homework problem from unit 06.

Synchronous EMF-method regulation in pu: \(\mathbf{E}_a=\mathbf{V}_\mathrm{pu}+\mathbf{I}_\mathrm{pu}(R_\mathrm{pu}+jX_{s,\mathrm{pu}})\), same phasor as in ohms.

When two machines share a bus, pick a system base (e.g. 100 MVA, 11 kV), convert both \(X\) to that base, then they add like parallel Thevenin impedances for fault current.

Temperature: \(R(\vartheta)=R_0(1+\alpha\vartheta)\) with \(\alpha\approx 0.0039/^\circ\mathrm{C}\) for copper from 0 °C, or the 234.5 °C inferred-temperature formula. Loss guarantees at 75 °C.

If a problem gives %Z and X/R, reconstruct \(R_\mathrm{pu}=Z_\mathrm{pu}/\sqrt{1+(X/R)^2}\), \(X_\mathrm{pu}=R_\mathrm{pu}(X/R)\).

## Mistakes

Using \(Z_b=V/\sqrt{3}I\) inconsistently. Either all phase or all the \(V_{LL}^2/S_{3\phi}\) formula.

Changing S base but forgetting \(Z_\mathrm{pu}\) scales with \(S\).

Adding transformer pu and motor pu on different kVA without rebasing.

Taking blocked-rotor \(X_\mathrm{br}\) as \(X_m\).

Using OCC voltage as line when the SCC current is phase, or vice versa, in \(Z_s=E/I\).

Reporting Swinburne efficiency as if stray load loss were zero without saying so. IEC/IEEE add a conventional stray percentage.

Running a heat run by locked-rotor at rated voltage. That is a fault. BR is reduced voltage.

Using cold DC resistance in an SC-derived \(R_\mathrm{eq}\) comparison without temperature correction, then declaring “IEEE discrepancy.”

Treating 1.0 pu speed as 1 r/min. 1.0 pu speed is rated speed.

Infinite-bus short-circuit current \(1/X_s\) with unsaturated \(X_s\) as a physical first-cycle current. First cycle is \(X_d''\), smaller than \(X_s\); \(1/X_s\) is the steady current if the field is not forced and the machine stays on line, an approximation.

Mixing \(H\) in MJ/MVA (seconds) with \(J\) in kg·m² without \(H=J\omega_m^2/(2S_b)\).

Transformer OC power as pu of SC power without noticing they are different tests. Core pu is \(P_\mathrm{OC}/S_r\), copper pu at full load is \(P_\mathrm{SC}/S_r\).

A worked pu habit: after computing \(Z_\mathrm{pu}\), convert back to ohms on the other winding as a check. Transformer \(Z_\Omega,\mathrm{LV}=Z_\mathrm{pu} V_{LV}^2/S\) and \(Z_\Omega,\mathrm{HV}=Z_\mathrm{pu} V_{HV}^2/S\); their ratio must be \(a^2\). If it is not, the base voltages did not follow the nameplate ratio. For a three-phase bank of single-phase units, \(S_b\) of the bank is three times one unit when you write a three-phase fault current, but each unit’s own SC test is on the single-phase rating. State which.

Induction-motor test traps in the lab: blocked-rotor voltage is applied only long enough to read meters; the rotor is a heater. Use a reduced-time or a current just below rated if the supply cannot hold the voltage. Separate friction from core by running no-load at several voltages and plotting \(P_0-3I_0^2 R_1\) versus \(V^2\); the intercept is F&W (plus a residual), the slope is core. That split matters when you later change frequency (V/f): F&W is mechanical, core is \(B\) and \(f\). IEEE 112 and IS 15999 are the standards; UG labs approximate them. Do not quote a precision of 0.1% efficiency from a two-wattmeter no-load test.

Synchronous-machine SCC must be at rated speed. If speed is low, \(E\) for a given \(I_f\) is low and the current for a given \(I_f\) on short circuit is roughly the same (resistance-limited only if \(R_a\) matters), but the OCC used in \(Z_s=E/I\) would be unscaled. Always reduce OCC voltages to rated speed by \(n_r/n_\mathrm{test}\) before forming \(Z_s\). ZPF lagging at rated current and rated voltage needs a load bank or a running motor; it is not the same as SCC. Potier reactance from a badly saturated triangle can exceed \(X_s\); that is a symptom, not a reactance to put in the phasor.

DC Hopkinson test: two identical machines, motor-generator, share losses from a small supply. Full-load copper and commutation are present; the supply provides the losses only. Swinburne cannot see armature reaction or stray load loss; it is a no-load test plus \(I^2 R\). Say which efficiency you computed. Retardation needs a known \(J\) (weigh a rotor, or a rundown with a known extra inertia, or an acceleration test with a known torque). Differentiating a noisy speed trace is the practical difficulty; fit a smooth \(\omega(t)\) first. Record ambient temperature with every resistance; a 10 °C error is a 4% copper-loss error, which swamps a 0.2% efficiency argument. Write the resistance-correction formula next to the raw milliohmmeter reading so the 75 °C value is the one that enters \(P_\mathrm{cu}\).

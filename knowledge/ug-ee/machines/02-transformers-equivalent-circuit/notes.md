# Ideal and practical single-phase transformer

A transformer is two or more windings coupled by a common flux, usually in a ferromagnetic core, used to change voltage and current levels at essentially the same frequency and with high efficiency. It is not a source of energy. Ideal-transformer algebra is the lossless, infinite-magnetizing-inductance, zero-leakage limit. Practical equivalent circuits put copper resistance, leakage reactance, magnetizing inductance, and core-loss resistance back in. This unit is the single-phase model; open-circuit and short-circuit tests, regulation formulas, and three-phase connections are the next unit.

Undergraduate courses treat the transformer as both a circuit element and a magnetic device. Faraday’s law sets the volts per turn. Ampere’s law sets the magnetizing current. Power invariance (neglecting loss) sets \(V_1 I_1 = V_2 I_2\) in the ideal case. Nameplate quantities — rated primary and secondary voltages, rated volt-amperes, frequency, and sometimes impedance in percent — are the numbers that later tests refer to.

## Concepts

An ideal transformer with turns \(N_1\) (primary) and \(N_2\) (secondary) obeys \(v_1/v_2 = N_1/N_2 = a\) and \(i_1/i_2 = N_2/N_1 = 1/a\) when the dots are observed and the secondary current is defined out of the dotted terminal (so that ampere-turns cancel). The turns ratio \(a\) is primary-to-secondary in this handbook unless a problem states otherwise. Instantaneous power into the ideal pair is zero: \(v_1 i_1 = v_2 i_2\). Impedance \(Z_L\) on the secondary appears at the primary as \(Z_\mathrm{in}=a^2 Z_L\). That reflection identity is the reason a 230/23 V transformer can match a low-voltage load to a higher-voltage source without a matching network of L and C.

Dots mark instantaneous voltage polarity. If both dotted terminals are positive at the same instant, the windings are series-aiding when connected that way. Reversing one winding subtracts voltages. Autotransformers exploit a common winding; they are still Faraday devices, not a different physics.

A practical transformer has winding resistances \(R_1\), \(R_2\), leakage inductances \(L_{1\ell}\), \(L_{2\ell}\), a magnetizing inductance \(L_m\) (or reactance \(X_m=\omega L_m\)), and a core-loss (no-load loss) resistance \(R_c\). The conventional equivalent circuit places \(R_1+jX_1\) in series on the primary, an ideal transformer of ratio \(a\), and \(R_2+jX_2\) in series on the secondary, with the shunt magnetizing branch \(R_c\parallel jX_m\) at the internal primary voltage. Referring the secondary to the primary replaces the ideal transformer by scaling: \(R_2'=a^2 R_2\), \(X_2'=a^2 X_2\), and the load likewise. The approximate circuit used in regulation calculations moves the shunt branch to the supply terminals and lumps \(R_\mathrm{eq}=R_1+R_2'\), \(X_\mathrm{eq}=X_1+X_2'\). That approximation is accurate when \(I_m\) is a few percent of rated current, which it is on power transformers.

Nameplate “impedance” \(Z_\mathrm{pu}\) or %Z is \(I_\mathrm{rated} Z_\mathrm{eq}/V_\mathrm{rated}\) on a chosen side. A 5% impedance transformer drops 5% of rated voltage across \(Z_\mathrm{eq}\) at rated current. Short-circuit current on a stiff bus is then about \(1/Z_\mathrm{pu}\) times rated, which is why %Z is a protection number as well as a regulation number.

Magnetizing current \(I_m\) lags the induced voltage by 90° in the linear model; core-loss current \(I_c\) is in phase with that voltage. The no-load current \(I_0=\sqrt{I_c^2+I_m^2}\) is typically 1–5% of rated for distribution transformers and higher for small shells. Because of saturation, \(i_m(t)\) is peaked even if \(v(t)\) is sinusoidal: Faraday forces \(\Phi\) to be the integral of \(v\), hence sinusoidal if \(v\) is, while the B-H curve maps sinusoidal \(B\) to a peaked \(H\). The third harmonic in magnetizing current is why three-phase core construction and delta windings matter (next unit).

Efficiency \(\eta = P_\mathrm{out}/P_\mathrm{in} = P_\mathrm{out}/(P_\mathrm{out}+P_\mathrm{cu}+P_\mathrm{core})\). Copper loss \(I^2 R_\mathrm{eq}\) varies with load current squared. Core loss is essentially constant if the primary voltage and frequency are constant (the usual grid case). Maximum efficiency occurs when \(P_\mathrm{cu}=P_\mathrm{core}\) at that voltage. All-day efficiency uses energy over 24 h, not a single load point; distribution transformers spend many hours at light load, so core loss is designed small.

Voltage regulation is \((V_\mathrm{nl}-V_\mathrm{fl})/V_\mathrm{fl}\) at a specified power factor, usually with primary voltage held at the value that produces rated secondary voltage at full load, or alternatively with primary held at rated and secondary allowed to rise at no load. State the convention. Lagging PF makes regulation worse (larger drop); leading PF can produce negative regulation (secondary voltage rises with load because of the capacitive current through \(X_\mathrm{eq}\)).

Inrush current when a transformer is energized can be many times rated because residual flux plus the first voltage half-cycle can demand a flux peak beyond saturation. It is not a fault; it decays with the magnetizing-circuit time constant. Protection settings must ride through inrush or use harmonic restraint.

Taps on the HV winding change \(a\) in small steps to compensate for supply or drop. An on-load tap changer is a mechanical/electronic device; off-circuit taps require de-energizing. The equivalent circuit does not change topology; \(a\) changes.

Frequency and voltage: Faraday \(E=4.44 f N \Phi_\mathrm{max}\). If a 50 Hz transformer is run at 60 Hz at the same voltage, \(\Phi_\mathrm{max}\) falls and magnetizing current falls; if run at 50 Hz on a 60 Hz voltage rating without reducing V, the core saturates. V/f is the magnetizing constraint, the same idea as induction-motor V/f control later.

Isolation, not just ratio, is a function. A 1:1 isolation transformer still has leakage, resistance, and interwinding capacitance. Safety earth, electrostatic shields, and creepage are application, not equivalent-circuit, issues, but they explain why a lab isolation transformer is not a jumper.

The referred equivalent circuit is a two-port. Reciprocity holds for a linear passive transformer: \(Z_{12}=Z_{21}\). An ideal transformer is not a reciprocal impedance two-port in the \(z\)-parameter sense because it has no finite \(z\) parameters; it is a voltage-current constraint. Do not ask for Thevenin of an ideal transformer alone without a source impedance.

## Equations

Ideal transformer (dot convention as above):

\[
\frac{v_1}{v_2} = \frac{N_1}{N_2} = a,\qquad \frac{i_1}{i_2} = \frac{1}{a},\qquad Z_\mathrm{in} = a^2 Z_L.
\]

Faraday, sinusoidal flux:

\[
e = N \frac{\mathrm{d}\phi}{\mathrm{d}t},\qquad E_\mathrm{rms} = 4.44\, f N \Phi_\mathrm{max} = 4.44\, f N B_\mathrm{max} A_c.
\]

Referred secondary (to primary):

\[
R_2' = a^2 R_2,\qquad X_2' = a^2 X_2,\qquad \mathbf{V}_2' = a\mathbf{V}_2,\qquad \mathbf{I}_2' = \mathbf{I}_2/a.
\]

Approximate series impedance:

\[
R_\mathrm{eq} = R_1 + R_2',\qquad X_\mathrm{eq} = X_1 + X_2',\qquad Z_\mathrm{eq} = R_\mathrm{eq} + j X_\mathrm{eq}.
\]

Shunt branch (primary):

\[
R_c = \frac{V_1^2}{P_\mathrm{core}},\qquad X_m = \frac{V_1}{I_m},\qquad I_c = \frac{V_1}{R_c}.
\]

Approximate voltage drop (rated current, PF angle \(\theta\), lagging positive in the cosine-sine form used below):

\[
\Delta V \approx I R_\mathrm{eq}\cos\theta + I X_\mathrm{eq}\sin\theta
\]

for lagging \(\theta\), with a sign change on the \(X\) term for leading. Percent regulation \(\approx \Delta V / V_\mathrm{rated}\).

Efficiency:

\[
\eta = \frac{x\,S_\mathrm{rated}\,\mathrm{pf}}{x\,S_\mathrm{rated}\,\mathrm{pf} + P_\mathrm{core} + x^2 P_\mathrm{cu,fl}},
\]

where \(x\) is the load fraction of rated VA.

Percent impedance:

\[
Z_{\%} = \frac{I_\mathrm{rated}|Z_\mathrm{eq}|}{V_\mathrm{rated}}\times 100.
\]

Autotransformer (two-winding transformer reconnection, common winding \(N_2\), series winding \(N_1-N_2\) if stepping  \(V_H\) to \(V_L\) with \(V_H/V_L=N_1/N_2\)):

\[
S_\mathrm{inductive} = S_\mathrm{throughput}\left(1-\frac{V_L}{V_H}\right)
\]

in the usual additive connection: the windings only transform a fraction of the throughput VA.

## Methods

Build the equivalent circuit from the nameplate and from tests (next unit) or from given \(R,X\). Always pick a reference side. Convert every ohm and every volt to that side before combining series elements. Convert the load impedance to the same side. Then it is an ordinary AC circuit: series \(Z_\mathrm{eq}\), shunt magnetizing if needed, source, load.

For load-flow style problems (given \(V_2\), \(P\), PF, find \(V_1\)): start at the secondary, form \(\mathbf{I}_2\) from \(S=V_2 I_2^*\) or from \(P=V_2 I_2\mathrm{pf}\). Refer \(\mathbf{I}_2\) and \(\mathbf{V}_2\) to the primary. Add \(\mathbf{I}_2' Z_\mathrm{eq}\) to \(\mathbf{V}_2'\) to get the internal voltage, then add the shunt current if the exact circuit is required. For regulation at constant primary voltage, reverse the walk.

Phasor diagram: \(\mathbf{V}_2'\) along the real axis, \(\mathbf{I}_2'\) at \(-\theta\) for lagging, then \(I R\) in phase with current and \(I X\) leading current by 90°. The primary internal voltage is the closing side. This diagram is how the approximate \(\Delta V\) formula is derived; using the formula without knowing the diagram is how leading/lagging signs flip.

Ideal-transformer problems: only ratio and power. Do not insert \(X_m\) unless asked. Current inverting: if voltage steps down, current steps up. Check watts: \(V_1 I_1 = V_2 I_2\) for the ideal pair (watts and VA in the lossless case).

Polarity test: apply a small AC or DC flick to one winding; the relative polarity of the induced voltage marks the dots. In the field, a “boost/buck” connection of LV and HV with a voltmeter tells additive versus subtractive polarity.

When both windings’ resistances are given in ohms on their own sides, never add \(R_1+R_2\) without referring. A 0.2 Ω LV winding is not “smaller” than a 2 Ω HV winding until scaled by \(a^2\).

Core sizing from Faraday: pick \(B_\mathrm{max}\) (1.2–1.6 T typical for 50 Hz steel), frequency, and voltage, solve for \(N A_c\). Window area then holds the copper. That is design, not analysis, but it explains why a 50 Hz transformer is larger than a 400 Hz aircraft transformer of the same VA.

Saturation check: compute \(\Phi_\mathrm{max}=V/(4.44 f N)\). If \(B_\mathrm{max}=\Phi_\mathrm{max}/A_c\) exceeds the knee, magnetizing current will be large and the linear \(X_m\) model fails. Reduce V or raise f.

For referred-circuit SPICE or hand mesh, the ideal transformer can be replaced by a dependent source pair \(v_1=a v_2\), \(i_2=a i_1\), or by scaling all secondary R, L, C by \(a^2\), \(a^2\), \(1/a^2\) respectively.

## Mistakes

Adding \(R_1\) and \(R_2\) in ohms on opposite sides. Refer first.

Using \(a=V_2/V_1\) while the handbook defined \(a=N_1/N_2\). State \(a\). Mixing \(V_1/V_2\) and \(N_2/N_1\) in the same line is the classic ratio bug.

Putting \(X_m\) in series with the load. Magnetizing branch is shunt. Series \(X_m\) would block power transfer.

Treating %Z as a resistance. It is \(|Z_\mathrm{eq}|/Z_\mathrm{base}\). The angle of \(Z_\mathrm{eq}\) is mostly inductive; \(X_\mathrm{eq}/R_\mathrm{eq}\) is often 3–10 on power transformers.

Using 4.44 with peak voltage or with \(\Phi_\mathrm{rms}\). The 4.44 is \(2\pi/\sqrt{2}\) for sinusoids and \(\Phi_\mathrm{max}\). Square-wave excitation uses 4.0, not 4.44.

Assuming regulation is always positive. Leading loads can raise secondary voltage.

Equating no-load current to magnetizing current. \(I_0\) has a core-loss component. On a good transformer \(I_c\) is not negligible compared with \(I_m\) at no load, though both are small versus rated current.

Forgetting that an ideal transformer isolates DC. A DC voltage on one winding is not transformed; only \(\mathrm{d}\phi/\mathrm{d}t\) couples. Applying DC to a winding is a short through \(R\) and a saturated core.

Using secondary current into the dotted terminal while keeping \(v_1/v_2=a\) without flipping the current relation. Ampere-turn balance requires opposite current sense relative to the dots.

Reporting efficiency using VA instead of watts. \(\eta\) is a power ratio. A 0.8 lagging load of 10 kVA is 8 kW, not 10 kW.

Ignoring temperature on resistance. Copper \(R\) at 75 °C is the usual rated-loss number; cold winding resistance from a DC ohmmeter is lower.

Treating autotransformer “savings” as free isolation. The common winding is not isolating; a break can put HV on the LV side.

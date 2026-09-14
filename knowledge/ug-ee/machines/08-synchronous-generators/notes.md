# Pitch, winding factor, OCC/SCC, regulation

A synchronous generator (alternator) has a DC-excited (or PM) rotor field spinning at \(n_s=120 f/P\), locking electrical frequency to mechanical speed. The stator is a distributed AC winding. Generated voltage depends on flux, speed, turns, and winding factors (pitch and distribution). Regulation — how much terminal voltage changes from no-load to load — is computed from OCC, SCC, and a synchronous-impedance or Potier model. This unit is the UG generator: winding geometry, phasor diagram (\(E_a=V_\phi+I_a R_a+j I_a X_s\)), and the classical regulation tests. Parallel operation and the motor are the next unit.

The air-gap flux wave is never a perfect sinusoid. Pitch factor and distribution factor extract the fundamental and suppress selected harmonics. That is why coils are short-pitched and why slots per pole per phase exceed one.

## Concepts

A full-pitch coil spans 180° electrical. A short-pitched coil spans \(\gamma < 180^\circ\); the pitch factor for the \(h\)th harmonic is \(k_p=\sin(h\gamma/2)\). Distribution of \(n\) slots per pole per phase with slot angle \(\alpha\) gives \(k_d=\sin(n\alpha/2)/(n\sin(\alpha/2))\) for the fundamental (and \(h\alpha\) for harmonics). Winding factor \(k_w=k_p k_d\). Breadth and pitch are chosen to cut 5th and 7th, which reduce voltage waveform distortion and stray heating.

Induced phase EMF: \(E_\mathrm{ph}=4.44 k_w f N_\mathrm{ph} \Phi_p\) with \(\Phi_p\) fundamental flux per pole. Line voltage depends on Y or Δ. Frequency \(f=NP/120\) is not optional: a 4-pole 50 Hz machine is a 1500 r/min machine. Prime-mover speed governors hold \(f\); exciters hold \(E_a\) and thus \(Q\) on an infinite bus.

Cylindrical-rotor (non-salient, turbo) machines have a nearly uniform air gap. Synchronous reactance \(X_s=X_\ell+X_a\) lumps leakage and armature reaction into one \(j I_a X_s\). The phasor \( \mathbf{E}_a=\mathbf{V}_\phi+\mathbf{I}_a R_a + j\mathbf{I}_a X_s \) (generator, lagging current as positive \(Q\) out). Salient-pole (hydro) machines split \(X_d\) and \(X_q\) (two-reaction theory, Blondel). Power then has an extra reluctance term \(\propto (1/X_q-1/X_d)\sin 2\delta\). UG often uses \(X_s\approx X_d\) for regulation even on salient machines as a first cut; Potier and ASA methods try to include saturation.

OCC: \(E_a\) versus field current \(I_f\) at rated speed, armature open. It is the magnetization curve. SCC: armature current versus \(I_f\) with the terminals shorted (low voltage, so unsaturated, almost a straight line). Synchronous impedance at a chosen \(I_f\) is \(Z_s=E_\mathrm{OCC}(I_f)/I_\mathrm{SCC}(I_f)\). Unsaturated \(X_s\) from the air-gap line overestimates voltage drop (pessimistic regulation). Saturated \(X_s\) from the OCC at rated voltage is optimistic. Potier (air-gap line plus a short-circuit-plus-rated-current triangle) extracts leakage reactance \(X_p\) (Potier reactance, a stand-in for \(X_\ell\)) and a saturation residual.

Voltage regulation \(\mathrm{reg}=(E_\mathrm{nl}-V_\mathrm{fl})/V_\mathrm{fl}\) at a specified PF. Lagging load (inductive) demagnetizes (armature reaction) and drops voltage more. Leading load (capacitive) magnetizes and can produce negative regulation (voltage rises on load). That is why an unloaded long line (Ferranti, capacitive) can over-excite a generator.

Power on an infinite bus (cylindrical, neglect \(R_a\)): \(P=3 V E_a \sin\delta / X_s\). \(Q=3(V E_a\cos\delta - V^2)/X_s\). Real power is prime-mover torque (governor, \(\delta\)). Reactive power is field current (AVR, \(E_a\)). That decoupling is the operating doctrine. Stability limit \(\delta=90^\circ\) in the simple model; practical \(\delta\) is much less.

Short-circuit ratio (SCR) \(= I_{f,\mathrm{OCC,rated V}} / I_{f,\mathrm{SCC,rated I}}\). It is roughly \(1/X_{s,\mathrm{pu}}\) unsaturated. High SCR: stiff voltage, large machine, typical of hydro. Low SCR: turbo-generators, more \(X_s\), more regulation, cheaper iron.

Damper (amortisseur) windings in salient poles damp hunting and provide a path for starting as an induction machine (motor unit). On a turbo rotor, the solid steel itself damps.

Armature resistance from a DC test, AC value a bit higher. For regulation, \(R_a\) is often small compared with \(X_s\) (0.01 pu vs 1.0 pu) but it still sets copper loss and a slight PF effect.

Zero-power-factor tests (lagging, rated current, rated voltage) plus OCC give the Potier triangle. Do not confuse ZPF with SCC: ZPF still has rated voltage, hence saturation.

## Equations

Speed–frequency:

\[
f=\frac{NP}{120},\qquad n_s=\frac{120 f}{P}.
\]

Winding factors (fundamental):

\[
k_p=\sin(\gamma/2),\qquad k_d=\frac{\sin(n\alpha/2)}{n\sin(\alpha/2)},\qquad k_w=k_p k_d.
\]

EMF:

\[
E_\mathrm{ph}=4.44 k_w f N_\mathrm{ph} \Phi_p.
\]

Cylindrical-rotor phasor (generator):

\[
\mathbf{E}_a=\mathbf{V}_\phi + \mathbf{I}_a R_a + j \mathbf{I}_a X_s.
\]

Approximate regulation (same trigonometric form as a transformer, with \(X_s,R_a\)):

\[
\mathrm{reg}\approx \frac{I R_a\cos\theta + I X_s\sin\theta}{V}\quad\text{(lagging \(\theta\))}.
\]

Synchronous impedance from tests at one \(I_f\):

\[
Z_s=\frac{E_\mathrm{OC}(I_f)}{I_\mathrm{SC}(I_f)},\qquad X_s=\sqrt{Z_s^2-R_a^2}.
\]

Power (three-phase, \(R_a=0\), cylindrical):

\[
P=\frac{3 V_\phi E_a}{X_s}\sin\delta,\qquad P_\mathrm{max}=\frac{3 V_\phi E_a}{X_s}.
\]

Salient ( \(R_a=0\) ):

\[
P=\frac{3 V E_a}{X_d}\sin\delta+\frac{3 V^2}{2}\left(\frac{1}{X_q}-\frac{1}{X_d}\right)\sin 2\delta.
\]

SCR \(\approx 1/X_{s,\mathrm{pu,unsat}}\).

## Methods

EMF from geometry: compute \(k_p\), \(k_d\), \(k_w\), then \(E_\mathrm{ph}\). For a 60° phase spread, \(n\alpha=60^\circ\). Short-pitch by one slot: \(\gamma=180^\circ-\alpha\).

Regulation by EMF method (synchronous impedance): from OCC/SCC get unsaturated \(X_s\) (air-gap line). For a given \(V,I,\mathrm{PF}\), compute \(|E_a|\) from the phasor, then \(\mathrm{reg}=(|E_a|-V)/V\). This is pessimistic.

MMF (ampere-turn) method: use OCC as a nonlinear mapping from MMF to voltage; combine field AT and armature AT at an angle depending on PF. Optimistic.

Potier / ASA: more work, closer to measured regulation. UG numericals usually demand the EMF method plus a comment on saturation error.

Infinite-bus operating point: given \(P\) and \(V\), \(|I|\cos\phi=P/(3V)\). If \(I_f\) (hence \(E_a\)) is given, solve \(\delta\) from the power formula, then \(Q\). If PF is given, reconstruct \(\mathbf{I}\), then \(\mathbf{E}_a=\mathbf{V}+R\mathbf{I}+jX_s\mathbf{I}\).

To find \(X_s\) in pu: \(Z_\mathrm{base}=V_\mathrm{ph,rated}/I_{a,rated}\), \(X_{s,\mathrm{pu}}=X_s/Z_\mathrm{base}\). SCC at rated current and OCC at rated voltage give SCR.

Parallel to infinite bus: synchronize (phase sequence, frequency, voltage, phase angle — the “lamps or synchroscope” ritual), then raise mechanical torque to export \(P\), raise excitation to export \(Q\) (or absorb \(Q\) if underexcited).

## Mistakes

Using \(E=4.44 f N \Phi\) without \(k_w\). Distributed windings are not concentrated coils.

Mixing electrical and mechanical degrees in pitch. One pole pitch is 180° electrical always, \(360^\circ/P\) mechanical.

Using line voltage in the per-phase phasor \(E_a=V+IR+jIX_s\). \(V\) is phase voltage.

Treating \(X_s\) from SCC/OCC at rated \(I_f\) as unsaturated when that \(I_f\) is on the OCC knee. State which \(X_s\).

Expecting lagging load to raise terminal voltage. It does the opposite on a stand-alone generator.

Using \(\delta=90^\circ\) as a normal operating point. It is the theoretical \(P_\mathrm{max}\), not a setpoint.

Confusing SCR with short-circuit current in amperes. SCR is a field-current ratio.

Applying cylindrical \(P=3VE\sin\delta/X_s\) to a salient machine at large \(\delta\) without the reluctance term when the problem gave \(X_d\neq X_q\).

Scaling OCC with field current when speed changed. OCC \(E\) scales with speed at given flux; tests are specified at rated speed.

Forgetting that SCC is essentially unsaturated: using SCC to “measure saturation” is wrong. Saturation lives on the OCC and ZPF.

Y-connecting a winding and then using coil voltage as line voltage without \(\sqrt{3}\).

Ignoring \(R_a\) in efficiency while keeping it in regulation, or the reverse, inconsistently in the same problem when both are asked.

Winding layout in a double-layer stator is not decoration for \(k_w\). Coils of span \(\gamma\) occupy two slots a pole-pitch apart (or less). The number of turns per phase \(N_\mathrm{ph}= (Z/2)/3\) for a three-phase machine with \(Z\) conductors, each coil having two sides. Fractional-slot windings (not an integer slots/pole/phase) appear on low-speed hydro units and on PM machines; their \(k_d\) still uses the distribution formula with the actual electrical slot angle, but the distribution may span more than one pole. UG problems almost always give integer \(n\). Harmonics: triplen EMFs are co-phasal in a three-phase winding and cancel in a line-to-line Y voltage if the winding is balanced; they can circulate in a delta. That is why a delta-connected stator must be able to stand triplen circulating current, and why Y is preferred for HV generators (also insulation: phase voltage is line/\(\sqrt{3}\)).

Saturation and \(X_s\): armature reaction flux path is mostly iron, leakage path is mostly air. As load current rises at a given terminal voltage, the iron saturates and the armature-reaction reactance \(X_a\) falls, while leakage \(X_\ell\) stays put. A single \(X_s\) cannot be both the OCC slope and the load-test drop. That is the whole reason the EMF method (unsaturated \(X_s\)) overestimates regulation and the MMF method underestimates it. Potier’s triangle tries to pull \(X_\ell\) out of a ZPF test so that saturation can be applied only to the remaining MMF. If a problem gives only OCC and SCC, it wants the EMF method; say so, and do not invent a Potier reactance.

Infinite-bus versus isolated: on an isolated load, \(f\) is the prime mover’s speed and \(V\) is the AVR’s problem; \(\delta\) is not a free operating coordinate in the same way. On an infinite bus, \(f\) and \(V\) are fixed and \(\delta\) and \(E_a\) are the two handles. Mixing the pictures — “the voltage fell so \(\delta\) increased” on an infinite bus — is a conceptual error. Voltage is clamped; current and \(\delta\) adjust.

Capability curve (intro): field heating limits overexcited \(Q\), armature heating limits \(|S|\), and \(\delta\) or stability limits underexcited \(Q\). UG does not need the full D-curve, but should know that a generator cannot supply arbitrary \(P\) and \(Q\) inside a rectangle. Automatic voltage regulators hold \(V\) by moving \(I_f\); overcurrent limiters and V/Hz (volts-per-hertz) limiters stop the operator from saturating the core at low speed. Those limiters are why a real \(E_a\) is not a free knob during a start-up.

# Symmetrical (bolted three-phase) faults and \(Z_\mathrm{bus}\)

A symmetrical fault is a balanced three-phase short. All phases see the same current magnitude; only the positive-sequence network is needed. It is usually the most severe fault for equipment rating on a solidly grounded system at generator terminals, and it is the first fault calculation taught because it is a linear circuit problem in the pu positive-sequence model. This unit covers prefault load vs. unloaded (E = 1.0 pu) approximations, Thevenin equivalent at the fault bus, \(Z_\mathrm{bus}\) building, generator reactance selection (\(X''\), \(X'\), \(X_s\)), and converting pu fault current to kA and MVA. Unbalanced faults are unit 05.

## Concepts

Prefault, the network is in sinusoidal steady state with voltages from a load-flow (unit 03). A bolted three-phase fault at bus \(k\) suddenly connects that bus to reference (neutral/ground in the positive-sequence diagram) through a fault impedance \(Z_f\), often \(Z_f=0\). During the first few cycles the machines look like voltage sources behind subtransient reactance \(X''_d\). After the subtransient period, transient reactance \(X'_d\) is used for relay times of several cycles to a second. Synchronous reactance \(X_s\) (or \(X_d\)) is a steady-state phasor model, not a fault-current model, except for a hypothetical sustained short with excitation held — and even then field forcing and saturation intervene. UG problems will name which reactance to use. When they say “subtransient fault current,” use \(X''\) for machines and transformer leakages and line \(jX\) as usual.

The unloaded prefault approximation sets every machine internal voltage to \(1.0\angle 0^\circ\) and neglects prefault currents (loads open, shunts ignored or only charging neglected). Then the Thevenin voltage at any bus is \(1.0\ \mathrm{pu}\) and the Thevenin impedance is the impedance looking into the dead network from that bus with machine internals shorted (voltage sources off). Fault current is \(\mathbf{I}_f=V_{\mathrm{th}}/(Z_{\mathrm{th}}+Z_f)\). This is the standard first-course calculation.

Loaded prefault: Thevenin voltage is the prefault bus voltage \(V_k(0)\) from load flow, and \(Z_{\mathrm{th}}=Z_{kk}\) of the bus impedance matrix of the passive network (sources off, i.e. machine voltages shorted, leaving \(X''\) connected to reference). The current injected by the fault into the network is \(-I_f\) at bus \(k\). Superposition: postfault voltages \(\mathbf{V}=\mathbf{V}(0)+Z_\mathrm{bus}(-I_f \mathbf{e}_k)\), so \(V_k^{\mathrm{post}}=V_k(0)-Z_{kk}I_f\), and with \(V_k^{\mathrm{post}}=Z_f I_f\) one gets \(I_f=V_k(0)/(Z_{kk}+Z_f)\). For a bolted fault \(Z_f=0\), \(V_k^{\mathrm{post}}=0\) and \(I_f=V_k(0)/Z_{kk}\).

\(Z_\mathrm{bus}=Y_\mathrm{bus}^{-1}\) in the same reference (ground). The diagonal \(Z_{kk}\) is the Thevenin impedance at bus \(k\). Off-diagonal \(Z_{ik}\) is the voltage at bus \(i\) when 1 pu current is injected at bus \(k\) with all sources off. Building \(Z_\mathrm{bus}\) by inversion is fine for 3–4 bus homework. Building by adding branches (algorithm: add a tree branch from a new bus to reference, add a link, add a shunt) is the classical “\(Z_\mathrm{bus}\) building algorithm.” UG may ask one or two building steps: adding a branch of impedance \(z\) from existing bus \(p\) to a new bus \(q\) creates a new row/column; adding a loop between \(p\) and \(q\) uses a rank-one update. Memorize the Thevenin meaning more tightly than every Kron update formula.

Short-circuit MVA at a bus is \(S_{\mathrm{sc}}=S_\mathrm{base}/|Z_{kk}|\) in three-phase MVA when \(V_{\mathrm{pre}}=1.0\ \mathrm{pu}\) bolted. Equivalently \(S_{\mathrm{sc}}=\sqrt{3}V_{\mathrm{LL}}I_f\) with actual volts and amperes. Equipment and breaker ratings are discussed in kA interrupting and MVA; this unit computes the prospective current, not the breaker physics (protection unit 10 and switchgear electives).

Current-limiting: series reactors, higher transformer impedance, and splitting buses reduce \(I_f\) at the cost of voltage drop and losses in normal operation. A generator feeding a fault through two parallel transformers has \(X_{\mathrm{th}}=X''+X_t/2\) if the transformers are identical.

Selection of \(X''\) vs \(X'\): ANSI/IEEE interrupting studies use a more detailed E/X method with decrement factors; UG uses a single reactance as stated. Do not mix \(X''\) of one machine with \(X_s\) of another in the same diagram unless the problem is illustrating time scales.

Synchronous machines as sources: the internal voltage \(E''=V_t+jX''I_{\mathrm{pre}}\) if prefault load is kept. Unloaded, \(E''=V_t\approx 1.0\). Induction motors contribute subtransient current for a few cycles (some codes require adding them); UG problems often omit motors unless listed.

Asymmetry and DC offset: a fault at voltage zero produces a decaying DC offset; the peak current can approach \(2\sqrt{2}I_{\mathrm{rms,sym}}\). Breaker “making” current uses this peak. The symmetrical RMS computed from \(V/X\) is the AC component. Mention DC offset; compute it only if asked (\(i(t)=\sqrt{2}I_{\mathrm{ac}}[\sin(\omega t+\alpha-\phi)-e^{-t/\tau}\sin(\alpha-\phi)]\)).

Infinite bus: a bus with \(Z_{\mathrm{th}}=0\) or a specified short-circuit MVA \(S_{\mathrm{sc}}\) giving \(Z_{\mathrm{th}}=S_\mathrm{base}/S_{\mathrm{sc}}\). A grid interconnection is often given that way.

Radial vs meshed: in a radial chain, \(Z_{\mathrm{th}}\) is the series sum of reactances from sources to the fault. In a mesh, use parallel combinations, delta-wye, or \(Z_\mathrm{bus}\). Do not series-sum around a loop.

Fault at the terminals of a generator: \(I''=E''/X''\), typically 4–8 pu, a large current. The same generator behind a transformer \(X_t=0.10\) pu has \(I''=E''/(X''+X_t)\), smaller. Unit transformers protect generators from nearby HV faults in that sense.

Per-unit consistency from unit 01 is assumed. Convert all \(X''\) to a common MVA base before paralleling.

Postfault voltages at other buses: \(V_i=V_i(0)-Z_{ik}I_f\). Relays and voltage-dip studies use this. For unloaded approximation \(V_i(0)=1\), \(I_f=1/Z_{kk}\), \(V_i=1-Z_{ik}/Z_{kk}\). Buses electrically close to the fault (\(Z_{ik}\approx Z_{kk}\)) collapse; remote buses stay near 1.0.

Breaker and equipment ratings are stated in RMS symmetrical kA, peak making kA, and sometimes MVA at a nominal kV. Converting \(I_{\mathrm{pu}}\) to kA uses the local voltage base, not the generator kV, when the fault is on the HV bus. A 11 kV machine behind a 11/132 kV transformer, fault on 132 kV: \(I_{\mathrm{base}}=S/(\sqrt{3}\times 132\,\mathrm{kV})\). The same pu current on the 11 kV side would use 11 kV and is a different kiloampere number because the transformer scales current. Report the bus you were asked.

X/R ratio of \(Z_{\mathrm{th}}\) sets the DC offset time constant \(\tau=L/R=(X/R)/\omega\). High X/R (EHV, near generators) means the offset dies slowly and the first-cycle peak is close to the full \(2\sqrt{2}\) factor. Distribution faults with more R have less offset. IEC/ANSI making-current factors are tabulated; UG may be asked only for the symmetrical RMS and a comment that the peak is up to \(2.55 I_{\mathrm{rms}}\) class numbers.

Circuit reduction versus \(Z_\mathrm{bus}\): a two-source, one-fault-bus ladder is faster as a parallel of two paths. A four-bus mesh with a fault at bus 3 is faster as \(Y^{-1}\) if you already have \(Y\). Do not spend exam time building a full Kron \(Z_\mathrm{bus}\) if a delta-wye reduction of reactances is six lines. The Thevenin impedance is the only diagonal you need for \(I_f\); you need a column of \(Z_\mathrm{bus}\) only if postfault voltages at several buses are required.

Loads as constant impedance: a 1.0 pu load at 1.0 pu voltage is a 1.0 pu impedance to ground and reduces \(Z_{kk}\) slightly. Neglecting it is conservative for current (slightly high \(I_f\)). Motor contributions do the opposite: they add a transient source and raise \(I_f\) for a few cycles. Utility short-circuit studies often include a motor factor; UG includes motors only when listed as machines with \(X''\).

A bolted fault on a bus that is also a generator terminal uses \(X''\) of that machine in parallel with the Thevenin of the rest of the system. If the rest is an infinite bus behind \(X_t+X_{\mathrm{line}}\), the two paths add in parallel. Do not omit the local machine; it often dominates \(I_f\).

## Equations

Bolted three-phase, unloaded:

\[
I_f=\frac{1.0}{Z_{kk}+Z_f},\qquad Z_f=0\Rightarrow I_f=\frac{1}{Z_{kk}}.
\]

Loaded prefault:

\[
I_f=\frac{V_k(0)}{Z_{kk}+Z_f}.
\]

Postfault voltages (sources-off \(Z_\mathrm{bus}\)):

\[
V_i=V_i(0)-Z_{ik}I_f.
\]

Short-circuit level:

\[
S_{\mathrm{sc,3\phi}}=\frac{S_\mathrm{base}}{|Z_{kk}|}\quad (V_{\mathrm{pre}}=1).
\]

Base current: \(I_\mathrm{base}=S_\mathrm{base}/(\sqrt{3}V_{\mathrm{LL,base}})\). Actual \(I_{\mathrm{kA}}=I_{\mathrm{pu}}I_\mathrm{base}\).

Generator terminal subtransient: \(I''=E''/jX''_d\).

Two sources in parallel to a fault through impedances \(Z_a,Z_b\): \(Z_{\mathrm{th}}=Z_a\parallel Z_b\), then split \(I_a=I_f Z_b/(Z_a+Z_b)\).

## Methods

1. Convert the one-line to a pu positive-sequence reactance diagram (\(R=0\) unless given). Machine internals to reference through \(X''\) (or as specified).
2. If asking Thevenin at bus \(k\), kill internal EMFs (short them) and compute \(Z_{kk}\) by circuit reduction or by inverting \(Y_\mathrm{bus}\).
3. \(I_f=V_{\mathrm{pre}}/(Z_{kk}+Z_f)\).
4. Split \(I_f\) in the live network with EMFs restored, or use superposition with the \(Z_\mathrm{bus}\) voltage formula.
5. Convert to kA and three-phase MVA. Report RMS symmetrical unless peak or asymmetrical is requested.

\(Y_\mathrm{bus}\) path: include machine \(1/jX''\) as shunts to reference at generator buses; invert; read \(Z_{kk}\). Do not include load impedances unless the problem says to (constant-impedance loads slightly reduce \(I_f\)).

Checks: \(|I_f|\) of several pu at a generator bus is plausible; a remote weak bus may be \(<1\ \mathrm{pu}\); voltages after fault between 0 and about 1.0 pu; \(S_{\mathrm{sc}}\) larger than machine MVA if multiple sources feed.

## Mistakes

Using \(X_s\) when the question says subtransient. Forgetting to convert machine pu \(X\) to the system MVA base. Adding reactances of parallel paths instead of paralleling. Using \(I=S/V\) without \(\sqrt{3}\) for three-phase kA. Taking \(Z_{kk}\) as a series sum in a meshed network. Applying sequence-network connections (unit 05) to a three-phase fault (only positive sequence, and \(Z_f\) in that network, not three \(Z_f\)). Setting \(V_{\mathrm{pre}}=0\). Inverting \(Y_\mathrm{bus}\) built without generator shunts to ground, which is singular or load-flow singular, and then calling that \(Z_{kk}\) a fault Thevenin. Using \(S_{\mathrm{sc}}=V^2/Z\) with \(V\) in kV and \(Z\) in pu. Omitting the unit transformer between generator and HV fault. Reporting \(I_f\) in pu as kA. Forgetting DC offset when asked for peak making current. Using prefault load current as the fault current.

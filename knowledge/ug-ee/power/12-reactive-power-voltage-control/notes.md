# Reactive power and voltage control: Q–V, shunt and series compensation

Voltage in an AC grid is a local quantity strongly tied to reactive power. Real power travels with angle (unit 02, unit 06); reactive power is generated or absorbed to keep \(|V|\) in band. Undergraduate power courses treat the Q–V relationship on a radial Thevenin equivalent, shunt capacitors and reactors, synchronous condensers, tap changers, series capacitors, and a first warning about voltage collapse. FACTS hardware details are unit 11; distribution drop is unit 09; this unit is the system-level Q–V toolkit.

## Concepts

A load \(P+jQ\) at the end of a line \(R+jX\) supplied from a stiff \(E\) has a receiving voltage \(V\) that drops as \(Q\) (and \(P\)) increase. For \(X\gg R\) (EHV), the linearized relation is \(\Delta V\approx (X \Delta Q + R \Delta P)/V\), so vars move voltage. For distribution \(R\sim X\), both P and Q drop voltage (unit 09). The Q–V curve at a bus, with P fixed, is a folded characteristic: two V solutions for a given Q below a maximum, coalescing at the nose (saddle-node). Operating on the upper part is normal; the lower part is the low-voltage solution of load flow (unit 03). Stiffening the system (more generation nearby, less X, shunt capacitors that are voltage-schedulable) raises the nose. A lagging load plus a tripped line can push the nose through the operating point: voltage collapse. Unlike rotor-angle first-swing (unit 06), collapse can be slow (tap changers trying to restore LV, loads recovering) or fast.

Sources of Q: synchronous generators and condensers (field current; limited by armature current, field current, and underexcitation/stability), shunt capacitors (cheap, \(Q=\omega C V^2\), collapse when V collapses), shunt reactors (absorb Ferranti Q on EHV at night), SVCs/STATCOMs (unit 11), line charging (\(B V^2/2\) each end of a \(\pi\)), and overexcited motors (rarely used on purpose). Sinks of Q: lagging loads, under-excited generators (absorbing vars to hold down voltage), transformers and lines (\(I^2 X\)), shunt reactors, underexcited motors.

Power-factor correction at a load is the industrial special case: reduce \(Q_{\mathrm{from\ grid}}\) with capacitors so that \(S\) and \(I\) fall at constant P (circuits pack, ac-power unit). At system level, capacitors are placed at buses where the voltage is low and the Q-margin is thin, not only at the meter.

Tap-changing transformers (OLTC) change the ratio \(t\). Raising tap on the load side of a step-down transformer raises load voltage by drawing more Q (and a little P redistribution) from the supply. During a depressed EHV voltage, OLTCs restoring customer voltage can deepen the EHV Q drain and accelerate collapse; some operational procedures freeze taps. Phase-shifting transformers control P more than V; they are a P-control device.

Series capacitors cancel part of line \(X\), reducing \(\Delta V\) for a given through-flow and raising \(P_{\max}\). They are a transmission tool (long 400 kV+ corridors). Distribution sometimes uses a little series C but ferroresonance and protection are issues. Shunt capacitors at the receiving end of a radial line raise \(V_R\) and supply the load’s Q so that the line does not have to carry it (less \(I\), less drop, less loss).

Synchronous condenser: a synchronous machine with \(P\approx 0\), Q dispatched by excitation, with inertia that also helps frequency. More expensive than capacitors, better at low V than switched C, used at weak inverter terminals and some urban substations. A generator with spare Mvar is the same physics with \(P\neq 0\); capability curves bound the point \((P,Q)\).

Voltage control hierarchy: (1) generator AVR holds \(V_t\) or a compensated HV bus; (2) plant-level Q sharing; (3) switched caps/reactors and OLTCs on slower clocks; (4) SVC/STATCOM in between; (5) operator setpoints from a state estimator. Secondary voltage control (pilot buses, regional Q) exists in some grids; UG mentions the idea.

Surge impedance loading (unit 02) again: below SIL the line produces Q, voltage high at light load (need reactors); above SIL the line eats Q, voltage low (need caps or nearby generation). EHV night/day switching of reactors is this story.

Flat voltage profile as a design objective: generation Q, midpoint compensation, or a shorter electrical distance. It is not always optimal for losses (slightly higher V reduces \(I^2R\) for constant-P loads, so operators often run toward the high band).

PV and QV curves in planning: vary P or Q at a bus until the Jacobian is singular. The distance to the nose is a voltage-stability margin. Continuation power flow traces the curve. UG should sketch it and compute a two-bus analytic nose for a lossless radial line.

Two-bus lossless radial: \(E\) infinite bus, line \(X\), load \(P+jQ\) with \(V\angle-\delta\). Then \(P=(EV/X)\sin\delta\), \(Q=(EV\cos\delta-V^2)/X\). Eliminate \(\delta\): \((P X)^2+(Q X+V^2)^2=(E V)^2\). For given P, Q, this is a quadratic in \(V^2\) with a discriminant that vanishes at the nose.

For a constant-\(P\), \(Q=0\) load, \(0=(EV\cos\delta-V^2)/X\) implies \(V=E\cos\delta\), hence \(P=(E^2/X)\cos\delta\sin\delta=(E^2/(2X))\sin 2\delta\). Then \(P_{\max}=E^2/(2X)\) at \(\delta=45^\circ\), \(V=E/\sqrt{2}\). The classical angle-stability \(P_{\max}=E^2/X\) at \(90^\circ\) assumes voltage held at both ends (two infinite buses, or AVRs holding \(V\)). Voltage-limited transfer on a radial load is half of that classic number. That distinction is the point of the two-bus nose.

Generator Q capability: at a given P, overexcitation (supplying Q) is limited by field current and by stator current, underexcitation (absorbing Q) by stator current, stability (loss-of-field relay 40, unit 10), and sometimes by end-region heating. A rectangular “±0.8 pf” box is a crude UG stand-in for the capability curve. Plant voltage-control contracts may require a pf range at the HV bus, which is not the same as the stator pf because of unit-transformer \(I^2X\).

Shunt reactor switching on EHV: line-connected reactors stay with the line and suppress Ferranti whenever the line is energized; bus reactors are switched with load. A line reactor that remains connected at heavy load eats Q that the corridor then needs from generators. Tertiary windings of autotransformers are a favourite place to hang reactors and capacitors in some utilities.

On-load tap changers have a deadband and a time delay (tens of seconds) so they do not tap on every flicker. Reverse-flow issues on feeders with PV (elective renewables) can make OLTCs hunt. In a transmission-level collapse scenario, the delayed tap restoration of aggregated distribution OLTCs is a standard slow-collapse narrative: each tap-up restores P and Q of voltage-sensitive loads, which further depresses EHV V.

Series capacitor location: mid-line is common; a platform sits at line potential. Bypass gaps or MOV plus a triggered bypass protect the C during faults. Bypass changes \(X_{\mathrm{net}}\) during the fault, which matters for both fault current (unit 04) and transient stability (unit 06). Compensating past ~70% of \(X_L\) is where SSR and protective-relaying (distance) complications pile up; UG treats 30–50% as a routine example.

Voltage setpoints: running a 400 kV grid at 1.02–1.05 pu lightens \(I^2R\) for a given P but raises insulation duty and transformer core flux if taps are not coordinated. Statutory customer LV bands are tighter than EHV operating bands. Do not apply a ±5% customer limit as a 400 kV operational cap without reading the grid code.

## Equations

Approximate drop, \(X\gg R\):

\[
\Delta V\approx \frac{RP+XQ}{V}.
\]

Shunt capacitor (three-phase, \(V\) line-to-line, \(C\) per phase wye-equivalent):

\[
Q_C=V^2\omega C.
\]

Load-convention absorbed Q of a capacitor is negative; the bank “supplies” \(Q_C\) to the bus.

Series compensation: \(X_{\mathrm{net}}=X_L-X_C\), degree \(k=X_C/X_L\).

Two-bus lossless, Q=0 load, voltage-limited:

\[
P_{\max}=\frac{E^2}{2X},\qquad V=\frac{E}{\sqrt{2}}\ \text{at the nose}.
\]

Both ends held at V (angle limit): \(P_{\max}=V^2/X\).

Line charging: \(Q_{\mathrm{chg}}=V^2 B\) with \(B=\omega C_{\mathrm{total}}\) as in unit 02.

Tap: \(V_{\mathrm{load}}\approx t V_{\mathrm{supply}}\) for an ideal transformer, with \(t\) the off-nominal ratio as defined on the one-line; real OLTC steps are typically 1.25% class.

## Methods

1. Convert to pu. Identify whether the problem holds both voltages (angle-limited P) or holds only sending E with a load (voltage-limited P).
2. For capacitor sizing to a pf target: \(Q_C=P(\tan\phi_1-\tan\phi_2)\) then \(C=Q_C/(\omega V^2)\) with the voltage at the bank.
3. For voltage raise on a radial Thevenin \(E,X\): linearize \(\Delta V\approx X\Delta Q/V\) or solve the quadratic \(V^2+Q X= E V\cos\delta\) with P constraint.
4. For SIL diagnostics: compute \(P_{\mathrm{SIL}}=V^2/Z_c\); compare actual P.
5. Sketch Q–V: large Q_load (absorbed) lowers V; capacitive injection raises V until a limit.

Checks: \(Q_C\) scales with \(V^2\) so a 0.9 pu voltage yields 0.81 of rated bank Mvar; generator Q inside the capability box; nose \(P_{\max}=E^2/(2X)\) only for the Q=0 radial case derived above; OLTC on the wrong side of a transformer raises the wrong voltage.

When placing a bank, put it on the side of the transformer where the voltage problem lives, or you will fight the leakage \(X_t\). A capacitor on a depressed bus does less (\(V^2\)); a STATCOM does better (unit 11).

## Mistakes

Using \(P_{\max}=V^2/X\) for a radial constant-power load whose receiving voltage is not regulated. Sizing C from \(Q=\omega C V\) missing a V. Applying shunt C formulas to a series capacitor. Forgetting \(V^2\) when the bus is not 1.0 pu. Raising generator \(V_t\) into overvoltage to support a remote bus when a local capacitor was the right tool — or the opposite, dumping capacitors on a generator bus that already has AVR. Treating voltage collapse as a first-swing EAC problem. Using pf correction \(Q_C\) at the customer when the voltage problem is EHV Ferranti (need reactors, not capacitors). Changing taps to fix a Q-deficient collapse in a direction that restores LV load and worsens EHV. Mixing three-phase and per-phase C by a factor of 3. Ignoring that a capacitor switched in at light load can cause a leading-pf overvoltage. Using SIL as a thermal rating. Writing \(\Delta V=XQ/V^2\). Assuming a synchronous condenser supplies P. Using lagging/leading names for generator Q with the opposite IEEE convention (state “absorbing vars” instead of arguing the word).

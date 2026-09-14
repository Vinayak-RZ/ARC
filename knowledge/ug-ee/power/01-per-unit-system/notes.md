# Base change, single-line diagrams, and the per-unit system

A power network mixes kilovolts, megawatts, ohms, and transformer turns ratios. Writing every impedance in ohms and every voltage in volts produces numbers that span many decades and that must be referred through every transformer. The per-unit (pu) system scales voltages, currents, impedances, and powers to chosen bases so that a transformer looks like a series leakage of a few tenths of a unit, a generator subtransient reactance sits near \(0.1\)–\(0.25\ \mathrm{pu}\), and a load of \(1.0\ \mathrm{pu}\) means “rated MVA at rated voltage.” Undergraduate power-system analysis, fault studies, and load flow all assume this language. This unit is that language: bases, the four-quantity constraint, change of base, single-line diagrams, and how transformers disappear into a common pu circuit.

Numbers here are original teaching examples. They are not copied from commercial textbooks or from GATE papers.

## Concepts

Four quantities define a single-phase or per-phase circuit: voltage \(V\), current \(I\), impedance \(Z\), and apparent power \(S\). They are not independent. Ohm’s law \(V=ZI\) and the power identity \(S=VI^*\) (RMS phasors, load convention) mean that choosing two bases determines the other two. The usual undergraduate choice is a voltage base \(V_\mathrm{base}\) and a power base \(S_\mathrm{base}\). Then

\[
I_\mathrm{base}=\frac{S_\mathrm{base}}{V_\mathrm{base}},\qquad Z_\mathrm{base}=\frac{V_\mathrm{base}}{I_\mathrm{base}}=\frac{V_\mathrm{base}^2}{S_\mathrm{base}}.
\]

A physical ohmic impedance \(Z_\Omega\) becomes \(Z_\mathrm{pu}=Z_\Omega/Z_\mathrm{base}\). A physical voltage becomes \(V_\mathrm{pu}=V/V_\mathrm{base}\). Per-unit current is \(I_\mathrm{pu}=I/I_\mathrm{base}\). Per-unit power is \(S_\mathrm{pu}=S/S_\mathrm{base}\). The same identities hold in pu: \(V_\mathrm{pu}=Z_\mathrm{pu}I_\mathrm{pu}\) and \(S_\mathrm{pu}=V_\mathrm{pu}I_\mathrm{pu}^*\) if the bases are consistent. Inconsistent bases (a voltage base that does not match the \(S\) and \(Z\) bases through the two identities) produce a circuit that does not obey Ohm’s law in pu. That is the first thing to check when a diagram “does not close.”

Three-phase work uses the same idea with a three-phase power base \(S_\mathrm{base,3\phi}\) and a line-to-line voltage base \(V_\mathrm{base,LL}\). The consistent impedance base on the per-phase Y-equivalent is

\[
Z_\mathrm{base}=\frac{V_\mathrm{base,LL}^2}{S_\mathrm{base,3\phi}}=\frac{V_\mathrm{base,\phi}^2}{S_\mathrm{base,1\phi}},
\]

where \(V_\mathrm{base,\phi}=V_\mathrm{base,LL}/\sqrt{3}\) and \(S_\mathrm{base,1\phi}=S_\mathrm{base,3\phi}/3\). Using line-to-line volts squared over three-phase MVA is the formula that must sit in muscle memory. Using phase volts with three-phase MVA, or line volts with per-phase MVA, is a factor-of-three error that appears in almost every first exam.

A transformer does not change pu voltage if the voltage bases on the two sides are chosen in the turns ratio. That is the whole point. If \(a=N_1/N_2=V_{\mathrm{rated},1}/V_{\mathrm{rated},2}\), pick \(V_{\mathrm{base},1}\) and set \(V_{\mathrm{base},2}=V_{\mathrm{base},1}/a\). Then an ideal transformer has \(V_{1,\mathrm{pu}}=V_{2,\mathrm{pu}}\) and \(I_{1,\mathrm{pu}}=I_{2,\mathrm{pu}}\) (power in equals power out), so the ideal transformer can be omitted from the pu single-line diagram. Only leakage (and magnetizing, if kept) remain as series (and shunt) pu impedances. Nameplate transformer impedance is already in pu on the transformer’s own rating. It must be changed to the system base before it is drawn next to a line or a machine that used a different MVA base.

Change of base is algebraic, not mystical. An impedance given as \(Z_\mathrm{pu}^\mathrm{old}\) on \((S_\mathrm{base}^\mathrm{old},V_\mathrm{base}^\mathrm{old})\) converts as

\[
Z_\mathrm{pu}^\mathrm{new}=Z_\mathrm{pu}^\mathrm{old}\cdot\frac{S_\mathrm{base}^\mathrm{new}}{S_\mathrm{base}^\mathrm{old}}\cdot\left(\frac{V_\mathrm{base}^\mathrm{old}}{V_\mathrm{base}^\mathrm{new}}\right)^2.
\]

If the voltage base is unchanged (same voltage level, only the MVA base of the study changes), the voltage-ratio factor is one and pu impedance scales with MVA base. That is why a machine quoted as \(X''=0.20\ \mathrm{pu}\) on \(50\ \mathrm{MVA}\) becomes \(0.40\ \mathrm{pu}\) on a \(100\ \mathrm{MVA}\) system base: twice the MVA base, twice the pu reactance. The ohmic reactance did not change. The yardstick did.

Voltage bases must follow transformers. A study that picks \(132\ \mathrm{kV}\) on a \(132\ \mathrm{kV}\) bus and then uses \(132\ \mathrm{kV}\) on the \(33\ \mathrm{kV}\) side of a \(132/33\ \mathrm{kV}\) transformer has broken the turns-ratio rule. The \(33\ \mathrm{kV}\) side base should be \(33\ \mathrm{kV}\) if the high-side base is \(132\ \mathrm{kV}\) and the transformer is rated \(132/33\). Off-nominal taps (a transformer rated \(138/13.8\) sitting in a \(132\ \mathrm{kV}\) network) require either an ideal off-nominal tap in the pu circuit or a careful restatement of bases. Undergraduate problems usually align rated voltages with bases so the tap is \(1.0\). When a tap \(t\) (pu of rated) is given, the pu model is a series leakage with an ideal transformer of ratio \(t\) on one side, or an equivalent \(\pi\) of off-nominal ratios. Do not absorb an off-nominal tap into \(Z_\mathrm{base}\) unless you write the formula you used.

Single-line (one-line) diagrams are the drawing convention of power systems. One line represents three phases of a balanced network. Symbols: generator as a circle with a terminal, transformer as two (or three) interleaved circles, transmission line as a single stroke, bus as a thick bar, circuit breaker as a square or X, load as an arrow. Impedances are marked in pu or in ohms with a stated base. The diagram is not a DC schematic: a “line” is a three-phase circuit with series \(R+jX\) and shunt \(B\), not a single wire to ground. Neutral and ground are omitted unless the study is unbalanced (sequence networks, unit 05) or grounding (unit 08). Balanced load flow and balanced faults live on the positive-sequence single-line diagram.

Per-unit voltages near \(1.0\) are normal. A bus at \(1.05\ \mathrm{pu}\) is 5% high. A load flow that reports \(0.4\ \mathrm{pu}\) voltage is a collapsed network, not a “weak” one in ordinary language. Per-unit currents near \(1.0\) mean rated current of the chosen \(S_\mathrm{base}\) at that voltage base, which is not necessarily the thermal rating of a particular feeder. Always state the bases in the header of a calculation: “\(S_\mathrm{base}=100\ \mathrm{MVA}\), \(V_\mathrm{base}=132\ \mathrm{kV}\) at bus 3, \(33\ \mathrm{kV}\) at bus 4.” Without that sentence the numbers are meaningless.

Motors and generators have nameplate kVA (or MVA) and rated voltage. Their pu impedances on nameplate must be converted to the study base. A small motor on a large system base has a large pu impedance (it barely loads the system). A large generator on a small study base has a small pu impedance (it looks like a stiff source). That is physical: short-circuit contribution scales with machine size.

Lines are usually given in ohms or in pu already on a stated voltage. A \(50\ \mathrm{km}\) line with \(0.4\ \Omega/\mathrm{km}\) of reactance on \(132\ \mathrm{kV}\) and \(100\ \mathrm{MVA}\) is \(Z_\mathrm{base}=132^2/100=174.24\ \Omega\), so \(X=20/174.24=0.115\ \mathrm{pu}\). Charging susceptance follows the same \(Z_\mathrm{base}\) (or \(Y_\mathrm{base}=1/Z_\mathrm{base}\)). Do not convert B with the impedance formula and then treat the result as a series element.

Advantages that actually matter in UG work: (1) transformer ideal ratios vanish; (2) comparable equipment has comparable pu numbers regardless of kV class, which is a sanity check; (3) three-phase factors of \(\sqrt{3}\) are absorbed into the bases if you are consistent, so the per-phase pu circuit looks like a single-phase circuit. Disadvantages: a sloppy base table silently corrupts every later study; off-nominal taps and three-winding transformers need extra care; restoring SI units for relay settings or thermal limits requires multiplying back by the local bases, and the local voltage base is bus-dependent.

A three-winding transformer has three voltage ratings and usually one MVA rating per winding that may differ (e.g. 100/100/40 MVA). Convert each winding leakage to a common \(S_\mathrm{base}\), then use the star-equivalent (three reactances from a fictitious star point to H, M, L). The star point is not a physical bus unless you create one. Autotransformers follow the same pu leakage on the winding MVA, but the through-MVA and the series/common winding split belong in a machines or transformer unit; here, treat the nameplate \(Z\%\) as given on the stated throughput rating and convert.

Per-unit admittance is \(Y_\mathrm{pu}=1/Z_\mathrm{pu}\) only if the same bases are used. Shunt capacitors quoted in Mvar at rated kV convert as \(Q_\mathrm{pu}=Q_\mathrm{Mvar}/S_\mathrm{base,MVA}\) at \(V=1.0\ \mathrm{pu}\). At a different voltage the reactive output scales as \(V^2\). That \(V^2\) law is why a capacitor bank “does less” when the bus is already depressed — the worst time to need vars.

Phase-shifting transformers and tap changers in series with a line add a complex tap \(t e^{j\phi}\) in the pu \(\pi\) or series model. Undergraduate load-flow introductions often keep \(t\) real. If \(\phi\neq 0\), \(Y_\mathrm{bus}\) is no longer symmetric. Mention it, then return to real taps until unit 03.

Grounding transformers, zigzag banks, and earthing compensators are sequence-network devices. They do not appear on a positive-sequence single-line diagram except as a note “solidly earthed” or “earthing transformer at bus 2.” Do not put a zigzag impedance in the positive-sequence pu circuit as if it carried load current.

Base of time and of frequency: pu speed and pu torque appear in machine and stability work (unit 06). For network studies in this unit, time is in seconds and \(\omega=2\pi f\) with \(f=50\) or \(60\ \mathrm{Hz}\) as given. Do not invent a “per-unit frequency” unless a machine-model card asks for it.

A worked habit: draw the single-line with kV on each section, write a base table (zone, \(V_\mathrm{base}\), \(S_\mathrm{base}\), \(Z_\mathrm{base}\)), convert every nameplate \(Z\%\) and every ohmic line to that table, then redraw a pu one-line with only pu numbers and no transformers (or with taps shown as \(t\)). The second drawing is what load flow and faults consume.

## Equations

Single-phase bases:

\[
I_\mathrm{base}=\frac{S_\mathrm{base}}{V_\mathrm{base}},\qquad Z_\mathrm{base}=\frac{V_\mathrm{base}^2}{S_\mathrm{base}},\qquad Y_\mathrm{base}=\frac{1}{Z_\mathrm{base}}.
\]

Three-phase (line-to-line voltage, three-phase power):

\[
Z_\mathrm{base}=\frac{(V_\mathrm{base,LL})^2}{S_\mathrm{base,3\phi}},\qquad I_\mathrm{base,line}=\frac{S_\mathrm{base,3\phi}}{\sqrt{3}\,V_\mathrm{base,LL}}.
\]

Per-unit conversion:

\[
Z_\mathrm{pu}=\frac{Z_\Omega}{Z_\mathrm{base}},\qquad V_\mathrm{pu}=\frac{V}{V_\mathrm{base}},\qquad S_\mathrm{pu}=\frac{S}{S_\mathrm{base}}.
\]

Change of base:

\[
Z_\mathrm{pu,new}=Z_\mathrm{pu,old}\times\frac{S_\mathrm{new}}{S_\mathrm{old}}\times\left(\frac{V_\mathrm{old}}{V_\mathrm{new}}\right)^2.
\]

Nameplate percent impedance \(Z\%=100\,Z_\mathrm{pu,nameplate}\). A transformer \(Z=8\%\) on \(40\ \mathrm{MVA}\) is \(0.08\) pu on \(40\ \mathrm{MVA}\).

Ideal transformer omitted when \(V_{\mathrm{base},1}/V_{\mathrm{base},2}=N_1/N_2\). Then \(V_{1\mathrm{pu}}=V_{2\mathrm{pu}}\) and \(S_{1\mathrm{pu}}=S_{2\mathrm{pu}}\).

## Methods

1. Choose a system \(S_\mathrm{base}\) (often \(100\ \mathrm{MVA}\)) and a voltage base in one zone (often a generator rated kV or a grid kV).
2. Propagate voltage bases through every transformer using rated ratios (or stated taps).
3. Compute \(Z_\mathrm{base}\) in each zone from \(V_\mathrm{LL}^2/S_{3\phi}\).
4. Convert lines from \(\Omega\) and machines/transformers from nameplate pu to the system base with the change-of-base formula.
5. Draw the pu single-line. Drop ideal transformers. Keep off-nominal taps as explicit \(t\).
6. Solve the pu circuit (KVL/KCL, \(Y_\mathrm{bus}\), Thevenin). Convert answers back to kV, kA, MVA by multiplying by the local bases.

Checks: pu voltages near 1; transformer pu Z on system base in a plausible band (a few percent to ~15% for two-winding power transformers); a \(100\ \mathrm{MVA}\) machine \(X''\approx 0.15\)–\(0.25\) on its own MVA; Ohm’s law in pu; three-phase \(S=\sqrt{3}V_\mathrm{LL}I_L\) restored from \(S_\mathrm{pu}S_\mathrm{base}\).

For a two-machine, two-transformer radial drill: convert both machine reactances and both transformer leakages to one \(S_\mathrm{base}\), add series pu reactances, apply a \(1.0\ \mathrm{pu}\) prefault voltage, and read fault current as \(1/X_\mathrm{th}\). That calculation is the bridge into unit 04.

When a problem mixes Δ and Y ratings, still use line-to-line kV as \(V_\mathrm{base}\) and three-phase MVA as \(S_\mathrm{base}\). The connection type affects sequence networks and harmonics, not the positive-sequence \(Z_\mathrm{base}\) formula.

## Mistakes

Using \(Z_\mathrm{base}=V_\mathrm{phase}^2/S_\mathrm{3\phi}\) (factor-of-three error). Forgetting to change transformer \(Z\%\) from nameplate MVA to system MVA. Using the same kV base on both sides of a transformer. Converting current with \(S/V\) instead of \(S/(\sqrt{3}V)\) for line current. Treating \(Z\%\) as ohms. Scaling pu Z with voltage linearly instead of with \(V^2\). Restoring kV using the wrong zone’s base after a transformer. Putting a zigzag earthing impedance in the positive-sequence diagram. Assuming \(1.0\ \mathrm{pu}\) voltage is \(1\ \mathrm{kV}\). Adding pu impedances that were computed on different MVA bases. Using \(S=VI\) instead of \(\sqrt{3}V_\mathrm{LL}I_L\) when converting a three-phase load into pu. Ignoring an off-nominal tap and still claiming \(V_\mathrm{pu}\) is continuous across the transformer. Writing \(I_\mathrm{base}=S_\mathrm{base}/(\sqrt{3}V_\mathrm{base})\) with \(V_\mathrm{base}\) in volts and \(S\) in MVA without converting to VA (a \(10^6\) error). Quoting pu current as “rated current of the line” when the base was system MVA, not the line’s thermal MVA.

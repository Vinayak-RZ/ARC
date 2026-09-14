# Cables, insulator strings, and grounding

A power network is not only reactances on a one-line. Conductors must be insulated from towers and from earth; underground and submarine circuits use cables; neutrals and equipment frames must be grounded so that fault current has a path and touch voltages stay tolerable. Undergraduate T&D courses treat cable construction and capacitance, string efficiency of suspension insulators, and the ideas of solid, impedance, and Peterson-coil grounding. Detailed soil ionization, GIS, and XLPE ageing models are specialist HV courses.

## Concepts

Overhead line insulation is mostly air plus porcelain, glass, or composite disc strings at towers. The number of discs grows with system voltage: a 132 kV string might have 9–11 discs, 400 kV many more — exact counts are utility practice, not a universal formula. Each disc is a capacitance to the next disc and a capacitance to the tower (metal). The result is a capacitive voltage divider that puts more voltage on the line-end disc than on the tower-end disc. String efficiency is (total voltage across the string) / (n × voltage across the most stressed disc). Equalizing methods: longer strings, guard rings (grading rings) that add capacitance at the line end, and sometimes a choice of disc capacitances. Rain, pollution, and altitude reduce withstand; creepage distance, not just dry flashover, governs polluted areas. Impulse withstand (lightning, switching) is a different test from power-frequency withstand (unit of HV engineering).

Pin insulators appear on distribution. Post insulators appear in substations. Suspension strings allow a broken conductor to swing without destroying the tower cross-arm in the same way a rigid pin would. Stay insulators interrupt guy wires.

Cables: a conductor, XLPE or oil-paper dielectric, screens, sheath, armour, and jacket. Compared with overhead lines, cables have much smaller spacing, hence much larger capacitance per kilometre and smaller inductance. Charging Mvar can limit AC cable length (tens of kilometres at EHV AC) unless reactors compensate; that is a driver for HVDC cables (unit 11). Single-core vs three-core: at HV, single-core cables in trefoil or flat formation dominate. Sheath bonding: solid bonding (sheath circulating currents, heat), single-point bonding (standing voltage on the open sheath, need SVLs), and cross-bonding (transpose sheaths to cancel induced voltage, the usual EHV practice). UG numericals often give capacitance per phase and ask charging current \(I_c=\omega C V_\phi\).

Cable current rating (ampacity) is a thermal problem: \(I^2R\) plus dielectric loss plus sheath loss, dissipated through soil or ducts with thermal resistivity. Derating for grouping and soil dryness matters more than a one-line \(Z\). Skin and proximity effects raise AC resistance. This unit computes electrical C and charging, not a full Neher–McGrath rating.

Inductance of a cable is low; series \(X\) is not the voltage-drop villain that it is on overhead — resistance and, for long AC cables, charging and reactive flow are. Ferranti on a cable can be severe for length that would still be “short” as overhead.

Insulation resistance and tanδ tests diagnose moisture. A high-pot test is a commissioning ritual with limits; do not confuse it with operating voltage.

Grounding (earthing):

- System grounding: how the power-system neutral is connected to earth. Solid (effective) grounding: \(X_0/X_1\) small, LG fault current high, healthy-phase overvoltage modest, relaying of LG easy. Resistance grounding: fault current limited to tens or hundreds of amperes, used on some industrial and MV systems. Reactance grounding. Resonant grounding (Petersen coil, arc-suppression coil) tunes \(3L\omega =1/\omega C\) of the zero-sequence network so that the inductive current cancels cable/overhead charging during a single-phase earth fault; the residual current is small and many transient faults self-extinguish. Ungrounded: no intentional neutral ground; earth faults are charging current only; overvoltages on healthy phases approach \(\sqrt{3}\) times; detection by residual voltage; not used on long overhead HV in modern grids.

- Equipment grounding: bonding frames to earth so that a live-to-frame fault trips a breaker instead of leaving the frame at a dangerous potential.

- Substation ground grid: mesh of buried conductors sized so that grid resistance, mesh voltage, and step voltage during a ground fault stay within IEEE-style body-current limits (body weight, fault duration). UG computes a crude \(R_g=\rho/(4r)\) for a circular plate analog or uses a given \(R_g\) with \(V=I_g R_g\). Soil resistivity \(\rho\) varies with moisture and season.

Ground-fault factor is the ratio of highest healthy-phase-to-ground voltage during a fault to the unfaulted phase-to-ground voltage. Effectively grounded systems keep it \(\le 1.4\) approximately (utility definitions vary around \(X_0/X_1\le 3\)). Arresters are rated with this in mind.

Tower footing resistance affects lightning backflash: a high footing resistance lets a lightning current raise the tower so high that insulators flash from tower to conductor. Counterpoise and driven rods reduce it. Not a load-flow parameter.

Neutral grounding transformer (zigzag or YNd) provides a zero-sequence path on an otherwise ungrounded delta or ungrounded-Y collection bus. Its impedance appears as \(Z_0\) in unit 05.

Corona on overhead lines: air ionization when surface gradient exceeds a critical value. Loss, audible noise, RI, and ozone. Bundling and conductor radius reduce gradient. Corona onset voltage formulas exist (Peek); UG may compute a critical gradient and compare. Cables do not corona in air but can suffer voids in the dielectric (partial discharge).

Sag and span are mechanical (catenary, ice, wind). They set mid-span clearance, which is an insulation coordination issue, but the calculation is civil/mechanical. Mention clearance; do not run a sag numerical unless asked.

String efficiency falls as \(n\) grows if \(K\) is fixed, which is why extra discs without a grading ring are a blunt instrument: you add insulation but the line-end disc still takes a disproportionate share. Guard rings add a capacitance from line to the lower discs’ metal, flattening the distribution. A worked \(n=4\) string is the same KCL ladder with one more node; do not memorize a four-disc closed form, write the three (or four) current-balance equations \(j\omega C(V_{k+1}-V_k)+j\omega KC V_k=j\omega C(V_k-V_{k-1})\) with the tower-end and line-end boundary conditions.

Cable dielectric: XLPE is dry, has a high working stress, and dominates new MV/HV cables. Oil-paper remains in some legacy EHV. EPR appears in industrial MV. The capacitance formula \(C=2\pi\varepsilon/\ln(D/d)\) assumes a cylindrical screen at \(D\); three-core belted cables without a per-phase screen have a more awkward field and a larger \(C_0/C_1\) issue. Screened single-core in trefoil has a computable GMD for inductance, analogous to overhead GMD.

Bonding copy-book: solid bonding — sheaths earthed both ends, circulating current \(I_{\mathrm{sheath}}\) induced by flux between conductor and sheath, extra heat, lowest standing voltage. Single-point — no circulating current, standing voltage \(E=\omega M I \ell\) at the open end, SVL protects against faults. Cross-bonding — three minor sections, sheaths transposed, nearly cancels induced voltage and circulating current; used on long EHV circuits. A UG problem that gives “sheath loss = 10% of conductor loss” is telling you to multiply \(I^2R\) by 1.10, not to derive Carson’s integrals.

Grounding transformers: a zigzag has small positive-sequence impedance (magnetizing only) and a defined zero-sequence impedance. It can be placed at a delta bus to permit earth-fault relaying without connecting a load-carrying winding to earth. In sequence diagrams it is an open circuit in \(Z_1\) and \(Z_2\) (or magnetizing, neglected) and a shunt \(Z_g\) in \(Z_0\).

Soil resistivity: 10 \(\Omega\cdot\mathrm{m}\) wet clay, hundreds in rock; a measured \(\rho\) in the dry season is the conservative design input. Two-layer soils make \(R_g\) formulas empirical. UG uses a uniform \(\rho\) and a stated electrode model.

## Equations

String of \(n\) discs, each self-capacitance \(C\), pin-to-tower (shunt) capacitance \(KC\). The line-end disc voltage \(V_n\) is the largest. String efficiency

\[
\eta=\frac{V_{\mathrm{string}}}{n V_n}.
\]

For \(n=3\) with shunt factor \(K\), a standard circuit solution is

\[
V_1=V',\quad V_2=V'(1+K),\quad V_3=V'(1+3K+K^2),
\]
\[
V_{\mathrm{string}}=V_1+V_2+V_3=V'(3+4K+K^2),
\]

where \(V'\) is the tower-end disc voltage. (Re-derive from KCL at the metal joints if the exam \(K\) definition differs.)

Cable charging, per phase:

\[
I_c=\omega C V_\phi,\qquad Q_{3\phi}=3 V_\phi I_c=V_{LL}^2 \omega C_{\mathrm{eq}}
\]

with \(C\) the given positive-sequence capacitance to the equivalent sheath/earth.

Petersen coil (resonant) inductance for total zero-sequence (three-phase) charging \(C_0\) per phase to ground:

\[
3\omega L = \frac{1}{\omega C_0}\quad\Rightarrow\quad L=\frac{1}{3\omega^2 C_0}
\]

for the coil in the neutral (check the \(C_0\) definition in the problem: sometimes \(C\) is given as complete three-phase earth capacitance).

Simple hemispherical electrode: \(R=\rho/(2\pi r)\). Circular plate on surface (approximate): \(R=\rho/(4r)\).

Touch voltage scale: \(V_g=I_g R_g\) as an upper bound on GPR (ground potential rise); mesh voltage is a fraction of GPR.

## Methods

Insulators: draw the capacitance ladder, write KCL, solve for disc voltages, compute \(\eta\). If a guard ring is given as extra capacitance \(\beta C\) at the line end, include it in the last node’s KCL.

Cables: take \(C\) from data or from coaxial formula \(C=2\pi\varepsilon/\ln(R/r)\) per metre for a single-core screened cable. Compute \(I_c\) at rated \(V_\phi\). Charging Mvar from sending-end or as \(V^2\omega C\).

Grounding: identify system-neutral type from the one-line (zigzag, \(R_n\), solid). For a fault-current problem, put \(3Z_g\) in the zero-sequence network (unit 05). For GPR, \(I_g\) is the earth-return portion of the fault, not the full phase current if shield wires carry some.

Checks: string \(\eta<1\) and decreases as \(K\) or \(n\) grows without grading; cable \(I_c\) of several amperes per kilometre at 132 kV is plausible; Petersen \(L\) in henries for MV cables is a large reactor; \(R_g\) of a substation often a fraction of an ohm to a few ohms.

## Mistakes

Using line-to-line voltage in \(I_c=\omega C V\) without converting to phase for a star-equivalent \(C\). Treating string efficiency as a power efficiency. Assuming equal disc voltages without grading. Putting Petersen coil in the positive-sequence diagram. Using \(Z_g\) instead of \(3Z_g\) in sequence networks. Computing cable ampacity from \(I=V/Z_{\mathrm{surge}}\) (wrong physics). Ignoring sheath bonding when discussing circulating current heat. Using overhead \(Z_0/Z_1\approx 3\) for a cable. Designing a ground grid from \(R=\rho/(4r)\) and calling the GPR equal to the legal touch voltage (mesh factor missing). Counting discs as a linear function of kV without manufacturer data and presenting it as a law. Forgetting that an ungrounded system still has charging current in an earth fault. Using dry-flashover kV as the creepage design in a coastal substation.

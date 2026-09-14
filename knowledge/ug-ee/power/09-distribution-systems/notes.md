# Distribution systems: feeders, radial versus ring, and voltage drop

Generation and EHV transmission deliver bulk power to bulk-supply points. Distribution takes it from there to loads: substations, primary feeders (typically 11 kV or 13.8 kV class), distribution transformers, and low-voltage secondaries (400/230 V or 208/120 V class). Undergraduate T&D courses compare radial, ring (loop), and interconnected networks; compute voltage drop and copper loss on a feeder with concentrated or uniformly distributed load; and introduce voltage control by taps, regulators, and capacitors (unit 12 overlap). Protection of laterals is unit 10. Unbalanced three-phase four-wire modelling at full detail is a distribution-engineering elective.

## Concepts

A feeder is the three-phase circuit leaving a substation bus to serve many laterals. A distributor is the circuit from which loads are tapped more or less continuously (UG language from older UK/Indian syllabi). A service mains is the last drop to a customer. The words overlap in practice; use the problem’s figure.

Radial feeder: one path from source to load. Cheap, simple protection (overcurrent, fuses), poor reliability (a fault blackouts everything downstream until repaired), and larger voltage drop at the tail. Most rural and many urban laterals are radial. Reclosers and sectionalizers improve reliability without making a true loop.

Ring (loop) main: a closed loop fed from one or two ends, often operated with a normally open point to stay radial for protection, or closed for better voltage and redundancy. A fault can be isolated by opening two switches; the rest stays live if the ring can be back-fed. More switchgear, more planning.

Interconnected (meshed) LV in dense cities: many paths, low losses, harder fault location, higher short-circuit levels. UG computes two-feeder parallel paths as a simple mesh.

Voltage drop on a single-phase two-wire DC distributor is \(IR\) and is the historical teaching example. AC three-phase drop uses \(I(R\cos\phi+X\sin\phi)\) per phase for lagging load (approximate magnitude drop), times \(\sqrt{3}\) for line-to-line if using line current and loop quantities carefully. The exact sending-end voltage is the phasor \(V_S=V_R+I(R+jX)\). Use the phasor form unless the problem asks for the approximate drop.

Uniformly distributed load of total current \(I\) on a feeder of resistance \(R\) (one-way, per phase) is equivalent, for voltage drop at the far end, to a concentrated current \(I\) at the midpoint: drop \(= (IR)/2\) if \(X=0\). For copper loss, a uniform load is equivalent to \(I^2 R/3\) (not \(I^2 R/2\)). Those two factors — 1/2 for drop, 1/3 for loss — are the most examined facts in this unit. Derive them: drop \(\int_0^\ell i(x) r\,dx\) with \(i(x)=I(1-x/\ell)\) and \(r=R/\ell\), giving \(IR/2\). Loss \(\int i(x)^2 r\,dx = I^2 R/3\).

Tapered (graded) conductors: theoretically, cross-section following the remaining current saves conductor metal for a given drop; practically, two or three standard sizes are used. UG may ask a two-section feeder.

Fed at both ends (DC or AC with same voltage at both ends): the load divides so that drops from each end match at a point of minimum voltage. For DC, the two end currents \(I_A,I_B\) satisfy \(I_A+I_B=\sum I_{\mathrm{loads}}\) and \(I_A R_A=I_B R_B\) along the path to the minimum-voltage bus, more generally KVL around the loop. Solve as a linear circuit, not as a guessing game.

Load factor \(=\mathrm{average\ load}/\mathrm{peak\ load}\). Diversity factor \(=\sum(\mathrm{individual\ peaks})/\mathrm{coincident\ peak}\). Utilization and demand factors appear in energy audits. A feeder is sized on coincident peak plus growth, not on the sum of nameplates. Copper loss scales with the square of current, so loss factor is not equal to (load factor)² except as a bound; empirical loss-factor formulas exist. UG often takes a stated peak current.

Voltage standards: LV customers typically +10%/−6% or similar statutory bands. Primary voltage drop budget might be 5% plus transformer drop plus LV drop. If the tail is low, options: thicker conductor, higher feeder kV, shorter reach, capacitors (raise V, cut \(I\) for the same P if they correct pf), or a voltage regulator (series autotransformer with taps). Sending-end tap up raises the whole profile and may overvoltage the head of the feeder at light load. Capacitors at the tail help heavy lagging load and can overvoltage at light load (unit 12).

Three-phase four-wire LV: unbalanced single-phase loads, neutral current, and sometimes a high-leg delta. UG balanced-feeder problems ignore unbalance unless a neutral current is asked as \(I_n=I_a+I_b+I_c\) phasor sum.

ACSR versus all-aluminium versus underground cable: resistance, ampacity, and \(X\). Distribution \(X/R\) is often order-1, unlike EHV where \(X\gg R\). So the \(IR\) term in drop is not negligible. Using a transmission-style \(P=V^2\sin\delta/X\) on an 11 kV feeder is the wrong model when \(\delta\) is tiny and \(R\) matters.

Power loss in a three-phase feeder: \(3I^2 R\) with \(I\) the line current and \(R\) the per-phase resistance. Percent loss \(=P_{\mathrm{loss}}/P_{\mathrm{load}}\). Efficiency \(=1-\) that, if no-load transformer losses are ignored.

Kelvin’s law (economic conductor size: annual energy-loss cost equals annual interest on conductor capital) is a historical UG topic. It ignores voltage-drop and ampacity constraints that usually bind first. Mention; compute only if asked.

Urban 11 kV ring-main units (RMUs) with SF6 or vacuum switches, and rural spur fuses, are equipment names for the reliability discussion, not a bill of materials.

Voltage drop allocation: a typical UG design sketch might allow 2–3% on the primary feeder, 1–2% on the distribution transformer (nameplate impedance plus loading), and 3–5% on the LV distributor, leaving the customer inside a ±6 to ±10% statutory band around nominal. If a calculation shows 12% primary drop (as in a worked question with a long 11 kV feeder and a heavy concentrated load), the feeder is undersized or too long: raise kV, parallel a second circuit, or add a midpoint capacitor or regulator. Percent drop is \(\Delta V_{\mathrm{LL}}/V_{\mathrm{rated}}\), not \(\Delta V_{\mathrm{phase}}/V_{\mathrm{LL}}\).

Uniform-load derivations, written once so they are not magic numbers. Let distance \(x\) from the sending end, length \(\ell\), linear current density \(I/\ell\). Remaining current at \(x\) is \(I(1-x/\ell)\). Resistance of a slice is \((R/\ell)dx\) per conductor. Voltage drop on that conductor from 0 to \(\ell\):

\[
\Delta V=\int_0^\ell I\bigl(1-\tfrac{x}{\ell}\bigr)\tfrac{R}{\ell}\,dx=IR/2.
\]

Loss in that conductor:

\[
P=\int_0^\ell \bigl[I(1-x/\ell)\bigr]^2\tfrac{R}{\ell}\,dx=I^2 R/3.
\]

For a three-phase feeder, multiply loss by 3 if \(R\) is per-phase one-way. For a DC two-wire circuit, use loop resistance in the drop formula and two conductors in the loss formula, which is the same as using \(R_{\mathrm{loop}}\) with \(I^2 R_{\mathrm{loop}}/3\).

A ring operated closed is a mesh of two paths. If the two sides have impedances \(Z_a,Z_b\) and a load at the junction, the currents split as in a current divider \(I_a=I Z_b/(Z_a+Z_b)\). Voltage drop from the common source to the load is \(I(Z_a\parallel Z_b)\). That is why a closed ring with equal sides halves the effective impedance relative to one radial of the same conductor — only when the load is at the far midpoint and the two halves are equal. A load near one end does not enjoy that factor of two.

Power-factor effect: the approximate drop \(I(R\cos\phi+X\sin\phi)\) shows that a lagging load is worse than unity pf not only because \(I=P/(\sqrt{3}V\mathrm{pf})\) is larger but because the \(X\sin\phi\) term adds. Leading pf can cancel the \(X\) term and even produce a rise. Capacitors on a feeder are therefore both a current reducer and a drop reducer; at light load they may need to be switched off (unit 12).

## Equations

Approximate three-phase line-to-line voltage drop (lagging \(\phi\)):

\[
\Delta V_{LL}\approx \sqrt{3}\,I(R\cos\phi+X\sin\phi).
\]

Exact: \(V_S=V_R+I(R+jX)\) per phase, then \(V_{LL}=\sqrt{3}|V_\phi|\).

Uniform load, resistance only, far-end drop: \(\Delta V=IR/2\). Copper loss: \(P_{\mathrm{cu}}=I^2 R/3\) per conductor (times 3 for three phases with the same \(R\) per phase).

Fed from both ends, two concentrated loads: write two KVL/KCL equations for the end currents.

Three-phase loss: \(P_{\mathrm{loss}}=3I^2R\).

Load factor: \(\mathrm{LF}=P_{\mathrm{avg}}/P_{\mathrm{peak}}\). Diversity: \(\mathrm{DF}=\sum P_{\mathrm{peak},i}/P_{\mathrm{coincident}}\).

## Methods

1. Convert the feeder to a per-phase series \(R+jX\) (or DC \(R\)).
2. Represent loads as concentrated currents or as a uniform density. For AC, get \(I=P/(\sqrt{3}V\,\mathrm{pf})\) at the given voltage (approximate with rated V if drop is small).
3. Compute drop by phasor or by the approximate formula. Compare to the allowed percent of rated.
4. For both-end feed, solve loop currents; locate the minimum-voltage point (where current reverses).
5. Losses from \(3I^2R\) with the actual current profile (use \(I^2R/3\) for uniform).

Checks: drop a few percent on a well-sized UG example; both-end feed drop less than one-end; uniform-load drop half of concentrated-at-end; loss factor between LF and 1.

If voltage is so low that \(I=P/(\sqrt{3}V)\) should use the receiving voltage, iterate once: compute drop at rated V, update \(V_R\), recompute \(I\). UG often skips the iteration.

## Mistakes

Using \(I^2R/2\) for uniform-load copper loss (that is the drop factor). Using DC drop on an inductive AC feeder. Mixing phase and line voltages in \(\sqrt{3}\). Sizing a feeder on the sum of nameplate kVA without diversity. Applying EHV SIL ideas to 11 kV. Assuming a closed ring has half the drop of a radial of the same conductor without computing the split. Using sending-end voltage as the load voltage in \(P=\sqrt{3}VI\,\mathrm{pf}\) after a large drop. Forgetting that capacitors reduce current only by supplying \(Q\), not by changing \(P\). Treating Kelvin’s law as a thermal ampacity check. Drawing a ring but analysing it as two independent radials with no KVL. Using \(P=V^2/R\) for a three-phase feeder loss.

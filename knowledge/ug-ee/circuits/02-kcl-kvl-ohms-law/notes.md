# KCL, KVL, Ohm's law, independent sources

Kirchhoff's laws and Ohm's law are the three algebraic statements that turn a lumped schematic into equations. They are not optional tricks; they are conservation of charge, conservation of energy around a loop under the lumped hypothesis, and the constitutive law of a linear resistor. Independent sources are the excitations. Together they solve every linear resistive network, either by inspection in trivial graphs or by systematic nodal and mesh analysis in later units.

## Concepts

Kirchhoff's current law (KCL) says that the algebraic sum of currents leaving a node is zero at every instant. Equivalently, the sum of currents into a closed surface is zero. This is charge conservation plus the lumped assumption that no charge piles up on a node of zero capacitance. A supernode is a closed surface that may enclose voltage sources; KCL still applies to the surface even when it does not apply in the naïve form at an interior floating node of a voltage source.

Kirchhoff's voltage law (KVL) says that the algebraic sum of voltage drops around any closed loop is zero at every instant. Under the lumped hypothesis this is Faraday's law with negligible magnetic flux through the loop area. If a circuit is drawn with a large loop around a transformer core, KVL in the naïve form fails and we must insert a mutual inductance or an induced emf element. In ordinary textbook planar graphs, KVL holds for every mesh and every loop.

Ohm's law for a linear time-invariant resistor is \( v = Ri \) with the passive sign convention. Resistance \( R \) is positive for passive materials at a fixed temperature. A negative resistance is an active local model (tunnel diode incremental resistance, or a dependent-source equivalent). Temperature, frequency (skin effect), and voltage (lamp filaments) can make \( R \) nonlinear; then Ohm's law is replaced by a \( v \)-\( i \) curve and small-signal linearization.

An independent voltage source specifies \( v(t) \) as a function of time, not of any circuit variable. An independent current source specifies \( i(t) \). Practical sources are modeled as an ideal source plus an internal resistance: Thévenin form \( v_s \) in series with \( R_s \), Norton form \( i_s \) in parallel with \( R_p \). Connecting two ideal voltage sources in parallel is allowed only if they are identical; otherwise the model is inconsistent. Connecting two ideal current sources in series is likewise inconsistent unless they are equal.

Reference directions are chosen by the analyst. KCL and KVL remain true for any consistent choice; only the signs in the written equations change. A common beginner error is to choose directions, then silently reverse them when a numerical current comes out negative. A negative result means the physical current is opposite the arrow; keep the arrow and keep the minus, or redraw and re-solve, but do not mix the two mid-algebra.

Ground is a chosen node with voltage zero. It is not necessarily earth. Chassis ground, analog ground, and earth ground are different conductors that may be bonded at one point. In KCL, ground is an ordinary node that often has a large returning current. In KVL, paths that go “through ground” are still loops.

Series elements share the same current. Parallel elements share the same voltage. Those geometric facts are KCL and KVL in disguise: two-terminal elements in series have one current by KCL at the interior node with nowhere else to go; two-terminal elements in parallel have equal voltages by KVL around the two-element loop.

Power from KCL and KVL: Tellegen's theorem (later unit) says that if the currents satisfy KCL and the voltages satisfy KVL, then \(\sum v_k i_k = 0\) over all branches. Instantaneously, sources and absorbers balance. That is why we can compute absorbed resistor power and infer delivered source power without a separate “energy law.”

Ideal meters: an ideal voltmeter is an open circuit; an ideal ammeter is a short. Placing an ammeter in parallel with a source, or a voltmeter in series with a branch, is a wiring error that the laws will still “solve,” giving huge currents or zero circuit current. The mathematics is not a substitute for a legal interconnection.

Dependent sources are controlled by a voltage or current elsewhere. They are not independent excitations; they are linear (or nonlinear) constitutive elements. Superposition treats independent sources one at a time and leaves dependent sources active. That distinction belongs in the theorems unit but is already needed when writing KCL/KVL with a VCCS present.

A practical lab story makes the same laws concrete. If a 9 V battery, a switch, and a lamp are in one loop, KVL says the battery voltage equals the lamp drop plus the tiny drop in the leads. Ohm's law on the lamp (nonlinear, actually) gives a current; KCL at the battery plus says that current is the only current. If someone adds a second lamp in parallel, KCL at the plus node now splits the current; KVL around each lamp loop still sees essentially 9 V. If they add the second lamp in series, KVL shares 9 V between two lamps and the current falls. Nothing in that paragraph used a theorem beyond KCL, KVL, and a constitutive curve. That is why this unit is placed before nodal matrices: students must believe the three laws on a breadboard before they trust a 4×4 conductance stamp. Ideal independent sources fail in the lab when the battery's internal resistance and the current limit of a bench supply appear; then the model is a source plus R_internal, still solved by the same three laws.

## Equations

KCL at node \( n \): \( \sum_k i_{nk} = 0 \) with \( i_{nk} \) leaving \( n \).

KVL around loop \( \ell \): \( \sum_m v_m = 0 \) with a consistent traverse direction.

Ohm: \( v_R = R i_R \) (PSC). Conductance form \( i_R = G v_R \).

Independent voltage source: \( v = v_s(t) \), \( i \) free. Independent current source: \( i = i_s(t) \), \( v \) free.

Series: \( i_1 = i_2 = \cdots \), \( v_\mathrm{eq} = \sum v_k \). Parallel: \( v_1 = v_2 = \cdots \), \( i_\mathrm{eq} = \sum i_k \).

Two resistors series: \( R_\mathrm{eq} = R_1 + R_2 \). Parallel: \( R_\mathrm{eq} = R_1 R_2 / (R_1 + R_2) \).

Power balance: \( \sum_{\text{sources}} P_\mathrm{del} = \sum_{\text{resistors}} P_\mathrm{abs} \) in DC resistive networks (Tellegen special case).

Internal resistance models: \( v_\mathrm{term} = v_s - R_s i_\mathrm{load} \) (Thévenin), \( i_\mathrm{term} = i_s - v_\mathrm{term}/R_p \) (Norton).

## Methods

Draw the circuit, label nodes, pick a ground. Assign a current to every branch or a voltage to every node. Write KCL at enough nodes (all but ground, or all including a check). Write KVL around enough loops (meshes for planar graphs). Substitute Ohm's law to eliminate extra variables. Solve the linear system. Then compute any requested power using the passive sign convention on each element.

For a single-loop circuit, one KVL plus Ohm gives the loop current immediately: \( i = v_s / \sum R \). For a single-node-pair (all sources and resistors in parallel), one KCL plus Ohm gives the node voltage: \( v = i_s / \sum G \). For mixed circuits, do not invent a “total resistance seen by all sources” unless you have reduced to one source.

When a voltage source sits between two non-ground nodes, use a supernode: write KCL for the combined surface and add the constraint \( v_a - v_b = v_s \). When a current source sits on a mesh boundary, use a supermesh: write KVL skipping that source and add the constraint on the two mesh currents.

Check: substitute the solution back into unused KCL or KVL equations. Check power balance. Check that an isolated current source current actually leaves its terminals into the rest of the network.

## Mistakes

Writing KCL as “currents in equal currents out” and then forgetting a third branch. Applying KVL to a path that is not closed. Using \( V = IR \) with the current of a different branch. Adding resistances that are not in series (they share a node with a third current path). Treating two voltage sources in parallel as “the average.” Changing the sign of a source because the current came out negative, then applying Ohm again with the new sign and the old polarity marks. Putting an independent current source in the Ohm formula as if it had a resistance. Grounding both ends of a voltage source. Writing node equations in currents mixed with loop equations in voltages without a translation. Assuming KVL holds around a loop that encloses a time-varying transformer flux without an emf term. Using peak AC values in DC Ohm's law. Ignoring that an open circuit current is zero even if a voltage exists across it, and that a short-circuit voltage is zero even if a current exists through it.

# Mutual inductance and coupled coils

Magnetically coupled coils share flux. Mutual inductance M quantifies the voltage induced in one coil by di/dt in the other. Coupled-circuit analysis is the lumped model of transformers before ideal-transformer turns-ratio models in machines. Dot convention, coupling coefficient, series aiding/opposing, and the T-equivalent are UG staples.

## Concepts

Faraday: \( v_2 = M di_1/dt \) with a sign from the sense of winding. The dot convention: if both currents enter dotted terminals, the mutual voltage in each coil is \( +M di_\mathrm{other}/dt \) when writing \( v = L di/dt \pm M di_\mathrm{other}/dt \) with passive signs on each coil. If one current enters a dotted terminal and the other leaves a dotted terminal, the mutual terms flip. Misreading dots is the dominant error.

Self inductances L1, L2 are always positive. Mutual M satisfies \( |M| \le \sqrt{L_1 L_2} \). Coupling coefficient \( k = M / \sqrt{L_1 L_2} \), \( 0 \le k \le 1 \). Tight coupling k ≈ 1 is an ideal transformer core; loosely coupled coils (k = 0.1) appear in wireless power and in loosely coupled lab transformers.

Energy stored: \( w = \frac12 L_1 i_1^2 + \frac12 L_2 i_2^2 \pm M i_1 i_2 \). The sign follows the dots (plus when both currents enter dots). The quadratic form is positive semidefinite because of the k ≤ 1 bound; otherwise the model could create energy.

Series aiding: two coils in series with dots so mutual adds, \( L_\mathrm{eq} = L_1 + L_2 + 2M \). Series opposing: \( L_1 + L_2 - 2M \). Parallel aiding/opposing have analogous formulas. These are used to measure M: \( M = (L_\mathrm{aid} - L_\mathrm{opp})/4 \).

T-equivalent: for a common reference, replace the pair by L1−M, L2−M, and a shunt M, valid when both currents are defined into the dotted terminals of a two-winding four-terminal network with a shared reference. If M is larger than L1, one series arm goes negative; that is allowed mathematically and is why the T model is sometimes awkward. A better model at high k is the ideal transformer plus leakage and magnetizing inductances (machines pack).

Phasor domain: \( \mathbf{V}_1 = j\omega L_1 \mathbf{I}_1 + j\omega M \mathbf{I}_2 \), with signs from dots. Mesh analysis is natural. Reflected impedance: a load ZL on coil 2 looks like \( \omega^2 M^2 / (Z_{22}) \) added to the primary, the classic loosely coupled transformer formula.

Ideal transformer limit: k=1, infinite magnetizing inductance, \( v_1/v_2 = n = i_2/i_1 \). That limit is not this unit's main algebra but is the sanity check for dots: dotted terminals have the same instantaneous polarity for voltages.

How to assign dots in a physical winding: if two coils are wound the same way on a core, the finishing ends (or both starting ends) are dots. In a figure, dots are given; do not “guess from Lenz” in two different ways in one problem. If a problem describes “flux of coil 1 linking coil 2 in the aiding sense when both currents enter the marked terminals,” that is the plus-M case.

Mesh equations with coupling, written slowly: for mesh 1, (R1 + jω L1) I1 + jω M I2 + (shared uncoupled terms) = V1, if both meshes enter dots. If mesh 2 leaves the dotted terminal of coil 2, that I2 term in mesh 1's KVL is −jω M I2. The same sign appears as −jω M I1 in mesh 2. The mutual terms are always symmetric in the bilateral case: Z12 = Z21 = ±jω M. That symmetry is reciprocity. A controlled source pretending to be mutual coupling will break it.

Open secondary: I2 = 0, then V1 = jω L1 I1, V2 = jω M I1, so the voltage ratio V2/V1 = M/L1 = k √(L2/L1), which equals n only if k=1 and L1/L2 = n². Shorted secondary: V2 = 0, I2 = −(M/L2) I1, and the primary looks like jω (L1 − M²/L2) = jω L1 (1−k²), the leakage inductance in the simple model. That formula is worth memorizing: tight coupling, shorted secondary, small primary impedance (except resistance).

Conductively coupled plus magnetically coupled: a common node between windings plus M. The T-model is attractive because it is three inductors a SPICE user can type. If M > L1 the series arm L1−M is negative; SPICE still accepts a negative inductor in linear AC. For time-domain transients, negative L is unpleasant; use the Gyrator or coupled-inductor statement (K = k). UG hand analysis should prefer the two-equation mutual form over a negative inductor.

Units and numbers: M is henries, same as L. A coupling of 50 µH between two 200 µH coils is k = 0.25. Audio transformers may have k = 0.99 and henries of primary; RF coils on a solenoid may have k = 0.05. Do not use ideal-transformer current reversal on the RF pair.

DC: after transients, coupled inductors are short circuits. A DC current can still store ½L i² ± M i1 i2. Switching a DC current off produces the same inductive kick as a single inductor, with extra coupled kick on the other winding (flyback). That sentence is the bridge to power-electronics isolated converters, which this pack does not design, but the sign of the flyback voltage follows the dots. Keep k dimensionless and M in henries in the same box so a later mesh does not treat k as an inductance.

## Equations

Time domain (both currents into dots): \( v_1 = L_1 \frac{di_1}{dt} + M \frac{di_2}{dt} \), \( v_2 = L_2 \frac{di_2}{dt} + M \frac{di_1}{dt} \).

\( k = M/\sqrt{L_1 L_2} \). \( M_\mathrm{max} = \sqrt{L_1 L_2} \).

Series aiding \( L = L_1+L_2+2M \); opposing \( L_1+L_2-2M \).

Phasor: \( \mathbf{V}_1 = j\omega L_1 \mathbf{I}_1 \pm j\omega M \mathbf{I}_2 \).

Reflected: \( Z_\mathrm{in} = j\omega L_1 + \omega^2 M^2 / (j\omega L_2 + Z_L) \) (dots such that the sign of M^2 is plus).

Energy: \( w = \frac12 L_1 i_1^2 + \frac12 L_2 i_2^2 + M i_1 i_2 \) (both into dots).

## Methods

Mark dots and current arrows before writing KVL. Write two mesh equations with ±jωM. Solve. Check energy or power: average P into both ports can be positive on one and negative on the other (transfer). For DC steady state, coupled inductors are shorts (unless superconducting persistent current, not UG circuits). For finding k from measurements, use aiding/opposing series test.

Design: choose n ≈ √(L1/L2) for a given turns ratio estimate, then k from core, then M. Leakage \( L_{\ell 1} = L_1(1-k) \) in the simple split.

Aiding versus opposing is a bench measurement, not a mystery. Series the windings two ways, measure L with a meter at a frequency where Cstray is negligible, then M = (Laid − Lopp)/4. If the two readings are 28 mH and 12 mH, M is 4 mH as in the questions. If they are almost equal, k is small. If one reading is near zero, k is near 1 and the opposing connection cancelled the flux. Do not apply a DC ohmmeter and call that henries. When writing time-domain v2 = M di1/dt with i2 = 0, a triangular i1 produces a square v2; that is a useful scope demo of Faraday on coupled coils and a check of the dot (the square’s sign flips if you reverse one winding).

## Mistakes

Wrong mutual sign. Using k > 1. Adding L1+L2 without ±2M when they share current in series. Using the T-model shunt M with inconsistent current directions. Treating coupled coils as an ideal transformer when k = 0.4. Forgetting that open-secondary primary looks like L1, not like zero. Applying DC resistance only and ignoring L at 50 Hz. Writing M in henries and ω in hertz in jωM. Using passive signs on one coil and active on the other without flipping. Claiming stored energy is always ½L1i1²+½L2i² without the cross term. Using k = M/(L1+L2). Drawing both dots at the “top” of the schematic automatically without reading the figure. Applying an ideal transformer current reversal when the secondary is open (I2 is zero, not I1/n). Measuring M with DC. Writing the T-model with shunt M while the currents are defined leaving both dots, which flips the sign of the series arms. Ignoring that a shorted turn on a core (k high) reflects a near-short to the primary and cooks the winding; that is the same reflected-impedance formula with ZL ≈ 0. Forgetting ω in jωM so that M looks like a resistance. Treating coupling as one-way (only v2 = M di1/dt) in a circuit where i2 is not zero; the primary also sees M di2/dt. A further check: the two-port z-parameters of a coupled pair (dots both at plus) are z11 = jωL1, z22 = jωL2, z12 = z21 = jωM, which must be reciprocal. If your mesh equations violate that, a sign is wrong. Keep a margin note of which currents enter dots before expanding KVL. Then the mutual signs do not drift mid-algebra.

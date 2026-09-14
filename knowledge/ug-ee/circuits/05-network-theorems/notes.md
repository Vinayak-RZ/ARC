# Thevenin, Norton, superposition, max power, Millman, reciprocity

Network theorems turn a complicated linear network into a simpler equivalent at a chosen pair of terminals, or they exploit linearity to split sources. They do not replace KCL and KVL; they are consequences of those laws for linear lumped circuits. UG syllabi (NITT circuit theory, AICTE-family BES, GATE overlay) expect Thévenin, Norton, source transformation, superposition, maximum power transfer, Millman's theorem for parallel branches, and reciprocity for bilateral networks. Dependent sources stay on when independent sources are killed. Nonlinearity voids superposition and the unique two-parameter equivalent.

## Concepts

Thévenin's theorem: any linear network seen from two terminals is equivalent to a single voltage \( v_\mathrm{Th} \) in series with \( R_\mathrm{Th} \) (or \( Z_\mathrm{Th} \) in AC). \( v_\mathrm{Th} \) is the open-circuit voltage at the terminals. \( R_\mathrm{Th} \) is the resistance seen into those terminals with independent sources deactivated—voltage sources replaced by shorts, current sources by opens—while dependent sources remain. If deactivation is awkward, \( R_\mathrm{Th} = v_\mathrm{oc}/i_\mathrm{sc} \), using the short-circuit current at the same terminals.

Norton's theorem is the dual: \( i_\mathrm{N} \) in parallel with \( R_\mathrm{N} \). Necessarily \( R_\mathrm{N} = R_\mathrm{Th} \) and \( i_\mathrm{N} = v_\mathrm{Th}/R_\mathrm{Th} = i_\mathrm{sc} \). Source transformation is the local version of the same pair. Equivalence holds only at the port. Power in \( R_\mathrm{Th} \) is not the power in the original internal resistors.

Superposition: in a linear network, each independent source contributes an additive term to every voltage and current. Compute with one independent source alive, others deactivated, then sum. Dependent sources remain in every subcircuit. Superposition does not apply to power, because power is quadratic. It does not apply to circuits with operating-point-dependent nonlinear models unless those models have already been linearized.

Maximum power transfer: for a DC Thévenin source driving a variable load \( R_L \), \( P_L = v_\mathrm{Th}^2 R_L / (R_\mathrm{Th}+R_L)^2 \) is maximized at \( R_L = R_\mathrm{Th} \), with \( P_\mathrm{max} = v_\mathrm{Th}^2 / (4 R_\mathrm{Th}) \). Efficiency at that point is 50 percent, which is usually unacceptable in power engineering; the theorem is a communications and instrumentation result (match the source), not a power-system operating rule. If \( R_L \) is fixed and \( R_\mathrm{Th} \) is variable, minimum \( R_\mathrm{Th} \) delivers more power; matching is not the same problem. In AC, match \( Z_L = Z_\mathrm{Th}^* \) for maximum average power, a later-unit statement.

Millman's theorem: several parallel branches, each a voltage source in series with a resistance, combine as \( v = (\sum v_k G_k)/(\sum G_k) \) across the parallel pair. It is nodal analysis with one unknown, dressed as a named theorem. Current-source parallels are even simpler: currents add, conductances add.

Reciprocity: in a linear bilateral network (no dependent sources, no gyrators), the transfer impedance \( V_\mathrm{out}/I_\mathrm{in} \) from port A to port B equals that from B to A. Interchanging an ideal voltage source and an ideal ammeter leaves the ammeter reading unchanged in the classic form. Reciprocity fails as soon as a controlled source or an ideal op-amp breaks bilaterality.

Special cases: \( R_\mathrm{Th} = 0 \) is an ideal voltage source; you cannot match it with \( R_L = 0 \) in practice. \( R_\mathrm{Th} = \infty \) is an ideal current source; Norton is the better picture. Negative \( R_\mathrm{Th} \) can appear with dependent sources (active networks); maximum power formulas that assume positive \( R \) then fail and stability must be checked.

Worked pattern for a dependent-source Thevenin: the open-circuit voltage still comes from nodal or mesh with the load removed. Deactivating independent sources may leave the dependent source with a zero control, giving RTh = voc/isc if you also compute a short, or it may leave an active linear network that looks like a resistor (possibly negative). The test-source method is the reliable default: attach 1 V at a–b with internals independent sources killed, find I into the plus of that 1 V, then RTh = 1/I. If I comes out negative, RTh is negative and the port can source power. Maximum power transfer for negative RTh is not a classroom match of RL = RTh (that would be a negative load); instead the port is active and you must discuss stability.

Superposition with three sources produces three subcircuits. Sketch them; do not try to do it in one drawing with mental erasures. A shorted voltage source can merge nodes and change which resistors are in parallel. An opened current source can split a node into two. The topology of subcircuit k is not the original topology. After summing voltages, compute one current from Ohm using the total voltage, not by superposing resistor currents that were computed with different equivalent resistances unless you are careful that those currents are in the same branch with the same reference.

Millman is nodal analysis with a single unknown node-pair. If a branch is a current source, add it to the numerator as an injected current and do not invent a fake Vk. If a branch is only R, Vk = 0 in the voltage-source formula. If the parallel bundle includes a dependent source, Millman's named formula is no longer worth using; write KCL.

Maximum power versus maximum efficiency versus a specified load voltage are three different design problems. Communications front-ends match. Battery-powered heaters want small RTh. A 5 V regulator specification wants RL such that vL is 5 V, which fixes RL once vTh and RTh are known, independent of the match condition. State which problem you are solving before writing RL = RTh.

Reciprocity is a theorem about a linear network with a symmetric constitutive matrix (no dependent sources, no gyrators, no ideal circulators). The practical check in UG is z12 = z21 of the two-port. Swapping a voltage source at port 1 with an ammeter at port 2, versus source at 2 and ammeter at 1, yields the same ammeter reading. Swapping a current source and a voltmeter is the dual form. If an op-amp is inside, do not expect equality.

## Equations

\( v_\mathrm{Th} = v_\mathrm{oc} \), \( i_\mathrm{N} = i_\mathrm{sc} \), \( R_\mathrm{Th} = R_\mathrm{N} = v_\mathrm{oc}/i_\mathrm{sc} \) (when both exist).

Load voltage: \( v_L = v_\mathrm{Th} \frac{R_L}{R_\mathrm{Th}+R_L} \). Load current: \( i_L = i_\mathrm{N} \frac{R_\mathrm{N}}{R_\mathrm{N}+R_L} \).

Superposition: \( v = \sum_k v^{(k)} \) over independent sources \( k \).

Max power (DC): \( R_L = R_\mathrm{Th} \), \( P_\mathrm{max} = \dfrac{v_\mathrm{Th}^2}{4 R_\mathrm{Th}} \).

Millman: \( v = \dfrac{\sum v_k / R_k}{\sum 1/R_k} \).

Reciprocity (impedance form): \( Z_{21} = Z_{12} \) in the open-circuit z-parameter matrix of a bilateral two-port.

## Methods

To find a Thévenin equivalent at terminals a–b: (1) remove the load; (2) compute open-circuit \( v_{ab} \); (3) compute \( R_\mathrm{Th} \) by deactivation or by \( v_\mathrm{oc}/i_\mathrm{sc} \) or by attaching a test source; (4) reattach the load to the series combination. Test-source method is mandatory when dependent sources make deactivation yield \( 0/0 \): apply \( 1\,\mathrm{A} \) at a–b, find \( v_{ab} \), that voltage is \( R_\mathrm{Th} \).

For superposition, sketch one subcircuit per independent source. Never kill a dependent source. Add algebraic voltages with the same polarity marks. Then compute power once from the total \( v \) and \( i \).

For maximum power, first get \( v_\mathrm{Th} \) and \( R_\mathrm{Th} \), then set \( R_L = R_\mathrm{Th} \) if \( R_L \) is free and positive. If \( R_L \) must be chosen from a table, pick the nearest and compute actual \( P_L \). If the problem asks for maximum power “available from the source” it means \( P_\mathrm{max} \), not the power at some other given load.

Millman: convert every series \( v,R \) to a current \( v/R \) into a common node, add, divide by total \( G \). Branches that are only resistors (no voltage source) still contribute their \( G \) to the denominator and zero to the numerator.

Reciprocity checks: excite port 1 with \( 1\,\mathrm{A} \), measure open \( v_2 \); then excite port 2 with \( 1\,\mathrm{A} \), measure open \( v_1 \); they match if the network is reciprocal.

## Mistakes

Deactivating a dependent source. Computing \( R_\mathrm{Th} \) with the load still attached. Using \( P = v_\mathrm{Th}^2 / R_\mathrm{Th} \) as load power (that would be a shorted Thévenin, infinite current if you also short). Superposing powers. Matching \( R_L \) for max power in a DC motor drive and calling it efficient. Finding \( v_\mathrm{oc} \) with the wrong polarity and then attaching the load with a flipped sign. Source-transforming a part of the circuit and then quoting an internal current as physical. Applying reciprocity to a circuit with a transistor small-signal dependent source. Millman with current sources thrown into the voltage-source formula without converting. Reporting \( R_\mathrm{Th} \) as the series of all resistors whether or not some were shorted by a deactivated voltage source. Using AC conjugate match formulas on a purely resistive DC problem, or DC match on a complex \( Z_\mathrm{Th} \).

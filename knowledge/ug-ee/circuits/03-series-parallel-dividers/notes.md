# Series-parallel reduction and dividers

Series-parallel reduction is the first systematic simplification: replace clusters of two-terminal resistors by a single equivalent, then unwind the voltages and currents with divider rules. It solves a large fraction of UG DC assignments without nodal matrices. It fails as soon as the graph is a bridge (Wheatstone unbalanced) or contains a dependent source that prevents two-terminal clustering. Knowing when it applies is as important as the arithmetic.

## Concepts

Two elements are in series if they share a node that has no other connection, so they carry identical current. Two elements are in parallel if they share the same pair of nodes, so they have identical voltage. These are topological facts, not statements about values. A 1 Ω and a 1 MΩ in series still share current; a 1 Ω and a 1 MΩ in parallel still share voltage.

Equivalent resistance \( R_\mathrm{eq} \) of a two-terminal network of resistors is the ratio \( V/I \) at that port when independent sources inside are deactivated (voltage sources shorted, current sources opened). For a purely resistive tree of series-parallel connections, \( R_\mathrm{eq} \) is built by recursively replacing series sums and parallel harmonic sums. The inverse, conductance, is more convenient for many parallels: \( G_\mathrm{eq} = \sum G_k \).

Voltage division: in a series string the voltage across \( R_k \) is \( v_k = v_\mathrm{total} \cdot R_k / \sum R \). The largest resistor takes the largest drop. Current division: in a parallel set the current through \( R_k \) is \( i_k = i_\mathrm{total} \cdot G_k / \sum G \), or for two resistors \( i_1 = i_\mathrm{total} \cdot R_2/(R_1+R_2) \). The smaller resistor takes the larger current.

Source transformation is the partner of reduction: a voltage source in series with \( R \) is equivalent at the terminals to a current source \( v_s/R \) in parallel with the same \( R \). Equivalence is at the port, not inside the box: internal currents differ. Ladder networks (series, shunt, series, shunt) are reduced from the far end toward the source, or analyzed by successive voltage/current division.

Loading: a divider designed for an open-circuit ratio changes when a load \( R_L \) parallels the bottom resistor. The loaded ratio uses \( R_2 \parallel R_L \). A “stiff” divider has \( R_2 \ll R_L \) so loading is negligible, at the cost of wasted standing current. Potentiometers are adjustable dividers; wiper current (meter loading) shifts the tap voltage.

Wye-delta (Y-Δ) transformations extend reduction to some non-series-parallel graphs. Three resistors in a triangle become three resistors in a star, and conversely, with the product-sum formulas. An unbalanced Wheatstone bridge is the classic case that needs Y-Δ or mesh/nodal, not naive series-parallel.

Units: keep Ω consistent. Mixing kΩ and Ω in a divider formula is a common silent error. Prefixes in current division with milliamps and kilohms actually cancel nicely if both are converted or both left as mA and kΩ with volt as the product, but only if you are consistent.

A ladder with five rungs is still series-parallel: start at the far shunt, combine it with the last series arm, combine with the previous shunt, and walk toward the source. Each step is either two things in series or two in parallel. Write the equivalent resistance at each node to ground; those numbers are the voltage-division denominators on the way back. The same walk in reverse, with the source voltage known, produces every node voltage without a matrix. This is how analog designers still estimate bias networks and how power engineers estimate a string of feeder laterals that happen to be purely series-parallel. When a cross-link appears, the walk stops and the graph is no longer a series-parallel reducible two-terminal network. Wheatstone, bridged-T, and lattice networks are the usual counterexamples. Y-Δ is a local rewrite that can restore reducibility: convert one triangle to a star, then the drawing may become series-parallel. If two conversions still leave a non-reducible core, stop and use nodal analysis. Do not invent a fake series connection through a bridge arm.

Divider design is a trade among stiffness, power, and noise. Stiff means small R1 and R2 compared with the load, so the Thevenin resistance of the divider R1∥R2 is low and load current barely shifts the tap. Power wasted is Vs²/(R1+R2). Johnson noise of the equivalent resistance matters in instrumentation. A 10 V to 5 V divider with 1 kΩ+1 kΩ wastes 50 mW and has RTh = 500 Ω; with 100 kΩ+100 kΩ it wastes 0.5 mW but a 10 MΩ meter still loads it by half a percent and a 1 MΩ scope probe loads it by 9 percent. State the load before choosing the decade. Potentiometers add a wiper resistance and a travel; the output is not exactly proportional to shaft angle if current is drawn from the wiper. For a light load, the law is almost linear; for R_L comparable to the pot value, the law sags in the middle. That sag is ordinary loaded voltage division with R2 as the bottom fraction of the track and R1 the top, then R2∥RL.

Source transformations inside a reduction: a 12 V source in series with 3 kΩ attached to a node can become 4 mA in parallel with 3 kΩ, after which parallels of current sources add. Transform back if a voltage is easier. Never report the current through the transformed 3 kΩ as the current through the original 3 kΩ; only the port of the transformed pair is equivalent. That single sentence saves a generation of wrong mesh currents after a transform.

## Equations

Series: \( R_\mathrm{s} = \sum_{k=1}^{n} R_k \). Parallel: \( \frac{1}{R_\mathrm{p}} = \sum_{k=1}^{n} \frac{1}{R_k} \). Two-parallel: \( R_\mathrm{p} = \frac{R_1 R_2}{R_1+R_2} \).

Voltage divider: \( v_k = v \frac{R_k}{\sum R} \) (series, no other taps loaded).

Current divider (two branch): \( i_1 = i \frac{R_2}{R_1+R_2} \), \( i_2 = i \frac{R_1}{R_1+R_2} \).

n-branch current divider: \( i_k = i \frac{G_k}{\sum G} \).

Source transform: \( i_s = v_s / R \), same \( R \).

Δ to Y: \( R_a = \frac{R_{ab} R_{ac}}{R_{ab}+R_{bc}+R_{ca}} \) (resistor at node a). Y to Δ: \( R_{ab} = \frac{R_a R_b + R_b R_c + R_c R_a}{R_c} \).

Loaded divider: \( v_L = v_s \frac{R_2 \parallel R_L}{R_1 + (R_2 \parallel R_L)} \).

## Methods

Identify series and parallel clusters from the graph, not from the drawing's visual proximity. Redraw if the schematic is stretched. Reduce innermost clusters first. After finding \( R_\mathrm{eq} \), find the source current or node voltage, then expand outward: each time you un-series, apply voltage division; each time you un-parallel, apply current division. Write intermediate voltages on the drawing so you do not lose a factor of two.

If a source is not at the port where you need \( R_\mathrm{eq} \), deactivate independent sources first. Do not deactivate dependent sources. If reduction stalls at a bridge, stop and switch to nodal, mesh, or Y-Δ.

For design, invert the divider: choose a convenient \( R_2 \) from a standard value table, then \( R_1 = R_2 (v_s/v_\mathrm{out} - 1) \) for the unloaded case, then check loading. Prefer E12/E24 values and recompute the actual ratio rather than pretending the exact algebra value is in the kit.

Verify with limits: if \( R_2 \to \infty \), voltage divider output → \( v_s \); if \( R_2 \to 0 \), output → 0. If two parallels, current in \( R \) → 0 as \( R \to \infty \). Power in each resistor \( v^2/R \) or \( i^2 R \) after voltages/currents are known; never assign the total source power to one resistor unless it is the only resistor.

A reduction checklist used in UG labs: photocopy the schematic, circle a series pair, replace with a single resistor drawn in the margin, recopy, circle a parallel pair, repeat until one R_eq remains. Then expand: the source current is Vs/Req. Un-replace the last parallel: those two resistors share that voltage or split that current. Continue until every original element has a number. This paper trail is slower than a clever insight and faster than a wrong insight. If at any step you cannot find a series or parallel pair, the network is not series-parallel; stop. Wheatstone with a galvanometer short is the usual trap. Another trap is two resistors that look parallel on a sloppy drawing but have a source between their top nodes. Redraw nodes as dots and wires as rubber bands until shared node-pairs are obvious.

## Mistakes

Calling two resistors series because they are drawn in a straight line even though a third branch leaves the midpoint. Using voltage division on resistors that are not in the same series chain. Using current division with resistances in the numerator the wrong way around (the current through \( R_1 \) is proportional to the other resistance in a two-branch divider). Reducing a network with a live independent source still inside when asked for equivalent resistance. Source-transforming and then reporting an internal resistor current as if it were the original circuit. Forgetting that \( R_1 \parallel R_2 \) is less than either, so a loaded divider always droops. Applying Y-Δ to the wrong three terminals. Adding conductances when the elements are in series. Designing a 10:1 divider with 10 MΩ resistors and then measuring it with a 10 MΩ voltmeter, which becomes a 5 MΩ bottom and a 2:1 error. Treating a potentiometer as two fixed resistors when the wiper current is unknown.

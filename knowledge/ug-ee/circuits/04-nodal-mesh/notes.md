# Nodal and mesh analysis

Nodal analysis writes KCL at nodes using unknown node voltages. Mesh analysis writes KVL around meshes using unknown mesh currents. They are the two industrial-strength methods for linear lumped networks. UG courses require both, plus supernode and supermesh patches for the sources that break the naive tableau. After this unit, reduction is optional sugar; the matrix is the default.

## Concepts

A node voltage is defined with respect to a chosen ground. Every branch voltage is a difference of node voltages, so KVL is automatic. Substituting constitutive laws (Ohm, sources) into KCL produces as many independent equations as unknown node voltages. For a connected graph with \( n \) nodes, there are \( n-1 \) independent KCL equations if there are no extra constraints; each grounded independent voltage source reduces the unknown count by tying a node to a known value.

A mesh is a loop that does not enclose other loops in a planar drawing. Mesh currents are fictitious circulating currents; the physical branch current is the algebraic sum of meshes sharing that branch. KCL is automatic. KVL on each mesh, with Ohm, yields the mesh matrix. Nonplanar graphs still have loop analysis, but “mesh” is reserved for planar embeddings.

Supernode: when an independent or dependent voltage source connects two non-ground nodes, KCL at those nodes individually cannot use the unknown source current. Combine the two nodes into a surface, write one KCL, and add \( v_a - v_b = v_s \) (or the dependent law). If one end is ground, simply set the other node to \( \pm v_s \) and skip that unknown.

Supermesh: when a current source sits on a branch shared by two meshes (or in the outer path), KVL cannot use the unknown voltage across the current source. Write KVL around the larger loop that avoids the current source, and add the mesh-current constraint \( i_a - i_b = i_s \).

Dependent sources: keep them active. Their controlling variables must be expressed in node voltages or mesh currents. The matrix is still linear if the dependent sources are linear. Superposition does not turn dependent sources off.

Conductance matrix (nodal, no voltage sources): \( G\mathbf{v} = \mathbf{i}_s \). Diagonal \( G_{kk} \) is the sum of conductances attached to node \( k \); off-diagonal \( G_{kj} \) is minus the conductance between \( k \) and \( j \). Resistance matrix (mesh, no current sources): \( R\mathbf{i} = \mathbf{v}_s \). Diagonal \( R_{kk} \) is the series resistance around mesh \( k \); off-diagonal \( R_{kj} \) is minus the resistance shared by meshes \( k \) and \( j \) if the mesh currents oppose through that resistor (usual drawing).

Modified nodal analysis (MNA) used in SPICE adds source currents as unknowns and stamps voltage sources as extra rows. UG hand analysis rarely needs the full MNA stamp, but supernodes are MNA in disguise.

Choosing the method: many voltage sources and a planar graph → mesh. Many current sources and a clear ground → nodal. A single non-ground voltage source → nodal plus one supernode is often smaller than mesh. Practice both on the same circuit until the matrices become mechanical.

## Equations

Nodal KCL at node \( k \): \( \sum_j G_{kj}(v_k - v_j) + G_{k0} v_k = i_{s,k} \) (currents of current sources leaving or entering consistently).

Supernode: \( \sum_{\text{leaving surface}} i = 0 \), \( v_p - v_q = v_s \).

Mesh KVL: \( \sum R_{\ell m} i_m = v_{s,\ell} \).

Supermesh constraint: \( i_p - i_q = i_s \) (sign from arrows).

Branch current from nodes: \( i_{kj} = G_{kj}(v_k - v_j) \). Branch voltage from meshes: \( v = R(i_\mathrm{left} - i_\mathrm{right}) \).

Power at a current source: \( p = v_\mathrm{across} i_s \) with PSC. Voltage-source current is not a mesh unknown unless that source is a branch with a defined mesh difference; compute it from KCL after voltages are known.

## Methods

Nodal recipe: (1) count essential nodes, pick ground; (2) label unknown node voltages; (3) if a voltage source is from a node to ground, assign that node; (4) supernode any floating voltage source; (5) write KCL in terms of voltages; (6) express dependent-source controls; (7) solve; (8) back-substitute currents and powers.

Mesh recipe: (1) confirm a planar drawing; (2) assign clockwise mesh currents (consistency beats aesthetics); (3) supermesh any interior current source; (4) write KVL; (5) solve; (6) reconstruct branch currents as differences.

Write the matrix in inspection form once the pattern is trusted, but on exams expand at least one KCL/KVL in words so a stamp sign error is visible. Check by an independent KCL at ground or by Tellegen power sum.

Op-amp ideal nodal: the inverting node is a virtual ground or a virtual short to the plus input, and plus-input current is zero. That is still nodal analysis with extra constraints, taught in electronics, but the algebra is the same.

Hand 2×2 practice until it is boring: node-voltage equations G11 v1 + G12 v2 = i1, G21 v1 + G22 v2 = i2, then v1 = (i1 G22 − i2 G12)/Δ. Do one fully numeric example with millisiemens so the determinant is a round number. Then repeat as mesh. The same circuit solved both ways is the best homework: if v and i disagree, the error is in one method and you have a debugging target. Include at least one supernode and one supermesh in that paired practice, because those are where signs die. When a current source is in parallel with a resistor, convert it or keep it as a right-hand side; do not also write Ohm as if the source current were the resistor current.

Op-amp ideal nodal: the inverting node is a virtual ground or a virtual short to the plus input, and plus-input current is zero. That is still nodal analysis with extra constraints, taught in electronics, but the algebra is the same.

A comparison of matrix size helps choose a method on sight. Count essential nodes (nodes where three or more elements meet, plus possibly a special two-element node you care about). Nodal unknowns ≈ essential nodes minus one, minus grounded voltage sources, plus extra currents if you use MNA. Mesh unknowns ≈ inner meshes, minus mesh currents fixed by current sources in an outer branch, plus supermesh constraints that do not add unknowns. Example: a planar ladder with four loops and a grounded voltage source on the left is often four meshes or three node voltages; pick the smaller. Example: a nonplanar five-crossing drawing has no meshes; use loops or nodes. Example: three floating voltage sources among four nodes is a supernode festival; mesh may be cleaner.

The conductance-stamp story, told slowly: for a resistor G between nodes i and j, KCL at i contains G(vi−vj) leaving toward j, so +G on the ii diagonal, −G on ij. At j the opposite, +G on jj and −G on ji. A resistor from i to ground stamps +G only on ii. A current source from ground into i stamps +Is on the right-hand side if the equation is Gv = i_into_node. A grounded voltage source removes vi as an unknown. Students who memorize stamps without writing one KCL in words will mis-stamp a supernode because the voltage-source branch current does not appear in G. Write the surface KCL once, then stamp.

Mesh stamps: around mesh k, every resistor on that mesh contributes +R to Rkk. A resistor shared with mesh m, with opposite mesh directions through it (both clockwise, so they oppose), contributes −R to Rkm and Rmk. A voltage source rise in the direction of ik belongs on the right-hand side. A current source that sits only on mesh k sets ik. Shared current source: supermesh, drop that row, add ik − im = Is. Dependent sources add a row that is not a pure R stamp; expand the controlling variable in mesh currents and move terms to the left.

Numerical hygiene: work in volts, amperes, and siemens, or consistently in mA and kΩ (volts still volts). Mixing 2200 Ω in one row and 2.2 kΩ treated as 2.2 in another row is a factor-of-a-thousand error that still produces a plausible-looking 7.4 V. After solving, compute unused KCL at ground: the currents into ground must sum to zero. Compute total source power versus resistor heat. If they disagree by more than rounding, an equation was wrong. If they agree, you may still have swapped two node labels in the report; check one obvious divider limit (set a resistor to zero in your head and see whether the solution tends to the right short).

## Mistakes

Using a nonplanar “mesh” that is actually a loop enclosing other loops and then missing an equation. Forgetting to subtract shared mesh currents through a resistor, doubling the drop. Writing \( G_{kj} \) positive off-diagonal. Grounding the wrong node and then reporting that node's voltage as an answer when the problem defined a different reference. Treating a dependent source as an independent source in superposition while doing nodal. Leaving a voltage-source current in a KCL equation as if it were known. Sign errors on supernode KCL (currents leaving the surface). Applying Ohm to a current source. Reporting mesh current as a physical current in a shared branch. Using SI prefixes inconsistently inside the matrix so one row is off by 1000. Solving for voltages and then computing \( P = V^2/R \) with a voltage that is not the voltage across that \( R \).

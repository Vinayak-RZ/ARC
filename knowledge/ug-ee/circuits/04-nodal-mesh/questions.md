# Questions — Nodal and mesh analysis

Original pedagogical numbers.

## Q1

### Given

Ground at the bottom. Left node A has a 4.0 mA source injecting into A, then 2.2 kΩ from A to ground. From A a 3.3 kΩ goes to node B. Node B has 4.7 kΩ to ground. An independent 6.0 V source has plus at B and minus at ground.

### Find

Voltage at A and current in the 3.3 kΩ (from A toward B).

### Solution

Node B is fixed: \( v_B = 6.0\,\mathrm{V} \). KCL at A (currents leaving through resistors, source entering): \( (v_A)/2.2\mathrm{k} + (v_A - 6)/3.3\mathrm{k} = 4.0\,\mathrm{mA} \). Multiply by 3300: \( 1.5 v_A + (v_A - 6) = 13.2 \) ⇒ \( 2.5 v_A = 19.2 \) ⇒ \( v_A = 7.68\,\mathrm{V} \). \( I_{3.3} = (7.68-6)/3300 = 0.509\,\mathrm{mA} \) A to B.

### Answer

\( v_A = 7.68\,\mathrm{V} \); \( I_{3.3} = 0.509\,\mathrm{mA} \) A→B.

## Q2

### Given

Two meshes. Mesh 1: 18 V source plus to a 270 Ω, then a 470 Ω shared with mesh 2, back through the source minus. Mesh 2: 470 Ω shared, then 330 Ω, then a 2.0 mA current source pointing up so that it is the right-hand branch of mesh 2 only (not shared). Both meshes clockwise.

### Find

Set up supermesh or constraint and find the two mesh currents.

### Solution

The 2.0 mA source is on the outer branch of mesh 2 only, so \( i_2 = 2.0\,\mathrm{mA} \) immediately (clockwise through that source). Mesh 1 KVL: \( 18 = 270 i_1 + 470(i_1 - i_2) \) ⇒ \( 18 = 740 i_1 - 470(0.002) \) ⇒ \( 18 + 0.94 = 740 i_1 \) ⇒ \( i_1 = 18.94/740 = 25.59\,\mathrm{mA} \). Shared resistor current \( i_1 - i_2 = 23.59\,\mathrm{mA} \) downward if \( i_1 \) clockwise on the left of the shared branch.

### Answer

\( i_1 = 25.59\,\mathrm{mA} \), \( i_2 = 2.00\,\mathrm{mA} \).

## Q3

### Given

Design a two-node (plus ground) resistive network driven by a 10.0 mA source into node 1 so that \( v_1 = 8.0\,\mathrm{V} \) and \( v_2 = 3.0\,\mathrm{V} \). Node 2 is loaded by 1.0 kΩ to ground. You may add \( R_{10} \) from 1 to ground and \( R_{12} \) from 1 to 2.

### Find

\( R_{10} \) and \( R_{12} \).

### Solution

Current in 1 kΩ at node 2: \( 3.0\,\mathrm{mA} \) to ground. That current must come through \( R_{12} \): \( (v_1-v_2)/R_{12} = 3.0\,\mathrm{mA} \) ⇒ \( 5/R_{12} = 0.003 \) ⇒ \( R_{12} = 1.667\,\mathrm{k}\Omega \). KCL at node 1: 10 mA in = current in \( R_{10} \) + current in \( R_{12} \). \( 8/R_{10} + 3.0\,\mathrm{mA} = 10\,\mathrm{mA} \) ⇒ \( 8/R_{10} = 7.0\,\mathrm{mA} \) ⇒ \( R_{10} = 1.143\,\mathrm{k}\Omega \).

### Answer

\( R_{12} = 1.67\,\mathrm{k}\Omega \), \( R_{10} = 1.14\,\mathrm{k}\Omega \).

## Q4

### Given

A supernode encloses a 5.0 V source between nodes X and Y (plus at X). Conductances: 1.0 mS from X to ground, 2.0 mS from Y to ground, 4.0 mS from X to Y (in parallel with the source—wait, that would short-inconsistent). No extra G between X and Y besides the source. A 3.0 mA source injects into X.

### Find

Explain whether a 4.0 mS in parallel with the voltage source is legal, then solve with that conductance omitted.

### Solution

A finite conductance in parallel with an independent voltage source is legal; it does not violate KVL. It does not affect node voltages (they are still 5 V apart and determined by the rest), but it draws extra current from the source. If the 4 mS were included, voltages would be the same as without it for the X,Y difference constraint, but KCL of the supernode would include that current internally—internal currents cancel on the surface. So supernode KCL is independent of G_xy. Omit or include G_xy: same \( v_X, v_Y \). Supernode: current to ground \( 1.0\times 10^{-3} v_X + 2.0\times 10^{-3} v_Y = 3.0\times 10^{-3} \), and \( v_X - v_Y = 5 \). Then \( v_X + 2 v_Y = 3 \), \( v_X = v_Y + 5 \) ⇒ \( v_Y + 5 + 2 v_Y = 3 \) ⇒ \( 3 v_Y = -2 \) ⇒ \( v_Y = -0.667\,\mathrm{V} \), \( v_X = 4.333\,\mathrm{V} \).

### Answer

G in parallel with a voltage source is legal and does not change \( v_X, v_Y \). \( v_X = 4.333\,\mathrm{V} \), \( v_Y = -0.667\,\mathrm{V} \).

## Q5

### Given

Three meshes clockwise. Shared resistors 100 Ω between 1–2 and 100 Ω between 2–3. Around mesh 1 also 220 Ω and a 12 V source. Around mesh 3 also 220 Ω (no extra source). Mesh 2 has only the two 100 Ω and a 330 Ω to complete. No current sources.

### Find

The mesh resistance matrix and \( i_2 \) after solving (12 V in mesh 1 only, rise in the direction of \( i_1 \)).

### Solution

\( R_{11} = 220+100 = 320 \), \( R_{22} = 100+330+100 = 530 \), \( R_{33} = 220+100 = 320 \). \( R_{12} = R_{21} = -100 \), \( R_{23} = R_{32} = -100 \), \( R_{13} = 0 \). Right-hand side \( [12, 0, 0]^\top \). Solve \( 320 i_1 - 100 i_2 = 12 \), \( -100 i_1 + 530 i_2 - 100 i_3 = 0 \), \( -100 i_2 + 320 i_3 = 0 \). From third, \( i_3 = (100/320) i_2 = 0.3125 i_2 \). First: \( 320 i_1 = 12 + 100 i_2 \), \( i_1 = 0.0375 + 0.3125 i_2 \). Second: \( -100(0.0375 + 0.3125 i_2) + 530 i_2 - 100(0.3125 i_2) = 0 \) ⇒ \( -3.75 - 31.25 i_2 + 530 i_2 - 31.25 i_2 = 0 \) ⇒ \( 467.5 i_2 = 3.75 \) ⇒ \( i_2 = 8.021\,\mathrm{mA} \). Then \( i_1 = 40.01\,\mathrm{mA} \), \( i_3 = 2.507\,\mathrm{mA} \).

### Answer

\( \mathbf{R} = [[320,-100,0],[-100,530,-100],[0,-100,320]]\,\Omega \); \( i_2 = 8.02\,\mathrm{mA} \).

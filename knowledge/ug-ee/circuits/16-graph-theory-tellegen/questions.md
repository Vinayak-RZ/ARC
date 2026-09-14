# Questions — Graph theory, Tellegen, duality

Original pedagogical numbers.

## Q1

### Given

A connected circuit graph has 7 nodes and 11 branches.

### Find

Number of tree branches, number of links, number of independent KCL equations, and independent KVL equations.

### Solution

Tree branches = n−1 = 6. Links = b−n+1 = 11−7+1 = 5. Independent KCL = 6. Independent KVL = 5. Check: 6+5 = 11 branch unknowns if each branch has one constitutive law.

### Answer

6 tree branches; 5 links; 6 KCL; 5 KVL.

## Q2

### Given

Three branches: resistor 8 V and 2 A (PSC, absorbing), voltage source 12 V with 2 A leaving plus, current source 2 A with 4 V plus where current leaves the source.

### Find

Derive Tellegen sum v_k i_k with PSC on each, and interpret.

### Solution

Resistor: v i = 16 W absorbed. Voltage source PSC would need current into plus; current leaves plus so p_PSC = −12×2 = −24 W (delivers 24 W). Current source: current leaves plus, p_PSC = −4×2 = −8 W (delivers 8 W). Sum 16 − 24 − 8 = −16 ≠ 0. Inconsistency: currents are not KCL-compatible (2 A through resistor and 2 A leaving voltage source cannot also have a 2 A current source in a three-branch loop without a stated topology). Recast as a single loop: resistor, voltage source, no third current source. Then I = 2 A, resistor 8 V, source 12 V would violate KVL (8≠12). Honest Tellegen example: loop of 12 V source and 8 Ω resistor, I = 1.5 A. Source: current leaves plus, −12×1.5 = −18 W. Resistor +18 W. Sum 0.

### Answer

A legal KCL+KVL set sums to 0; the three-number list as given is not a valid graph assignment. Legal series example: −18 W + 18 W = 0.

## Q3

### Given

Design a proper tree for a connected network with one voltage source, one current source, two capacitors, one inductor, and four resistors (10 elements, count nodes as needed: assume a connected graph with n chosen so the sources are placeable).

### Find

Which elements should be in the proper tree if both capacitors can be in the tree and the inductor can be a link, and the current source is a link.

### Solution

Proper tree: include the voltage source, exclude the current source (it must be a link/cut-set member), include as many C as possible (both), exclude L if possible (L is a link). Fill remaining tree slots with resistors. Tree size n−1. Elements: 1 vs + 1 is + 2 C + 1 L + 4 R = 9 branches? “10 elements” may count a short. With 9 branches, links = 9−n+1. Current source and inductor as links (2), so remaining links = 9−n+1−2 wait we choose tree of n−1 branches from {vs, 2C, 4R} (7 candidates) excluding is and L. n−1 ≤ 7. If the graph is connected with 9 branches, n = 9 − ℓ + 1. If 2 links are is and L, ℓ≥2; if only those two links, ℓ=2, n=8, tree = 7, which uses vs + 2C + 4R exactly. That is the intended proper tree.

### Answer

Tree: voltage source, both capacitors, all four resistors. Links: current source and inductor.

## Q4

### Given

A student dualizes a 5 Ω resistor in series with a 2 H inductor into a 5 Ω resistor in series with a 2 F capacitor.

### Find

Explain the correct dual of that series pair driven by a voltage source.

### Solution

Dual of series is parallel. Dual of vs is a current source. Dual of 5 Ω is 5 S (0.2 Ω) not 5 Ω. Dual of 2 H is 2 F. So a current source in parallel with 0.2 Ω in parallel with 2 F. Keeping “5 Ω series 2 F” is the wrong topology and the wrong resistance number.

### Answer

Parallel current source, G = 0.2 S, C = 2 F; not series 5 Ω and 2 F.

## Q5

### Given

Planar connected graph: a square of four resistors plus one diagonal (five branches, four nodes).

### Find

ℓ, whether meshes = 2, and a tree.

### Solution

n=4, b=5, ℓ=5−4+1=2. Two inner meshes if the diagonal is drawn inside the square (two triangles). A tree has 3 branches: any three that touch all four nodes without a cycle, e.g. a spanning chain of three sides, omitting one side and the diagonal as links—or two sides and the diagonal if they do not form a triangle.

### Answer

2 links / 2 meshes; tree has 3 branches (e.g. three sides of a spanning path).

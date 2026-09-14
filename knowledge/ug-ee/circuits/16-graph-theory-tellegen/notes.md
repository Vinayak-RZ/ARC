# Graph theory, Tellegen, duality

Network topology makes Kirchhoff's laws independent of element types. A connected graph with n nodes and b branches has a reduced incidence matrix of rank n−1, n−1 independent KCL equations, and b−(n−1) independent KVL equations (the cyclomatic number, number of meshes in a planar connected graph). Trees, links (chords), fundamental cut-sets and loops are the systematic way to pick those equations. Tellegen's theorem is the power-balance identity that follows from KCL and KVL alone. Duality swaps voltage and current, loops and cut-sets, R and G, L and C, series and parallel.

## Concepts

A graph of a lumped circuit replaces each two-terminal element by an edge and each node by a vertex. Directed graphs assign a reference direction to each branch current. A tree is a connected acyclic spanning subgraph; it has n−1 branches. The remaining b−n+1 branches are links. Each link with the tree path between its vertices forms a fundamental loop. Each tree branch defines a fundamental cut-set (the tree branch plus the links that reconnect the two parts of the graph). KVL on fundamental loops and KCL on fundamental cut-sets are independent and complete.

Loop analysis in this language is not restricted to planar meshes; fundamental loops work on nonplanar graphs. Mesh analysis is the planar special case. Node analysis uses the reduced incidence matrix A: A i = 0 is KCL, v = A^T v_node is KVL automatically.

Tellegen: if i satisfies KCL and v satisfies KVL on the same directed graph, then \( \sum_{k=1}^{b} v_k i_k = 0 \) at the same time, even if v and i come from different element laws or different instants (the “quasi-power” form), provided they share the graph. Ordinary power conservation is the special case of the same network at the same time. Tellegen does not need linearity, reciprocity, or passivity. It is why superposition of power fails (power is not a Kirchhoff quantity) while superposition of v and i works (linearity).

Duality: a planar graph has a dual whose nodes correspond to meshes of the original (plus the outer face) and whose branches cross the original branches. Element duals: resistance ↔ conductance (R ↔ 1/R in SI if we insist on ohms vs siemens with the same number only after scaling), voltage source ↔ current source, inductor ↔ capacitor (L ↔ C with v↔i), series ↔ parallel, open ↔ short, KVL ↔ KCL. The dual of a series RLC voltage-driven loop is a parallel GCL current-driven node. Duality is a construction, not a numerical identity of every circuit; nonplanar graphs have no dual in the plane.

Tie-set (loop) matrix B: B v = 0 is KVL. Cut-set matrix Q: Q i = 0 is KCL. Orthogonality B Q^T = 0 is the discrete analogue of Tellegen.

Proper tree for RLC: a tree that contains all voltage sources, no current sources, as many capacitors as possible, and as few inductors as possible. State variables are then capacitor tree voltages and inductor link currents. That is the topological origin of the state-space models used in later control courses.

Incidence matrix example, four nodes in a square, branches around the square clockwise plus one diagonal. After deleting the ground row, A is 3×5 with 0, ±1 entries, two nonzeros per branch column (or one if the branch goes to ground). KCL A i = 0 is three scalar equations. A tree of three sides that form a spanning tree has columns that form an invertible 3×3; those tree currents are not independent (they are determined by the links through KVL and elements), but the matrix split A = [At Al] with At invertible is the standard textbook partition. Then link currents are the independent current variables in loop analysis: i_tree = −At^{-1} Al i_link.

Tellegen's two-network form is surprisingly useful: voltages from circuit A, currents from circuit B, same graph. Then Σ v^A i^B = 0. Choosing B as a small-signal circuit and A as a DC operating point, or B as an adjoint network, is how analog designers later prove sensitivity identities. At UG, the message is that the identity is topological. If a student “proves” power balance by adding I²R and forgetting a dependent source that can deliver P, Tellegen still holds; the dependent source is a branch with a v and an i. Missing that branch is why the sum missed.

Dual construction, step by step, for a series voltage source, R, L, C loop (one mesh). One inner face, one outer face: two dual nodes. Each original branch is crossed by a dual branch: current source (dual of vs), G = 1/R, C_dual = L, L_dual = C, all in parallel between the two dual nodes. That is the parallel current-driven GCL tank. Initial conditions dualize: iL(0) in the original is vC(0) in the dual with the swapped element. Planarity mattered: we had one mesh. A nonplanar K3,3 circuit has no planar dual; you can still write equations, you just cannot draw a dual circuit in the plane.

Illegal graphs: a loop of voltage sources with a nonzero KVL sum is inconsistent (explosion in a simulator's first Newton step). A cut-set of current sources with a nonzero KCL sum is inconsistent. A capacitor loop with inconsistent voltages at 0− produces an impulse. An inductor cut-set with inconsistent currents produces a voltage impulse. Graph theory predicts these before element values are substituted.

Numbering: UG exam problems sometimes ask only for counts: b, n, ℓ, tree size. Connected assumed unless stated. Each separate piece of a disconnected graph adds its own tree; a graph with p parts has n−p tree branches in a forest. Most circuit graphs are connected because of a common ground; if a transformer isolates two windings without a drawn magnetizing branch to a common node, some models treat two parts coupled by M, which is not a topological edge in the electric graph. Mutual inductance is an element law between two existing edges, not a third edge, unless you add a T-model core node.

## Equations

\( n \) nodes, \( b \) branches, connected: tree branches \( n-1 \), links \( \ell = b-n+1 \).

KCL: \( A i = 0 \) (A is (n−1)×b). KVL: \( v = A^T \phi \) with node potentials \( \phi \), or \( B v = 0 \).

Tellegen: \( v^T i = 0 \).

Planar meshes: \( \ell = \) number of meshes (including? inner meshes = ℓ for a connected planar graph drawn without crossings, inner faces).

Duality: \( v \leftrightarrow i \), \( R \leftrightarrow G \), \( L \leftrightarrow C \), \( v_s \leftrightarrow i_s \).

Incidence: \( a_{kj} = +1 \) if branch j leaves node k, −1 if it enters, 0 else.

## Methods

To write a complete set: pick a tree, write KVL on each fundamental loop or KCL on each cut-set, substitute constitutive laws. For Tellegen checks, list every branch v and i with PSC, sum products, expect ~0 within rounding. For duality, draw the planar graph, place a dual node in each face, cross each branch with a dual branch, assign dual elements.

When counting meshes, do not include the outer unbounded face as a mesh current; it is the dependent one. When counting dual nodes, the outer face does become a node (often ground of the dual).

Use graph arguments to detect illegal connections: a loop of only voltage sources, a cut-set of only current sources, which make A i = 0 and B v = 0 inconsistent with the sources.

A counting drill: draw K4, the complete graph on four nodes (six edges). Then n=4, b=6, ℓ=3. It is planar (a triangle with a nested node, or a square with two diagonals is not planar—K4 is planar, K5 is not). Three independent KVL. A tree is a Y of three edges. Dual of a planar embedding of K4 is another 4-node 6-edge graph. Tellegen: six products v_k i_k sum to zero if the six currents satisfy KCL at four nodes (three independent) and the six voltages satisfy the three KVL. You can pick voltages from Ohm on one set of resistors and currents from a different experiment on the same wiring; the sum is still zero. That is the quasi-power form, and it is the reason Tellegen is more than “energy is conserved.”

## Mistakes

Counting a tree with a cycle. Using mesh analysis on a nonplanar drawing without adding extra loops correctly. Forgetting the outer face in duality. Applying Tellegen with currents from one circuit and voltages from another without sharing the same directed graph. Claiming Tellegen requires RLC linearity. Dualizing a voltage source to a voltage source. Treating n nodes as n independent KCL equations (ground removes one). Setting ℓ = b − n instead of b − n + 1. Using a tree that includes a current source (it cannot set that branch voltage via a tree path in the usual proper-tree recipe). Sign chaos in A from mixing leaving/entering conventions mid-matrix. Confusing duality of elements with complementary energy (which is a different, variational idea).

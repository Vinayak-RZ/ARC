# Unsymmetrical faults and sequence networks

Unbalanced short circuits — single line-to-ground (LG), line-to-line (LL), and double line-to-ground (LLG) — are the majority of real faults. Fortescue’s symmetrical components split a three-phase set into positive, negative, and zero sequences. Each sequence sees its own network. The fault type dictates how those three networks are connected at the fault point. This unit is the UG toolkit: sequence operators, transformer sequence connections, sequence network reduction to Thevenin impedances \(Z_1,Z_2,Z_0\) at the fault bus, and the four standard fault formulas including the bolted three-phase case as a check. Open-conductor faults and simultaneous faults are mentioned only as existence proofs.

## Concepts

A three-phase phasor set \((V_a,V_b,V_c)\) transforms as

\[
\begin{pmatrix}V_0\\V_1\\V_2\end{pmatrix}
=\frac13\begin{pmatrix}1&1&1\\1&a&a^2\\1&a^2&a\end{pmatrix}
\begin{pmatrix}V_a\\V_b\\V_c\end{pmatrix},
\]

with \(a=e^{j120^\circ}=e^{j2\pi/3}\), \(a^2=e^{-j120^\circ}\), \(1+a+a^2=0\). Inverse: \(V_a=V_0+V_1+V_2\), \(V_b=V_0+a^2 V_1+a V_2\), \(V_c=V_0+a V_1+a^2 V_2\). The same matrix applies to currents. Sequence 1 is the ordinary balanced positive-sequence set used in load flow. Sequence 2 is a backwards-rotating balanced set. Sequence 0 is the in-phase residual, three times the neutral current in a Y: \(I_n=3I_0\).

In a linear balanced network (transposed lines, balanced loads, machines with symmetric windings) the sequences decouple. Each sequence has a Thevenin equivalent at the faulted bus: \(E_1\) (prefault positive-sequence voltage, often \(1.0\ \mathrm{pu}\)) behind \(Z_1\); negative sequence has \(E_2=0\) behind \(Z_2\); zero sequence has \(E_0=0\) behind \(Z_0\). Unbalanced loads or untransposed lines couple sequences; UG ignores that.

Typical impedances: for a synchronous machine \(Z_1=jX''_d\) (subtransient, as in unit 04), \(Z_2\approx jX''_d\) (often taken equal to \(X''\) or a stated \(X_2\)), \(Z_0\) is smaller or comparable depending on grounding of the winding (solidly grounded Y has a finite \(X_0\), often \(0.05\)–\(0.15\) plus \(3Z_g\)). Transformers: leakage \(X_t\) appears in positive and negative sequences equally. Zero-sequence path depends on winding connection and grounding:

- Y-grounded / Y-grounded: zero-sequence current can flow through both sides if there is a ground path; leakage appears in \(Z_0\) like \(Z_1\), plus \(3Z_g\) at each grounded star point that carries \(I_0\).
- Y-grounded / Δ: zero-sequence current circulates in the delta and returns through the grounded-Y neutral. The delta side does not pass \(I_0\) to the next network. In the zero-sequence diagram the transformer is a series \(X_t\) from the Y-grounded bus to reference (through the delta’s circulating path), and the delta-side network is disconnected from that shunt.
- Y-ungrounded / anything: open in zero sequence on the ungrounded-Y side.
- Δ / Δ: no zero-sequence path to ground; magnetizing only.

Lines: \(Z_1=Z_2=z_+\ell\). \(Z_0\) is larger, typically \(2\)–\(3.5\) times \(Z_1\) for overhead lines with earth return, because earth-return inductance is high. Cables have different \(Z_0/Z_1\). Never use \(Z_0=Z_1\) for an overhead line unless told.

Fault connections (phase a the reference, bolted unless \(Z_f\) is given):

Three-phase (abc): only positive sequence, \(I_1=E_1/(Z_1+Z_f)\), \(I_2=I_0=0\). Same as unit 04.

LG (a-g): the three sequence networks in series. \(I_0=I_1=I_2=E_1/(Z_1+Z_2+Z_0+3Z_f)\). Phase current \(I_a=3I_1\), \(I_b=I_c=0\).

LL (b-c): positive and negative sequences in parallel, zero sequence absent. \(I_1=-I_2=E_1/(Z_1+Z_2+Z_f)\), \(I_0=0\). \(I_b=-I_c\) involving \(a\) operators.

LLG (b-c-g): positive sequence in series with the parallel of negative and zero. \(I_1=E_1/(Z_1+Z_2\parallel Z_0)\) when \(Z_f=0\), with more algebra if fault impedances sit in the connections. Then \(I_2\) and \(I_0\) split from \(-I_1\) through the parallel.

The series/parallel pictures are the thing to draw first. Deriving them from \(V_a=Z_f I_a\), \(I_b=I_c=0\) (LG) and Fortescue is a good once-per-semester exercise; afterwards use the pictures.

Which fault is worst? At a solidly grounded bus, LG current can exceed three-phase current if \(Z_0<Z_1\) (typical near a grounded-Y transformer). At an ungrounded bus \(Z_0=\infty\) and LG current is zero (actually capacitive charging, not UG bolted-fault). LL is often milder than three-phase when \(Z_2\approx Z_1\): \(I_L=\sqrt{3}E/(Z_1+Z_2)\approx 0.866\) times the three-phase current. Always compute; do not assume three-phase is largest.

Voltage of healthy phases during LG: they can rise toward line-to-line on an ungrounded system (full displacement of the neutral). On a solidly grounded system the healthy-phase overvoltage is modest. This is why grounding type (unit 08) and arrester ratings couple to this unit.

Sequence currents in machines: negative-sequence current heats rotor iron (counter-rotating field). Relays use \(I_2^2 t\) limits. Zero-sequence in a transformer is a design constraint for the tank and delta winding. UG computes the currents; thermal limits are named, not designed here.

Prefault load: same as unit 04, \(E_1=V_k(0)\). Unloaded \(E_1=1.0\angle 0\). Negative- and zero-sequence networks have no internal EMFs for ordinary machines (a voltage regulator does not create \(E_2\)).

Phase designation: if the faulted phase is b rather than a, rotate the labels or insert \(a\) factors. Exam problems almost always fault phase a for LG and phases b-c for LL.

Open-conductor (series) faults are dual in spirit: they insert sequence networks in parallel or series in a different pattern (one open phase: series connection of sequences in the series-path sense). Simultaneous LG at two locations needs two ports. UG core stops at shunt faults at one bus. If a question says “conductor of phase a open at the sending end,” draw the series-fault interconnection from a handbook you trust in an elective; do not reuse the shunt LG picture.

Transformer phase shift of \(30^\circ\) (Yd11, Dyn1, and so on) rotates positive-sequence voltages and currents by \(\pm 30^\circ\) and negative-sequence by the opposite angle. Zero-sequence does not pass through a Yd bank. For a fault on the delta side, HV-side line currents may show a characteristic 2-1-1 split even for a single-phase fault. Many UG numericals stay on one voltage level and ignore the 30° shift; if both sides’ currents are asked, apply the vector group.

Earth wires and overhead-ground-wire return reduce \(Z_0\) relative to a no-ground-wire Carson's line. Cable sheaths do the same. If the problem gives \(Z_0=3Z_1\), use it; do not “correct” it to a memory of 3.5.

Numerical hygiene: compute \(I_0,I_1,I_2\) first and keep them in rectangular form. Inverse-transform with \(a=-0.5+j\sqrt{3}/2\) as a complex number, not as a spoken “120 degrees” that then gets applied to the wrong sequence. Check \(I_a+I_b+I_c=3I_0\) on paper before boxing the answer. For LG, two phase currents must be essentially zero; if they are not, the interconnection was wrong.

A residual CT connection (three CTs with secondaries summing to a residually connected earth-fault relay) measures \(3I_0\). That is why earth-fault pickup can be much more sensitive than phase overcurrent: load does not produce \(I_0\) in a balanced feeder. Unit 10 uses this; this unit produces the \(3I_0\) number.

Solid versus impedance grounding changes only \(Z_0\) (plus \(3Z_g\)). The positive-sequence diagram is the same as unit 04. Never retune \(Z_1\) because the neutral resistor changed.

LLG algebra is the place students lose signs. After \(I_1\) is found through \(Z_1+Z_2\parallel Z_0\), the interconnection is: positive-sequence in series with the parallel of negative and zero, with \(I_0+I_2=-I_1\), \(V_2=-Z_2 I_2\), \(V_0=-Z_0 I_0\), and \(V_1=V_2=V_0\) at the fault point for bolted LLG on phases b and c. The last equality is the check: \(E_1-Z_1 I_1=-Z_2 I_2=-Z_0 I_0\). If that fails, the current split is wrong.

Fault impedance in LLG (arc in the lines versus in the ground) sits in different branches of the interconnection. If the problem does not give \(Z_f\), treat the fault as bolted. If it gives a single \(Z_f\) in the ground, that \(Z_f\) is in the zero-sequence branch as \(3Z_f\) analogous to LG.

## Equations

Operator \(a=e^{j2\pi/3}\). Inverse transform:

\[
V_a=V_0+V_1+V_2,\quad I_a=I_0+I_1+I_2.
\]

Thevenin at fault bus: \(E_1\), \(Z_1,Z_2,Z_0\).

Three-phase: \(I_1=E_1/Z_1\), \(I_a=I_1\).

LG (a-g), fault impedance \(Z_f\):

\[
I_0=I_1=I_2=\frac{E_1}{Z_1+Z_2+Z_0+3Z_f},\qquad I_a=3I_1.
\]

LL (b-c), \(Z_f\) between lines:

\[
I_1=-I_2=\frac{E_1}{Z_1+Z_2+Z_f},\qquad I_0=0,\qquad I_b=-I_c= (a^2-a)I_1.
\]

(\(a^2-a=-j\sqrt{3}\), so \(|I_b|=\sqrt{3}|I_1|\).)

LLG (b-c-g), bolted:

\[
I_1=\frac{E_1}{Z_1+Z_2 Z_0/(Z_2+Z_0)},\quad
I_2=-I_1\frac{Z_0}{Z_2+Z_0},\quad
I_0=-I_1\frac{Z_2}{Z_2+Z_0}.
\]

Neutral current at a grounded star: \(I_n=3I_0\).

## Methods

1. Build three sequence networks from the one-line. Include grounding \(3Z_g\) only in zero sequence. Connect transformer zero-sequence diagrams from winding type, not from positive-sequence habit.
2. Reduce each network to \(Z_1,Z_2,Z_0\) at the fault bus. Record \(E_1\).
3. Draw the interconnection for the requested fault. Solve for \(I_0,I_1,I_2\).
4. Inverse-transform to phase currents. Convert to kA with the local \(I_\mathrm{base}\).
5. Optional: sequence voltages \(V_1=E_1-Z_1 I_1\), \(V_2=-Z_2 I_2\), \(V_0=-Z_0 I_0\), then phase voltages.

Checks: LG with \(Z_0=\infty\) gives \(I=0\); LL with \(Z_2=Z_1\) gives \(|I_L|=\sqrt{3}/2\) times three-phase \(|I_{3\phi}|=E/Z_1\), i.e. \(\sqrt{3}E/(2Z_1)\); \(I_a+I_b+I_c=3I_0\); only one phase current nonzero for LG.

If \(Z_f\) is in the ground path of LG, it appears as \(3Z_f\) in the series connection (because \(I_0\) flows in the fault as \(3I_0\) times \(Z_f\) in the phase domain, and the sequence KVL uses \(I_0\)).

## Mistakes

Putting \(3Z_g\) in the positive-sequence diagram. Passing zero-sequence current through a delta winding to the next bus. Using \(Z_0=Z_1\) on an overhead line without data. Connecting networks in parallel for LG (that is LLG/LL, not LG). Forgetting \(I_a=3I_1\) on LG and reporting \(I_1\) as the phase current. Using \(I_{\mathrm{base}}\) of the wrong kV side. Mixing \(a\) and \(a^2\) so that LL currents appear on phase a. Adding \(Z_f\) instead of \(3Z_f\) in LG. Using \(X_s\) in sequence networks when \(X''\) was specified. Computing three-phase fault with all three networks in series. Dropping the minus signs when splitting \(I_2,I_0\) in LLG, then failing \(I_b+I_c+I_a=3I_0\). Treating \(Z_2\) of a transformer as different from \(Z_1\) (they are equal for a static transformer).

# Load flow: \(Y_\mathrm{bus}\), Gauss–Seidel, and Newton–Raphson at UG level

Load flow (power flow) is the steady-state AC solution of a network: given generator scheduled powers and voltage magnitudes, transformer taps, and loads, find bus voltage phasors and therefore line flows and losses. It is not a transient study and not a fault study. Every undergraduate power-system analysis course builds \(Y_\mathrm{bus}\), classifies buses, and iterates Gauss–Seidel and/or Newton–Raphson on a tiny network (2–5 buses) by hand or with a short program. This unit is that core. Optimal power flow, interior-point methods, and three-phase unbalanced distribution power flow are out of scope.

## Concepts

A bus has a complex voltage \(\mathbf{V}_i=V_i e^{j\theta_i}\) (or \(V_i\angle\theta_i\)) and a complex injected power \(\mathbf{S}_i=P_i+jQ_i=\mathbf{V}_i\mathbf{I}_i^*\). Injected means into the network from generators minus loads at that bus (load convention on the load, generator convention on the source; the net injection is \(S_{\mathrm{gen}}-S_{\mathrm{load}}\)). Kirchhoff plus the linear network gives \(\mathbf{I}=Y_\mathrm{bus}\mathbf{V}\). Combining with \(S_i=V_i I_i^*\) produces the nonlinear power-flow equations.

\(Y_\mathrm{bus}\) construction from a \(\pi\)-model network: for a branch between \(i\) and \(k\) with series admittance \(y_{ik}=1/z_{ik}\) and shunt \(j b_{ik}/2\) at each end (plus any shunt capacitor \(y_i^{\mathrm{sh}}\) at the bus),

\[
Y_{ii}=\sum_{k\text{ adjacent}} \bigl(y_{ik}+j b_{ik}/2\bigr)+y_i^{\mathrm{sh}},\qquad Y_{ik}=-y_{ik}\ (i\neq k).
\]

Off-nominal tap: if a transformer from \(i\) to \(k\) has tap \(t\) on the \(i\) side (ideal ratio \(t:1\), leakage \(y\) on the \(k\) side in a common convention), the extra terms make \(Y_{ii}=y/t^2\), \(Y_{kk}=y\), \(Y_{ik}=Y_{ki}=-y/t\) for a real tap. Other textbooks put the leakage on the tap side; pick one convention and stay with it. For hand problems, taps are often \(1.0\) and the transformer is just a series \(jX\).

Bus types:

- Slack (swing): \(V\) and \(\theta\) given (usually \(\theta=0\)). \(P\) and \(Q\) are unknown; the slack supplies whatever is needed to balance loads plus losses. One slack is required because absolute angle is free and because losses are not known a priori.
- PV (generator, voltage-controlled): \(P\) and \(V\) given. \(Q\) and \(\theta\) unknown. \(Q\) must later respect \(Q_{\min}\le Q\le Q_{\max}\); if a limit binds, the bus is switched to PQ with \(Q\) fixed at the limit and \(V\) free.
- PQ (load): \(P\) and \(Q\) given (usually negative injections if \(P,Q\) are loads). \(V\) and \(\theta\) unknown.

A pure voltage-controlled bus with \(P=0\) is a synchronous condenser: PV with zero real power.

Gauss–Seidel (GS) iterates the rearranged current equation. From \(I_i=\sum_k Y_{ik}V_k\) and \(I_i=(P_i-jQ_i)/V_i^*\) one obtains

\[
V_i^{(p+1)}=\frac{1}{Y_{ii}}\left(\frac{P_i-jQ_i}{(V_i^{(p)})^*}-\sum_{k\neq i} Y_{ik}V_k^{\mathrm{latest}}\right).
\]

Use newest voltages for buses already updated in this sweep (Gauss–Seidel, not Jacobi). For a PV bus, after computing a complex \(V_i\), restore the scheduled magnitude: \(V_i\leftarrow V_i^{\mathrm{sch}}\cdot V_i/|V_i|\), and optionally back-compute \(Q_i=\mathrm{Im}(V_i I_i^*)\) to test limits. Slack is never updated. Acceleration \(\alpha\) replaces \(V\) by \(V^{\mathrm{old}}+\alpha(V^{\mathrm{new}}-V^{\mathrm{old}})\); \(\alpha\approx 1.6\) is a common textbook suggestion and can also diverge. UG hand work usually uses \(\alpha=1\) for one or two iterations.

GS is easy to program and slow (linear convergence), sensitive to slack placement, and awkward with PV buses. It is still the right first algorithm because you can see each bus voltage being pulled by the mismatch current.

Newton–Raphson (NR) solves \(f(x)=0\) where \(x=[\theta_{\mathrm{unknown}},V_{\mathrm{unknown}}]\) and \(f\) is the vector of \(\Delta P\) at PV and PQ buses and \(\Delta Q\) at PQ buses. The mismatch at bus \(i\) is scheduled injection minus computed injection \(P_i^{\mathrm{calc}}(V,\theta)\), \(Q_i^{\mathrm{calc}}(V,\theta)\). Polar NR is the UG standard:

\[
P_i=\sum_k V_i V_k\bigl(G_{ik}\cos\theta_{ik}+B_{ik}\sin\theta_{ik}\bigr),
\]
\[
Q_i=\sum_k V_i V_k\bigl(G_{ik}\sin\theta_{ik}-B_{ik}\cos\theta_{ik}\bigr),
\]

with \(\theta_{ik}=\theta_i-\theta_k\) and \(Y_{ik}=G_{ik}+jB_{ik}\). The Jacobian \(J=\partial(P,Q)/\partial(\theta,V)\) is partitioned into \(H,N,M,L\) blocks. One NR step: solve \(J\Delta x=-f\) (or \(J\Delta x=\Delta S\)) and update \(\theta\leftarrow\theta+\Delta\theta\), \(V\leftarrow V+\Delta V\). Quadratic convergence when the start is close; a flat start \(V=1\angle 0\) usually works on well-posed UG networks. Ill-conditioned cases (long radial, heavy load) may need a better start or a damped step.

Decoupled and fast-decoupled NR use \(P\)–\(\theta\) and \(Q\)–\(V\) weak coupling in high-X networks: off-diagonal \(N\) and \(M\) neglected, and \(B'\) and \(B''\) approximations of \(-\mathrm{Im}(Y)\). They are the workhorse of older production programs. UG exams may ask you to write the \(2\times 2\) Jacobian of a two-bus system, not to derive BX/XB variants in full.

Two-bus illustration: slack bus 1 at \(V_1=1.0\angle 0\), PQ bus 2 with load \(P_2+jQ_2\) (injections negative), line \(y=1/(jX)=-j/X\). Then \(P_2=-(V_1 V_2/X)\sin\theta_2\) if \(\theta_2\) is the angle of bus 2 (power into the network at 2 is negative of power into the load). The signs must follow the injection convention you wrote in \(Y_\mathrm{bus}V=I\). Draw power arrows.

Line flows: after voltages converge, series current \(I_{ik}=y_{ik}(V_i-V_k)+j(b_{ik}/2)V_i\) (sending-end \(\pi\)), \(S_{ik}=V_i I_{ik}^*\). Losses on that branch \(S_{ik}+S_{ki}\) equal \(I_{\mathrm{series}}^2 Z\) plus nothing from lossless shunts. Sum of all bus injections equals total generation minus total load equals total losses.

Slack generation is not a “free lunch”: it is the unknown that makes \(\sum P_{\mathrm{inj}}=P_{\mathrm{losses}}\). If you specified every generator P including a would-be slack, the problem is over-specified unless a distributed slack is defined (not UG).

DC load flow is the linearization \(P_i=\sum_k B_{ik}(\theta_i-\theta_k)\) with \(V=1\), \(G=0\), \(\sin\theta\approx\theta\). It is used for security-constrained dispatch and LMP sketches. It cannot compute voltages or Q. Mention it; do not confuse it with the AC solution.

Multiple solutions: the power-flow map can have a low-voltage solution near voltage collapse. Flat-start NR on a solvable network usually finds the high-voltage (stable) solution. Continuation power flow is postgraduate.

Hand-sized \(Y_\mathrm{bus}\) mistakes are almost always shunts and taps. A line \(\pi\) contributes \(j b/2\) to each terminal diagonal and \(-1/z\) to the off-diagonal; a shunt capacitor at a bus contributes only to that diagonal. If you put charging on the off-diagonal, the row sum of \(Y_\mathrm{bus}\) is no longer the shunt, and a zero-injection bus with no shunt would not satisfy \(Y_{\mathrm{row}}\mathbf{1}=0\) in a purely series network. That row-sum check is the fastest debug: for a network with no shunts, \(Y\mathbf{1}=0\) (singular, as expected before a slack is chosen in the power-flow Jacobian, not in \(Y\) itself — \(Y\) of a floating network is singular; we still invert the reduced Jacobian, not \(Y\)). \(Y_\mathrm{bus}\) for load flow includes shunts and is usually invertible; \(Y_\mathrm{bus}\) for fault studies includes generator \(1/jX''\) to reference and is definitely invertible.

PV–PQ switching deserves a second paragraph because it is the most common “the voltage is 1.04 but Q is 3 pu” bug. A small machine cannot hold a 1.04 pu voltage on a weak bus; NR will demand an impossible Q. The correct UG action is to freeze Q at \(Q_{\max}\) and free \(V\). After the next iteration, \(V\) will sag. If an exam does not mention limits, do not invent them. If it lists \(Q_{\max}\), you must test.

Angle reference: only differences \(\theta_i-\theta_k\) appear in \(P\) and \(Q\). The slack angle is a gauge. Reporting a bus angle of \(350^\circ\) after wrapping is the same as \(-10^\circ\); keep angles in a principal interval so the Jacobian linearization \(\sin\theta\approx\theta\) is not applied at \(350^\circ\) in a DC-load-flow homework.

Three-winding transformers and phase shifters make \(Y\) unsymmetric or add a fictitious star bus. For this unit, if a phase shift \(\phi\) is given, \(Y_{ik}=-|y|/t\,e^{-j\phi}\) in one off-diagonal and the conjugate-unlike partner on the other; \(P\) can be steered. Skip unless the problem states \(\phi\).

## Equations

Network law:

\[
\mathbf{I}=Y_\mathrm{bus}\mathbf{V},\qquad S_i=V_i I_i^*.
\]

Power equations (polar):

\[
P_i=V_i\sum_k V_k(G_{ik}\cos\theta_{ik}+B_{ik}\sin\theta_{ik}),
\]
\[
Q_i=V_i\sum_k V_k(G_{ik}\sin\theta_{ik}-B_{ik}\cos\theta_{ik}).
\]

Gauss–Seidel update as above. Acceleration: \(V\leftarrow V^{\mathrm{old}}+\alpha\Delta V\).

Newton:

\[
\begin{pmatrix}\Delta P\\\Delta Q\end{pmatrix}
=
\begin{pmatrix}H&N\\M&L\end{pmatrix}
\begin{pmatrix}\Delta\theta\\\Delta V\end{pmatrix}.
\]

Typical diagonal Jacobian terms (for \(i\) not slack; \(V\) in pu):

\[
H_{ii}=\frac{\partial P_i}{\partial\theta_i}=-Q_i-B_{ii}V_i^2,\qquad L_{ii}=\frac{\partial Q_i}{\partial V_i}=\frac{Q_i}{V_i}-B_{ii}V_i,
\]

with off-diagonals from differentiating the sum; write them from first principles on a two-bus exam rather than memorizing every index.

Two-bus lossless:

\[
P_{12}=\frac{V_1 V_2}{X}\sin(\theta_1-\theta_2).
\]

## Methods

1. Draw the one-line, convert to pu, replace lines and transformers by \(\pi\) or series \(jX\).
2. Build \(Y_\mathrm{bus}\) (include shunts on the diagonal).
3. Classify buses; assign slack; list scheduled \(P,V\) or \(P,Q\).
4. Flat start: \(V=1.0\angle 0\) at PQ, \(V=V^{\mathrm{sch}}\angle 0\) at PV.
5. Iterate GS or one NR step as asked. For GS on PV, hold \(|V|\) and compute \(Q\).
6. After convergence, compute slack \(P,Q\), line flows, and losses. Check \(\sum P_{\mathrm{gen}}=\sum P_{\mathrm{load}}+\sum P_{\mathrm{loss}}\).

Hand NR on 2–3 buses: compute \(P^{\mathrm{calc}},Q^{\mathrm{calc}}\) from the polar formulas, mismatches \(\Delta P=P^{\mathrm{sch}}-P^{\mathrm{calc}}\), form \(J\) by differentiating or by the compact \(H_{ii}\) formulas, solve the linear system.

If \(Q\) limit is exceeded at a PV bus, switch to PQ at \(Q_{\mathrm{lim}}\) and release \(V\). If later \(Q\) would return inside the band at the scheduled \(V\), switch back (production code); UG usually only tests one switch.

Checks: \(|V|\) between about \(0.95\) and \(1.05\) in a healthy UG example; angles a few degrees on short systems; losses a few percent of load; slack \(P>0\) if it is a generator.

## Mistakes

Building \(Y_{ik}=+y_{ik}\) (wrong sign; off-diagonal is negative). Putting shunt \(B/2\) into the off-diagonal. Using load as a positive injection in \(P_i-jQ_i\) without a minus. Updating the slack in GS. Forgetting to restore \(|V|\) on a PV bus. Mixing degrees and radians in \(\sin\theta\) (NR Jacobians need radians). Using \(S=VI\) instead of \(VI^*\). Computing line flow with \((V_i-V_k)/z\) but omitting charging when the problem used a \(\pi\). Treating DC load flow as giving \(Q\). Two slacks without a tying equation. Flat start in degrees written as \(V=1\angle 0\) then using \(\theta=0^\circ\) inside a cosine that expected radians in a programmed NR — in hand work, convert \(\delta\) to radians before multiplying into \(H\Delta\theta\). Sign error \(\Delta P=P^{\mathrm{calc}}-P^{\mathrm{sch}}\) while still using \(\Delta x=J^{-1}\Delta P\) as if the mismatch were scheduled minus calculated. Ignoring tap squares in \(Y_{ii}\). Adding MW and Mvar into \(Y_\mathrm{bus}\).

# Laplace-domain networks and initial conditions

The Laplace transform turns integro-differential circuit equations into algebra in s. Impedances become Z(s) = R, sL, 1/(sC). Initial conditions appear as independent sources: a capacitor voltage V0 becomes a series V0/s or a parallel C V0 current source; an inductor current I0 becomes a series L I0 voltage source or a parallel I0/s current source. Inverse Laplace, usually by partial fractions, returns v(t) and i(t) for t ≥ 0, transients and forced response together. This unit sits between circuits and signals; it is the systematic replacement for guessing exponentials.

## Concepts

Unilateral Laplace \( F(s) = \int_{0^-}^\infty f(t) e^{-st} dt \) includes impulses at the origin and the initial-condition jump from 0− to 0+. Circuit books must pick 0− or 0+ consistently. Using 0− in the transform of derivatives puts vC(0−) and iL(0−) into the s-domain circuit, which is convenient because those are the states that cannot jump under finite sources.

s-domain Ohm: V(s) = Z(s) I(s) for initially relaxed elements. If not relaxed, add the initial-condition sources. KCL, KVL, nodal, mesh, Thévenin all apply to the transformed network. Switching at t=0 is modeled by including sources that exist for t>0 (step = 1/s times amplitude) and the IC sources from t=0−.

Poles of a response are the natural frequencies, the same s1, s2 as in the characteristic equation of the ODE method. Zeros depend on which variable is observed. A canceled pole-zero pair means that variable does not see that mode (hidden mode), but another variable might.

Partial fractions: proper rationals. If degree of numerator is not lower, divide first. Repeated poles from critical damping produce t e^{αt} terms. Complex poles produce damped sinusoids; keep them as quadratics or convert to polar residues.

Impulse and step: δ(t) ↔ 1, u(t) ↔ 1/s. A capacitor switched onto a voltage step without series R implies an impulsive current; the Laplace method handles it if you keep 0− values and allow impulses. Physically add a little R.

Transfer function H(s) = Vout/Vin with zero initial conditions. It is not the full story when IC are nonzero; use superposition of the IC-source circuit and the driven relaxed circuit.

s-domain circuit diagrams deserve the same polarity care as time-domain ones. The capacitor IC voltage source V0/s is oriented the same way as the actual vC(0−): plus toward the plus of C. The inductor IC voltage source L I0 is oriented as a drop in the direction of iL(0−), matching v = L di/dt − L i(0−) when i and v are PSC. Getting that minus wrong flips the entire transient. After solving, the initial-value theorem on VC(s) must recover vC(0+), which equals vC(0−) if no impulse of current occurred. If IVT disagrees with the 0− value, either an impulse is real (capacitor loop) or a sign is wrong.

Partial fractions in engineering form: for a real pole, r = (s−p) F(s) |_{s=p}. For a repeated pole of order 2, A2 = (s−p)² F(s) |_{s=p}, A1 = d/ds[(s−p)² F(s)] |_{s=p}. For a complex pair, keep a quadratic and match coefficients to e^{αt}(B1 cos ωt + B2 sin ωt), which is less error-prone than conjugate residues if the algebra is messy. Cover-up method fails if the numerator degree is not lower; divide out a constant or an s term first (a series C with a step voltage can produce a constant in I(s)).

Relationship to ODE methods: the characteristic polynomial is the denominator of the relaxed H(s), the same as det of the s-domain mesh matrix. The Laplace method does not add physics; it adds bookkeeping for IC and for non-exponential sources (ramps, steps, switched sinusoids). A switched cosine is L{cos ωt} = s/(s²+ω²) if it starts at t=0. A cosine that existed for all negative time is not a unilateral transform of that formula; you would include IC from t=0− matching that cosine.

Impedance Z(s) is not a phasor. You may evaluate Z(jω) to get the sinusoidal impedance after transients die. You may not write Z(s) = j s L. That hybrid is nonsense. Similarly, do not put 45° angles on an s-domain schematic.

Stability: poles of a passive RLC network lie in Re(s)≤0, and jω poles are simple (LC undamped). Adding active dependent sources can push poles to the right; then the inverse Laplace grows and the linear model is only valid for a short time. FVT is then also illegal.

A complete UG recipe: (1) 0− DC analysis, (2) s-domain circuit with IC sources and transformed sources, (3) nodal or mesh in s, (4) V(s), (5) partial fractions, (6) v(t) for t>0, (7) check 0+ and ∞. Skip a step only if the problem is source-free first-order, in which the exponential method is shorter—but Laplace still works and is a good check. If step 7 fails, the usual bug is the polarity of V0/s or treating L I0 as a time-domain battery that remains after t=0 instead of an s-domain bookkeeping term. Re-draw the s-circuit and restate 0− values in a margin box before algebra.

## Equations

Relaxed: \( Z_L(s) = sL \), \( Z_C(s) = 1/(sC) \), \( Z_R = R \).

Capacitor IC (0−): series with C: \( V_0/s \); or parallel current source \( C V_0 \).

Inductor IC (0−): series voltage source \( L I_0 \); or parallel current \( I_0/s \).

Derivative: \( \mathcal{L}\{f'(t)\} = s F(s) - f(0^-) \).

Final value: \( \lim_{t\to\infty} f(t) = \lim_{s\to 0} s F(s) \) if poles of sF are in the left half-plane.

Initial value: \( f(0^+) = \lim_{s\to\infty} s F(s) \).

Inverse: \( F(s) = \sum \frac{r_k}{s-p_k} \ \to\ \sum r_k e^{p_k t} u(t) \).

## Methods

Draw the t>0 schematic. Replace L, C by Z(s) plus IC sources from 0−. Transform independent sources (step, sinusoid, exponential). Solve for the requested transform. Partial-fraction invert. Check f(0+) against circuit continuity and f(∞) against DC analysis (C open, L short).

For a sinusoid, the particular solution can be left as the imaginary-axis poles of the source, plus transients from circuit poles. Do not use phasors until transients are declared dead.

Design: place poles by choosing R, L, C as in second-order transients, then use H(s) to shape zeros (series C for high-pass, etc.).

A partial-fraction checklist: is F(s) proper? If not, divide. Factor the denominator over the reals. Cover-up each simple real pole. For a quadratic s² + 2αs + ω0², write (as+b)/(quadratic) and match a, b from coefficients, invert to e^{−αt} sinusoid. Apply IVT and FVT. If FVT says 12 V and DC analysis says 12 V, the constant term in the expansion is right. If IVT says 8 V and the capacitor was at 8 V, the high-s expansion is right. Those two checks catch most algebra bugs before a tutor does. Keep u(t) in the inverse if the problem is picky about t<0 being zero. Do not invert terms from IC sources as extra time-domain batteries that stay forever unless they really are 1/s terms.

## Mistakes

Dropping IC sources. Using 1/sC but also adding V0/s with the wrong polarity (the voltage source plus should be the plus of V0 on the capacitor). Mixing 0+ and 0− in the derivative rule. Inverse Laplace forgetting u(t). Applying the final-value theorem to an undamped sinusoid. Canceling a pole that is still needed for another output, then claiming the circuit is first-order. Using jω impedances in an s-domain diagram. Partial fractions with a repeated pole using only 1/(s-p) and omitting 1/(s-p)^2. Sign error on L I0: the source polarity is that of a voltage drop in the direction of I0 (passive). Writing ZC = sC. Inverting 1/(s+3)(s+5) as e^{−3t}+e^{−5t} without residues 1/2 and −1/2. Dropping u(t) and then using the expression for t<0. Applying FVT to a right-half-plane pole. Using phasor jωL in the same drawing as 1/sC. Forgetting to transform a switched source: a DC source that was always there is V/s only for the unilateral t>0 model if we use 0− IC; if the source was already on for t<0, it belongs in the 0− analysis, not as an extra V/s at t=0. Double-counting that source is a common Laplace error. Another: treating C v(0) current-source model and V0/s series model as additive rather than alternative. Pick one IC model per element. Check with a first-order RC you already know: VC(s) must invert to the exponential you could have written in unit 06. If it does not, stop; do not proceed to a second-order inverse. The same check applies to RL: I(s) = I0/(s+R/L) must invert to I0 e^{−(R/L)t}. Those two templates validate the IC source polarity before any heroic residue algebra. A third template is the switched DC series RC charging from zero: VC(s) = (Vs/s)(1/RC)/(s+1/RC), which inverts to Vs(1−e^{−t/RC}). If your s-circuit with V0=0 does not reduce to that, the divider in s is wrong. Fix the s-circuit before inverting anything else. A wrong IC polarity cannot be repaired by a clever residue. Redraw the entire s-domain circuit carefully, then invert.

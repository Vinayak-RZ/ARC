# Laplace transforms

The (unilateral) Laplace transform is the default algebraic method for linear lumped circuits with switches, for classical control transfer functions, and for solving constant-coefficient ODEs with initial conditions built in. This unit is the transform as mathematics used in those courses: definition, region of convergence for the unilateral case, a working table, operational theorems, inverse by partial fractions, and the initial- and final-value theorems. Network topology and impedance in \(s\) is a circuits unit; here \(F(s)\) is a function of a complex variable, inverted by algebra plus the inversion integral mentioned only so that residues (unit 10) have a place to land.

Bilateral Laplace and a full ROC discussion belong with signals courses when two-sided signals appear. UG EE circuit analysis almost always uses the unilateral transform
\[
F(s)=\int_{0^-}^\infty f(t)e^{-st}\,dt,
\]
the lower limit \(0^-\) so that impulses at the origin and initial-condition jumps are captured.

## Concepts

The transform converts differentiation in \(t\) into multiplication by \(s\), minus initial-condition polynomials. Integration in \(t\) becomes division by \(s\). Convolution of causal signals becomes a product of transforms. That is the entire reason to learn the table: linear ODEs become linear algebraic equations in \(s\). After solving for \(Y(s)\), invert.

The complex variable is \(s=\sigma+j\omega\). For a causal exponential \(e^{at}u(t)\), the integral converges when \(\operatorname{Re}(s)>a\) (more precisely \(\operatorname{Re}(s)>\operatorname{Re}(a)\)). Unilateral transforms of the standard UG table (steps, ramps, damped sinusoids, finite-order polynomials times exponentials) are rational functions. A rational \(F(s)=N(s)/D(s)\) in lowest terms has poles where \(D=0\) and zeros where \(N=0\). Properness (\(deg N < deg D\)) is required for a strictly proper system function mapping a Laplace-transformable input to an output without a delta in \(h(t)\); improper functions correspond to differentiators or through terms.

Partial-fraction inversion is the workhorse. Distinct poles: \(F(s)=\sum K_i/(s-p_i)\), each term inverting to \(K_i e^{p_i t}u(t)\). Complex conjugate poles are kept as a quadratic factor and inverted as a damped sinusoid, or split into complex residues and combined at the end. Repeated poles produce terms \(t^{m-1}e^{pt}/(m-1)!\) from \(1/(s-p)^m\). If \(F(s)\) is improper, first polynomial-divide; the polynomial in \(s\) inverts to impulses and derivatives of impulses at \(t=0\).

Operational theorems worth living with: linearity; time shift \(f(t-t_0)u(t-t_0)\leftrightarrow e^{-s t_0}F(s)\) for \(t_0>0\); frequency shift \(e^{-at}f(t)\leftrightarrow F(s+a)\); scaling \(f(at)\leftrightarrow (1/a)F(s/a)\) for \(a>0\); differentiation \(f'(t)\leftrightarrow sF(s)-f(0^-)\); second derivative \(s^2 F(s)-sf(0^-)-f'(0^-)\); integration \(\int_{0^-}^t f\leftrightarrow F(s)/s\); multiplication by \(t\) is \(-dF/ds\); convolution \(f*g\leftrightarrow F(s)G(s)\) for causal convolution on \([0,\infty)\).

The initial-value theorem \(f(0^+)=\lim_{s\to\infty}sF(s)\) (under standard hypotheses: \(F\) strictly proper, no impulsive part) and the final-value theorem \(f(\infty)=\lim_{s\to 0}sF(s)\) (only if all poles of \(sF(s)\) lie in the open left half-plane, except possibly a simple pole at \(s=0\)) are used constantly to check inversion. The final-value theorem does **not** apply to undamped sinusoids or to unstable poles. Applying it to \(\omega/(s^2+\omega^2)\) falsely predicts a final value of 0, while \(\sin\omega t\) has no final value.

Transfer functions in control are ratios \(G(s)=Y(s)/U(s)\) at zero initial conditions. The same \(G(s)\) is the Laplace transform of the impulse response. Poles of \(G\) are the characteristic roots of the ODE. Zeros affect the shape of the transient and the residue sizes, not the natural frequencies (unless cancellation). Cancellation of a right-half-plane pole by a zero is not a physical deletion of that mode if the cancelled mode is still in the state; that is a later control warning. Mathematically, a cancelled factor is gone from the reduced rational function.

The convolution theorem is how a circuit with impulse response \(h(t)\) and input \(u(t)\) produces \(y=h*u\) without an integral if you stay in \(s\). Inverse Laplace of a product is the convolution; sometimes the integral in \(t\) is easier, sometimes the partial fractions of the product are easier. Choose.

Multivalued functions \(\sqrt{s}\) and \(\ln s\) appear in distributed-parameter and fractional models; UG lumped EE stays rational. Delay \(e^{-sT}\) is transcendental and appears in transport lags and in ideal sampled-data with a hold. Inverse of \(e^{-sT}F(s)\) is a shifted \(f(t-T)u(t-T)\). Do not series-expand \(e^{-sT}\) and invert term by term unless you know you want an infinite impulse train.

Units: if \(f(t)\) is volts, \(F(s)\) has units volt-seconds (because of \(dt\)). Engineers usually omit the units on \(F(s)\) and keep them on time functions. The variable \(s\) has units of inverse seconds. Writing a transfer function \(1/(2s+3)\) without stating whether the \(2\) is \(2\ \mathrm{s}\) is a modelling omission.

The inversion integral
\[
f(t)=\frac{1}{2\pi j}\int_{\gamma-j\infty}^{\gamma+j\infty} F(s)e^{st}\,ds
\]
along a vertical Bromwich line to the right of all poles, closed in the left half-plane for \(t>0\), is evaluated by residues (unit 10). For rational \(F\), residues reproduce partial fractions. That is why the two units sit in the same pack.

## Equations

Definition (unilateral, \(0^-\)):

\[
F(s)=\mathcal{L}\{f\}(s)=\int_{0^-}^\infty f(t)e^{-st}\,dt.
\]

Elementary pairs (\(t\ge 0\), \(u(t)\) the unit step, \(\delta\) the Dirac impulse):

\[
\mathcal{L}\{\delta(t)\}=1,\qquad \mathcal{L}\{u(t)\}=\frac{1}{s},\qquad \mathcal{L}\{t^n u(t)\}=\frac{n!}{s^{n+1}},
\]
\[
\mathcal{L}\{e^{-at}u(t)\}=\frac{1}{s+a},\qquad \mathcal{L}\{\cos\omega t\, u(t)\}=\frac{s}{s^2+\omega^2},\qquad \mathcal{L}\{\sin\omega t\, u(t)\}=\frac{\omega}{s^2+\omega^2},
\]
\[
\mathcal{L}\{e^{-at}\cos\omega t\, u(t)\}=\frac{s+a}{(s+a)^2+\omega^2},\qquad \mathcal{L}\{e^{-at}\sin\omega t\, u(t)\}=\frac{\omega}{(s+a)^2+\omega^2}.
\]

Differentiation and shift:

\[
\mathcal{L}\{f'(t)\}=sF(s)-f(0^-),\qquad \mathcal{L}\{f(t-t_0)u(t-t_0)\}=e^{-st_0}F(s)\ (t_0>0).
\]

Initial and final value (hypotheses as in Concepts):

\[
f(0^+)=\lim_{s\to\infty}sF(s),\qquad f(\infty)=\lim_{s\to 0}sF(s).
\]

Partial fractions, simple poles:

\[
F(s)=\sum_i\frac{K_i}{s-p_i},\qquad K_i=(s-p_i)F(s)\big|_{s=p_i}.
\]

Repeated pole of order 2 at \(p\):

\[
\frac{A}{(s-p)^2}+\frac{B}{s-p},\qquad A=(s-p)^2 F(s)\big|_{s=p},\quad B=\frac{d}{ds}\big[(s-p)^2 F(s)\big]_{s=p}.
\]

Convolution (causal):

\[
\mathcal{L}\{(f*g)(t)\}=F(s)G(s),\qquad (f*g)(t)=\int_{0^-}^t f(\tau)g(t-\tau)\,d\tau.
\]

## Methods

Confirm the problem is unilateral: known \(f(t)\) for \(t>0\), initial conditions at \(0^-\), or a transfer function at rest. Transform the ODE or the integro-differential circuit equations term by term. Replace each capacitor by \(1/sC\) in series with a voltage source \(v_C(0^-)/s\), or use the parallel current-source model \(C v_C(0^-)\); replace each inductor by \(sL\) in series with \(-L i_L(0^-)\). Solve the algebraic network for the desired \(F(s)\).

Before inverting, factor the denominator completely over the reals (linear and irreducible quadratic factors). If \(\deg N\ge \deg D\), divide. Perform partial fractions. For a quadratic \(s^2+2\zeta\omega_n s+\omega_n^2\), complete the square to \((s+\zeta\omega_n)^2+\omega_d^2\) and match the damped-sine and damped-cosine table rows. Do not invent new table entries if a shift \(F(s+a)\) plus a standard pair will do.

Cover-up for simple poles: multiply by \((s-p)\) and set \(s=p\). For a quadratic factor kept intact, equate coefficients after clearing the denominator, or use complex cover-up at \(s=-\zeta\omega_n+j\omega_d\) and convert the pair of complex residues into a real amplitude and phase:
\[
\frac{Ke^{j\phi}}{s-(\alpha+j\omega)}+\frac{Ke^{-j\phi}}{s-(\alpha-j\omega)}\ \longleftrightarrow\ 2Ke^{\alpha t}\cos(\omega t+\phi)\,u(t).
\]

Apply the initial-value theorem to the solved \(Y(s)\) and compare with the circuit’s \(y(0^+)\). Apply the final-value theorem only after checking pole locations of \(sY(s)\). If the theorem is illegal, say so; do not write \(y(\infty)=0\) for a sustained oscillator.

When a delay \(e^{-sT}\) multiplies a rational function, invert the rational part and then shift. When two delays appear (piecewise sources), split \(F(s)\) into groups each with one exponential factor.

To invert \(1/(s(s+a))\) quickly, write \(\frac{1}{a}(1/s-1/(s+a))\) rather than running a general residue machine. Build a personal short table of those pairs that appear in RC and RL steps.

If inversion looks messy, differentiate a simpler pair: multiplication by \(t\) is \(-d/ds\). Example: \(\mathcal{L}\{t e^{-at}\}=1/(s+a)^2\).

A switched circuit with a piecewise source (pulse of duration \(T\)) is \(V(s)=(1-e^{-sT})/s\) times a DC gain. Invert the step response and subtract the same waveform delayed by \(T\). Do not expand \(e^{-sT}\) as \(1-sT+\cdots\) and invert the truncation unless a short-time series is the stated goal; the exact inverse is the delayed pair.

When several initial-condition sources appear (each capacitor and inductor), keep them on the diagram until \(Y(s)\) is written, then collect numerator polynomials. Dropping one \(Cv_C(0^-)\) source is the usual missing-term bug in a second-order inversion. After inverting, check \(v_C(0^+)\) and \(i_L(0^+)\) against the given \(0^-\) values when no impulse is present: they must match.

## Mistakes

Using \(f(0^+)\) in the differentiation theorem. The theorem uses \(f(0^-)\). After a switch, \(0^-\) and \(0^+\) differ for some variables (not for capacitor voltage or inductor current in the non-impulse case). Mixing them double-counts or drops the initial-condition source.

Applying the final-value theorem to \(s/(s^2+\omega^2)\) or to a right-half-plane pole and reporting a finite limit that does not exist.

Forgetting to polynomial-divide an improper \(F(s)\). Partial fractions on an improper function are incomplete; the inverse misses \(\delta(t)\) or \(\delta'(t)\).

Writing \(\mathcal{L}\{\cos\omega t\}=\omega/(s^2+\omega^2)\) (that is sine). Cosine has \(s\) in the numerator.

Dropping \(u(t)\) and then shifting. The pair \(f(t-t_0)u(t-t_0)\) is not \(f(t-t_0)\) without the window; a cosine that existed for negative time does not transform unilaterally to the two-sided formula.

Using bilateral ROC language on a unilateral circuit problem, or marking a pole to the right of a Bromwich line that was never drawn. For unilateral causal signals of exponential type, invert with the causal table and \(u(t)\).

Sign error in the frequency-shift theorem: \(e^{-at}f(t)\) maps to \(F(s+a)\), so a damping \(e^{-3t}\) replaces \(s\) by \(s+3\), moving poles left.

Cover-up at a repeated pole as if it were simple. The residue of \(1/(s-p)^2\) is not the cover-up number \(A\) of the \(1/(s-p)^2\) term alone; there is also a \(B/(s-p)\) term from the derivative.

Cancelling \((s+2)\) in a transfer function and then using initial conditions that still excite that mode in an unreduced state model. Reduced \(G(s)\) hides unobservable/uncontrollable modes.

Units of \(s\) in Bode plots later: writing \(\omega=10\) without rad/s, then using \(s=j10\) in a polynomial with coefficients that were fitted in different units.

Inverting \(e^{-2s}/(s+1)\) as \(e^{-2t}e^{-t}\). The delay multiplies in \(s\), it does not add to the time constant in that way. Correct: \(e^{-(t-2)}u(t-2)\).

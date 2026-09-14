# Describing function and limit cycles intro

Nonlinear UG control in a first course is mostly one idea: a memoryless nonlinearity in an otherwise linear loop can be replaced, for nearly sinusoidal motions, by an amplitude-dependent complex gain \(N(A)\) — the describing function (DF). Intersection of \(-1/N(A)\) with the Nyquist plot of the linear \(L(j\omega)\) predicts a periodic oscillation (limit cycle) and gives a first stability heuristic. This unit is that prediction for saturation, relay, and dead zone, and the Loeb/Nyquist graphical stability rule — not Lyapunov theory beyond a one-line mention, and not chaos.

## Concepts

A true LTI Nyquist plot cannot enclose a stable isolated periodic orbit: linear systems oscillate only from \(j\omega\) eigenvalues, with amplitude set by initials, not by a unique attracting cycle. Limit cycles need a nonlinearity. Van der Pol, a relay servo, and a saturated oscillator are the standard pictures. UG analysis uses harmonic balance, not a full Poincaré map.

Assume the loop signal into the nonlinearity is \(x(t)=A\sin\omega t\), and the nonlinearity \(n(\cdot)\) is odd, memoryless, and time-invariant. Expand \(n(x(t))\) in a Fourier series; keep the fundamental
\[
n(x(t))\approx a_1\cos\omega t+b_1\sin\omega t.
\]
The describing function is the complex ratio of that fundamental to the input phasor,
\[
N(A)=\frac{b_1+ja_1}{A}
\]
(with conventions matching \(\sin\) as the reference). For odd memoryless \(n\), \(N(A)\) is real: \(a_1=0\),
\[
N(A)=\frac{2}{\pi A}\int_0^\pi n(A\sin\theta)\sin\theta\,d\theta.
\]
The linear remainder of the loop is \(L(s)\). Harmonic balance at the switching point of the nonlinearity says
\[
1+N(A)L(j\omega)=0\qquad\Leftrightarrow\qquad L(j\omega)=-\frac{1}{N(A)}.
\]
Graphically: plot \(L(j\omega)\) (Nyquist) and the locus of \(-1/N(A)\) as \(A\) goes from 0 to \(\infty\). Intersections \((\omega,A)\) are predicted limit cycles.

Saturation at levels \(\pm M\) with unit slope in the linear region (or slope \(k\)): for \(A\le M\), \(N(A)=k\) (or 1). For \(A>M\),
\[
N(A)=\frac{2k}{\pi}\bigl(\sin^{-1}\tfrac{M}{A}+\tfrac{M}{A}\sqrt{1-(M/A)^2}\bigr)
\]
which falls as \(1/A\) for large \(A\). Thus \(-1/N(A)\) starts at \(-1/k\) and runs out the negative real axis to \(-\infty\).

Ideal relay (\(\pm M\) with no dead zone): \(N(A)=4M/(\pi A)\), real. \(-1/N=-(\pi A)/(4M)\) covers the whole negative real axis as \(A\) varies. A relay servo with a type-1 plant that already crosses the negative real axis will oscillate; the crossing frequency is \(\omega\) from \(L(j\omega)\), and \(A\) from \(|L|=1/N(A)\).

Relay with hysteresis is not memoryless; \(N(A)\) is complex, and \(-1/N\) is a line off the real axis. Dead zone (no output for \(|x|<\delta\)) has \(N(0)=0\) and a peak \(N\); \(-1/N\) covers a bounded real segment.

Stability of the predicted cycle (Loeb / graphical): if as \(A\) increases through the intersection, the \(-1/N\) locus goes from the “stable side” of \(L(j\omega)\) to the unstable side (the side that would be encircled in the linear Nyquist sense), the cycle is often unstable (a jump away). The opposite is a stable cycle. For the common case \(P=0\), \(L\) crossing the negative real axis once, and saturation’s \(-1/N\) running left along that axis: the intersection is a stable limit cycle if increasing \(A\) moves \(-1/N\) further left, outside the encirclement — the usual saturated oscillator. Treat the rule as a heuristic; confirm by simulation when the plot is complicated.

Filtering hypothesis: \(L(j\omega)\) must attenuate higher harmonics (low-pass plant, relative degree \(\ge 1\), preferably 2). A DF prediction on a wideband plant with a sharp nonlinearity can be quantitatively wrong. Relays plus double integrators are the textbook-friendly case.

Jump resonance and multiple intersections: a cubic nonlinearity plus a lightly damped \(L\) can give three intersections, two stable amplitudes with hysteresis as frequency is swept. UG should recognize multiple crossings, not compute Duffing charts.

Lyapunov: a first course may state that V-functions can prove global stability of the origin for some nonlinear loops (Lur’e, circle criterion) without predicting oscillation amplitude. DF does the opposite: it predicts oscillation and does not prove anything global. The circle criterion is a sufficient Nyquist condition using a sector \([k_1,k_2]\) instead of \(N(A)\). Mention it; do not examine it as a full method here.

Do not linearize a relay as “gain \(\infty\)” and then apply Routh: that is the other extreme from DF, and it misses the finite amplitude.

## Equations

DF (odd, memoryless):
\[
N(A)=\frac{2}{\pi A}\int_0^\pi n(A\sin\theta)\sin\theta\,d\theta.
\]
Ideal relay \(\pm M\):
\[
N(A)=\frac{4M}{\pi A}.
\]
Saturation (slope 1, level \(M\)), \(A\ge M\):
\[
N(A)=\frac{2}{\pi}\left(\sin^{-1}\frac{M}{A}+\frac{M}{A}\sqrt{1-\frac{M^2}{A^2}}\right).
\]
Balance:
\[
L(j\omega)=-\frac{1}{N(A)}.
\]
Relay amplitude at a real-axis crossing \(L(j\omega_u)=-r\), \(r>0\):
\[
\frac{\pi A}{4M}=r\qquad\Rightarrow\qquad A=\frac{4M r}{\pi}.
\]
(If \(L(j\omega_u)=-r\), then \(-1/N=-r\) ⇒ \(N=1/r=4M/(\pi A)\).)

## Methods

Identify the nonlinearity and list \(N(A)\) from a table or the integral. Sketch \(-1/N(A)\) in the polar plane (usually a piece of the negative real axis). Sketch \(L(j\omega)\). Read intersections. At each, get \(\omega\) from the \(L\) parameterization and \(A\) from \(N(A)= -1/L\). Apply the graphical stability heuristic. State the filtering assumption.

For a relay plus \(L(s)=K/[s(s+a)]\), \(\mathrm{Im}\,L=0\) never happens at finite \(\omega\neq 0\) except at \(\omega=\infty\) where \(L=0\); there may be no intersection and no DF cycle (the linearization at small \(A\) has infinite gain and the type-1 loop is marginally... actually infinite-gain relay around \(1/[s(s+a)]\) is a famous oscillator? \(N L = [4M/(\pi A)] K/[s(s+a)]= -1\). That requires \(L\) negative real. \(L(j\omega)=K/[j\omega(j\omega+a)]=-K\omega^2/(\omega^2(\omega^2+a^2))-j \cdots\) wait \(1/[j\omega(a+j\omega)]=(a+j\omega)^{-1}(-j/\omega)\). Real part: compute \(L(j\omega)=K/[j\omega a-\omega^2]=K/(-\omega^2+j a\omega)\). Multiply by conjugate: \(K(-\omega^2-j a\omega)/(\omega^4+a^2\omega^2)\). Real part \(=-K/(\omega^2+a^2)<0\) for all \(\omega\). Imaginary part \(=-K a/[\omega(\omega^2+a^2)]\neq 0\) except \(\omega\to\infty\). So \(L\) never crosses the negative real axis at finite \(\omega\); DF predicts no intersection except \(A\to\infty,\omega\to\infty\). A relay with a double integrator \(K/s^2\) does: \(L(j\omega)=-K/\omega^2\), purely negative real, intersection at every \(\omega\) matching \(K/\omega^2=\pi A/(4M)\). Frequency and amplitude are linked by one equation; need another (e.g. specified \(K\)) — actually infinitely many \(\omega\) satisfy if \(A\) can adjust: for each \(\omega\), \(A=4M K/(\pi\omega^2)\). That would suggest a continuum, which means the filtering/DF hypotheses are degenerate (the linear part is not strictly low-pass in a way that selects one harmonic). Prefer \(K/[s(s+a)(s+b)]\), which has a single negative-real crossing (Routh), hence a unique DF prediction.

Recipe for exam plants: compute the linear \(j\omega\) crossing as in Routh/Nyquist, then get \(A\) from \(N(A)\).

If no intersection, DF predicts no limit cycle (the origin may be globally attracting, or a more exotic motion may exist — DF is silent).

## Mistakes

Using small-signal linearization of a relay (slope infinite or zero) and quoting Routh as the oscillation condition without amplitude.

Plotting \(N(A)\) instead of \(-1/N(A)\) on the Nyquist paper.

Forgetting that \(N\) for saturation is constant for \(A\) below the knee, so \(-1/N\) starts at \(-1\), not at 0.

Applying DF to an even nonlinearity (rectifier) without a DC term; the odd assumption failed.

Trusting DF on a relative-degree-zero loop that does not filter the square wave from a relay.

Confusing orbital stability of a cycle with Hurwitz stability of the origin. Both can appear on the same diagram: small \(A\) may be an unstable equilibrium, large \(A\) a stable cycle.

Using \(\omega\) from the linear \(K_u\) of a *proportional* gain when the nonlinearity’s \(N(A)\) is not that gain: the frequency at intersection is where \(L(j\omega)\) hits \(-1/N(A)\), which for real \(N\) is still the same \(\omega_u\) as a gain-varying linear loop, with \(K_{\mathrm{eq}}=N(A)\). That part is OK; the mistake is to insert \(K_u\) from a different plant.

Reporting the relay output amplitude \(M\) as the limit-cycle amplitude of the input to the relay. \(A\) is the input amplitude.

Ignoring units: \(N(A)\) has units of the incremental gain (output/input of the nonlinearity).

A complete relay+type-1 third-order numerical, matching the Routh story. Plant \(L(s)=K/[s(s+1)(s+2)]\) with a fixed \(K=4\), relay \(\pm 1\) in front (so the linear plot is \(4 G_0\) and the DF gain \(N=4/(\pi A)\) multiplies it). Negative-real crossing of \(G_0=1/[s(s+1)(s+2)]\) occurs at \(\omega=\sqrt{2}\), \(|G_0|=1/6\) in the sense that \(K_u=6\) for \(1+K G_0=0\), i.e. \(G_0(j\sqrt{2})=-1/6\). Then \(L(j\sqrt{2})=4\times(-1/6)=-2/3\). Balance \(L=-1/N\) ⇒ \(N=3/2=4/(\pi A)\) ⇒ \(A=8/(3\pi)=0.849\). Predicted cycle: frequency \(1.414\,\mathrm{rad/s}\), relay-input amplitude 0.85. Graphical stability: \(-1/N=-(\pi A)/4\) runs from \(0^-\) (tiny \(A\), huge \(N\)) out to \(-\infty\) (large \(A\)). Increasing \(A\) moves the point left. At the intersection \(-2/3\), moving left goes *away* from the origin along the negative real axis, typically out of the region that the linear Nyquist would count as “inside” for \(P=0\) if the critical point were that far left — the standard conclusion is a *stable* limit cycle. Small signals (\(A\to 0\)) see infinite relay gain, which for this plant is past \(K_u=6\) (since \(K_{\mathrm{eq}}=K N\to\infty\)), hence locally unstable origin; trajectories grow until the DF cycle. That is the textbook relay servo: chatter at a well-defined frequency, not unbounded runaway, provided the plant rolls off.

Saturation instead of a relay: \(N(A)\le k\), so \(-1/N\) only exists on \((-\infty,-1/k]\). If the Nyquist of \(L\) crosses the negative real axis at \(-0.4\) and \(k=1\), then \(-1/k=-1\) is left of \(-0.4\): no intersection, and the linear gain \(k\) already has GM \(=1/0.4>1\), so the origin is locally stable and DF predicts no cycle. If the crossing is at \(-1.5\), linear GM is negative, origin unstable, and \(-1/N\) will meet \(L\) at some \(A>M\), a stable saturation cycle (the actuator slams the rails every period). That is “the loop is unstable until the amp clips, then it sings at \(\omega_u\).” Hardware engineers know this as an unintended oscillator after a gain increase.

Dead zone: small signals see \(N=0\), the loop is open, a small bias can sit in the zone (sticktion, valve overlap). Large signals see \(N\) approaching the slope outside the zone. If that slope would have been unstable, there can be a jump into a cycle once a disturbance pushes \(A\) past a threshold — two intersections, one unstable (the threshold) and one stable (the cycle). Hunting in old process controllers with valve dead band is this picture.

Hysteresis relay (width \(h\), height \(M\)):
\[
N(A)=\frac{4M}{\pi A}\sqrt{1-(h/A)^2}-j\frac{4Mh}{\pi A^2},\qquad A\ge h.
\]
The imaginary part shifts \(-1/N\) off the real axis to a line \(\mathrm{Re}=- \pi h/(4M)\) (a vertical line). Intersection with \(L(j\omega)\) is no longer forced to be a real-axis crossing of \(L\); frequency shifts. On-off thermostats with hysteresis are designed this way on purpose: the cycle amplitude and frequency are the specification, not a bug.

When DF fails: a plant with a sharp resonance and a saturation can produce almost-periodic beating, not a single sinusoid; the fundamental-only balance is incomplete. A relay with delay can chatter at very high frequency (the delay’s spiral provides many intersections); the lowest-\(\omega\) stable intersection is the one the loop usually sits on, but startup transients can lock to another. Report DF as a prediction, then simulate one cycle of \(x(t)\) if the course allows a computer. Without a computer, stick to plants that are strictly proper of relative degree \(\ge 2\) and a single real-axis crossing.

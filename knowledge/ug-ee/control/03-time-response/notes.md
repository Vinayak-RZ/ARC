# First- and second-order time response, error constants

Transient specs and steady-state error are how a UG course grades a closed-loop design before Bode or root locus ever appear. First-order lags have one number \(\tau\). Second-order prototypes have \(\zeta\) and \(\omega_n\), and a short list of formulas for overshoot, peak time, and settling. Type number and position/velocity/acceleration constants \(K_p,K_v,K_a\) turn the final-value theorem into a table of step/ramp/parabola errors. This unit is those formulas, their hypotheses (dominant pair, unity feedback, standard-form numerator), and the ways they are misapplied to zeros, to type 0 ramps, and to non-unity \(H\).

## Concepts

A first-order plant or closed loop \(Y/R=a/(s+a)\) with \(a>0\) has time constant \(\tau=1/a\). Unit-step response: \(y(t)=1-e^{-t/\tau}\) for \(t\ge 0\). Rise time 10–90% is about \(2.2\tau\). Settling to 2% is about \(4\tau\); to 5% about \(3\tau\). There is no overshoot. DC gain is 1 in this prototype; a general \(K/(s+a)\) steps to \(K/a\). Bandwidth (–3 dB) of \(a/(s+a)\) is \(a\) rad/s. Faster poles (larger \(a\)) track better and reject constant disturbances better in a 1-dof loop with more gain, but they need more actuator effort.

A prototype second-order underdamped closed loop is
\[
T(s)=\frac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2},\qquad 0<\zeta<1.
\]
Poles at \(-\zeta\omega_n\pm j\omega_d\) with \(\omega_d=\omega_n\sqrt{1-\zeta^2}\). Unit-step response:
\[
y(t)=1-\frac{e^{-\zeta\omega_n t}}{\sqrt{1-\zeta^2}}\sin(\omega_d t+\phi),\qquad \phi=\arccos\zeta=\tan^{-1}\frac{\sqrt{1-\zeta^2}}{\zeta}.
\]
Peak time \(t_p=\pi/\omega_d\). Percent overshoot
\[
\mathrm{PO}=100\exp\left(\frac{-\zeta\pi}{\sqrt{1-\zeta^2}}\right)
\]
depends on \(\zeta\) only. Settling time to 2%: \(t_s\approx 4/(\zeta\omega_n)\) (the real-part envelope). Rise time 0–100% is approximately \(1.8/\omega_n\) for \(\zeta\approx 0.5\), but the accurate 10–90% needs a chart; exams that want a number usually want \(t_p\) or \(t_s\) or PO. Delay time to 50% is roughly \(1.1/\omega_n\) at \(\zeta=0.7\).

Damping regions: \(\zeta>1\) overdamped (two real poles), \(\zeta=1\) critical, \(0<\zeta<1\) underdamped, \(\zeta=0\) undamped sinusoid, \(\zeta<0\) unstable. A closed-loop pair with \(\zeta=0.7\) is the usual analog of “a bit of overshoot, fast settle.” \(\zeta=0.4\) rings; \(\zeta=1\) is sluggish for the same \(\omega_n\).

Zeros and extra poles. A zero in \(T(s)\) (from a PD controller or a plant zero) increases overshoot relative to the prototype of the same poles. A third real pole to the left of the pair, several times \(\zeta\omega_n\) away, is “dominant-pair” neglected. If the third pole is not fast, the PO formula lies. A RHP zero (non-minimum phase) undershoots first. Never apply the PO formula to \(T(s)=(2s+1)\omega_n^2/(\cdots)\) without comment.

Type number of a unity-feedback loop is the number of open-loop integrators in \(L(s)=G_c G H\), i.e. the multiplicity of \(s=0\) in the denominator of \(L\). Type 0: finite DC open-loop gain, nonzero step error. Type 1: zero step error, finite ramp error. Type 2: zero step and ramp error, finite parabola error. Higher types are rare and expensive (phase lag at every frequency).

Static error constants, unity negative feedback, standard \(L(s)\):
\[
K_p=\lim_{s\to 0}L(s),\qquad
K_v=\lim_{s\to 0}s L(s),\qquad
K_a=\lim_{s\to 0}s^2 L(s).
\]
Unit-step error \(e_{ss}=1/(1+K_p)\) (type 0) or 0 (type \(\ge 1\)). Unit-ramp error \(e_{ss}=1/K_v\) (type 1) or 0 (type \(\ge 2\)) or \(\infty\) (type 0). Unit-parabola \(t^2/2\) error \(e_{ss}=1/K_a\) (type 2). These are final-value theorem applications to \(E(s)=S(s)R(s)\) with \(S=1/(1+L)\), and they require that the closed loop be stable. An unstable loop has no \(e_{ss}\) of this kind; Routh first.

Non-unity \(H\) changes the interpretation of \(e=r-y\) versus \(e=r-Hy\). If the problem defines error as \(r-y\) but the loop is \(H\neq 1\), the step error is not \(1/(1+K_p)\) with \(K_p=\lim L\). Reduce to an equivalent unity-feedback plant or write \(Y=T R\) and \(e_{ss}=\lim(r-y)\).

Disturbance errors: a constant load at the plant input of a type-1 speed loop may still produce zero steady speed error; a type-0 loop will not. Use \(Y=G_{\mathrm{yd}}D\) and final-value, not the \(K_v\) table blindly.

Ramp inputs of slope \(A\) scale the unit-ramp error by \(A\). Specs such as “less than 0.01 rad lag at 2 rad/s slew” are \(A/K_v\le 0.01\) with \(A=2\).

Dominant-pole design: place a closed-loop pair for PO and \(t_s\), then hope other poles are left. A zero of the controller used to cancel a plant pole removes that mode from \(T\) but not from disturbance TFs if the cancellation is in \(G_c G\) the wrong way. Cancellation of unstable plant poles is not a method.

## Equations

First order \(T=1/(\tau s+1)\):
\[
y_{\mathrm{step}}(t)=1-e^{-t/\tau},\qquad t_{s,2\%}\approx 4\tau,\qquad \omega_{bw}=1/\tau.
\]

Second order underdamped:
\[
\omega_d=\omega_n\sqrt{1-\zeta^2},\qquad t_p=\frac{\pi}{\omega_d},\qquad t_{s,2\%}\approx\frac{4}{\zeta\omega_n},
\]
\[
\mathrm{PO}=100\exp\left(\frac{-\zeta\pi}{\sqrt{1-\zeta^2}}\right).
\]
Real part \(\sigma=\zeta\omega_n\). Pole angle from the negative real axis: \(\theta=\cos^{-1}\zeta\).

Error constants (unity feedback, stable closed loop):
\[
e_{\mathrm{step}}=\frac{1}{1+K_p},\quad
e_{\mathrm{ramp}}=\frac{1}{K_v},\quad
e_{\mathrm{parab}}=\frac{1}{K_a}.
\]

Final-value theorem (poles of \(sF(s)\) in open LHP):
\[
\lim_{t\to\infty}f(t)=\lim_{s\to 0}s F(s).
\]

Standard second-order from \(L=K/(s(s+a))\): \(\omega_n=\sqrt{K}\), \(2\zeta\omega_n=a\), so \(\zeta=a/(2\sqrt{K})\).

## Methods

Identify whether the given \(T(s)\) is prototype form. If the numerator is not \(\omega_n^2\), factor out DC gain, then decide whether a zero is present. Extract \(\omega_n\) from \(\sqrt{\text{const term}}\) of the monic den, and \(\zeta\) from the \(s\) coefficient via \(2\zeta\omega_n\).

To meet PO and \(t_s\): from PO get \(\zeta\) (solve or memorize: PO 16% ⇒ \(\zeta\approx 0.5\); PO 5% ⇒ \(\zeta\approx 0.7\); PO 1% ⇒ \(\zeta\approx 0.83\)). Then \(\sigma=\zeta\omega_n=4/t_s\) for 2% settle, hence \(\omega_n=\sigma/\zeta\). Place the pair at \(-\sigma\pm j\sigma\tan(\arccos\zeta)\).

Error-constant recipe: write \(L(s)\) as a rational, count integrators (type). Take the matching limit \(K_p,K_v,\) or \(K_a\). Confirm closed-loop stability (Routh on \(1+L=0\)) before quoting \(e_{ss}\). Scale by input amplitude/slope.

If \(H\neq 1\), form \(T=G/(1+GH)\) and \(e_{ss}=\lim_{s\to 0}s(1-T)R(s)\) for error \(r-y\).

First-order measurement: fit \(\tau\) from a step test as the time to 63% of final, or from the slope at the origin of a first-order step (\(1/\tau\)). Second-order: measure PO and \(t_p\), invert the formulas for \(\zeta,\omega_n\).

When the plant is type 1 and the controller is proportional \(K\), \(K_v=K\lim sG\) and ramp error is \(1/K_v\). Increasing \(K\) reduces ramp error and reduces \(\zeta\) for \(L=K/(s(s+a))\), increasing overshoot. That trade is the reason lag (for \(K_v\)) and lead (for \(\zeta\)) exist in unit 08.

Do not use settling \(4/\sigma\) on an overdamped pair: the slower real pole dominates, \(t_s\approx 4/|p_{\mathrm{slow}}|\).

Worked second-order identification from a scope shot is worth practising until it is boring. Read the steady value \(y(\infty)\). Percent overshoot is \(100(y_{\mathrm{peak}}-y(\infty))/y(\infty)\) only if the prototype DC gain is 1; if \(T(0)=0.8\), divide by 0.8 first or the \(\zeta\) chart is wrong. Peak time is the first peak, not the second. Invert PO to \(\zeta\) with the exponential formula, not with a straight-line guess of “about 0.5.” Then \(\omega_d=\pi/t_p\) and \(\omega_n=\omega_d/\sqrt{1-\zeta^2}\). Check that \(2\zeta\omega_n\) matches the decay of successive peaks: the logarithmic decrement \(\ln(A_k/A_{k+1})=\zeta\omega_n T_d=2\pi\zeta/\sqrt{1-\zeta^2}\). If the decrement disagrees with the PO-derived \(\zeta\), the response is not prototype (a zero is present, or a third pole, or the system is nonlinear).

Type and \(K_v\) from a Bode sketch (preview of unit 06): a type-1 loop has a low-frequency slope of \(-20\,\mathrm{dB/dec}\); the intercept of that asymptote with 0 dB is \(K_v\) in rad/s. A type-2 loop has \(-40\,\mathrm{dB/dec}\) and intercepts 0 dB at \(\sqrt{K_a}\). Students who only memorize the \(\lim s\to 0\) formulas miss that a measured Bode already contains the error constants. Conversely, a time-domain ramp test: apply \(r(t)=At\), wait until the lag is constant, then \(e_{ss}=A/K_v\). If the lag grows without bound, the loop is type 0 or unstable — Routh the characteristic polynomial before blaming \(K_v\).

Sensitivity of overshoot to an extra zero: if \(T(s)=(\tau_z s+1)\omega_n^2/(s^2+2\zeta\omega_n s+\omega_n^2)\), the zero adds a term proportional to \(\tau_z \dot{y}_{\mathrm{proto}}\) on the step response, which peaks earlier and higher. A PD controller in unity feedback puts a closed-loop zero at the PD zero; quote PO from the poles alone and you will undershoot the true overshoot, sometimes by a factor of two. A PI controller puts a closed-loop zero near the origin and a nearby pole; the pair is a slow tail, not extra overshoot. Learn to look at the zeros of \(T\), not only of \(L\).

Actuator effort is part of time response. For \(U=G_c E=G_c(R-Y)\), a step \(R\) produces an initial \(u(0^+)\) equal to \(G_c(\infty)\) times the step if \(G_c\) is biproper. PD and unfiltered derivative kick the actuator; that kick is why hardware derivative terms are filtered and why a spec on \(t_r\) without a spec on \(u_{\max}\) is incomplete. First-order closed loops with high \(a\) have \(u(0^+)\) large for the same reason (high-frequency gain of the loop).

When two first-order lags cascade in closed loop they are not first-order. Reduce \(T(s)\) and classify. A “time constant 0.2 s in series with 0.05 s, gain 10, unity feedback” is second order; compute \(\zeta,\omega_n\) rather than adding time constants. Adding open-loop time constants is a process-control approximation for *open-loop* step tests, not for closed-loop poles.

## Mistakes

Applying \(\mathrm{PO}(\zeta)\) to a system with a closed-loop zero, or to \(\zeta>1\).

Using \(\omega_n\) in \(t_p=\pi/\omega_n\) instead of \(\omega_d\). Peak time uses the damped frequency.

Quoting \(e_{ss}=0\) for a type-0 loop on a step because “feedback kills error.” Type 0 has \(e_{ss}=1/(1+K_p)\).

Computing \(K_v\) on a type-0 \(L\) and reporting a finite ramp error. The ramp error diverges (the output lags without bound or settles to a different slope).

Using error-constant tables on an unstable closed loop. Final-value hypotheses fail; the time response grows.

Treating \(t_s=4/\omega_n\) (missing \(\zeta\)). The exponent is \(\zeta\omega_n\).

Forgetting to scale: unit-ramp formulas with a ramp of slope 5.

Mixing 2% and 5% settling (3 vs 4 time constants) in a numerical that specified one of them.

Using \(K_p=\lim G(s)\) instead of \(\lim L(s)=G_c G H\).

Reporting percent overshoot as the fractional overshoot without ×100 when the question asked for percent, or the reverse.

Dominant-pair neglect when a closed-loop pole from a PI zero-pole pair sits near the origin: the slow zero–pole doublet makes a long tail (creep) that \(4/\sigma_{\mathrm{pair}}\) misses.

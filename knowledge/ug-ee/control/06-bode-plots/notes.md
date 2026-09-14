# Bode plots: asymptotes, gain and phase margins

A Bode diagram is the frequency response \(L(j\omega)\) drawn as \(20\log_{10}|L|\) in dB and \(\angle L\) in degrees versus \(\log\omega\). Asymptotic sketches of poles, zeros, and \(K/s^r\) factors are a UG exam skill; gain margin and phase margin read off that sketch (or a more accurate curve) are the practical stability margins for a stable open-loop plant. This unit is factor templates, corner frequencies, the two margins, delay, and the relationship to closed-loop bandwidth — not Nyquist encirclements (next unit).

## Concepts

For \(L(s)=K\dfrac{\prod(1+s/\omega_z)}{s^r\prod(1+s/\omega_p)\prod(s^2/\omega_n^2+2\zeta s/\omega_n+1)}\) (normalized time-constant form), the Bode magnitude is the sum of the dB of each factor; the phase is the sum of the phases. That additivity is why sketches are piecewise.

A constant \(K>0\) is a horizontal \(20\log_{10}K\) dB and 0° phase. A negative \(K\) adds \(-180^\circ\) and is an inverted loop (unusual as a plant gain).

Integrator \(1/s^r\): magnitude \(-20r\) dB/decade through 0 dB at \(\omega=1\) if the constant is 1; more generally the low-frequency asymptote of \(K/s^r\) crosses 0 dB at \(\omega=(K)^{1/r}\). Phase is \(-90^\circ r\) for all \(\omega\). A differentiator is the opposite slope and \(+90^\circ r\).

Real pole \(1/(1+s/\omega_p)\): magnitude asymptote 0 dB until \(\omega_p\), then \(-20\) dB/dec. Phase goes from 0° to \(-90^\circ\), with \(-45^\circ\) at \(\omega_p\). A decade below, phase is about \(-5.7^\circ\); a decade above, about \(-84^\circ\). Straight-line phase sketches often use a 0° to \(-90^\circ\) ramp from \(0.1\omega_p\) to \(10\omega_p\). A real zero is the mirror (\(+20\) dB/dec, \(+90^\circ\)).

Quadratic pair: slope changes by \(-40\) dB/dec at \(\omega_n\). Phase goes \(0\to-180^\circ\). The magnitude peak is \(Q=1/(2\zeta)\) above the asymptote if \(\zeta<0.707\), at \(\omega_n\sqrt{1-2\zeta^2}\) when that is real. Do not put a resonant peak on a \(\zeta=0.8\) pair.

Type number \(r\) is the low-frequency slope in units of \(-20\) dB/dec. You can read type off a Bode magnitude plot without the formula.

Crossover frequencies. Gain crossover \(\omega_g\) (also \(\omega_c\)): \(|L(j\omega_g)|=1\) (0 dB). Phase crossover \(\omega_p\): \(\angle L(j\omega_p)=-180^\circ\) (plus odd multiples if the phase wraps). Phase margin \(\mathrm{PM}=\angle L(j\omega_g)+180^\circ\). Gain margin \(\mathrm{GM}=1/|L(j\omega_p)|\) in absolute units, or \(-20\log_{10}|L(j\omega_p)|\) in dB. Both margins positive means that at the two special frequencies the plot has not yet reached the critical point, for a stable open-loop minimum-phase loop that is the usual UG sufficient picture. Non-minimum-phase or open-loop unstable plants need Nyquist (unit 07); Bode margins can lie.

A delay \(e^{-j\omega T}\) does not change magnitude and subtracts \(\omega T\) radians of phase. It wrecks PM at high \(\omega_g\). Padé is optional; for sketches, just add \(-\omega T\times 180/\pi\) degrees at the frequencies of interest.

Minimum-phase systems: all zeros (and poles) in the closed LHP. Then magnitude uniquely determines phase up to the type. A RHP zero (non-minimum phase) has the same \(|L|\) as the reflected LHP zero but opposite phase contribution, so the Bode phase is more negative and PM is worse. All-pass factors \((s-a)/(s+a)\) are 0 dB everywhere and a falling phase.

Closed-loop bandwidth, for a well-damped unity-feedback loop, is near \(\omega_g\), often \(0.5\omega_g\) to \(\omega_g\) depending on PM. Tracking error at low frequency is small when \(|L|\) is large (high \(K_v\) shows as a high low-frequency asymptote for type 1). Disturbance rejection at a frequency is good when \(|L|\) is large there, until actuator limits.

Reading a sketch vs an accurate plot: the straight-line magnitude is exact for \(K/s^r\) and is within 3 dB at a real corner. Phase straight-line is rougher. Exam numericals that ask for PM from an “asymptotic Bode” usually want you to compute \(L(j\omega)\) exactly at the \(\omega\) you found from the magnitude asymptote, or they give a table. When they want a sketch only, mark corners, slopes, and the two margins qualitatively.

Lead raises PM (adds phase in a band). Lag lowers \(\omega_g\) and can restore PM after a gain increase for error constants. That design is unit 08; this unit must still compute PM of a given \(L\).

## Equations

\[
L(j\omega)=|L|e^{j\phi},\qquad \mathrm{dB}=20\log_{10}|L|.
\]
\[
\mathrm{PM}=\phi(\omega_g)+180^\circ,\qquad |L(j\omega_g)|=1.
\]
\[
\mathrm{GM}_{\mathrm{dB}}=-20\log_{10}|L(j\omega_p)|,\qquad \phi(\omega_p)=-180^\circ.
\]
Delay: \(\phi_{\mathrm{delay}}=-\omega T\) rad.

Real-pole phase: \(\phi=-\tan^{-1}(\omega/\omega_p)\).

Quadratic magnitude:
\[
\left|\frac{\omega_n^2}{(j\omega)^2+2\zeta\omega_n(j\omega)+\omega_n^2}\right|
=\frac{\omega_n^2}{\sqrt{(\omega_n^2-\omega^2)^2+(2\zeta\omega_n\omega)^2}}.
\]

Low-frequency type-1: \(L\sim K_v/s\), so \(|L|=K_v/\omega\), 0 dB at \(\omega=K_v\).

## Methods

Factor \(L(s)\) into Bode form (time constants, not \(s+a\) without converting \(\omega=a\)). List corners on a log-\(\omega\) axis. Draw the low-frequency asymptote from \(K/s^r\). At each corner, change slope by \(\pm 20\) dB/dec per real factor, \(\pm 40\) per quadratic. Optionally correct ±3 dB at real corners and the resonant peak.

Phase: start at \(-90^\circ r\). Add each factor’s arctangent (or the decade ramp sketch). Include delay.

Find \(\omega_g\) from the magnitude plot or by solving \(|L(j\omega)|=1\). Read \(\phi(\omega_g)\), then PM. Find \(\omega_p\) from \(\phi=-180^\circ\), then GM. If phase never reaches \(-180^\circ\) and \(|L|\) rolls off, GM is infinite (typical of second-order type 1 \(K/(s(s+a))\)).

For a numerical without a plot, compute \(L(j\omega)\) at a few frequencies around the expected crossover (start with the 0 dB intercept of the two-slope approximation). Refine.

Stability from Bode (minimum-phase, open-loop stable): PM>0 and GM>0. Typical specs: PM \(30^\circ\)–\(60^\circ\), GM \(\ge 6\) dB. PM \(\approx 100\zeta\) degrees is a rough second-order map (\(\zeta=0.6\) ↔ PM \(\approx 60^\circ\)), not a theorem for higher order.

Non-minimum-phase: still draw Bode, but do not conclude stability from PM>0 without a Nyquist count. Sketch both magnitude and phase of a RHP zero as a reminder that the dB plot looks “minimum phase” while the phase plot does not.

## Mistakes

Using \(\log_{10}|L|\) without the 20, or using \(10\log_{10}\) (that is power, not amplitude).

Corner at \(1/\omega_p\) when the factor was already \(1/(1+s/\omega_p)\). The corner is \(\omega_p\).

Phase of \(1/(j\omega\tau+1)\) as \(-\omega\tau\) in degrees without \(\tan^{-1}\).

Finding PM at \(\omega_p\) or GM at \(\omega_g\) (swapping the two frequencies).

Forgetting the type’s \(-90^\circ r\) as the phase floor before other corners contribute.

Treating a RHP zero as a LHP zero in phase (same magnitude error is invisible on the dB plot).

Reading \(\omega_g\) from the phase plot.

Omitting a constant \(K\) in dB: \(20\log_{10}K\). For \(K=50\), that is 34 dB, not 50 dB.

Applying Bode PM as a closed-loop pole damping for a system with an extra slow pole: the approximation is for a dominant pair.

Sketching a quadratic as \(-20\) dB/dec.

Sign of PM: \(\phi=-120^\circ\) is PM \(=+60^\circ\), not \(-120^\circ\). \(\phi=-200^\circ\) is PM \(=-20^\circ\) (unstable for the usual MP OL-stable case).

A full asymptotic sketch of \(L(s)=40(s+2)/[s(s+4)(s+20)]\) is the standard midterm plot. Bode form: \(L=40\cdot 2(1+s/2)/[s\cdot 4(1+s/4)\cdot 20(1+s/20)]=(1)(1+s/2)/[s(1+s/4)(1+s/20)]\), so \(K_v=1\,\mathrm{s}^{-1}\). Corners at 2 (zero, \(+20\)), 4 (pole, \(-20\)), 20 (pole, \(-20\)). Low-frequency slope \(-20\,\mathrm{dB/dec}\) through 0 dB at \(\omega=1\). Between 2 and 4 the slope is 0 dB/dec (flat), so the magnitude is approximately \(K_v/\omega\) until 2, then holds constant until 4, then \(-20\) until 20, then \(-40\). The flat shelf is a lead-like interval from the zero at 2 beating the pole at 4; that shelf is exactly why a lead compensator looks like a +20 then a pole. Phase: start at \(-90^\circ\); add \(+\tan^{-1}(\omega/2)\); subtract \(\tan^{-1}(\omega/4)\) and \(\tan^{-1}(\omega/20)\). At \(\omega=1\), phase \(\approx -90+26.6-14.0-2.9\approx -80^\circ\), so if the 0 dB crossing were near 1, PM would be about \(100^\circ\). The actual \(\omega_g\) is near the shelf; compute \(|L(j\omega)|=1\) numerically around \(\omega=2\) to 6 rather than trusting the LF intercept. This is the usual story: the virtual \(K_v\) intercept is not \(\omega_g\) once a corner sits below that intercept.

Gain margin for type-1 second-order \(L=K/[s(s+a)]\): phase approaches \(-180^\circ\) only as \(\omega\to\infty\), where \(|L|\to 0\), so GM \(=\infty\). Phase margin is finite and is the only margin that bites. For \(L=K/[s(s+a)(s+b)]\), phase does cross \(-180^\circ\) at a finite \(\omega_p\), GM is finite, and that \(\omega_p\) is the same number as the Routh \(\omega_u\). Computing GM two ways (Bode phase crossover versus Routh \(K_u/K\)) is a check: \(\mathrm{GM}=K_u/K\) in absolute units when the only gain parameter is \(K\) and the crossing is unique.

Decibels of a factor-of-two: \(6\,\mathrm{dB}\) not \(3\,\mathrm{dB}\) (the latter is power-halving). A GM of 6 dB means you can double the gain before the crossing. A PM of 30° is a light, ringing loop; 60° is a comfortable analog servo; 80° looks overdamped. Relating PM to \(\zeta\) for a prototype loop, \(\mathrm{PM}\approx 100\zeta\) degrees is a back-of-envelope for \(0.3<\zeta<0.8\); the actual formula is \(\mathrm{PM}=\tan^{-1}(2\zeta/\sqrt{-2\zeta^2+\sqrt{1+4\zeta^4}})\) which nobody memorizes, they look up 65° ↔ \(\zeta\approx 0.7\).

Non-minimum-phase zero at \(s=+z\): magnitude identical to \(s+z\) reflected, phase of \((j\omega-z)\) rather than \((j\omega+z)\), so the phase *falls* through the corner instead of rising. A plant \(G=(1-s\tau)/(1+s\tau)\) times a lag is all-pass in magnitude (0 dB extra) and a monotone phase drop of \(-180^\circ\). Crossover must sit well below \(1/\tau\) or PM vanishes. Inverse-response processes (level in a boiler, some tanks) are this; lead compensation that raises \(\omega_g\) into the RHP-zero band is counterproductive.

Transport delay on Bode: add \(-\omega T\times 180/\pi\) degrees at the \(\omega\) you care about, after the rational phase is computed. Delay margin is \(\mathrm{PM}_{\mathrm{rad}}/\omega_g\) seconds: the extra delay that eats the remaining PM. A loop with \(\omega_g=10\,\mathrm{rad/s}\) and \(\mathrm{PM}=40^\circ=0.70\,\mathrm{rad}\) has delay margin \(70\,\mathrm{ms}\). That number is often more honest than GM for networked or sampled loops.

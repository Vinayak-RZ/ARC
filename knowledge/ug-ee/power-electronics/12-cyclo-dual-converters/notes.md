# Cycloconverters and dual converters

A cycloconverter synthesizes a lower-frequency AC waveform directly from AC by concatenating segments of the source, using phase-controlled bridges. A dual converter is two anti-parallel controlled rectifiers that together cover four quadrants of DC \(V\)–\(I\), with or without circulating current. Both are thyristor-era topologies that remain on UG syllabi because large low-speed drives and reversing DC drives still use the ideas, and because they test firing-angle, inversion, and circulating-current algebra.

## Concepts

Cycloconverter, single-phase to single-phase (teaching circuit): a positive-centre converter and a negative-centre converter, each a controlled rectifier, feed the load in alternate groups of half-cycles of the *output*. During the positive output half, the positive converter is phased to produce a positive mean that follows a slow sinusoid; the negative converter is blocked. Then they swap. The output frequency \(f_o\) is set by how often you swap. The output voltage is a patchwork of input half-sines, so harmonics of both \(f_i\) and \(f_o\) appear. Distortion grows as \(f_o\) approaches \(f_i\). The usual UG bound is \(f_o\le f_i/3\) for a three-phase to three-phase six-pulse cyclo, so a 50 Hz supply yields at most about 16–20 Hz of decent waveform.

Three-phase to three-phase cycloconverters use 18 or 36 thyristors (two six-pulse bridges per output phase, anti-parallel). Circulating-current mode keeps both bridges alive with a reactor, improving waveform and allowing smooth reversal; non-circulating mode blocks one group at a time, saving loss but requiring a current-zero detection and a blanking time. Blocking mode is more common at high power.

Control: the firing angle \(\alpha(t)\) of each bridge is modulated so that \(V_{dc}(t)=V_{do}\cos\alpha(t)\) tracks \(V_m\sin\omega_o t\). That implies \(\alpha(t)=\arccos(m\sin\omega_o t)\) in the continuous, no-overlap model, with modulation index \(m\le 1\). Overlap and discontinuous current distort this. Input pf is poor: the source sees a lagging, chopped current whose fundamental lags even at \(m=1\). Reactive power is a known cyclo drawback versus a PWM VSI.

Compared with a VSI: no DC link capacitor, inherent four-quadrant capability (the load can send power back by swapping which bridge inverts), but line-frequency devices, bulky transformers sometimes, and a low \(f_o\) ceiling. Compared with an AC voltage controller: the cyclo *does* change frequency; the AC controller does not.

Dual converter: two fully controlled bridges anti-parallel on a DC load (or on a DC machine armature). Bridge P produces positive \(V_t\) with positive current; bridge N produces negative \(V_t\) with negative current. Four-quadrant drive is then natural.

Circulating-current dual converter: both bridges are gated at once with \(\alpha_P+\alpha_N=180^\circ\) so that their mean voltages match (\(V_{do}\cos\alpha_P=-V_{do}\cos\alpha_N\)). A reactor absorbs the instantaneous voltage difference (the ripple). Circulating current \(I_{\mathrm{cir}}\) flows in the reactor and the two bridges even at no load. Advantages: no dead time at current reversal, continuous current in each bridge, linear four-quadrant control. Disadvantages: extra loss, extra reactor, bridges must be rated for load plus circulating current.

Non-circulating dual converter: only one bridge is pulsed at a time. When current reverses, a lockout delay waits for current zero. Cheaper, less loss, a small dead band in torque near zero unless the current loop is fast.

Mode of operation with a DC motor: \(\alpha_P\) sets speed in Q1; inversion of P or use of N handles braking and reverse. The algebra is unit 03 plus a second \(\alpha\).

Never fire both bridges as rectifiers with \(\alpha_P+\alpha_N\neq 180^\circ\) in circulating mode, or a huge DC voltage difference appears across a small resistance (short). The \(180^\circ\) pair is mandatory.

A cycloconverter is easiest if you first imagine a dual converter whose DC mean is not constant but is slowly waved through \(\pm V_{do}\). Each output half-cycle is one polarity of that dual converter. The “slow sinusoid” is assembled from many line-frequency segments, so the output looks like a sine only after the load inductance filters it, and only if many segments fit in one output half-cycle — which is exactly why \(f_o\) must be well below \(f_i\). At \(f_o = f_i/3\) you have about 1.5 input cycles per output half-cycle on a single-phase teaching cyclo, which is already crude; three-phase six-pulse groups help by offering more segments per output degree.

Circulating versus blocking in cyclos mirrors dual converters. Circulating current (with inter-group reactors) keeps both polarities alive, reduces crossover distortion, and wastes current. Blocking waits for output current zero before swapping groups. At a mill’s inertia the wait is acceptable. At a servo it would not be — but servos are PWM VSIs anyway.

Input current of a cyclo is not a 50 Hz sine at a displacement \(\cos\phi_{\mathrm{load}}\). Each thyristor still fires at a time-varying \(\alpha\), so the line current’s fundamental lags more than the load, and distortion is rich in sidebands around multiples of \(f_i\) offset by multiples of \(f_o\). UG papers sometimes ask a qualitative “pf is poor”; they rarely ask a full Fourier series. Do not claim \(\mathrm{pf}=\cos\alpha_{\mathrm{avg}}\) without a stated model.

Dual-converter circulating current is not a fault current if the reactor is present and \(\alpha_P+\alpha_N=180^\circ\). It is a designed triangle (or a more complicated ripple) superimposed on the load current in each bridge. Thyristor RMS must be computed from load plus this ripple. If the reactor is too small, circulating current is huge; if too large, current reversal (when you want the load current to swing through the circulating pedestal) is slow. That is the design trade, analogous to choosing \(L\) in a CCM chopper.

Non-circulating dual converters need a current sensor that is trusted near zero. Residual current in a large \(L_a\) can fool a simple threshold; a lockout timer is the conservative UG answer. During lockout the machine coasts, so a hoist needs a mechanical brake. Four-quadrant choppers (H-bridge) avoid this at high \(f_s\) because current is continuous and reversal is just a PWM sign change — the reason dual converters have retreated to very high power.

Transformer coupling of dual converters (separate secondaries for P and N) can isolate circulating paths. Centre-tapped schemes exist. UG numericals usually assume a common AC bus and a DC reactor.

## Equations

Ideal bridge mean:

\[
V_d=V_{do}\cos\alpha,\qquad V_{do}=\frac{2V_m}{\pi}\ \text{(1ph)}\ \text{or}\ \frac{3\sqrt{2}}{\pi}V_{LL}\ \text{(3ph)}.
\]

Cyclo modulation (slow envelope):

\[
\cos\alpha(t)=m\sin\omega_o t,\qquad |m|\le 1,\qquad f_o\lesssim f_i/3.
\]

Dual converter, circulating, matching means:

\[
\alpha_N=180^\circ-\alpha_P,\qquad \langle v_P\rangle=\langle v_N\rangle.
\]

Circulating reactor: the difference of the two instantaneous bridge voltages appears across \(L_{\mathrm{cir}}\). Peak-to-peak circulating current is on the order of \(\Delta\lambda/L_{\mathrm{cir}}\) where \(\Delta\lambda\) is the volt-second of one ripple pulse. UG problems sometimes give \(L\) and a trapezoidal voltage difference.

Non-circulating: \(I_{\mathrm{cir}}=0\), lockout time \(t_{\mathrm{blank}}\) after current zero, typically a few milliseconds at 50 Hz.

Four-quadrant map:

- Q1: P rectifying, \(I>0\), \(\alpha_P<90^\circ\)
- Q2: P inverting or N rectifying depending on circulating vs non-circulating implementation, \(I<0\), \(V>0\)
- Q3: N rectifying, \(I<0\), \(V<0\)
- Q4: N inverting, \(I>0\), \(V<0\) (plugging-like if the machine still has positive \(E_a\))

Power: \(P=V_t I_a\). Regeneration when \(P<0\).

## Methods

1. Cyclo: state \(f_o/f_i\), pick \(m\), write \(\alpha=\arccos(m\sin\omega_o t)\) at a requested instant if asked. Sketch which group (P or N) is active in that output half-cycle.
2. Dual converter: if circulating, set \(\alpha_N=180^\circ-\alpha_P\) before any current calculation. If non-circulating, identify the unique live bridge from the signs of \(V^*\) and \(I\).
3. Motor: \(V_t=V_{do}\cos\alpha=E_a+I_a R_a\) with signs. Check inversion margin \(\alpha+u+\gamma\le 180^\circ\) on the inverting bridge.
4. Circulating current: if a numerical \(L\) and a voltage-difference waveform are given, integrate \(v_L=L di/dt\). If not, leave \(I_{\mathrm{cir}}\) as a design parameter that adds to RMS thyristor current.
5. Do not size a cyclo as a 50 Hz motor supply from 50 Hz mains without a very large pulse number and even then expect ugly harmonics — the UG answer is “use a VSI.”

Worked pattern — dual: \(V_{do}=540\,\mathrm{V}\), want \(V_t=300\,\mathrm{V}\) circulating. \(\cos\alpha_P=300/540=0.556\), \(\alpha_P=56.3^\circ\), \(\alpha_N=123.7^\circ\). If a cyclo at the same \(V_{do}\) wants a peak of 300 V, that is \(m=300/540=0.556\), and \(\alpha(t)=\arccos(0.556\sin\omega_o t)\), which is a different use of the same cosine, not a dual-converter pair of constant angles.

## Mistakes

- Setting \(f_o=f_i\) in a cyclo as if it were an AC controller or a matrix converter.
- Dual converter: \(\alpha_P=\alpha_N\) (both rectifying) — a DC short through the two bridges.
- Forgetting the circulating reactor in circulating mode.
- Using semi-converters in a dual converter and expecting inversion.
- Mixing cyclo (AC out) with dual converter (DC out).
- Applying PWM \(m_a\) formulae to a cyclo \(\cos\alpha\) modulator without mapping \(m\leftrightarrow V_{peak}/V_{do}\).
- Non-circulating: reversing pulses before current is zero (line-to-line shoot through via the two bridges).
- Ignoring that cyclo input pf is worse than the output \(\cos\phi\).

A numerical pattern that shows up every year: given \(V_{do}\) and a requested \(V_t\), \(\alpha_P=\arccos(V_t/V_{do})\) and \(\alpha_N=180^\circ-\alpha_P\). If \(|V_t|>V_{do}\), the request is infeasible without a tap change. If the machine \(E_a+I_a R_a\) needs a sign change, you have changed quadrant and possibly changed which bridge is live. Write the signs before the arccos.

This unit closes the UG converter catalogue: AC–AC frequency change without a DC link, and four-quadrant DC without an H-bridge chopper. PWM VSIs have taken most new low-voltage applications; the algebra of \(\alpha\) and circulating current remains exam-live. Keep cyclo and dual converter in separate mental folders — one makes AC at \(f_o\), the other makes DC that can reverse.

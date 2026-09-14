# Uncontrolled rectifiers: single-phase and three-phase diode bridges, overlap

An uncontrolled rectifier uses diodes only. The AC side dictates when each diode conducts; there is no firing angle. UG courses treat the single-phase half-wave, the single-phase full-wave bridge (and the centre-tap twin), and the three-phase six-pulse bridge as the core. Source inductance makes the current hand-off take a finite overlap (commutation) angle \(u\), which drops the DC voltage below the ideal average. This unit is average-value and waveform analysis, not closed-loop PFC.

## Concepts

A single-phase half-wave diode feeding a resistive load conducts when the source is positive and is idle when the source is negative. Average load voltage is \(V_m/\pi\) for an ideal diode and a sinusoid of peak \(V_m\). The supply current is unidirectional, so a transformer feeding this circuit sees a DC component and can saturate — that is why half-wave is a teaching circuit, not a product. With an inductive load and no freewheel path, current can extend into the negative half-cycle until energy in \(L\) is spent; the diode still cannot reverse, so the voltage follows the AC source negative while current is positive (first-quadrant voltage, second-quadrant power for part of the cycle). A freewheel diode across the load clamps voltage to about zero during that interval and improves the DC current smoothness.

A single-phase full-wave bridge uses four diodes. Two conduct at a time. For a resistive load the load voltage is a full-wave rectified sinusoid: average \(2V_m/\pi\), RMS \(V_m/\sqrt{2}\). Each diode sees PIV \(V_m\). Transformer utilisation is better than half-wave because the secondary current is AC (odd harmonics plus fundamental). With a highly inductive DC load the current is nearly flat; each pair of diodes conducts for \(180^\circ\), and the DC voltage waveform is still \(|v_s|\) but the current is a square ±\(I_{dc}\) on the AC side. Displacement factor is unity for the square-wave current aligned with voltage; distortion factor is \(2\sqrt{2}/\pi\approx 0.90\); power factor is therefore about 0.90 in the large-\(L\) ideal case.

A capacitor-input filter after a single-phase bridge is the analog-electronics reservoir capacitor: conduction near the peaks, large peak diode current, ripple at \(2f_{\mathrm{line}}\). Power-electronics courses often prefer the inductive (current-stiff) DC load because it matches DC-motor armatures and DC-link inductors. State which filter you have before writing an average-voltage formula.

Three-phase six-pulse diode bridge: six diodes, two at a time (one from the top group, one from the bottom), DC voltage equal to the line-to-line voltage of the currently conducting pair. Instantaneous DC voltage is the envelope of the three line-to-line waveforms, switching every \(60^\circ\). Average DC voltage with no overlap is

\[
V_{dc}=\frac{3\sqrt{2}}{\pi}V_{LL,\mathrm{rms}}\approx 1.35\,V_{LL}.
\]

Ripple is smaller than single-phase: six pulses per cycle. AC-side current per phase is a quasi-square wave of \(120^\circ\) conduction (positive) and \(120^\circ\) negative, with \(60^\circ\) zeros if the DC current is constant — the classic six-step current. Harmonics of the AC current sit at \(6k\pm 1\). This is the front end of many voltage-source inverters (diode rectifier + capacitor DC link).

Overlap (commutation): real sources have inductance \(L_s\) (transformer leakage plus line). When the DC current transfers from one diode to the next, both diodes in a group conduct together and the two AC voltages are shorted through \(2L_s\). During that interval the DC voltage is the average of the two involved line voltages, not the higher one. The overlap angle \(u\) satisfies, for a three-phase bridge with DC current \(I_{dc}\),

\[
\cos\alpha-\cos(\alpha+u)=\frac{2\omega L_s I_{dc}}{V_{LL,\mathrm{peak}}}
\]

with \(\alpha=0\) for diodes. The DC voltage drops by \(\Delta V = (3/\pi)\omega L_s I_{dc}\) for the six-pulse bridge (the classic \(3\omega L_s I_{dc}/\pi\) term). Overlap also lengthens the current-transfer interval, rounding the AC current edges and slightly changing harmonics. If \(u\) is large, a diode bridge can fail to commutate under heavy current and weak AC (voltage collapse / commutation failure language borrowed from HVDC). UG problems usually give \(L_s\), \(I_{dc}\), and \(V_{LL}\) and ask for \(u\) and \(V_{dc}\).

Single-phase overlap: two diodes commuting through \(2L_s\) (or \(L_s\) depending on how the leakage is drawn). The DC mean falls by \(2\omega L_s I_{dc}/\pi\) for a single-phase bridge with constant DC current. Do not mix the single-phase and three-phase coefficients.

PIV and current ratings: in the three-phase bridge each diode blocks the peak line-to-line voltage. Average diode current is \(I_{dc}/3\) (each diode conducts \(120^\circ\) of the cycle in the large-\(L\) model). RMS diode current is \(I_{dc}/\sqrt{3}\). These numbers size the package.

Transformer connection: a three-phase bridge on a wye secondary with no path for triplen zero-sequence current is fine for the six-pulse waveform. Delta windings circulate triplens. Twelve-pulse rectifiers (two bridges, 30° phase shift, series or parallel DC) cancel 5th and 7th on the AC side; they appear as a named extension, not a full design exercise.

Discontinuous current: if \(L\) on the DC side is small and the load is light, current reaches zero each pulse. Then the simple \(1.35 V_{LL}\) formula is optimistic: the voltage follows the AC peaks more, average rises toward the peak, and the overlap model (which assumed constant \(I_{dc}\)) fails. Always check continuity: integrate \(v_L = Ri + L di/dt\) or use the rule that a large \(L/R\) compared with the pulse period keeps current continuous.

Inrush and precharge: a diode bridge onto a discharged capacitor looks like a short for a millisecond. UG labs use a precharge resistor or a controlled ramp. Surge rating \(I_{FSM}\) of the diodes must cover that pulse.

Compared with controlled rectifiers (next unit), the diode bridge cannot reduce DC voltage except by the AC tap or by overlap drop. It also cannot invert (send power back to AC) because diodes do not reverse voltage into a negative DC mean in the rectifier sense. Regeneration needs a controlled bridge or an active front end.

A laboratory picture is the DC-side waveform on a scope with AC coupling off. A single-phase bridge into a large C is a nearly flat line with 100 Hz teeth; into a large L it is a full-wave rectified sine at the same peaks as the AC, with current a triangle or a flat pedestal. Students mix those two pictures and then apply \(2V_m/\pi\) to a capacitor-input supply (too low) or \(V_m\) to an inductive supply (too high). State the filter before the formula. Three-phase six-pulse into a large C is almost a DC with a small 300 Hz ripple; into a large L it is the six-pulse envelope with current flat. Overlap rounds the notches: you can see a brief interval where \(v_{dc}\) sits between two line-to-line voltages. That notch depth growing with load is the \(3\omega L_s I_{dc}/\pi\) term made visible.

Transformer ratings for three-phase bridges use RMS line current \(I_{dc}\sqrt{2/3}\) in the large-\(L\) model, not \(I_{dc}\). Secondary VA is therefore larger than \(P_{dc}\) by the distortion factor. Twelve-pulse (two secondaries, 30° shift) cancels the 5th and 7th on the primary if the DC sides are series- or parallel-connected with equal current share. UG may ask why the 5th vanished, not to design the phase-shifting transformer.

Line notching from overlap injects voltage notches into a weak AC system. Other equipment on the same bus sees those notches. A series AC inductor (or a dedicated rectifier transformer with leakage) is sometimes added on purpose to limit \(di/dt\) and to isolate notches from the plant bus, at the cost of more \(u\) and more DC voltage drop. That trade is the same number as the overlap formula.

## Equations

Single-phase half-wave, resistive, ideal diode, \(v_s=V_m\sin\omega t\):

\[
V_{dc}=\frac{V_m}{\pi},\quad I_{dc}=\frac{V_{dc}}{R},\quad V_{\mathrm{rms,load}}=\frac{V_m}{2}.
\]

Single-phase bridge, resistive:

\[
V_{dc}=\frac{2V_m}{\pi},\quad V_{\mathrm{rms,load}}=\frac{V_m}{\sqrt{2}},\quad \mathrm{PIV}=V_m.
\]

Single-phase bridge, constant \(I_{dc}\) (large \(L\)):

\[
V_{dc}=\frac{2V_m}{\pi},\quad i_s=\pm I_{dc}\ \text{(square)},\quad \mathrm{THD}_i=\sqrt{\frac{\pi^2}{8}-1}.
\]

Single-phase bridge overlap drop (constant \(I_{dc}\), source inductance \(L_s\) per side as in the usual loop \(2L_s\)):

\[
V_{dc}=\frac{2V_m}{\pi}-\frac{2\omega L_s I_{dc}}{\pi}.
\]

Three-phase six-pulse, no overlap:

\[
V_{dc}=\frac{3\sqrt{2}}{\pi}V_{LL}=1.3505\,V_{LL},\qquad V_{dc,\mathrm{peak}}=\sqrt{2}V_{LL}.
\]

Three-phase overlap angle and DC voltage (\(\alpha=0\)):

\[
u=\arccos\left(1-\frac{2\omega L_s I_{dc}}{\sqrt{2}V_{LL}}\right),\qquad V_{dc}=\frac{3\sqrt{2}}{\pi}V_{LL}-\frac{3\omega L_s I_{dc}}{\pi}.
\]

Diode currents (three-phase, continuous \(I_{dc}\)):

\[
I_{D,\mathrm{avg}}=\frac{I_{dc}}{3},\qquad I_{D,\mathrm{rms}}=\frac{I_{dc}}{\sqrt{3}}.
\]

Ripple factor of the unfiltered three-phase envelope is small; the Fourier series of \(v_{dc}(t)\) has a sixth-harmonic leading term. UG exams sometimes ask the peak-to-peak of the six-pulse waveform without \(L\) or \(C\):

\[
v_{dc}(t)=\sqrt{2}V_{LL}\cos\omega t\quad\text{on }(-\pi/6,\pi/6)\ \text{relative to a pulse centre}.
\]

At the pulse edges \(\omega t=\pm\pi/6\), \(v_{dc}=\sqrt{2}V_{LL}\cos(\pi/6)=\sqrt{3/2}\,V_{LL}\), so the unfiltered ratio of min to mean is fixed.

## Methods

1. Sketch one period of the relevant AC voltages (phase and line-to-line). Mark which diodes are on. For three-phase, the top group follows the most positive phase; the bottom group follows the most negative phase.
2. Write \(v_{dc}(t)\) as the conducting line-to-line voltage. Average by integrating over \(60^\circ\) (three-phase) or \(180^\circ\) (single-phase full-wave).
3. If \(L_s\) is given, apply the overlap voltage-drop formula. Solve \(u\) from the cosine identity. If \(u\) comes out imaginary or \(>60^\circ\), the constant-current commutation model has broken (too much current, too little voltage).
4. Check continuous vs discontinuous DC current. If the question says “highly inductive,” use constant \(I_{dc}\). If \(R\) and \(L\) are both given, estimate \(\tau=L/R\) versus the pulse width.
5. Rate diodes: PIV, \(I_{\mathrm{avg}}\), \(I_{\mathrm{rms}}\), surge. Transformer secondary RMS current follows from the AC waveform (square or \(120^\circ\) blocks).
6. Power: \(P_{dc}=V_{dc}I_{dc}\). AC real power equals \(P_{dc}\) if diodes are ideal. Distortion factor from the current Fourier series if a pf is asked.

Worked pattern — three-phase bridge: \(V_{LL}=415\,\mathrm{V}\), \(I_{dc}=40\,\mathrm{A}\), \(L_s=0.80\,\mathrm{mH}\), 50 Hz. Ideal \(V_{dc0}=1.35\times 415=560\,\mathrm{V}\). Drop \(3\omega L_s I_{dc}/\pi=3\cdot 314\cdot 0.0008\cdot 40/\pi=12.0\,\mathrm{V}\). \(V_{dc}=548\,\mathrm{V}\). Then \(u=\arccos(1-2\omega L_s I_{dc}/(\sqrt{2}V_{LL}))\).

## Mistakes

- Using \(1.35 V_{\mathrm{phase}}\) instead of \(1.35 V_{LL}\) for the six-pulse mean.
- Mixing peak and RMS: \(V_m=\sqrt{2}V_{\mathrm{rms}}\); three-phase \(V_{LL}=\sqrt{3}V_{\mathrm{ph}}\) for a wye.
- Applying the three-phase overlap coefficient \(3/\pi\) to a single-phase bridge.
- Forgetting that two diodes conduct in a single-phase bridge (two forward drops if \(V_F\) is not neglected).
- Treating capacitor-input and inductor-input as the same average. Capacitor-input average is near the peak; inductor-input average is the pulse mean \(2V_m/\pi\) or \(1.35 V_{LL}\).
- Using \(I_{D,\mathrm{avg}}=I_{dc}/2\) on a three-phase bridge (that is closer to single-phase thinking). Six diodes share \(I_{dc}\); each conducts one-third of the time.
- Ignoring overlap when \(L_s\) is given, then wondering why measured \(V_{dc}\) sagged with load.
- Drawing three-phase current as a sinusoid. With large DC inductance it is a 120° block, not a sine.
- Claiming a diode bridge can invert. Average \(V_{dc}\) stays positive; regeneration of a reversing DC machine needs a controlled converter.
- PIV: using phase peak instead of line-to-line peak on the three-phase bridge.
- Half-wave transformer saturation: omitting the DC current in the secondary from the “why we do not use this” discussion.

Uncontrolled rectifiers are the stiff positive DC source for later inverters and choppers. Overlap is the first appearance of commutation, which unit 08 generalizes.

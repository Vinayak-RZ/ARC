# Phase-controlled converters

A phase-controlled converter uses thyristors (SCRs) whose firing instant is delayed by an angle \(\alpha\) after the natural diode instant. Delay reduces the average DC voltage; with a reversing DC mean the same bridge can invert and send power back to the AC source. UG depth is the single-phase fully controlled bridge, the single-phase half-controlled (semi-converter) bridge, the three-phase fully controlled six-pulse bridge, and inversion, overlap, and extinction angle. PWM active front ends belong with inverters, not here.

## Concepts

Natural diode conduction in a single-phase bridge would start at the voltage zero-crossing (resistive) or at the current-transfer instant (inductive). An SCR cannot start until it is both forward-biased and gated. Waiting an angle \(\alpha\) after that natural instant chops out the early part of the AC voltage from the DC average. For a single-phase fully controlled bridge with constant DC current,

\[
V_{dc}=\frac{2V_m}{\pi}\cos\alpha.
\]

At \(\alpha=0\) this matches the diode bridge. At \(\alpha=90^\circ\), \(V_{dc}=0\). For \(\alpha>90^\circ\), \(V_{dc}\) is negative while \(I_{dc}\) stays positive (thyristors still conduct in the same direction): power \(V_{dc}I_{dc}\) is negative, which is inversion. Inversion requires a DC source (a machine back-emf, a charged inductor-current into a reversing voltage, or another converter) that can push current against the negative mean. Extinction must finish before the next commutation window; the extinction angle \(\gamma\) and overlap \(u\) constrain \(\alpha_{\max}\approx 180^\circ-u-\gamma\).

A half-controlled (semi) converter mixes two SCRs and two diodes (or an equivalent freewheel path). Average voltage is

\[
V_{dc}=\frac{V_m}{\pi}(1+\cos\alpha)
\]

for the usual single-phase semi-converter with constant current. It cannot go negative: inversion is lost, but a freewheel path exists so inductive current does not force the AC source to take negative voltage. Ripple is worse than a fully controlled bridge at the same \(\alpha\) in some regions and better in others; exams compare Fourier components. The semi-converter is a one-quadrant DC supply.

Three-phase fully controlled bridge: six SCRs, firing sequence 60° apart. Average

\[
V_{dc}=\frac{3\sqrt{2}}{\pi}V_{LL}\cos\alpha=1.35\,V_{LL}\cos\alpha.
\]

Overlap modifies this to \(1.35 V_{LL}\cos\alpha - 3\omega L_s I_{dc}/\pi\), or equivalently \(1.35 V_{LL}(\cos\alpha+\cos(\alpha+u))/2\) after substituting the cosine identity for \(u\). Inversion at \(\alpha>90^\circ\) is the classic HVDC and regenerative DC-drive story at UG level.

Firing pulses: each SCR needs a pulse (or a train of pulses) every cycle while it is supposed to conduct. In a three-phase bridge a SCR that should take over may see a brief reverse interval during overlap; a pulse train covering \(120^\circ\) is the practical fix. Dual converters (unit 12) use two bridges anti-parallel.

Reactive power: a controlled rectifier with \(\alpha>0\) draws lagging current. Displacement factor is \(\cos\alpha\) in the large-\(L\), no-overlap model for the fully controlled bridge (AC current is a square or 120° block shifted by \(\alpha\)). Distortion remains. Input pf is therefore worse than a diode bridge. This is a reason later courses prefer PWM rectifiers.

Discontinuous current: at large \(\alpha\) and small \(L\), current may hit zero each half-cycle. Then the \(\cos\alpha\) formula overstates the drop (voltage follows the AC wave after current zero until the next firing). Always verify continuity if \(L\) and \(R\) are given. The boundary can be found by integrating the AC voltage minus \(V_{dc}\) across \(L\), but many UG problems simply state “highly inductive.”

Transformer tap plus \(\alpha\): industrial DC supplies sometimes use both. For a given \(V_{dc}\), smaller \(\alpha\) means better pf, so tap first, then fine-control \(\alpha\).

Compared with choppers: a phase-controlled rectifier makes a variable DC from AC at line frequency switching. A chopper makes variable DC from DC at high frequency. Drives use both: rectifier (or diode + chopper) then motor.

A laboratory mental model that keeps the algebra honest is the delayed window. Draw one line-to-line (or one single-phase) sinusoid. Mark the natural diode instant. Slide a vertical line by \(\alpha\). Everything to the left of that line is denied to the DC bus; everything to the right, until the next commutation, is applied. The average of a cosine that has been delayed by \(\alpha\) is the un-delayed average times \(\cos\alpha\). That is the whole fully-controlled story, including why inversion is a cosine that has gone negative rather than a new topology. Overlap then shaves a triangle off the rising edge of each pulse: two devices share current, the DC voltage is the mean of two AC voltages, and the lost volt-seconds equal \(2 L_s I_{dc}\) per commutation. Six commutations per cycle in a three-phase bridge produce the \(3\omega L_s I_{dc}/\pi\) drop. If you remember only one overlap sentence, remember that one.

Firing electronics at UG depth is a ramp (or a cosine-wave) compared with a DC control voltage, plus a pulse transformer or an opto-isolated gate driver. Cosine-wave crossing makes \(V_{dc}\) linear in the control voltage because \(\cos\alpha\) is the quantity you want. A linear-in-\(\alpha\) ramp does not linearize \(V_{dc}\). Exam problems that give a control voltage and a cosine firing circuit are asking you to see that mapping. Pulse trains, not single needles, are used in three-phase bridges so that a device that was reverse-biased during overlap still gets a gate when it becomes forward-biased.

Discontinuous current is the usual trap in a lab with a lightly loaded RL. The DC voltage waveform then shows pieces of the AC sinusoid after current zero, and a voltmeter on the DC side reads higher than \((2V_m/\pi)\cos\alpha\) (single-phase) or \(1.35 V_{LL}\cos\alpha\) (three-phase). Speed of a DC motor therefore sags less than the continuous model predicted. The cure is more armature inductance or a heavier load, not a different \(\cos\alpha\) identity. When a problem states “highly inductive,” it is licensing the continuous formula; when it gives a numerical \(L\) and \(R\), you must test.

Input current harmonics of a six-pulse controlled bridge sit at \(5,7,11,13,\ldots\) with amplitudes that, in the large-\(L\) square-block model, fall as \(1/n\). Displacement shifts with \(\alpha\); distortion is mostly \(\alpha\)-independent in that model. Power-factor correction at this level is “keep \(\alpha\) small and use a transformer tap,” not a PWM rectifier. Active front ends belong with unit 05–07.

Safety and commutation failure deserve one paragraph because they are how inversion dies. If \(\alpha\) is too large, overlap too long, or the AC voltage sags, the outgoing device has not recovered before the incoming AC voltage tries to reverse the intended current path. Two devices then strap an AC line-to-line pair — a short. HVDC and mill drives manage this with extinction-angle control (\(\gamma\)-control) rather than raw \(\alpha\)-control in inversion. UG problems encode the same idea as \(\alpha+u+\gamma\le 180^\circ\).

## Equations

Single-phase fully controlled, constant \(I_{dc}\), no overlap:

\[
V_{dc}=\frac{2V_m}{\pi}\cos\alpha,\qquad P_{dc}=V_{dc}I_{dc},\qquad \mathrm{DF}=\cos\alpha.
\]

With overlap \(u\) (single-phase, source \(L_s\) as in the \(2L_s\) loop):

\[
V_{dc}=\frac{2V_m}{\pi}\cos\alpha-\frac{2\omega L_s I_{dc}}{\pi}.
\]

Single-phase semi-converter, constant \(I_{dc}\):

\[
V_{dc}=\frac{V_m}{\pi}(1+\cos\alpha).
\]

Three-phase fully controlled, no overlap:

\[
V_{dc}=\frac{3\sqrt{2}}{\pi}V_{LL}\cos\alpha.
\]

Three-phase with overlap:

\[
\cos\alpha-\cos(\alpha+u)=\frac{2\omega L_s I_{dc}}{\sqrt{2}V_{LL}},\qquad V_{dc}=\frac{3\sqrt{2}}{\pi}V_{LL}\cos\alpha-\frac{3\omega L_s I_{dc}}{\pi}.
\]

Inversion condition (continuous current, ideal): \(\alpha>90^\circ\) and a DC EMF \(E > |V_{dc}|\) in the right polarity so current stays in the thyristor direction. Extinction limit:

\[
\alpha+u+\gamma \le 180^\circ.
\]

RMS line current (three-phase, constant \(I_{dc}\)): \(I_{s,\mathrm{rms}}=I_{dc}\sqrt{2/3}\). Fundamental displacement \(\varphi_1=\alpha\) (no overlap).

## Methods

1. Identify fully controlled vs half-controlled vs diode. Write the matching \(V_{dc}(\alpha)\) before touching numbers.
2. If \(L_s\) is present, subtract the overlap drop. Compute \(u\) from the cosine identity; reject \(\alpha\) that violate \(\alpha+u+\gamma\le 180^\circ\) in inversion.
3. Power and pf: \(P=V_{dc}I_{dc}\). Apparent power from RMS voltage and RMS current. Displacement factor \(\cos\alpha\) only in the ideal fully controlled, continuous-current model — do not quote it for a semi-converter without derivation.
4. Quadrants: fully controlled bridge with unidirectional current is two-quadrant in the \(V\)–\(I\) plane (positive \(I\), \(V\) both signs). Dual converter is four-quadrant. Semi-converter is one-quadrant.
5. Sketch \(v_{dc}(t)\): delayed segments of the AC wave. Average is the integral of those segments, which is how \(\cos\alpha\) appears.
6. Firing unit: convert a requested \(V_{dc}\) into \(\alpha=\arccos(V_{dc}/V_{dc0})\). Clip \(\alpha\) to the legal inversion margin.

Worked pattern — three-phase: \(V_{LL}=415\,\mathrm{V}\), \(\alpha=35^\circ\), \(I_{dc}=30\,\mathrm{A}\), no overlap. \(V_{dc}=1.35\times 415\times\cos 35^\circ=459\,\mathrm{V}\). \(P=13.8\,\mathrm{kW}\). Displacement factor \(0.82\) lagging. If overlap of 8 V is then announced, subtract it from 459 V before computing power; do not apply \(\cos\alpha\) a second time.

## Mistakes

- Using \(\cos\alpha\) on a semi-converter as if it were fully controlled. Semi-converter is \((1+\cos\alpha)\).
- Forgetting that \(\alpha=0\) is the diode case, not “off.” Off is no pulses, current zero (except freewheel paths).
- Inverting with a semi-converter. It cannot produce negative \(V_{dc}\).
- Applying \(\alpha>90^\circ\) without a DC EMF; current discontinuous and inversion fails.
- Mixing \(V_m\) (phase peak) with \(V_{LL}\) in the three-phase formula.
- Using \(\cos\alpha\) as the distortion factor. It is the displacement factor in the ideal model; distortion factor is separate (\(\approx 3/\pi\) related numbers on six-step current).
- Ignoring overlap in inversion: commutation failure (shoot-through of the AC source via two devices) is the physical penalty.
- Computing \(I_{dc}=V_m/R\) with a large series \(L\) as if the load were resistive instantaneous Ohm’s law. Average \(V_{dc}=R I_{dc}+E\) for a motor.
- Pulse at \(\alpha\) measured from the wrong origin (phase voltage zero vs line-voltage crossing). Three-phase natural instant is the line-to-line crossing.

Phase control is line-frequency synthesis of a DC mean. Choppers (next DC–DC unit) synthesize a DC mean at high frequency from an already-existing DC bus.

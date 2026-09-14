# PWM techniques: SPWM, hysteresis, unipolar and bipolar

Pulse-width modulation is how a VSI (or a chopper) synthesizes a variable average voltage with harmonics pushed near the switching frequency instead of at low order. UG courses treat sinusoidal PWM (SPWM) for three-phase and single-phase inverters, bipolar versus unipolar single-phase PWM, a first look at third-harmonic injection and space-vector PWM (named), and hysteresis (bang-bang) current control. Carrier-based comparison is the working method.

## Concepts

A carrier (usually a triangle or sawtooth at \(f_c\)) is compared with a reference (modulating) signal at \(f_m\), the desired fundamental. When the reference exceeds the carrier, the pole switches to the positive DC rail; otherwise to the negative rail (two-level leg). The duty of that leg, locally averaged over one carrier period, tracks the reference if \(f_c\gg f_m\). Amplitude modulation index

\[
m_a=\frac{\hat V_{\mathrm{mod}}}{\hat V_{\mathrm{tri}}}
\]

sets the fundamental magnitude in the linear region \(m_a\le 1\). Frequency modulation index \(m_f=f_c/f_m\) should be an odd integer (and a multiple of three in three-phase) to cancel even harmonics and triplens as intended. Asynchronous PWM (\(m_f\) not integer) is used at high \(f_c\) in digital drives; beats can appear.

Linear SPWM, single-phase bipolar: the same reference (opposite on the other leg) produces a two-level line voltage \(\pm V_{dc}\). Fundamental peak \(\hat V_{o1}=m_a V_{dc}\) for the full-bridge bipolar definition used here (some notes write \(m_a V_{dc}/2\) for a half-bridge pole voltage). Always state whether \(m_a\) is pole-to-midpoint or full-bridge. In this handbook: pole voltage relative to DC midpoint is \(v_{ao}=(m_a V_{dc}/2)\sin\omega t\) in linear SPWM, so a full-bridge bipolar output (two poles, opposite references) has \(\hat V_{o1}=m_a V_{dc}\). Unipolar PWM uses a phase-shifted carrier or a rectified comparison so that the bridge output visits \(+V_{dc}\), 0, and \(-V_{dc}\). Harmonics of unipolar sit near \(2f_c\), which eases filtering. Bipolar harmonics sit near \(f_c\).

Overmodulation: \(m_a>1\) clips the reference. Fundamental grows toward the square-wave limit \(4V_{dc}/\pi\) (full-bridge) but low-order harmonics return. Six-step is the extreme.

Three-phase SPWM: three references 120° apart, one triangle. Line-to-line fundamental peak is \(m_a V_{dc}\) in the linear range (because line voltage is the difference of two poles, each \(m_a V_{dc}/2\)). Maximum linear RMS line voltage is \((\sqrt{3}/2\sqrt{2})m_a V_{dc}\) with \(m_a=1\), i.e. \(0.612 V_{dc}\), which is less than six-step’s \(0.780 V_{dc}\). Third-harmonic injection or SVPWM extends the linear region so the line-to-line can reach \(V_{dc}/\sqrt{2}=0.707 V_{dc}\) RMS before overmodulation — about 15% more voltage. UG exams often ask the 0.612 versus 0.707 versus 0.780 comparison.

Dead time reduces the actual fundamental slightly and adds low-order odd harmonics; digital compensators add a pulse-width correction.

Hysteresis current control: a current reference \(i^*\) is compared with measured \(i\). If \(i>i^*+h\), switch to decrease current; if \(i<i^*-h\), switch to increase. The current stays in a band of width \(2h\). Switching frequency is not constant; it depends on DC bus, \(L\), and \(h\). Simple, fast, ugly spectrum. Used in current-regulated VSIs, active filters, and some servo drives. Average-frequency estimate \(f_{sw}\approx V_{dc}/(6h L)\) for a three-phase inverter is a rough UG formula; treat it as an estimate.

Other named methods: selected harmonic elimination (SHE) solves \(\alpha_i\) to null chosen harmonics at low \(f_{sw}\) (square-wave with chops); space-vector PWM (SVPWM) implements the same volt-second average as a three-phase reference plus a triplen common mode; trapezoidal and staircase modulation appear in older notes.

Chopper PWM is the DC case of the same idea: a DC reference versus a triangle produces duty \(D\), and \(V_{out}=D V_{in}\) in a buck. There is no \(m_f\) story, only \(f_c\).

Carrier polarity and alignment change which sidebands cancel. A unipolar single-phase scheme that compares \(v_{\mathrm{mod}}\) and \(-v_{\mathrm{mod}}\) against one triangle produces a three-level \(v_{ab}\) whose double-frequency carrier cancellation is the point. A bipolar scheme that gates the two legs as strict complements produces a two-level \(v_{ab}\) with energy around \(f_c\). If a figure in a question shows \(+V_{dc},0,-V_{dc}\), it is unipolar (or a three-level NPC, which is a different topology). If it shows only \(\pm V_{dc}\), it is bipolar. Do not quote a Bessel formula you cannot derive; quoting the cluster location is enough.

Sampling in digital PWM (regular sampled, naturally sampled) shifts harmonics slightly and is mentioned so that a microcontroller lab does not surprise you. Naturally sampled is the analog comparator story. Regular sampled holds \(v_{\mathrm{mod}}\) for a carrier period; it is what a timer-plus-compare register does. At modest \(m_f\) the difference is visible on a spectrum analyser; at \(m_f>50\) UG treats them as the same \(m_a\) law.

Third-harmonic injection is a common-mode trick. Adding \(k\sin 3\omega t\) to each phase reference does not appear in \(v_{LL}\) (the third is common), but it flattens the peaks of the references so you can raise the fundamental amplitude without clipping the carrier. The usual \(k=1/6\) is the textbook choice that extends the linear region to the 0.707 \(V_{dc}\) RMS line voltage. Space-vector PWM does the same average as a particular piecewise common-mode injection; the hexagon in the \(\alpha\beta\) plane is the picture, and the maximum circular locus inside the hexagon is that same 15% gain. You do not need to implement seven-segment switching to use the 0.707 number.

Hysteresis in three phases cannot independently constrain all three currents if the machine is isolated-star, because \(i_a+i_b+i_c=0\). Two-phase hysteresis plus a dependent third, or a space-vector hysteresis, appear in papers as names. Variable \(f_{sw}\) also beats against the DC-link capacitor rating and against acoustic noise. Clocked hysteresis (a clock enables a switch decision at most once per period) caps \(f_{sw}\) at the clock. That hybrid is how some current-regulated VSIs stay both fast and EMI-bounded.

Dead time is a low-order harmonic generator: it inserts a polarity-dependent error of about \(t_{dt} V_{dc} f_c\) in the average pole voltage. Compensation adds or subtracts a duty equal to \(t_{dt}/T_c\) according to current sign. If current crosses zero inside the carrier period, compensation is imperfect and a zero-current clamp distortion appears — a named effect in drive inverters, not something to model in every numerical.

## Equations

Pole voltage (DC midpoint reference), linear SPWM:

\[
\langle v_{ao}\rangle = \frac{V_{dc}}{2} m_a \sin\omega t,\qquad 0\le m_a\le 1.
\]

Three-phase line-to-line fundamental RMS, linear SPWM:

\[
V_{LL,1}=\frac{\sqrt{3}}{2\sqrt{2}} m_a V_{dc}=0.612\, m_a V_{dc}.
\]

SVPWM / third-harmonic injection linear ceiling:

\[
V_{LL,1,\max}=0.707\, V_{dc}\quad\text{(RMS)}.
\]

Six-step ceiling:

\[
V_{LL,1}=0.780\, V_{dc}.
\]

Single-phase unipolar: harmonic sidebands around \(2m_f\). Bipolar: around \(m_f\). Bessel-sideband amplitudes are not required in every UG paper; the location of the first cluster is.

Hysteresis band (single-phase, DC bus \(\pm V_{dc}/2\) equivalent, inductance \(L\)):

\[
\frac{di}{dt}\approx\frac{V_{\mathrm{applied}}-e}{L},\qquad \Delta t_{\mathrm{rise}}\approx\frac{2h L}{V_{dc}-2e_{\mathrm{avg}}}.
\]

Modulation indices:

\[
m_a=\frac{\hat V_{\mathrm{mod}}}{\hat V_{\mathrm{tri}}},\qquad m_f=\frac{f_c}{f_m}.
\]

## Methods

1. Fix the definition of \(m_a\) (pole vs bridge) before computing \(V_1\). Write the pole formula, then subtract poles for line voltage.
2. Choose \(m_f\): odd, triple for three-phase synchronized PWM. At high \(f_c\), asynchronous is acceptable.
3. If a required \(V_{LL}\) is below \(0.612 V_{dc}\), linear SPWM can do it: \(m_a=V_{LL}/(0.612 V_{dc})\). If higher, inject third harmonic / SVPWM up to 0.707, else overmodulate toward 0.780.
4. Unipolar vs bipolar: pick unipolar when the filter is small and a three-level bridge output is available (single-phase full bridge with two carriers or opposite references on a shared carrier — check the textbook drawing). Bipolar is simpler (one comparator, two-level \(v_{ab}\)).
5. Hysteresis: pick \(h\) from allowed current ripple; estimate \(f_{sw}\); if \(f_{sw}\) is too high, enlarge \(h\) or add a clocked (period-limited) hysteresis.
6. Dead-time compensation: add \(t_{dt}/T_c\) to the duty in the direction of current if the question asks.

Worked pattern — SPWM motor: \(V_{dc}=560\,\mathrm{V}\) (rectified 400 V). Linear max \(V_{LL}=0.612\times 560=343\,\mathrm{V}\) RMS. A 400 V motor needs SVPWM/overmodulation or a higher bus.

## Mistakes

- Using \(0.78 m_a V_{dc}\) as if SPWM were six-step scaled by \(m_a\). Linear SPWM is 0.612, not 0.780.
- Mixing peak pole voltage \(m_a V_{dc}/2\) with RMS line voltage.
- Setting \(m_f=12\) (even, not multiple of 3) in a three-phase synchronized scheme and expecting triplen cancellation as in the odd-triple case.
- Claiming unipolar and bipolar have the same first harmonic cluster.
- Treating hysteresis \(f_{sw}\) as a set parameter; it is an outcome.
- Overmodulation without acknowledging extra 5th and 7th.
- Using a single-phase bipolar formula on a three-phase line voltage.
- Forgetting that \(m_a>1\) is not “invalid,” it is overmodulation with a defined (compressed) fundamental.

A last bookkeeping note: \(m_a\) is not duty \(D\). In a chopper, a DC reference versus a triangle *is* \(D\). In an inverter, the local duty of a pole is \(0.5 + 0.5 m_a \sin\omega t\) (two-level, midpoint-referenced). Confusing those two is how a student writes \(V_{LL}=D V_{dc}\) for an SPWM motor drive.

PWM is the practical voltage-control layer on the inverters of unit 05 and the AC drives of unit 10. Chopper duty in unit 04 is the DC special case of the same comparison. Need more words on spectra: the first sideband pair of bipolar SPWM sits at \(m_f \pm 2\), not at \(m_f \pm 1\), for naturally sampled odd functions; UG can treat “near \(f_c\)” as the location without a Bessel expansion. Unipolar moves that story to \(2f_c\). If a filter is sized from \(f_c\) on a unipolar bridge, it is oversized by about an octave — wasteful, not unsafe.

# Inverters: VSI, CSI, single-phase and three-phase, harmonics

An inverter converts DC to AC. Undergraduate courses split voltage-source inverters (VSI) from current-source inverters (CSI), then treat single-phase half-bridge and full-bridge square-wave and PWM operation, three-phase six-step (180° and 120°) bridges, and the harmonic content of the resulting waveforms. PWM details occupy the next unit; here the topology, the DC-link type, and the Fourier picture dominate.

## Concepts

A VSI is fed from a stiff DC voltage (battery, rectified mains plus capacitor). The AC side looks like a switched voltage; current is determined by the load (typically inductive machines). Freewheel diodes anti-parallel to the transistors are mandatory because inductive current cannot stop when a transistor turns off. A CSI is fed from a stiff DC current (a large inductor after a current-regulated front end). The AC side looks like a switched current; capacitors or a machine back-emf provide a voltage path. Series diodes with thyristors appear in classical CSI thyristor drives. Most modern motor drives on the UG syllabus are VSI with a diode rectifier plus DC capacitor (two-level IGBT bridge).

Single-phase half-bridge VSI: two capacitors split the DC bus, two switches, AC load from the midpoint of the switches to the capacitor midpoint. Output voltage levels are \(+V_{dc}/2\) and \(-V_{dc}/2\). Full-bridge (H-bridge): four switches, output levels \(+V_{dc}\), \(-V_{dc}\), and zero if both poles share a rail (bipolar vs unipolar PWM is unit 07). Square-wave full-bridge: \(v_o(t)=+V_{dc}\) for \(180^\circ\) and \(-V_{dc}\) for \(180^\circ\). Fourier series is odd harmonics, \(b_n=4V_{dc}/(n\pi)\) for odd \(n\). Fundamental peak \(4V_{dc}/\pi\). RMS of the square wave is \(V_{dc}\). Harmonic distortion is large; inductive loads filter current more than voltage.

Quasi-square (phase-shifted poles, or notched) waveforms insert zero-voltage intervals to reject a chosen harmonic (classically the third). UG problems ask for the notch angle \(\beta\) that nulls the \(n\)th harmonic: \(\cos(n\beta)=0\) depending on definition of \(\beta\). State the angle convention before computing.

Three-phase two-level VSI: six switches, three legs. 180° conduction: each switch on for \(180^\circ\), complementary device in the same leg on for the other \(180^\circ\) with dead time. Line-to-line voltage is a six-step waveform taking \(\pm V_{dc}\) and 0. Line-to-line fundamental peak is \((2\sqrt{3}/\pi)V_{dc}\) in the usual Fourier result, so RMS fundamental line voltage is \(\sqrt{6}\,V_{dc}/\pi\approx 0.780 V_{dc}\). Phase voltage relative to the DC midpoint is a six-step \(\pm V_{dc}/2\) staircase. 120° conduction is a CSI-like or thyristor-legacy pattern where each device conducts \(120^\circ\); it appears for comparison and for CSI. Never mix 120° and 180° formulae.

Dead time: both devices in a VSI leg must not conduct at once (shoot-through shorts the DC capacitor). A microsecond-scale delay is inserted. The load current then flows in diodes during the gap, slightly distorting the voltage (a few volts of error and extra low-order harmonics). UG analysis often neglects dead time except as a named non-ideality.

CSI three-phase: DC current \(I_{dc}\) is switched among phases, typically \(120^\circ\) blocks. AC current is a quasi-square; voltage is load-determined. Commutation requires capacitors or a machine with sufficient back-emf (auto-sequential commutated inverter, load-commutated inverter for synchronous machines). Harmonics of current are \(6k\pm 1\).

Harmonics: integer multiples of the fundamental that the switching waveform injects. For a square wave, \(n=3,5,7,\ldots\). Triple-n harmonics are common-mode in balanced three-phase line-to-line voltages and cancel on the lines of a 180° VSI (no third in \(v_{LL}\)). Load current harmonics \(I_n=V_n/(n\omega L)\) for an inductor, so voltage THD is worse than current THD on an inductive machine. Standards (named, not quoted as legal text) limit injected current harmonics on the AC mains — that is the rectifier’s problem more than the inverter’s motor-side problem, but PWM inverters still produce EMI at \(f_s\).

Modulation index, in square-wave mode, is essentially maxed: you cannot get more fundamental than \(4V_{dc}/\pi\) (single-phase square) without overmodulation into square from PWM. Reducing fundamental at a fixed \(V_{dc}\) requires PWM or a variable DC link (chopper + square-wave inverter, the old CSI/VSI drive split).

Voltage control methods at UG: (1) vary DC link, (2) PWM (unit 07), (3) cancellation by multiple inverters / multi-level (named). Frequency control is the switching timeline of the fundamental period, independent of amplitude except through V/f coupling in drives (unit 10).

A six-step VSI is best understood as three square-wave poles at 120°. Each pole is \(+V_{dc}/2\) for 180° and \(-V_{dc}/2\) for 180° relative to the DC midpoint. Line voltage is the difference of two poles, which produces the familiar \(+V_{dc}, +V_{dc}/2, 0, -V_{dc}/2, -V_{dc}\) staircase (the exact levels depend on whether you plot line-to-line or pole-to-pole with a defined zero). The third harmonic is common-mode on the three poles, so it vanishes from \(v_{LL}\) but it is present in phase-to-midpoint voltage. That is why a three-phase motor with an isolated star point does not see triplen line-to-line harmonics in 180° conduction, while a single-phase square-wave inverter is full of triplens.

Current-source inverters deserve a second physical picture. The DC inductor will not let current stop. Each commutation must hand that current to another phase, often through a capacitor that rings with the load inductance. Auto-sequential commutated inverters (ASCI) are the UG name for capacitor-commutated CSI induction-motor drives. Load-commutated inverters (LCI) need a machine that can supply leading current — typically a synchronous motor with over-excitation. If the machine loses excitation, commutation fails in the same way a thyristor rectifier fails in inversion. A PWM CSI with reverse-blocking IGBTs or series diodes is the modern relative; UG analysis still uses 120° current blocks as the Fourier baseline.

Harmonic heating in a machine is not optional decoration. Each \(I_n\) produces copper loss \(I_n^2 R\) and torque ripple at \(6k\) times electrical frequency for the usual \(6k\pm 1\) voltage harmonics of a six-step VSI. Iron loss also rises. A PWM inverter at a few kilohertz pushes the first strong voltage cluster near \(f_c\), where leakage inductance already attenuates current, so torque ripple at 6f drops. That is the engineering reason unit 07 exists. Square-wave (six-step) remains on papers because the Fourier series is closed-form and because some high-power CSI/LCI drives still run there.

Blanking, shoot-through, and the DC-link capacitor are one system. The capacitor’s ESR and ESL ring with the inverter’s \(di/dt\). A snubber or a laminated bus is unit 08; the inverter unit only insists that the DC voltage stay stiff on the scale of a switching period. If the front end is a diode bridge, regeneration raises \(V_{dc}\) until a brake chopper fires or something fails. If the front end is an active rectifier, regeneration is a current command reversal. Naming the front end is part of naming the inverter.

Single-phase inverters in UPS applications often add an LC filter so that the load sees a sine, not a square. The inverter is still a VSI; the filter is a low-pass with cutoff between \(f_m\) and \(f_c\). Resonance with nonlinear loads is a design issue beyond UG numericals, but the student should not compute “the output RMS” of a filtered UPS as \(V_{dc}\) of the square wave.

## Equations

Single-phase square-wave full-bridge, odd \(n\):

\[
v_o(t)=\sum_{n\ \mathrm{odd}}\frac{4V_{dc}}{n\pi}\sin n\omega t,\qquad V_{1,\mathrm{peak}}=\frac{4V_{dc}}{\pi},\qquad V_{\mathrm{rms}}=V_{dc}.
\]

THD of the voltage (square wave):

\[
\mathrm{THD}_v=\sqrt{\frac{V_{\mathrm{rms}}^2}{V_{1,\mathrm{rms}}^2}-1}=\sqrt{\frac{\pi^2}{8}-1}\approx 0.483.
\]

Three-phase 180° VSI, line-to-line fundamental:

\[
V_{LL,1,\mathrm{rms}}=\frac{\sqrt{6}}{\pi}V_{dc}\approx 0.7797\,V_{dc},\qquad V_{ph,1,\mathrm{rms}}=\frac{\sqrt{2}}{\pi}V_{dc}.
\]

Line-to-line waveform Fourier (180° conduction), harmonics \(n=6k\pm 1\):

\[
V_{LL,n,\mathrm{peak}}=\frac{4V_{dc}}{n\pi}\cos\frac{n\pi}{6}\quad\text{(use a consistent definition; many texts quote } \frac{2\sqrt{3}V_{dc}}{n\pi}\text{ for the fundamental)}.
\]

The fundamental matches \(2\sqrt{3}V_{dc}/\pi\) peak line-to-line, which is \(\sqrt{6}V_{dc}/\pi\) RMS.

Load current harmonic for series \(R+L\):

\[
I_n=\frac{V_n}{\sqrt{R^2+(n\omega L)^2}}.
\]

CSI AC current (120° blocks, magnitude \(I_{dc}\)):

\[
I_{1,\mathrm{peak}}=\frac{2\sqrt{3}}{\pi}I_{dc}.
\]

Power (balanced, fundamental): \(P=\sqrt{3}V_{LL}I_L\cos\phi_1\) using fundamental components, plus harmonic copper loss \(R\sum I_n^2\).

## Methods

1. Name VSI vs CSI from the DC link: capacitor voltage-stiff vs inductor current-stiff.
2. For square-wave or six-step, write the piecewise \(v(t)\) over one cycle, then either integrate for RMS or use the tabulated Fourier coefficients. Do not treat a six-step waveform as a sinusoid of peak \(V_{dc}\).
3. Convert \(V_{dc}\) to fundamental RMS before using AC-machine equivalent-circuit formulae.
4. Harmonic currents: divide each voltage harmonic by the impedance at \(n\omega\). THD from RMS of leftover harmonics over fundamental.
5. Dead time and device drops: subtract \(2V_{CE}\) roughly from the DC bus if a numerical on-state is given; otherwise ideal.
6. Shoot-through check: never gate both devices in a VSI leg. CSI has the dual: never open the DC current path without a freewheel.

Worked pattern — three-phase 180° VSI: \(V_{dc}=600\,\mathrm{V}\). \(V_{LL,1}=0.780\times 600=468\,\mathrm{V}\) RMS. A 415 V motor is then slightly into field weakening or you PWM-down. Fifth harmonic voltage is \(V_1/5\), current roughly \(I_1/25\) on a pure \(L\).

## Mistakes

- Using \(V_{LL}=V_{dc}\) as the motor RMS voltage. The fundamental is \(0.78 V_{dc}\), not \(V_{dc}\).
- Mixing peak, peak-to-peak, and RMS of a square wave. Square-wave RMS is the amplitude, not amplitude/\(\sqrt{2}\).
- Applying single-phase \(4V_{dc}/\pi\) to a three-phase line voltage.
- Forgetting freewheel diodes on a VSI feeding an induction motor.
- Treating CSI and VSI harmonics as interchangeable (voltage harmonics vs current harmonics).
- Including triplen harmonics in line-to-line 180° VSI voltages.
- Computing power with total RMS voltage and fundamental current (mismatched pair).
- 120° vs 180° conduction mix-up in the six-switch bridge.
- Ignoring that a diode-rectifier front end cannot regenerate; a VSI motor going into generation dumps energy into the DC capacitor (brake chopper or active front end needed).

Inverters set the AC waveform. PWM (next unit) is how the same VSI reduces the low-order harmonics that this unit just computed for square-wave mode.

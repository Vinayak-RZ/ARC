# Phasors and AC steady state

Sinusoidal steady-state analysis replaces \( d/dt \) with \( j\omega \) and time-domain sinusoids with complex phasors. It applies only after transients have died, in linear time-invariant circuits driven by sinusoids of one frequency (or by superposition, several frequencies handled separately). This unit is the language of AC circuits: impedance, admittance, KCL/KVL in the phasor domain, and the polar/rectangular arithmetic UG students must make automatic.

## Concepts

A time sinusoid \( v(t) = V_m \cos(\omega t + \phi) \) maps to the phasor \( \mathbf{V} = V_m e^{j\phi} = V_m \angle \phi \), with the convention that the real part of \( \mathbf{V} e^{j\omega t} \) is the instantaneous signal. Some texts use RMS phasors \( \mathbf{V}_\mathrm{rms} = (V_m/\sqrt{2})\angle\phi \); never mix peak and RMS in one diagram. Frequency \( f = \omega/(2\pi) \) is the same throughout a linear network in the sinusoidal steady state; only amplitudes and phases differ.

Impedance \( \mathbf{Z} = \mathbf{V}/\mathbf{I} \) for a two-terminal element in the phasor domain. Resistor: \( Z_R = R \). Inductor: \( Z_L = j\omega L \). Capacitor: \( Z_C = 1/(j\omega C) = -j/(\omega C) \). Admittance \( Y = 1/Z \). Series impedances add; parallel admittances add. Ohm's law, KCL, and KVL hold for phasors exactly as for DC, because they are linear.

Leading and lagging: a current that peaks before the voltage across an element is leading (capacitive). A current that peaks after the voltage is lagging (inductive). The angle of \( \mathbf{Z} \) is \( \theta = \phi_v - \phi_i \). Reactance \( X = \mathrm{Im}(Z) \); \( X>0 \) inductive, \( X<0 \) capacitive.

Source transformation, nodal, mesh, Thévenin, Norton, superposition all transfer to phasors. Superposition of different frequencies must return to the time domain before adding (or keep separate phasors tagged by \( \omega \)). DC is the special case \( \omega = 0 \): inductors short, capacitors open.

Polar arithmetic: multiply magnitudes, add angles; divide magnitudes, subtract angles. Rectangular is required for addition. Convert every number to one representation before mixing. Euler's formula \( e^{j\theta} = \cos\theta + j\sin\theta \) is the only identity needed.

Frequency as a parameter: \( Z(\omega) \) is a function; a circuit that is inductive at one \( \omega \) may be capacitive at another. Resonance is the zero-reactance special case (next unit). Passive sign convention still governs instantaneous \( v(t)i(t) \); average power needs the next unit's RMS and cosine of angle.

Why phasors work: a linear ODE with constant coefficients, driven by Re{Ve^{jωt}}, has a particular solution of the same form. Substituting converts each derivative to a jω factor. The homogeneous solution dies if the network is passive and has some R. “Steady state” means we have waited several time constants of the slowest pole. If a homework problem says “find i(t) for t>0 after a switch” and the source is sinusoidal, phasors alone are not enough unless it also says “long after” or “steady state.” If it says “AC circuit” without a switch, phasors are enough.

Polar versus rectangular is a discipline. Addition of two voltages: rectangular. Multiplication of V = IZ: polar is faster. A calculator in degree mode while the problem used radians in ωt = 400t is fine for the phase of Z, because ωt stays symbolic; but 30° must not be entered as 30 rad. Write angles with a degree sign. Convert 0.6435 rad to 36.87° if the rest of the problem is in degrees. Never add 30° to 0.5 rad.

Impedance of real components: a coil is jωL plus a series r, sometimes plus a stray C. A capacitor is 1/(jωC) plus ESR and a tiny ESL. At 50 Hz, a typical electrolytic still looks like C; at 100 kHz it may look like an inductor. UG problems state ideal L and C unless they give r. When they give a coil “100 mH, 12 Ω,” that 12 Ω is in series at the working frequency by assumption.

Nodal phasors use complex Y: G + jωC + 1/(jωL). Mesh uses complex Z. Supernodes still exist for floating voltage sources. The matrix is complex; invert with Cramer's rule by hand on 2×2, or separate real and imaginary and solve 4×4 real, which is usually worse. Keep the 2×2 complex.

Graphical phasor diagrams are not optional decoration. For series RL, draw I along the real axis, VR in phase, VL leading I by 90°, Vs as the vector sum. For parallel RC, draw V along the real axis, IR in phase, IC leading by 90°. The diagram tells you whether an answer with VL larger than Vs is possible (yes, in RLC). It also catches a capacitor drawn as lagging.

Multiple frequencies: a DC offset plus 50 Hz plus 150 Hz is three phasor problems plus a DC problem. Time-domain v(t) is the sum of the four reconstructions. You cannot draw one phasor diagram for all of them. Power, however, will need RMS of the sum, which is the root-sum-square of the component RMS values for orthogonal harmonics (next unit).

## Equations

\( v(t) = \mathrm{Re}\{\mathbf{V} e^{j\omega t}\} \) with \( \mathbf{V} = V_m \angle \phi \).

\( Z_L = j\omega L \), \( Z_C = 1/(j\omega C) \), \( Z_R = R \).

\( \mathbf{V} = \mathbf{Z}\mathbf{I} \). Series: \( Z_\mathrm{eq} = \sum Z_k \). Parallel: \( 1/Z_\mathrm{eq} = \sum 1/Z_k \).

Voltage division: \( \mathbf{V}_k = \mathbf{V} Z_k / \sum Z \). Current division with admittances analogously.

Nodal: \( \mathbf{Y}\mathbf{V} = \mathbf{I}_s \). Mesh: \( \mathbf{Z}\mathbf{I} = \mathbf{V}_s \).

Impedance rectangular: \( Z = R + jX \), \( |Z| = \sqrt{R^2+X^2} \), \( \theta = \tan^{-1}(X/R) \) in the correct quadrant.

Time-domain reconstruction: \( i(t) = I_m \cos(\omega t + \psi) \) if \( \mathbf{I} = I_m\angle\psi \).

## Methods

Convert all sources to cosine (or all to sine) of the same \( \omega \). Draw the impedance circuit. Solve as if DC with complex numbers. Convert answers back to instantaneous form if asked. For multiple sources at the same \( \omega \), keep phasors and superpose in the complex plane. For different \( \omega \), solve separately and add time functions.

Choose RMS or peak and write it on the schematic. If a problem gives “120 V RMS, 50 Hz,” the phasor magnitude is 120 if you work in RMS, or \( 120\sqrt{2} \) if peak. Power formulas in the next unit assume a consistent choice.

Check: at high frequency capacitors tend to shorts and inductors to opens; at low frequency the opposite. A computed current through a capacitor leading its voltage by 90° is a sanity check. Angle of a passive impedance must lie in \([-90^\circ, +90^\circ]\).

A conversion drill: 8 − j6 Ω is 10∠−36.87°. Times 2∠20° A is 20∠−16.87° V. Back to time domain with ω known: 20 cos(ωt − 16.87°) if 20 was a peak phasor. If 20 was RMS, the time-domain peak is 20√2. Write which. Another drill: three series Z of 10, j10, −j5. Sum is 10 + j5 = 11.18∠26.57°, not 25 Ω. Draw the polygon. Nodal 2×2 with Y = 0.02−j0.01 and a mutual 0.005 should be inverted by hand once in a lifetime so SPICE is not magic. Then trust SPICE for 20-node AC sweeps.

## Mistakes

Adding two phasors of different frequencies. Using \( \omega \) in hertz in \( j\omega L \). Treating \( -j \) as \( j \) for capacitors. Mixing peak voltage with RMS current in \( V = IZ \). Applying DC inductor-short rules to 50 Hz. Writing \( \tan^{-1}(X/R) \) and dropping the quadrant when \( R<0 \) (active) or when adding voltages. Forgetting that KVL around a loop of phasors is a vector polygon, not a scalar sum of RMS values. Using time-domain derivatives on phasors. Reporting \( |V_1| + |V_2| \) as the series voltage magnitude. Assuming the current is in phase with the source voltage in an RLC loop. Copying a Thévenin impedance but attaching it with a time-domain cosine source mixed into the phasor circuit. Using RMS addition of voltages that are not in phase. Treating j as a number you can cancel from numerator and denominator without tracking angle, then losing 90°. Writing ω = 50 for a 50 Hz inductor instead of 314 rad/s. Forgetting that a DC term in a mixed source needs a separate DC circuit, not a phasor at ω = 0 stuffed into the same complex matrix as 50 Hz unless you really mean ω = 0. Reporting the imaginary part of a current as “the reactive current in amperes RMS” without the correct geometric interpretation. A further drill: convert 120∠−90° V RMS to 120√2 cos(ωt − 90°) = 120√2 sin(ωt) peak instantaneous, not 120 sin(ωt). Keep the √2. When a problem states “phasor diagram not to scale,” still check that the right angle at an inductor is actually 90° in your sketch, because a 60° sketch produces a wrong graphical sum even if the arithmetic was never done.

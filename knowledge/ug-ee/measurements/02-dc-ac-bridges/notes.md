# DC and AC bridges: Wheatstone, Kelvin, Maxwell, Schering, Wien

A bridge is a null instrument: you adjust until a detector reads zero, then the unknown is a ratio of standards. Null methods beat deflection methods for precision because the detector only needs sensitivity, not a calibrated scale, and because source-amplitude drift drops out of a balance equation that is homogeneous in voltage. This unit is the DC Wheatstone and Kelvin double bridges and the AC family used in a first measurements course: Maxwell’s inductance bridge, Hay (mentioned as the high-Q cousin), Schering for capacitance and dissipation, and Wien for frequency or a parallel RC. Wagner earth and detector/source swap are practical details that keep a balance from being a theatre of stray capacitance.

## Concepts

Wheatstone: four resistances \( P,Q,R,S \) in a diamond, source on one diagonal, galvanometer on the other. Balance \( P/Q = R/S \) (or \( P/R = Q/S \), depending on which arms you call ratio arms). The unknown is usually \( S = R\,P/Q \) with \( P/Q \) a decade ratio and \( R \) a decade box. Sensitivity is highest when the four arms are comparable and the galvanometer is matched to the Thevenin resistance seen from the detector nodes. Thevenin resistance of a balanced Wheatstone with source internal resistance neglected is the parallel of the two divider pairs. A low-resistance unknown is a bad Wheatstone problem: lead and contact resistance sit in series with the unknown and are not rejected.

Kelvin double bridge exists to measure milliohms to a few ohms (shunts, transformer winding DC resistance, bus bars). The unknown \( R_x \) and a standard \( R_s \) carry the same heavy current. Two ratio pairs \( p/q \) and \( p'/q' \) are used; a yoke (the “link”) of small but unknown resistance \( r \) joins \( R_x \) and \( R_s \). If the second ratio equals the first, \( p/q = p'/q' \), the yoke resistance drops out of the balance and \( R_x = R_s\,p/q \). That is the whole point. Potential leads must be taken from the inner voltage terminals of a four-terminal resistor. Using two-terminal connections on a shunt makes the Kelvin bridge a Wheatstone with extra wiring.

Maxwell’s inductance-capacitance bridge (Maxwell-Wien) measures an unknown inductance \( L_x \) with series resistance \( R_x \) against a parallel combination of a variable capacitor \( C \) and resistor \( R_3 \) in one arm, with two non-reactive ratio arms \( R_2,R_4 \). Balance (one common arm labelling) gives \( L_x = R_2 R_4 C \) and \( R_x = R_2 R_4 / R_3 \). It is convenient for medium Q (say 1 to 10) because both balances are independent of frequency if the components are ideal. Hay’s bridge puts the capacitor in series with a resistor in the known arm and is preferred for high-Q coils (small dissipation): the balance then involves \( \omega \) and you must know frequency.

Anderson’s bridge is a Maxwell variant with an extra resistor and the detector relocated so that a fixed capacitor can be used; UG courses mention it as a laboratory inductance bridge with a good Q range. Mutual inductance bridges (Carey-Foster, Heaviside) appear in older syllabi; if they appear, they still reduce to a null of two voltage drops.

Schering bridge measures a capacitor \( C_x \) with loss modelled as a series \( R_x \) (or a parallel \( G_x \)). A typical arm set: unknown in one arm, a lossless standard capacitor \( C_s \) in the adjacent arm, and in the opposite arm a parallel \( C_4 \) across \( R_4 \), with \( R_3 \) the remaining arm. Balance yields \( C_x = C_s R_4/R_3 \) and \( R_x = R_3 C_4 / C_s \) (check the figure you were given: textbooks permute labels). Dissipation factor \( D = \omega C_x R_x = \omega C_4 R_4 \) in that labelling — \( D \) comes from the operator’s \( C_4,R_4 \) and frequency, which is why Schering is also a tanδ bridge for insulation. For high-voltage Schering, \( C_s \) is a compressed-gas standard, the low arms are near ground, and a guarded detector is mandatory.

Wien bridge: a series RC in one arm and a parallel RC in the adjacent arm, two resistors completing the diamond. At balance, \( \omega^2 = 1/(R_1 R_2 C_1 C_2) \) and a resistance ratio equals a capacitance ratio (for equal components, \( R_3/R_4 = 2 \)). Used as a frequency-selective network (Wien oscillator) and as an audio-frequency measuring bridge. It is not a general impedance bridge; it is tuned to one frequency.

AC detectors: vibration galvanometer (historical, tuned), headphones (audio), CRO, or a phase-sensitive detector / lock-in. A DMM AC voltmeter is a blunt detector; it does not tell you in-phase versus quadrature, so you chase two knobs blindly. A phase-sensitive detector lets you balance resistive and reactive conditions almost independently.

Wagner earth: an auxiliary divider from source to earth, adjusted so that the detector terminals sit at earth potential. Stray capacitances from detector leads to earth then carry no voltage and disappear from the balance. Essential on AC capacitance work; optional on DC.

Source and detector may be interchanged in a four-arm bridge (reciprocity) without changing the balance equation; sensitivity and the effect of source impedance do change. Never interchange them in a Kelvin double bridge without redrawing: the current leads and potential leads are not a simple diamond.

Balance conditions are two real equations (real and imaginary, or magnitude and phase). You need two adjustable elements, or one element plus frequency. A single knob cannot generally null an AC bridge.

Q-factor of a coil \( Q=\omega L/R \). Maxwell’s parallel-capacitor arm is awkward when \( Q \) is very high (the parallel \( R_3 \) becomes huge). Hay is then cleaner. For a lossy capacitor, series \( R_x \) is small; Schering’s \( D=\omega C R \) is the quantity insulation people quote, not \( Q=1/D \).

Strays: residual inductance of resistors, lead inductance, and the capacitance of a decade box. Substitution methods (replace the unknown by a standard without disturbing geometry) cancel a large class of strays. A coaxial construction and a three-terminal capacitor (guard) are how precision capacitance labs look; a student breadboard is not that.

## Equations

Wheatstone balance:

\[
\frac{P}{Q}=\frac{R}{S}\quad\Rightarrow\quad S=R\frac{P}{Q}.
\]

Thevenin resistance seen by the galvanometer (balanced, ideal source):

\[
R_{th}=\bigl(P\parallel Q\bigr)+\bigl(R\parallel S\bigr).
\]

Kelvin double bridge (equal ratios):

\[
\frac{p}{q}=\frac{p'}{q'}\quad\Rightarrow\quad R_x=R_s\frac{p}{q}.
\]

(The yoke \( r \) cancels only when the two ratios match.)

Maxwell inductance-capacitance (one standard labelling: unknown \( L_x,R_x \); opposite arm \( R_3\parallel C_3 \); ratio arms \( R_2,R_4 \)):

\[
L_x=R_2 R_4 C_3,\qquad R_x=\frac{R_2 R_4}{R_3}.
\]

Hay (high Q; series \( r,C \) in the known arm) involves \( \omega \):

\[
L_x=\frac{R_2 R_4 C}{1+\omega^2 r^2 C^2},\qquad
R_x=\frac{R_2 R_4 r \omega^2 C^2}{1+\omega^2 r^2 C^2}.
\]

For \( Q=\omega L_x/R_x\gg 1 \), \( L_x\approx R_2 R_4 C \).

Schering (labelling: \( C_x,R_x \) series unknown; \( C_s \) standard; \( R_3 \); \( R_4\parallel C_4 \)):

\[
C_x=C_s\frac{R_4}{R_3},\qquad R_x=R_3\frac{C_4}{C_s},\qquad D=\omega C_x R_x=\omega C_4 R_4.
\]

Wien (series \( R_1,C_1 \); parallel \( R_2,C_2 \); ratio \( R_3/R_4 \)):

\[
\omega_0^2=\frac{1}{R_1 R_2 C_1 C_2},\qquad
\frac{R_3}{R_4}=\frac{R_1}{R_2}+\frac{C_2}{C_1}.
\]

Equal components \( R_1=R_2=R \), \( C_1=C_2=C \): \( \omega_0=1/(RC) \), \( R_3/R_4=2 \).

Small-deflection sensitivity (Wheatstone): galvanometer current \( \approx V_s \delta/(4R) \) for equal arms \( R \) and fractional unbalance \( \delta \) in one arm — order-of-magnitude only; derive from the Thevenin open-circuit unbalance voltage \( V_s \delta/4 \) divided by \( R_{th}+R_g \).

## Methods

Draw the diamond, label every arm, write two voltage-divider expressions from a source node to the two detector nodes, set them equal, separate real and imaginary parts. Do not memorize twelve labelled figures: derive. If the problem gives a figure with \( Z_1 Z_2 = Z_3 Z_4 \), use that product form (adjacent arms).

For Maxwell, confirm which arm contains the parallel RC. If you swap series versus parallel, you have Hay or a wrong \( L_x \). Check Q: \( Q=\omega L_x/R_x = \omega C_3 R_3 \) in the Maxwell labelling above. If that Q is 50 and they still used Maxwell, mention that Hay would be preferred.

Kelvin: always verify \( p/q=p'/q' \) is stated or adjusted. If the ratios are unequal, the yoke term remains: there is a correction \( R_x = R_s p/q + r\cdot(\text{ratio mismatch}) \). Do not ignore \( r \) unless equality is given.

Schering at high voltage: compute \( D=\omega C_4 R_4 \) first if they ask tanδ; then \( C_x \). Frequency must be known. 50 Hz versus 60 Hz is a 20% change in \( D \) if you use the wrong \( \omega \).

Wien as a frequency meter: if \( C_1=C_2 \) and \( R_1=R_2 \) are ganged, \( f=1/(2\pi RC) \). If the ratio arm is not 2, you are not at the equal-component balance; do not use \( 1/(2\pi RC) \).

Procedure in a lab: (1) choose a detector that can see the unbalance (DC galvo vs AC lock-in), (2) set ratios so the unknown is mid-range of the decade box, (3) for AC, balance in-phase then quadrature, iterate, (4) Wagner-earth if the null is shallow or hand-wave sensitive, (5) reverse the source if thermal EMFs are suspected (DC), (6) write the formula that matches the figure actually wired.

Uncertainty: the relative error of \( S=RP/Q \) is the sum of relative errors of \( R,P,Q \) (limiting). Decade boxes have residual reactance; at 1 kHz a “non-inductive” resistor still has a few nH to µH — enough to spoil a precision Maxwell if you pretend it is purely real.

## Mistakes

Using Wheatstone on a 0.05 Ω shunt without four-terminal (Kelvin) connections.

Forgetting that Kelvin cancellation of the yoke requires matched ratios, not merely “a double bridge.”

Maxwell versus Hay: applying \( L=R_2 R_4 C \) to a Hay figure without the \( 1+\omega^2 r^2 C^2 \) denominator.

Writing Schering \( D=\omega C_x R_x \) with \( f \) in hertz but using \( \omega=f \) instead of \( 2\pi f \).

Wien: using \( f=1/(2\pi RC) \) when the two time constants differ.

Treating the galvanometer as a voltmeter with a calibrated scale: at balance the current is zero; off balance you only need direction and a sense of “closer.”

Ignoring source frequency on Hay and on Schering \( D \), or assuming Maxwell’s \( L_x=R_2 R_4 C \) holds when the ratio arms are reactive.

Swapping source and detector on a Kelvin current circuit.

Not guarding a three-terminal capacitor: cable capacitance lands in parallel with \( C_x \) and you measure the cable.

Reporting \( L_x \) in henries when \( R_2 R_4 C \) was computed with mixed kΩ and nF without converting to SI (the classic \( 10^{\pm 3} \) or \( 10^{\pm 9} \) disaster).

Chasing a null that is limited by harmonics: an AC bridge balanced at the fundamental can still show a detector reading if the source is distorted and the unknown is nonlinear (iron-cored coil). Use a frequency-selective detector or a better source.

A muscle-memory Wheatstone: \( P=1000\,\Omega \), \( Q=100\,\Omega \), \( R=351.2\,\Omega \), \( S=R P/Q = 3512\,\Omega \). If \( R \) has 0.05% limiting error and the ratio arms 0.02% each, \( \Delta S/S = 0.09\% \).

Muscle-memory Maxwell: \( R_2=400\,\Omega \), \( R_4=300\,\Omega \), \( C_3=0.250\,\mu\mathrm{F} \), \( R_3=5.00\,\mathrm{k}\Omega \). \( L_x = 400\times 300\times 0.250\times 10^{-6} = 0.0300 \) H. \( R_x = 400\times 300 / 5000 = 24.0\,\Omega \). At 1 kHz, \( Q=\omega L/R = 2\pi\times 1000\times 0.03/24 = 7.85 \), a Maxwell-friendly coil.

Muscle-memory Schering: \( C_s=100 \) pF, \( R_3=1000\,\Omega \), \( R_4=318\,\Omega \), \( C_4=0.50 \) nF, \( f=50 \) Hz. \( C_x = 100\times 318/1000 = 31.8 \) pF. \( D=\omega C_4 R_4 = 2\pi\times 50\times 0.50\times 10^{-9}\times 318 = 5.00\times 10^{-5} \). Tiny D is a good gas capacitor; a plastic film would be larger.

Muscle-memory Wien: \( R=10.0\,\mathrm{k}\Omega \), \( C=15.9 \) nF, equal arms, \( R_3/R_4=2 \). \( f=1/(2\pi RC)=1/(2\pi\times 10^4\times 15.9\times 10^{-9})=1000 \) Hz.

If a problem gives an unbalanced Wheatstone and asks galvanometer current, you must include \( R_g \) and the source resistance; the balance formula does not apply. Compute the two divider voltages, their difference, and \( R_{th} \) with the detector removed, then \( I_g=V_{th}/(R_{th}+R_g) \).

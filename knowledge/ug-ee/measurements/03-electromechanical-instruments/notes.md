# Electromechanical instruments: PMMC, moving iron, electrodynamometer

Analog pointer instruments convert a torque into a scale reading. Three UG mechanisms cover almost every exam: the permanent-magnet moving-coil (PMMC) milliammeter and its voltmeter/ammeter extensions; moving-iron (MI) attraction and repulsion instruments for AC or DC RMS-ish current and voltage; and the electrodynamometer used as a transfer instrument and as a wattmeter. Damping, controlling torque, range extension by shunts and multipliers, and the difference between average, RMS, and true power are the supporting ideas. Digital meters (unit 05) did not make these torque equations obsolete: they still explain why a PMMC on AC reads zero, why MI reads a square-wave differently from a dynamometer, and why a wattmeter connection error can reverse or double.

## Concepts

A pointer instrument needs three torques. Deflecting torque \( T_d \) comes from the measurand (ampere-force on a coil, or iron in a field). Controlling torque \( T_c \) comes from springs (or gravity in older meters) and is proportional to angle, \( T_c = k_s \theta \), so that at rest \( T_d=T_c \) gives a unique \( \theta \). Damping torque \( T_{damp} \) is viscous in angle rate: eddy currents in a PMMC aluminium former, air vane, or oil. Underdamped meters oscillate; overdamped meters crawl; critical damping is the usual design aim. Without control springs a PMMC would slam to the stop; without damping it would swing forever.

PMMC (D’Arsonval): a coil in a radial permanent-magnet field, current \( I \) in \( N \) turns of area \( A \). Torque \( T_d = NBA I \) (uniform radial field). Scale is linear in current. The movement measures average current, because inertia and damping make \( \theta \) follow the mean torque. On a sinusoid the mean of \( I \) is zero, so a PMMC reads zero AC unless you rectify. A rectifier PMMC (AC voltmeter) is average-responding, scaled to read RMS of a sine: it is wrong on other waveforms by the form-factor ratio. Sensitivity of a voltmeter is ohms per volt: \( R_m / V_{\mathrm{FSD}} = 1/I_{\mathrm{FSD}} \). A 50 µA movement is 20 kΩ/V. Range extension: series multiplier \( R_{se} = V/I_m - R_m \) for a voltmeter; shunt \( R_{sh} = I_m R_m /(I-I_m) \) for an ammeter. Swamping resistance of manganin in series with the copper coil reduces temperature error of a PMMC millivoltmeter.

Moving iron: a piece of iron is sucked into a coil (attraction type) or two irons repel (repulsion type). Torque goes as \( I^2 \mathrm{d}L/\mathrm{d}\theta \) (energy method): the instrument reads RMS for a periodic current if the iron does not saturate and if frequency is not so high that eddy currents and coil inductance ruin the current. Scale is cramped at the low end (square law) unless the iron geometry is shaped to linearize. MI works on DC and AC; on DC, hysteresis of the iron can shift the reading. Used as cheap AC panel voltmeters and ammeters. Frequency error: inductive reactance of the coil plus eddy-current shielding. A MI voltmeter needs a series swamping resistor, mostly non-inductive, to keep the current in the coil closer to \( V/R \).

Electrodynamometer: two coils, one fixed (field) and one moving, no iron in the best instruments (air-cored). Torque \( \propto I_1 I_2 \mathrm{d}M/\mathrm{d}\theta \). As an ammeter, both coils carry the current (or a shunt fraction): \( T_d \propto I^2 \), RMS. As a voltmeter, both coils in series with a multiplier: RMS voltage. As a wattmeter, the current coil is in series with the load and the pressure (voltage) coil is across the load through a series resistor \( R_p \): average torque \( \propto \overline{v i} \), true average power, including on non-sinusoids if the coils follow the waveforms (limited bandwidth). Dynamometer wattmeter reads \( VI\cos\phi \) on sinusoids. Connection: current coil toward the supply for the “system” convention, pressure coil on the load side or supply side with a compensation for coil loss. Low-power-factor wattmeters have a weak controlling spring and compensated pressure-coil current so that at \( \cos\phi=0.2 \) you still have a usable deflection.

Compensation: pressure-coil current is not exactly the load voltage over \( R_p \) if you include the current-coil drop; a compensating coil or a connection choice (pressure coil supply-side versus load-side) reduces the error. For a voltmeter used with an ammeter to get power on DC, you have the same two-connection problem: you either include the ammeter drop in the voltmeter or the voltmeter current in the ammeter.

Three-phase power: two-wattmeter method, \( P=W_1+W_2 \), \( \tan\phi=\sqrt{3}(W_1-W_2)/(W_1+W_2) \) on a balanced load. A single wattmeter plus a switching box is a laboratory cousin. Reactive power needs a 90° phase-shift network or a varmeter.

Creeping, friction, and residual magnetism: MI and dynamometer have more friction than a jewelled PMMC. Tapping the case is a shameful but traditional way to free a stuck pointer; a better instrument has spring-loaded jewels and is used in the intended orientation.

Hot-wire and electrostatic instruments: hot-wire (expansion from \( I^2 R \)) is true RMS, slow, obsolete as a student meter. Electrostatic voltmeter (attraction of plates) measures RMS voltage at high V with tiny current — still used as a high-voltage transfer device. Thermocouple true-RMS: a heater and a thermocouple; square-law, true RMS, fragile overload.

Damping and time: a laboratory PMMC can have a 1 s settling time; do not read it while it is swinging. A wattmeter on a motor start-up is not a transient recorder; use a DSO (unit 05).

Earth and polarity: PMMC has polarity; reverse DC pegs the stop the other way. MI and dynamometer on AC do not show polarity. Wattmeter current-coil and pressure-coil polarity marks (±) must be respected or the pointer drives backward.

## Equations

PMMC deflecting torque and balance:

\[
T_d = NBA I = k_s \theta \quad\Rightarrow\quad \theta = \frac{NBA}{k_s} I.
\]

Voltmeter multiplier and ammeter shunt:

\[
R_{se}=\frac{V}{I_m}-R_m,\qquad
R_{sh}=\frac{I_m R_m}{I-I_m},\qquad
m=\frac{I}{I_m}=1+\frac{R_m}{R_{sh}}.
\]

Ohms per volt: \( 1/I_{\mathrm{FSD}} \).

Moving-iron energy torque:

\[
T_d=\frac{1}{2}I^2\frac{\mathrm{d}L}{\mathrm{d}\theta}.
\]

Electrodynamometer:

\[
T_d = I_1 I_2 \frac{\mathrm{d}M}{\mathrm{d}\theta}.
\]

Wattmeter mean torque \( \propto \overline{v i} = P \). Sinusoidal: \( P=VI\cos\phi \).

Rectifier PMMC on a sine, scaled as RMS: form factor \( \pi/(2\sqrt{2})\approx 1.11 \). On a square wave of amplitude \( A \), true RMS is \( A \), average of absolute is \( A \), so a sine-calibrated rectifier meter reads \( A/1.11 \approx 0.90 A \).

Two-wattmeter (balanced, star or delta):

\[
W_1+W_2=P_{3\phi},\qquad
W_1=V_L I_L\cos(30^\circ+\phi),\quad
W_2=V_L I_L\cos(30^\circ-\phi).
\]

Swamping: coil copper \( R_c(T)=R_{c0}(1+\alpha\Delta T) \), series manganin \( R_s \) nearly \( \alpha\approx 0 \), so the relative temperature error of a millivoltmeter shrinks by \( R_c/(R_c+R_s) \).

## Methods

To extend a PMMC: always start from \( I_m \) and \( R_m \) of the movement. For a multi-range ammeter, Ayrton (universal) shunt keeps the movement-plus-shunt loop closed when switching ranges so the movement is never open in a current circuit. For a multi-range voltmeter, a string of multipliers, one per range, with the movement at the bottom.

To decide which instrument: DC milliamps, linear, polarity — PMMC. AC RMS panel, cheap — MI. Transfer standard DC↔AC or true power — dynamometer. True RMS of a distorted waveform — thermal or a true-RMS DMM, not a rectifier PMMC and not an uncompensated MI if saturation or frequency error is in play.

Wattmeter errors to write down before connecting: (1) pressure-coil current not equal to load current (connection), (2) current-coil voltage drop, (3) phase defect of the pressure coil (inductance of the coil versus \( R_p \)) which looks like a PF error, (4) stray fields on an unshielded dynamometer, (5) frequency. Compensation coil and a series capacitor in the pressure circuit are the textbook fixes for (3).

Reading a non-linear MI scale: interpolate on the printed scale, not on a linear ruler across the glass.

For rectifier instruments, state the waveform. If the problem does not specify sine, do not assume the 1.11 factor.

Overload: a PMMC movement is typically 50 µA to 10 mA full scale; a shunt can still burn while the movement survives, or the reverse if the shunt goes open. Fuses on the 10 A range of a multimeter are not optional decoration.

## Mistakes

Using a PMMC on AC and calling the zero reading “no voltage.”

Treating a rectifier AC voltmeter as true RMS on a triac waveform.

Applying MI \( T\propto I^2 \) and then expecting a linear scale without looking at \( \mathrm{d}L/\mathrm{d}\theta \).

Wattmeter: swapping current-coil and pressure-coil connections to the load (the pressure coil cannot carry line current).

Two-wattmeter: taking \( W_1-W_2 \) as power, or forgetting that one wattmeter can reverse at PF \( < 0.5 \).

Computing \( R_{sh} \) with \( I \) instead of \( I-I_m \) in the denominator.

Ohms-per-volt using FSD current of a different range.

Ignoring temperature on a copper coil millivoltmeter without swamping.

Calling a dynamometer wattmeter reading “VA” or “VAR.”

Reading a 0–5 A MI at 0.3 A as if the class index still gave a tight percent-of-reading (it is percent of FSD, and the scale is weak at the bottom).

A worked PMMC: movement \( 5 \) mA, \( 20\,\Omega \). 0–10 A ammeter: \( R_{sh}=0.005\times 20/(10-0.005)=0.010005\,\Omega \approx 0.0100\,\Omega \). 0–100 V voltmeter: \( R_{se}=100/0.005 - 20 = 19980\,\Omega \). Sensitivity \( 200 \) Ω/V.

Worked wattmeter: \( V=230 \) V, \( I=4.0 \) A, \( \mathrm{PF}=0.6 \) lag, \( P=552 \) W. If the pressure coil is 0.05 A, 2000 Ω, the pressure-coil loss is \( (230)^2/2000=26.45 \) W if connected on the load side you may include that loss in \( P \); subtract it if you wanted load power only. Always state which power.

Worked two-wattmeter: balanced 400 V line, 5 A line, PF 0.5 lag so \( \phi=60^\circ \). \( W_1=400\times 5\cos(90^\circ)=0 \), \( W_2=400\times 5\cos(30^\circ)=1732 \) W, sum 1732 W, and \( P=\sqrt{3}\times 400\times 5\times 0.5=1732 \) W. At PF 0.5 one meter is zero, not broken.

Worked form factor: sine \( V_m=100 \) V, true RMS \( 70.71 \) V, rectifier meter (sine-calibrated) reads 70.71 V. Square wave \( \pm 70.71 \) V has true RMS 70.71 V but the sine-calibrated rectifier reads \( 70.71/1.11=63.7 \) V. A dynamometer voltmeter reads 70.71 V on both (ideal).

Worked MI: if \( L(\theta)=L_0+k\theta \) with \( k \) constant, \( T_d=\frac12 I^2 k \), scale \( \propto I^2 \). If the iron is shaped so \( \mathrm{d}L/\mathrm{d}\theta \propto 1/I^2 \) you cannot do that independently of \( I \); you shape so \( \mathrm{d}L/\mathrm{d}\theta \) falls as \( \theta \) rises to stretch the upper scale. Do not fight the figure: read the printed scale.

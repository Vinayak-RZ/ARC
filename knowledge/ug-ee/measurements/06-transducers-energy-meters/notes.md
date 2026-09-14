# Transducers and induction energy meters

A transducer converts a physical measurand into an electrical signal that a meter, ADC, or energy register can accept. This unit is the UG set: resistive strain gauges, RTDs and thermocouples for temperature, a sketch of LVDT and piezoelectric devices, and the induction-type single-phase energy meter that still appears in every measurements syllabus even where utilities have gone digital. Phantom loading, meter constants, and creeping complete the energy-meter story. Transducer circuits reuse the Wheatstone bridge (unit 02) and error combination (unit 01).

## Concepts

Strain gauge: a metal foil or semiconductor whose resistance changes with strain. Gauge factor \( G_f = (\Delta R/R)/\varepsilon \) with \( \varepsilon=\Delta L/L \). Metal foils have \( G_f \) near 2; semiconductors can be 50–200 but are more temperature-sensitive and nonlinear. A single active gauge in a Wheatstone quarter-bridge gives a small \( \Delta V \) at the detector: \( V_o \approx V_s G_f \varepsilon / 4 \) for equal arms. Temperature expansion of the specimen and of the gauge looks like strain; a dummy gauge on an unstrained piece of the same metal, in an adjacent arm, cancels common-mode temperature. Half-bridge and full-bridge arrangements increase sensitivity and cancel temperature better. Poisson gauges (transverse) appear in rosettes. Lead resistance in a quarter-bridge is a systematic error; three-wire RTD-like compensation exists for gauges too. Bonding, alignment, and transverse sensitivity are laboratory realities: a gauge at 45° is not measuring the axial strain you wrote in the lab report.

RTD (resistance temperature detector): platinum (Pt100) is 100 Ω at 0 °C, \( \alpha\approx 0.00385\,\mathrm{K}^{-1} \) in the industrial Callendar range. Callendar–Van Dusen equation adds a small quadratic (and a \( W \) term below 0 °C). Two-wire connection dumps lead resistance into the reading; three-wire cancels matched leads in a bridge; four-wire Kelvin is the laboratory method. Self-heating: excitation current \( I^2 R \) warms the element; use 1 mA or so for a Pt100 unless the problem states otherwise. Nickel and copper RTDs exist; copper is linear-ish but low R.

Thermocouple: two dissimilar metals, Seebeck EMF \( E\approx \alpha_{AB}(T_h-T_c) \) for small ranges, actually a polynomial (NIST types J, K, T, E, S, R, B). You always measure a difference: the cold junction must be known (ice bath, or cold-junction compensation with an RTD at the terminals). Type K (Chromel–Alumel) is the student workhorse, ~41 µV/°C near room temperature. Polarity, extension wire of the same type, and not introducing a third metal at a temperature gradient are the practical rules. A thermocouple is not a thermometer by itself; it is a differential EMF source of a few millivolts.

Thermistor: semiconductor, large negative \( \alpha \) (NTC), Steinhart–Hart equation, sensitive in a narrow band, nonlinear, self-heating easy. Used in protection and cheap probes more than in precision lab thermometry.

LVDT: linear variable differential transformer. A core moves in a transformer with two opposing secondaries; the differential AC voltage is linear with displacement over a stroke, phase tells direction. Null at centre. Needs an AC excitation and a demodulator (phase-sensitive rectifier). Excellent resolution, contactless.

Piezoelectric: charge \( q=d F \) for a force; good for dynamic pressure and vibration, not for static force (charge leaks). Needs a charge amplifier.

Photovoltaic / photoconductive: light meters; photodiode current ~ irradiance in reverse bias (photoconductive mode) or photovoltaic mode. UG mention only.

Energy meter, induction type, single phase: a light aluminium disc is driven by the interaction of fluxes from a pressure (voltage) coil and a current coil, exactly so that the instantaneous torque is proportional to \( vi \) and the average torque to average power. A braking magnet provides a drag \( \propto \) speed, so speed \( \propto \) power and the number of revolutions \( \propto \) energy. Meter constant \( K \) in rev/kWh (or the inverse, Wh/rev). Registration \( E = N/K \) if \( K \) is rev/kWh. Creeping: disc turns with no load because of slight voltage-coil torque; a magnetic brake hole or a stop pin limits it. Light-load compensation (shading ring, lag coil) and friction compensation are adjustments. Power-factor: the voltage-coil flux must lag the voltage by nearly 90° so that the driving torque follows \( \cos\phi \); a lag plate (copper shading) adjusts that quadrature. If the lag adjustment is wrong, the meter is fast or slow at lagging PF even if it is right at unity.

Phantom (fictitious) loading: to test a meter at 10 A, 230 V, 0.5 PF without a 2.3 kW load, energize the voltage coil at rated V from one source and the current coil from a low-voltage high-current source, with a phase-shifting arrangement if PF is required. Power taken from the supply is small; the meter “thinks” it sees \( VI\cos\phi \). Nameplate current and voltage must still match the coils.

Three-phase energy: two-element induction meters (two discs or one disc two elements) analogous to two-wattmeter. CT/PT ratios multiply the meter constant as in unit 04.

Digital energy meters: sampling wattmeter + time, class 0.5 S / 0.2 S, harmonics, four-quadrant (import/export, Q). The induction disc is the syllabus object; the digital meter is what you will actually commission.

## Equations

Gauge factor and quarter-bridge:

\[
G_f=\frac{\Delta R/R}{\varepsilon},\qquad
\frac{V_o}{V_s}\approx\frac{G_f\varepsilon}{4}\quad(\text{one active arm, equal resistances}).
\]

Full-bridge four active gauges (two tensile, two compressive): \( V_o/V_s = G_f\varepsilon \) (ideal).

Pt100 linear sketch:

\[
R(T)=R_0\bigl(1+\alpha T\bigr),\quad R_0=100\,\Omega,\ \alpha=3.85\times 10^{-3}\ \mathrm{K}^{-1},\ T\ \mathrm{in\ °C}.
\]

Callendar (above 0 °C): \( R=R_0(1+AT+BT^2) \).

Seebeck (local):

\[
\mathrm{d}E=\alpha_{AB}(T)\,\mathrm{d}T,\qquad E=\int_{T_c}^{T_h}\alpha_{AB}(T)\,\mathrm{d}T.
\]

Induction meter:

\[
T_d \propto \Phi_v \Phi_i \cos\phi \propto V I \cos\phi,\qquad
T_b \propto n,\qquad n\propto P,\qquad E=\int P\,\mathrm{d}t \propto N.
\]

If \( K \) is rev/kWh: \( E_{\mathrm{kWh}}=N/K \). If \( k \) is Wh/rev: \( E_{\mathrm{Wh}}=N k \).

Percent error of an energy meter:

\[
\varepsilon=\frac{\text{measured}-\text{true}}{\text{true}}\times 100\%
=\frac{N_{\mathrm{actual}}-N_{\mathrm{true}}}{N_{\mathrm{true}}}\times 100\%.
\]

A “fast” meter has positive error (registers too much).

Phantom load true energy in time \( t \): \( E=V I t\cos\phi \) (use the actual coil V and I). Compare with \( N/K \).

## Methods

Strain: mount dummy gauge for temperature; use a stable \( V_s \); compute \( \varepsilon \) from \( G_f \) and \( \Delta R \) or from \( V_o \). Check that \( \Delta R/R \) is tiny (microstrain × 2): 1000 µε on \( G_f=2 \) is 0.2% of R.

RTD: three-wire or four-wire; convert \( R \) to \( T \) with the stated \( \alpha \) or table; do not use a thermocouple polynomial on an RTD.

Thermocouple: measure EMF, add cold-junction temperature correctly (if terminals are at 25 °C, you add the EMF that a table assigns from 0 to 25 °C, then invert the table for the hot junction — do not add 25 °C to a mV-linear guess except as a rough K-type 41 µV/°C estimate).

Energy meter test: run \( N \) revolutions, time them, compute true kWh from \( V,I,\mathrm{PF},t \), compare with \( N/K \). Adjust brake magnet for speed at rated load; adjust lag coil at 0.5 PF lag; check creeping at 50% or 110% voltage, no current (per the standard used in the lab).

Phantom: isolate which source feeds which coil; the product \( VI\cos\phi \) uses the voltage across the pressure coil and the current through the current coil, not the power drawn from the wall.

## Mistakes

Using \( G_f=2 \) on a semiconductor gauge.

Two-wire RTD on a long cable and blaming the platinum.

Thermocouple without cold-junction treatment, or using copper leads on a type-K extension.

Energy: mixing rev/kWh with Wh/rev (reciprocal).

Calling a fast meter “negative error.”

Phantom load: using supply-socket watts as the true energy.

Ignoring PF on an induction meter (lag adjustment).

Putting strain gauges in adjacent arms both in tension so temperature cancels but strain also cancels.

LVDT: reading the AC amplitude and throwing away phase, so the sign of displacement is lost.

Self-heating an RTD with 10 mA in still air and comparing to a thermocouple in a bath.

A strain walk-through: \( R=120\,\Omega \), \( G_f=2.10 \), \( \varepsilon=800\,\mu\varepsilon \). \( \Delta R = G_f \varepsilon R = 2.10\times 800\times 10^{-6}\times 120=0.2016\,\Omega \). Quarter-bridge \( V_s=10 \) V, \( V_o\approx 10\times 2.10\times 800\times 10^{-6}/4=4.20 \) mV.

Pt100: 100 Ω at 0 °C, 138.5 Ω at 100 °C with \( \alpha=0.00385 \). At 40 °C linear guess \( R=100(1+0.00385\times 40)=115.4\,\Omega \).

K-type sketch: 4.10 mV with cold junction 0 °C ≈ 100 °C if 41 µV/°C. If cold junction is 25 °C and you measure 4.10 mV, hot junction is about \( 100+25=125 \) °C in that linear model.

Energy: \( K=750 \) rev/kWh, 45 revolutions, \( E=45/750=0.060 \) kWh \( =60 \) Wh. True load 230 V, 2 A, PF 1, 8 min \( =480 \) s: \( E_{\mathrm{true}}=230\times 2\times 480=220800 \) J \( =61.33 \) Wh. Error \( (60-61.33)/61.33=-2.2\% \) (slow).

Phantom: voltage coil 230 V, current coil 5 A, PF 1, 6 min, \( K=1200 \) rev/kWh. True energy \( 230\times 5\times 360/1000=414 \) Wh \( =0.414 \) kWh. Expected revolutions \( 0.414\times 1200=496.8 \). If 510 rev, error \( (510-496.8)/496.8=+2.66\% \) fast.

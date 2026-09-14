# Digital instruments, CRO, and DSO; Lissajous

A digital multimeter (DMM) turns a voltage into a number by analog-to-digital conversion; a cathode-ray oscilloscope (CRO) or digital storage oscilloscope (DSO) turns a voltage into a picture versus time (or versus another voltage). This unit is dual-slope and related DMM techniques, probe loading, oscilloscope deflection and timebase, sampling and aliasing on a DSO, and Lissajous figures for frequency ratio and phase. Analog electromechanical meters (unit 03) still win on simplicity and true average power; the CRO wins on waveform and timing.

## Concepts

DMM analog front end: a range divider, possibly an RMS converter (true-RMS thermal or analog computing versus average-responding), then a DC ADC. Counting ADCs in UG courses: dual-slope (integrating) is the classic. Integrate the unknown \( V_x \) for a fixed time \( T_1 \) on an integrator; then discharge with a reference \( V_r \) of opposite polarity and time \( T_2 \) until the integrator returns to zero. \( V_x = V_r T_2/T_1 \). Power-line interference averages toward zero if \( T_1 \) is an integer number of line periods. Dual-slope is slow (a few readings per second) and excellent for DC meters. Successive-approximation (SAR) ADCs are faster; flash ADCs are fastest and expensive; sigma-delta is what many 6½-digit bench meters use. Resolution in bits: a 3½-digit display is 1999 counts, about 11 bits. Accuracy is not resolution: read the percent-of-reading plus digits spec (unit 01).

Autoranging, input impedance (often 10 MΩ on DC volts, much less on some current ranges via a shunt), fuse on the current jack, and the four-wire ohms mode for milliohms are practical DMM literacy. Never measure voltage with the leads in the 10 A jack. True-RMS DMMs have a crest-factor limit; a tall spike train can read wrong or overload the RMS converter even if the RMS is modest.

CRO analog: a cathode-ray tube with electrostatic deflection. Vertical deflection \( y = k_v v_y(t) \), horizontal \( x = k_h v_x(t) \) or a linear timebase ramp. Sensitivity in V/div, timebase in s/div. Bandwidth: a Gaussian-ish roll-off, rise time \( t_r \approx 0.35/B \) for a first-order-ish scope (the 0.35 number is the usual UG mnemonic). Probe: 1× versus 10×. A 10× probe is a 9 MΩ resistor plus a trim capacitor forming a compensated divider with the scope’s 1 MΩ ∥ 15 pF. Uncompensated, square waves sprout overshoot or rounded corners. 10× reduces loading (10 MΩ, few pF) and divides the signal by 10: you must set the probe factor on the DSO or multiply the scale. Ground lead inductance makes a loop; a short ground spring is required for nanosecond edges.

Triggering: edge, level, source (CH1, line, ext), slope. Without a stable trigger the display runs. Dual-trace: chop (low frequency, switches between channels during the sweep) versus alternate (one channel per sweep — bad for comparing two slow non-repetitive events). XY mode: timebase off, CH1 vs CH2, Lissajous.

DSO: samples through an ADC, stores, displays. Sampling rate \( f_s \) must satisfy Nyquist for the bandwidth you care about; more realistically 5–10 samples per period of the highest harmonic you want to see. Equivalent-time sampling (repetitive waveforms) can reconstruct faster edges than \( f_s \) would allow in one shot; single-shot captures are limited by real-time \( f_s \). Aliasing: a 1 kHz sine sampled at 1.5 kHz looks like 0.5 kHz. Use the analog bandwidth limit, a higher \( f_s \), or an anti-alias filter. Record length and time/div set how much history you see. 8-bit vertical resolution is typical on cheap DSOs (256 levels); averaging improves noise for repetitive signals.

Lissajous: two sinusoids, same frequency, phase \( \phi \). Ellipse; \( \sin\phi = \pm a/A \) where \( a \) is intercept on an axis and \( A \) is the max on that axis (several equivalent formulas: \( \sin\phi = Y_{\mathrm{intercept}}/Y_{\mathrm{max}} \)). Circle if equal amplitudes and \( \pm 90^\circ \). Line if \( 0^\circ \) or \( 180^\circ \) (slope sign). Frequency ratio \( f_y:f_x \) equals the number of horizontal tangencies : vertical tangencies (or loops on the axes). A 3:2 figure has three humps one way and two the other. Used to compare an unknown oscillator to a standard when you have no counter.

Frequency measurement with a CRO: periods on the graticule, \( T = (\#\text{div})\times(\text{time/div}) \), \( f=1/T \). A counter/timer is better; Lissajous against a standard is classical. Phase: dual-trace time delay \( \Delta t \), \( \phi=360^\circ \Delta t/T \), or Lissajous.

Digital voltmeter (bench) versus handheld DMM: integration time, guarding, 6½ digits, four-wire ohms, ratio mode. A student handheld is fine for 0.5% work and not for a 50 ppm resistor.

Isolation: a typical scope ground is mains earth. Measuring both ends of a shunt that is not earth-referenced with two grounded probes shorts something through the earth. Use isolated probes, a differential probe, or a battery DMM. This is a safety and a circuit-integrity issue.

FFT mode on a DSO is a DFT of the stored record (signals pack): window, bins, leakage. Do not treat a cheap FFT as a calibrated spectrum analyzer.

## Equations

Dual-slope:

\[
V_x = V_r\frac{T_2}{T_1}.
\]

If the clock is \( f_{\mathrm{ck}} \) and counts are \( N_1,N_2 \), \( T_2/T_1=N_2/N_1 \).

Scope:

\[
v = (\text{div})\times(\text{V/div})\times(\text{probe factor}),\qquad
T = (\text{div})\times(\text{s/div}),\qquad f=1/T.
\]

Rise time (UG mnemonic):

\[
t_r \approx \frac{0.35}{B},\qquad
t_{r,\mathrm{sys}}\approx\sqrt{t_{r,\mathrm{scope}}^2+t_{r,\mathrm{probe}}^2+t_{r,\mathrm{source}}^2}.
\]

10× probe compensation: time constants \( R_1 C_1 = R_2 C_2 \) with \( R_1=9\,\mathrm{M}\Omega \), \( R_2=1\,\mathrm{M}\Omega \), \( C_2=C_{\mathrm{scope}}+C_{\mathrm{cable}} \), \( C_1 \) trimmable.

Lissajous, equal frequency:

\[
\sin\phi = \frac{y_{\mathrm{intercept}}}{y_{\mathrm{max}}} = \frac{x_{\mathrm{intercept}}}{x_{\mathrm{max}}}.
\]

Frequency ratio: \( f_y/f_x = N_x/N_y \) where \( N_x \) is the number of points of tangency with a vertical line (count carefully; include both sides consistently).

Nyquist: \( f_s > 2 f_{\max} \). Aliased frequency \( |f - m f_s| \) nearest to DC, for integer \( m \).

Phase from dual-trace: \( \phi = 2\pi \Delta t / T \).

ADC quantization: \( q = \mathrm{FSR}/2^n \), quantization noise variance \( q^2/12 \) (uniform).

## Methods

DMM: choose a range so the reading uses most of the counts; record range and spec; use DC for DC, true-RMS AC for distorted AC, not the cheap average-responding AC mode. For resistance below 1 Ω, four-wire or a Kelvin bridge (unit 02).

CRO setup: (1) probe compensated on a square calibrator, (2) V/div and coupling (DC unless you must kill a huge offset — AC coupling hides DC and droops square waves), (3) time/div to show 2–5 periods, (4) trigger on the channel of interest, (5) measure with cursors, not eyeball if the DSO has them.

Lissajous phase: measure intercept and peak on the same axis; \( \phi \) in the correct quadrant from the tilt (ellipse leaning which way, trajectory direction if you can see it). Frequency ratio: count lobes against a locked standard.

DSO anti-alias: if a “50 Hz” sine changes frequency when you change time/div, you were aliased. Increase \( f_s \) (faster timebase or higher sample-rate mode) until the frequency is stable.

Loading: 10 MΩ ∥ 15 pF at 1 MHz is about 10 kΩ reactance — a 10× probe is not optional on a 2 kΩ node at RF. At DC, 10 MΩ loading of a 100 kΩ source is 1% (unit 01).

## Mistakes

Leaving the probe on 10× while the scope thinks 1× (or the reverse): factor-of-ten voltage error.

Uncompensated 10× probe and believing the overshoot is the circuit.

AC coupling on a PWM waveform and calling the displayed average “the DC bus.”

Grounding both probes on a floating shunt (earth loop / short).

Aliasing on a DSO and reporting a tidy but wrong frequency.

Using dual-slope formulas for a SAR meter’s speed (they are different converters).

Lissajous: swapping \( N_x \) and \( N_y \), or using \( \sin\phi=a/A \) when amplitudes on X and Y are different without using the intercept formula correctly.

Measuring period on a noisy trigger (jittery display) instead of averaging many cycles.

Ignoring crest factor on a true-RMS DMM with a pulsed current.

Assuming 8-bit DSO vertical accuracy is 0.4% of full screen as a calibration spec — it is often worse, and the analog front end dominates.

A dual-slope walk-through: \( T_1=100.0 \) ms, \( V_r=10.00 \) V, \( T_2=37.40 \) ms, \( V_x=3.740 \) V. If line frequency is 50 Hz, \( T_1=5 \) cycles, good rejection.

CRO: 4.6 divisions peak-to-peak, 5 V/div, 10× probe: \( V_{pp}=4.6\times 5\times 10=230 \) V. Time: 4.0 div/period, 2 ms/div, \( T=8.0 \) ms, \( f=125 \) Hz.

Lissajous: \( y_{\max}=4.0 \) div, \( y_{\mathrm{int}}=2.0 \) div, \( \sin\phi=0.5 \), \( \phi=30^\circ \) or \( 150^\circ \); the ellipse orientation distinguishes.

Bandwidth: 100 MHz scope, \( t_r\approx 3.5 \) ns. A 2 ns edge will look like about \( \sqrt{2^2+3.5^2}\approx 4 \) ns if the probe is ideal.

Sampling: 1 µs/div, 10 div screen, 1000 points: \( f_s=100 \) MSa/s. A 30 MHz sine has only ~3.3 samples/period — visible but not a pretty sine. Nyquist is 50 MHz; the analog bandwidth may already be 20 MHz on that setting.

DMM spec: \( \pm(0.05\%\text{ rdg}+2\text{ digits}) \), 20.000 V range, reading 10.000 V, one digit = 1 mV. \( \Delta V=5 \) mV \( + 2 \) mV \( = 7 \) mV \( = 0.07\% \) of reading.

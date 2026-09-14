# Questions — PMMC, MI, electrodynamometer

Original pedagogical numbers.

## Q1

### Given

PMMC movement \( I_m=2.00 \) mA, \( R_m=25.0\,\Omega \).

### Find

Shunt for a 0–1.00 A ammeter and series multiplier for a 0–50.0 V voltmeter.

### Solution

\( R_{sh}=I_m R_m/(I-I_m)=0.002\times 25/(1-0.002)=0.05010\,\Omega \). \( R_{se}=V/I_m-R_m=50/0.002-25=24975\,\Omega \).

### Answer

\( R_{sh}=50.10\,\mathrm{m}\Omega \); \( R_{se}=24.975\,\mathrm{k}\Omega \).

## Q2

### Given

A 50 µA, 2000 Ω PMMC used as a voltmeter.

### Find

Ohms-per-volt sensitivity and the multiplier for a 10.0 V range.

### Solution

Sensitivity \( 1/I_m=20\,\mathrm{k}\Omega/\mathrm{V} \). \( R_{se}=10/50\times 10^{-6}-2000=198000\,\Omega \).

### Answer

\( 20\,\mathrm{k}\Omega/\mathrm{V} \); \( R_{se}=198\,\mathrm{k}\Omega \).

## Q3

### Given

Sinusoidal load \( V=230 \) V RMS, \( I=3.00 \) A RMS, \( \mathrm{PF}=0.800 \) lag. A dynamometer wattmeter is correctly connected.

### Find

The wattmeter reading.

### Solution

\( P=VI\cos\phi=230\times 3\times 0.8=552 \) W.

### Answer

\( 552 \) W.

## Q4

### Given

Rectifier PMMC voltmeter calibrated to read RMS of a sine (form factor 1.11). It is connected to a square wave of amplitude 10.0 V (true RMS \( 10.0 \) V).

### Find

The meter reading.

### Solution

Mean of absolute value is 10.0 V. Sine-calibrated scale multiplies by 1.11 relative to average, i.e. reading \( = 1.11\times V_{\mathrm{avg,abs}} \) but the 1.11 is already built so that \( V_{\mathrm{rms,sine}}=1.11 V_{\mathrm{avg}} \). For the square wave \( V_{\mathrm{avg,abs}}=V_{\mathrm{rms}} \), so the meter reads \( 1.11\times 10 / 1.11 = 10\times (V_{\mathrm{avg}}/V_{\mathrm{avg,sine\ rms\ scaling}}) \). Explicitly: meter indication \( = 1.11\times \) (mean of full-wave rectified waveform). For the square wave that mean is 10.0 V, so indication \( = 11.1 \) V. Wait: standard result is rectifier meters read high on square waves by 1.11 if they display “RMS” using the sine form factor. Indication \( = k \overline{|v|} \) with \( k=1.11 \). Square: \( \overline{|v|}=10 \), reading 11.1 V. True RMS is 10 V.

### Answer

\( 11.1 \) V (sine-RMS scale); true RMS is \( 10.0 \) V.

## Q5

### Given

Balanced three-phase, line 415 V, line 8.00 A, PF 0.500 lag. Two-wattmeter method.

### Find

The two wattmeter readings and the total power.

### Solution

\( \phi=60^\circ \). \( W_1=V_L I_L\cos(30^\circ+\phi)=415\times 8\cos 90^\circ=0 \). \( W_2=415\times 8\cos(30^\circ-60^\circ)=3320\cos(-30^\circ)=2875 \) W. Total \( P=\sqrt{3}\times 415\times 8\times 0.5=2875 \) W. Also \( W_1+W_2=2875 \) W.

### Answer

\( W_1=0 \), \( W_2=2.88 \) kW, \( P=2.88 \) kW.

## Q6

### Given

Moving-iron ammeter whose torque constant gives \( \theta\propto I^2 \) (constant \( \mathrm{d}L/\mathrm{d}\theta \)). Full-scale 5.00 A at \( 90^\circ \).

### Find

Pointer angle at 2.50 A.

### Solution

\( \theta/\theta_{\mathrm{fs}}=(I/I_{\mathrm{fs}})^2 \), \( \theta=90\times(0.5)^2=22.5^\circ \).

### Answer

\( 22.5^\circ \).

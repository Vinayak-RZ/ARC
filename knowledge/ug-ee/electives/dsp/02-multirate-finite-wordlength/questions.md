# Questions — Decimation, quantization effects

Original pedagogical numbers.

## Q1

### Given

Input sample rate \(f_s=8\,\mathrm{kHz}\). Decimate by \(M=4\) after an ideal anti-alias filter.

### Find

Output rate and the required digital cutoff (radians per *input* sample, and Hertz).

### Solution

\(f_{s,\mathrm{out}}=8000/4=2\,\mathrm{kHz}\). Cutoff \(\omega_c=\pi/M=\pi/4\) at the input rate, i.e. analog \(f_c=(8\,\mathrm{kHz})/(2\cdot 4)=1\,\mathrm{kHz}\).

### Answer

\(2\,\mathrm{kHz}\); \(\omega_c=\pi/4\) (\(1\,\mathrm{kHz}\)).

## Q2

### Given

Interpolate by \(L=3\) from \(f_s=2\,\mathrm{kHz}\). The expander inserts zeros then a lowpass runs.

### Find

Output rate, number of zeros inserted between samples, anti-image cutoff in Hertz, and DC gain of that lowpass.

### Solution

Output rate \(6\,\mathrm{kHz}\). Two zeros between samples. Cutoff \(f_s/2=1\,\mathrm{kHz}\) (i.e. \(\pi/L\) at the *high* rate is \(1\,\mathrm{kHz}\)). Gain \(L=3\).

### Answer

\(6\,\mathrm{kHz}\); 2 zeros; \(1\,\mathrm{kHz}\); gain \(3\).

## Q3

### Given

Uniform rounding quantizer, \(b=8\) bits two’s-complement fraction in \((-1,1)\), full-scale sine.

### Find

\(\Delta\), \(\sigma_e^2\), and SQNR in dB.

### Solution

\(\Delta=2^{-7}=1/128\). \(\sigma_e^2=\Delta^2/12=1/(16384\cdot 12)=1/196608\approx 5.09\times 10^{-6}\). SQNR \(\approx 6.02\times 8+1.76=49.92\,\mathrm{dB}\).

### Answer

\(\Delta=2^{-7}\); \(\sigma_e^2=2^{-14}/12\); SQNR \(\approx 49.9\,\mathrm{dB}\).

## Q4

### Given

Direct-form FIR, 9 taps, each product rounded with the \(\Delta\) of Q3, input quantization neglected.

### Find

Output roundoff variance.

### Solution

Nine independent rounding sources, each \(\Delta^2/12\). \(\sigma^2=9\Delta^2/12=(3/4)\Delta^2=(3/4)\cdot 2^{-14}=3\cdot 2^{-16}\).

### Answer

\(3\cdot 2^{-16}\) (\(\approx 4.58\times 10^{-5}\)).

## Q5

### Given

First-order IIR pole \(a=0.9\), rounding step \(\Delta=2^{-7}\), zero input. Deadband bound \(\Delta/\bigl(2(1-|a|)\bigr)\).

### Find

The bound on a granular limit-cycle amplitude.

### Solution

\(1-|a|=0.1\). Bound \(= (2^{-7})/(2\cdot 0.1)=2^{-7}/0.2=2^{-7}\cdot 5=5/128\approx 0.0391\).

### Answer

\(5/128\approx 0.039\).

## Q6

### Given

Rate change \(8\,\mathrm{kHz}\to 12\,\mathrm{kHz}\) by integers \(L,M\).

### Find

Coprime \(L,M\) and the intermediate rate if interpolation is done first.

### Solution

\(12/8=3/2\), so \(L=3\), \(M=2\). Upsample by 3: \(24\,\mathrm{kHz}\), then decimate by 2: \(12\,\mathrm{kHz}\).

### Answer

\(L=3\), \(M=2\); intermediate \(24\,\mathrm{kHz}\).

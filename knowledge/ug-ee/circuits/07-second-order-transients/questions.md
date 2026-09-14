# Questions — RLC second-order transients

Original pedagogical numbers.

## Q1

### Given

Series RLC, \( R = 200\,\Omega \), \( L = 50\,\mathrm{mH} \), \( C = 0.50\,\mu\mathrm{F} \), source-free, \( i_L(0) = 8.0\,\mathrm{mA} \), \( v_C(0) = 12\,\mathrm{V} \) with polarity such that KVL is \( L di/dt + Ri + v_C = 0 \) and \( i = C dv_C/dt \).

### Find

Damping type, \( \omega_0 \), \( \alpha \), and \( i(t) \) for \( t>0 \).

### Solution

\( \omega_0 = 1/\sqrt{LC} = 1/\sqrt{5\times 10^{-2}\times 5\times 10^{-7}} = 1/\sqrt{2.5\times 10^{-8}} = 6325\,\mathrm{rad/s} \). \( \alpha = R/(2L) = 200/(0.10) = 2000\,\mathrm{s}^{-1} \). \( \alpha < \omega_0 \): underdamped. \( \omega_d = \sqrt{6325^2 - 2000^2} = 5999\,\mathrm{rad/s} \). \( i(t) = e^{-2000 t}(B_1 \cos\omega_d t + B_2 \sin\omega_d t) \). \( i(0) = B_1 = 0.008 \). \( di/dt(0) = -2000 B_1 + \omega_d B_2 = -(v_C(0)+R i(0))/L = -(12+1.6)/0.05 = -272 \). Then \( -16 + 5999 B_2 = -272 \) ⇒ \( B_2 = -0.04267 \). So \( i(t) = e^{-2000 t}(0.008\cos 5999 t - 0.0427\sin 5999 t)\,\mathrm{A} \).

### Answer

Underdamped; \( \omega_0 = 6.32\times 10^3\,\mathrm{rad/s} \), \( \alpha = 2.00\times 10^3\,\mathrm{s}^{-1} \); \( i(t) = e^{-2000t}(8.00\cos 5999 t - 42.7\sin 5999 t)\,\mathrm{mA} \).

## Q2

### Given

Parallel RLC: \( C = 2.0\,\mu\mathrm{F} \), \( L = 8.0\,\mathrm{mH} \), R unknown. Need critical damping.

### Find

Derive \( R_\mathrm{crit} \).

### Solution

Parallel \( \alpha = 1/(2RC) \), \( \omega_0 = 1/\sqrt{LC} = 1/\sqrt{8\times 10^{-3}\times 2\times 10^{-6}} = 7916\,\mathrm{rad/s} \). Critical: \( \alpha = \omega_0 \) ⇒ \( 1/(2RC) = \omega_0 \) ⇒ \( R = 1/(2 C \omega_0) = 1/(2\times 2\times 10^{-6}\times 7916) = 31.58\,\Omega \). Equivalently \( R_\mathrm{crit} = \frac12 \sqrt{L/C} = 0.5 \sqrt{4000} = 31.62\,\Omega \).

### Answer

\( R = 31.6\,\Omega \).

## Q3

### Given

Design a series RLC snubber-like ring: \( L = 220\,\mu\mathrm{H} \), want \( f_d \approx 25\,\mathrm{kHz} \) and \( \zeta \approx 0.20 \).

### Find

C and R (approximate \( \omega_d \approx \omega_0 \) if justified).

### Solution

For \( \zeta = 0.2 \), \( \omega_d = \omega_0 \sqrt{1-\zeta^2} = 0.980 \omega_0 \), so \( \omega_0 \approx 2\pi 25000 / 0.980 = 1.603\times 10^5\,\mathrm{rad/s} \). \( C = 1/(\omega_0^2 L) = 1/( (1.603e5)^2 \times 2.20e-4 ) = 177\,\mathrm{nF} \). Series \( \zeta = R/2 \sqrt{C/L} \) ⇒ \( R = 2\zeta \sqrt{L/C} = 0.40 \sqrt{220e-6/177e-9} = 0.40 \times 35.26 = 14.1\,\Omega \).

### Answer

\( C \approx 177\,\mathrm{nF} \), \( R \approx 14.1\,\Omega \).

## Q4

### Given

A student uses \( i(t) = A e^{-\alpha t}\cos\omega_0 t \) for a series RLC with \( \alpha = 5000 \), \( \omega_0 = 4000 \) rad/s.

### Find

Explain why the formula is invalid and which form applies.

### Solution

Here \( \alpha > \omega_0 \), overdamped; there is no real \( \omega_d \) and the oscillation form is wrong. Roots \( s = -5000 \pm \sqrt{25e6 - 16e6} = -5000 \pm 3000 \), so \( s_1 = -2000 \), \( s_2 = -8000 \). Use \( i(t) = A_1 e^{-2000 t} + A_2 e^{-8000 t} \).

### Answer

Overdamped; \( i(t) = A_1 e^{-2000t} + A_2 e^{-8000t} \).

## Q5

### Given

Series RLC to a 10 V DC step, \( i_L(0)=0 \), \( v_C(0)=0 \), underdamped. R = 8.0 Ω, L = 4.0 mH, C = 10 µF.

### Find

\( v_C(\infty) \), \( \omega_d \), and \( v_C(t) \) constants via \( v_C(0) \) and \( i_C(0^+)=0 \).

### Solution

DC final: inductor short, capacitor open, \( v_C(\infty) = 10\,\mathrm{V} \). \( \omega_0 = 1/\sqrt{4e-3\times 10e-6} = 5000 \), \( \alpha = 8/(2\times 0.004) = 1000 \), \( \omega_d = 4899 \). \( v_C(t) = 10 + e^{-1000 t}(A\cos\omega_d t + B\sin\omega_d t) \). \( v_C(0)=0 \) ⇒ \( 10+A=0 \) ⇒ \( A=-10 \). \( i_C = C dv_C/dt \), \( i_C(0^+)=i_L(0)=0 \). Differentiate: \( dv_C/dt(0) = -1000 A + \omega_d B = 0 \) ⇒ \( 10000 + 4899 B = 0 \) ⇒ \( B = -2.041 \). So \( v_C(t) = 10 - e^{-1000 t}(10\cos 4899 t + 2.04\sin 4899 t)\,\mathrm{V} \).

### Answer

\( v_C(\infty)=10\,\mathrm{V} \); \( \omega_d = 4.90\times 10^3\,\mathrm{rad/s} \); \( v_C(t) = 10 - e^{-1000t}(10\cos 4899t + 2.04\sin 4899t)\,\mathrm{V} \).

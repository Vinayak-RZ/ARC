# Questions — Bode plots

Original pedagogical numbers.

## Q1

### Given

\(L(s)=20/[s(s+4)]\).

### Find

The asymptotic low-frequency 0 dB intercept, the corner, and the high-frequency slope.

### Solution

\(L=5/[s(s/4+1)]=K_v/s\times 1/(1+s/4)\) with \(K_v=5\). Low-frequency (type 1) 0 dB at \(\omega=K_v=5\,\mathrm{rad/s}\) if the pole at 4 were absent; the corner is \(4\,\mathrm{rad/s}\), below that intercept, so the actual magnitude already has slope \(-40\) dB/dec after \(\omega=4\). Low-frequency slope \(-20\) dB/dec until \(\omega=4\), then \(-40\) dB/dec. The \(K/s\) line \(20/\omega\) (because \(L\sim 20/s^2\times s/(1)\) wait): \(L\sim 20/(4s)=5/s\) for \(\omega\ll 4\), 0 dB at 5 rad/s, but 5>4 so that intercept is virtual. High-frequency \(L\sim 20/s^2\), slope \(-40\) dB/dec, 0 dB when \(20/\omega^2=1\), \(\omega=\sqrt{20}=4.47\).

### Answer

Corner \(4\,\mathrm{rad/s}\); LF asymptote \(5/s\) (virtual 0 dB at 5 rad/s); HF slope \(-40\) dB/dec.

## Q2

### Given

\(L(s)=8/(s(s+2))\).

### Find

Exact gain-crossover \(\omega_g\) and the phase margin.

### Solution

\(|L(j\omega)|=8/(\omega\sqrt{\omega^2+4})=1\) ⇒ \(8=\omega\sqrt{\omega^2+4}\) ⇒ \(64=\omega^2(\omega^2+4)\) ⇒ \(\omega^4+4\omega^2-64=0\). Let \(u=\omega^2\), \(u^2+4u-64=0\), \(u=-2+\sqrt{68}=-2+8.246=6.246\), \(\omega_g=2.499\,\mathrm{rad/s}\). \(\phi=-90^\circ-\tan^{-1}(\omega/2)=-90-\tan^{-1}(1.250)=-90-51.34=-141.3^\circ\). \(\mathrm{PM}=180-141.3=38.7^\circ\).

### Answer

\(\omega_g=2.50\,\mathrm{rad/s}\); \(\mathrm{PM}=38.7^\circ\).

## Q3

### Given

\(L(s)=K/s^3\) with \(K>0\) (three integrators).

### Find

Phase as a function of \(\omega\), and whether PM can be positive.

### Solution

\(\angle L=-270^\circ\) for all \(\omega\). \(|L|=K/\omega^3=1\) at \(\omega=K^{1/3}\). \(\mathrm{PM}=-270+180=-90^\circ\), independent of \(K\). PM cannot be positive. (GM is 0 dB at every \(K\) in the sense that phase is already \(-270^\circ\), which is an odd multiple wrapping; Nyquist is the right picture: the plot is the negative imaginary axis stacked — actually \(1/(j\omega)^3=j/\omega^3\), positive imaginary. Careful: \((j\omega)^3=j^3\omega^3=-j\omega^3\), so \(1/(j\omega)^3=j/\omega^3\), phase \(+90^\circ\). Wait. \(j=e^{j\pi/2}\), \(j^3=e^{j3\pi/2}=-j\), \(1/j^3=1/(-j)=j\), phase \(+90^\circ\). Three integrators: phase \(+90^\circ\) or equivalently \(-270^\circ\). PM defined as \(\phi+180\): if we take \(\phi=+90\), PM \(=270^\circ\) which is the wrong branch; the nearest \(-180^\circ\) equivalent is \(-270^\circ\), PM \(-90^\circ\). The loop is unstable for all \(K>0\) by Routh on \(s^3+K=0\).)

### Answer

\(\phi=-270^\circ\) (principal equivalent \(+90^\circ\)); \(\mathrm{PM}=-90^\circ\); cannot be made positive by \(K\).

## Q4

### Given

A delay \(T=0.1\,\mathrm{s}\) is added to \(L_0(s)=4/(s+4)\) (open-loop, no extra integrator), unity feedback.

### Find

Phase at \(\omega=10\,\mathrm{rad/s}\) with and without delay, and the delay’s phase contribution there.

### Solution

\(L_0(j10)=4/(4+j10)\), \(\phi_0=-\tan^{-1}(10/4)=-68.2^\circ\). Delay: \(-\omega T=-1\,\mathrm{rad}=-57.3^\circ\). Total \(\phi=-125.5^\circ\).

### Answer

Without delay \(-68.2^\circ\); delay adds \(-57.3^\circ\); total \(-125.5^\circ\).

## Q5

### Given

\(L(s)=12(s+1)/[s(s+3)(s+10)]\).

### Find

Bode corners and the low-frequency \(K_v\) (type and 0 dB intercept of the \(K_v/s\) asymptote).

### Solution

Type 1. Rewrite \(L=12(1+s)/[s\cdot 3(1+s/3)\cdot 10(1+s/10)]=0.4(1+s)/[s(1+s/3)(1+s/10)]\). \(K_v=0.4\,\mathrm{s}^{-1}\). Corners: zero at 1 rad/s, poles at 3 and 10. LF 0 dB intercept of \(K_v/s\) at \(\omega=0.4\,\mathrm{rad/s}\).

### Answer

Type 1; \(K_v=0.4\,\mathrm{s}^{-1}\); corners \(1,3,10\,\mathrm{rad/s}\); LF 0 dB at \(0.4\,\mathrm{rad/s}\).

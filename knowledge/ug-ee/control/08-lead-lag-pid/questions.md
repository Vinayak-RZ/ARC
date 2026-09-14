# Questions — Lead/lag, PID, Ziegler–Nichols intro

Original pedagogical numbers.

## Q1

### Given

A lead compensator must supply \(\phi_m=50^\circ\) at its peak.

### Find

The ratio \(\alpha\) (pole/zero time-constant ratio, \(0<\alpha<1\)) and \(\omega_m\tau\).

### Solution

\(\sin 50^\circ=0.766=(1-\alpha)/(1+\alpha)\). Then \(0.766(1+\alpha)=1-\alpha\) ⇒ \(0.766+0.766\alpha=1-\alpha\) ⇒ \(1.766\alpha=0.234\) ⇒ \(\alpha=0.133\). \(\omega_m=1/(\tau\sqrt{\alpha})\) ⇒ \(\omega_m\tau=1/\sqrt{0.133}=2.74\).

### Answer

\(\alpha=0.133\); \(\omega_m\tau=2.74\).

## Q2

### Given

Plant \(G=4/[s(s+4)]\), lag \(C=(10s+1)/(100s+1)\) (DC gain 1). Unity feedback.

### Find

\(K_v\) with \(C=1\) and with this lag, and the lag pole and zero.

### Solution

Without lag, \(L=4/[s(s+4)]\), \(K_v=1\). Lag form \(\frac{\tau s+1}{\beta\tau s+1}\) with \(\tau=10\), \(\beta\tau=100\), \(\beta=10\). But DC gain of \(C\) is 1, so \(\lim s L\) is unchanged: \(K_v\) stays 1. (This lag attenuates high frequency; it does not raise \(K_v\).) Zero at \(0.1\,\mathrm{rad/s}\), pole at \(0.01\,\mathrm{rad/s}\). To raise \(K_v\) one would use \(C=\beta(\tau s+1)/(\beta\tau s+1)\) with \(\beta=10\), giving \(K_v=10\).

### Answer

\(K_v=1\) both times for the given \(C\); zero \(0.1\), pole \(0.01\) rad/s. (Need leading \(\beta\) to raise \(K_v\).)

## Q3

### Given

Plant \(G=1/[s(s+1)(s+2)]\). Ultimate gain from Routh is \(K_u=6\), \(\omega_u=\sqrt{2}\).

### Find

Ziegler–Nichols PID \(K_p,T_i,T_d\) and \(P_u\).

### Solution

\(P_u=2\pi/\omega_u=2\pi/\sqrt{2}=4.442\,\mathrm{s}\). \(K_p=0.6\times 6=3.6\). \(T_i=P_u/2=2.221\,\mathrm{s}\). \(T_d=P_u/8=0.555\,\mathrm{s}\).

### Answer

\(P_u=4.44\,\mathrm{s}\); \(K_p=3.6\); \(T_i=2.22\,\mathrm{s}\); \(T_d=0.555\,\mathrm{s}\).

## Q4

### Given

PI controller \(C=K_p+K_i/s\) with \(K_p=2\), \(K_i=0.5\), plant \(G=3/(s+3)\), unity negative feedback.

### Find

Open-loop type, \(K_p^{\mathrm{err}}\) (position constant), and \(e_{ss}\) to a unit step.

### Solution

\(L=C G=(2s+0.5)/[s]\cdot 3/(s+3)=(6s+1.5)/[s(s+3)]\). Type 1. \(K_p^{\mathrm{err}}=\infty\), \(e_{\mathrm{step}}=0\). (Ramp: \(K_v=\lim s L=1.5/3=0.5\), \(e_{\mathrm{ramp}}=2\), not asked.)

### Answer

Type 1; \(K_p^{\mathrm{err}}=\infty\); \(e_{ss}=0\) (unit step).

## Q5

### Given

Uncompensated \(KG(j\omega)\) has \(\omega_g=6\,\mathrm{rad/s}\) and \(\mathrm{PM}=22^\circ\). Spec \(\mathrm{PM}\ge 50^\circ\). A lead will be designed with a \(10^\circ\) safety in \(\phi_m\).

### Find

The required \(\phi_m\) and the corresponding \(\alpha\).

### Solution

Deficit \(50-22=28^\circ\), plus \(10^\circ\) ⇒ \(\phi_m=38^\circ\). \(\sin 38^\circ=0.616=(1-\alpha)/(1+\alpha)\). \(0.616+0.616\alpha=1-\alpha\) ⇒ \(1.616\alpha=0.384\) ⇒ \(\alpha=0.238\).

### Answer

\(\phi_m=38^\circ\); \(\alpha=0.238\).

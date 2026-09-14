# Questions — 1st/2nd order, error constants

Original pedagogical numbers.

## Q1

### Given

Closed-loop \(T(s)=6/(s+6)\). Unit step at \(t=0\).

### Find

Time constant, 2% settling time, and \(y(0.2)\).

### Solution

\(\tau=1/6\,\mathrm{s}\). \(t_{s,2\%}\approx 4\tau=0.667\,\mathrm{s}\). \(y(t)=1-e^{-6t}\), \(y(0.2)=1-e^{-1.2}=0.699\).

### Answer

\(\tau=0.167\,\mathrm{s}\); \(t_s\approx 0.667\,\mathrm{s}\); \(y(0.2)=0.699\).

## Q2

### Given

Prototype \(T(s)=25/(s^2+4s+25)\).

### Find

\(\zeta\), \(\omega_n\), percent overshoot, and peak time \(t_p\).

### Solution

\(\omega_n=5\), \(2\zeta\omega_n=4\) ⇒ \(\zeta=0.4\). \(\omega_d=5\sqrt{1-0.16}=5\sqrt{0.84}=4.583\). \(t_p=\pi/4.583=0.685\,\mathrm{s}\). \(\mathrm{PO}=100\exp(-0.4\pi/\sqrt{0.84})=100\exp(-1.370)=25.4\%\).

### Answer

\(\zeta=0.4\), \(\omega_n=5\,\mathrm{rad/s}\), \(\mathrm{PO}=25.4\%\), \(t_p=0.685\,\mathrm{s}\).

## Q3

### Given

Unity negative feedback, \(L(s)=12/[s(s+4)]\). Closed loop is stable.

### Find

Type, \(K_v\), and steady-state error to a ramp \(r(t)=3t\).

### Solution

One free integrator: type 1. \(K_v=\lim_{s\to 0}s L=12/4=3\). Unit-ramp error \(1/K_v=1/3\); slope 3 ⇒ \(e_{ss}=1\).

### Answer

Type 1; \(K_v=3\,\mathrm{s}^{-1}\); \(e_{ss}=1\).

## Q4

### Given

Specs: PO \(\le 16\%\) (take \(\zeta=0.5\)) and 2% settling \(t_s\le 0.8\,\mathrm{s}\) for a prototype second-order \(T\).

### Find

The smallest \(\omega_n\) that meets both, and the corresponding pole pair.

### Solution

\(\zeta=0.5\) from PO. \(t_s\approx 4/(\zeta\omega_n)\le 0.8\) ⇒ \(\zeta\omega_n\ge 5\) ⇒ \(\omega_n\ge 10\). Poles \(-\zeta\omega_n\pm j\omega_n\sqrt{1-\zeta^2}=-5\pm j 8.660\).

### Answer

\(\omega_n=10\,\mathrm{rad/s}\); poles \(-5\pm j8.66\).

## Q5

### Given

Unity feedback, \(L(s)=K/(s+2)^2\). Unit step.

### Find

\(K_p\) and \(e_{ss}\) as functions of \(K\), assuming \(K>0\) so the loop is stable.

### Solution

Type 0, \(K_p=\lim L=K/4\). \(e_{ss}=1/(1+K/4)=4/(4+K)\). (Routh on \(s^2+4s+4+K=0\) has all positive coefficients for \(K>-4\); for \(K>0\) stable.)

### Answer

\(K_p=K/4\); \(e_{ss}=4/(K+4)\).

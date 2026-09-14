# Worked questions — AC voltage controllers

## Q1
### Given
A single-phase AC voltage controller, resistive load \(R=25\,\Omega\), source 230 V RMS, 50 Hz, firing angle \(\alpha=70^\circ\). Ideal devices.
### Find
Load RMS voltage, load power, and power factor.
### Solution
\(\alpha=70\pi/180=1.2217\,\mathrm{rad}\). \(\pi-\alpha+\tfrac12\sin 140^\circ=3.1416-1.2217+0.5\times 0.6428=2.2413\). \(V_L=230\sqrt{2.2413/\pi}=194.4\,\mathrm{V}\). \(P=194.4^2/25=1512\,\mathrm{W}\). \(\mathrm{pf}=V_L/230=0.845\).
### Answer
\(V_L=194\,\mathrm{V}\), \(P=1.51\,\mathrm{kW}\), \(\mathrm{pf}=0.845\)

## Q2
### Given
Integral-cycle control of the same 230 V, \(25\,\Omega\) heater: 7 cycles on, 3 cycles off.
### Find
Load RMS voltage and average power.
### Solution
On-fraction \(D=7/10=0.7\). \(V_L=230\sqrt{0.7}=192.4\,\mathrm{V}\). Full power \(230^2/25=2116\,\mathrm{W}\). Average power \(0.7\times 2116=1481\,\mathrm{W}\).
### Answer
\(V_L=192\,\mathrm{V}\), \(P=1.48\,\mathrm{kW}\)

## Q3
### Given
RL load, \(R=8\,\Omega\), \(L=25\,\mathrm{mH}\), 50 Hz, 120 V RMS source. Phase-controlled AC controller.
### Find
Load phase angle \(\phi\) and the minimum legal firing angle \(\alpha_{\min}\).
### Solution
\(\omega L=7.854\,\Omega\). \(\phi=\arctan(7.854/8)=0.775\,\mathrm{rad}=44.4^\circ\). \(\alpha_{\min}=\phi=44.4^\circ\).
### Answer
\(\phi=44.4^\circ\), \(\alpha_{\min}=44.4^\circ\)

## Q4
### Given
Resistive AC controller, \(V_s=120\,\mathrm{V}\) RMS, \(\alpha=90^\circ\).
### Find
\(V_{L,\mathrm{rms}}\) using the standard integral formula.
### Solution
\(\alpha=\pi/2\). \(\pi-\pi/2+\tfrac12\sin\pi=\pi/2\). \(V_L=120\sqrt{(\pi/2)/\pi}=120/\sqrt{2}=84.85\,\mathrm{V}\).
### Answer
\(V_L=84.9\,\mathrm{V}\)

## Q5
### Given
A 3 kW, 230 V heater is to be run at 1.2 kW average by integral-cycle control. Cycle groups must be whole cycles.
### Find
The smallest period \(n+m\) with integer \(n,m\) that matches 1.2 kW exactly, and the corresponding \(n,m\).
### Solution
Power fraction \(1.2/3=0.4\). Smallest integers: \(n=2\), \(m=3\), period 5 cycles. RMS voltage \(230\sqrt{0.4}=145.4\,\mathrm{V}\).
### Answer
\(n=2\) on, \(m=3\) off (period 5); \(V_L=145\,\mathrm{V}\)

## Q6
### Given
Single-phase resistive controller, \(V_m=340\,\mathrm{V}\), \(\alpha=0\) versus \(\alpha=120^\circ\).
### Find
The ratio \(P(\alpha=120^\circ)/P(\alpha=0)\).
### Solution
Full power proportional to \(V_m^2/2\) over \(R\), i.e. to \(V_{\mathrm{rms}}^2\). At \(\alpha=120^\circ=2\pi/3\), \(\pi-\alpha+\tfrac12\sin 240^\circ=3.1416-2.0944+0.5\times(-0.8660)=0.6142\). \(V_L/V_s=\sqrt{0.6142/\pi}=0.442\). Power ratio \(0.442^2=0.196\).
### Answer
\(0.196\) (about 19.6% of full power)

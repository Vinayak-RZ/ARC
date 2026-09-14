# Worked questions — commutation and snubbers

## Q1
### Given
A line-commutated SCR has \(t_q=80\,\mu\mathrm{s}\). In a 50 Hz fully controlled bridge, \(\alpha=150^\circ\) and overlap \(u=8^\circ\).
### Find
The extinction (reverse-bias) angle \(\gamma\) and whether \(t_{\mathrm{reverse}}>t_q\).
### Solution
\(\gamma=180-150-8=22^\circ\). \(t_{\mathrm{reverse}}=22/360\times 0.020=1.222\,\mathrm{ms}=1222\,\mu\mathrm{s}\gg 80\,\mu\mathrm{s}\). Commutation margin is ample.
### Answer
\(\gamma=22^\circ\), \(t_{\mathrm{rev}}=1.22\,\mathrm{ms}\) (OK)

## Q2
### Given
Class-B style resonant pulse: \(L=20\,\mu\mathrm{H}\), \(C=5.0\,\mu\mathrm{F}\), capacitor precharge \(V=200\,\mathrm{V}\). Load current to be commutated is 80 A.
### Find
Peak pulse current, pulse half-period, and whether the pulse can reverse the SCR current.
### Solution
\(I_{\mathrm{pk}}=V\sqrt{C/L}=200\sqrt{5\times 10^{-6}/20\times 10^{-6}}=200\sqrt{0.25}=100\,\mathrm{A}\). Half-period \(\pi\sqrt{LC}=\pi\sqrt{1.0\times 10^{-10}}=31.4\,\mu\mathrm{s}\). \(100>80\), so the pulse can drive net current through zero (margin 20 A).
### Answer
\(I_{\mathrm{pk}}=100\,\mathrm{A}\), \(t_{\pi}=31.4\,\mu\mathrm{s}\), yes

## Q3
### Given
RCD snubber, \(I_0=15\,\mathrm{A}\) at turn-off, allowed \(dv/dt=400\,\mathrm{V/\mu s}\). \(V_{dc}=250\,\mathrm{V}\), \(f_{sw}=16\,\mathrm{kHz}\). Assume \(C_s\) charges to the bus each cycle.
### Find
Minimum \(C_s\), energy per cycle, and snubber resistor dissipation.
### Solution
\(C_s\ge 15/(400\times 10^6)=37.5\,\mathrm{nF}\). Use \(40\,\mathrm{nF}\). \(E=\tfrac12\times 40\times 10^{-9}\times 250^2=1.25\,\mathrm{mJ}\). \(P=1.25\times 10^{-3}\times 16000=20.0\,\mathrm{W}\).
### Answer
\(C_s=40\,\mathrm{nF}\), \(E=1.25\,\mathrm{mJ}\), \(P=20.0\,\mathrm{W}\)

## Q4
### Given
Stray \(L_{\sigma}=150\,\mathrm{nH}\), turn-off current 40 A, no clamp. Energy \(\tfrac12 L I^2\) must be absorbed by a clamp capacitor that may rise 50 V above the 400 V bus.
### Find
The energy and the \(C_{\mathrm{clamp}}\) that absorbs it over a 50 V rise (use \(\tfrac12 C(V_2^2-V_1^2)\)).
### Solution
\(E=\tfrac12\times 150\times 10^{-9}\times 40^2=120\,\mu\mathrm{J}\). \(V_1=400\), \(V_2=450\). \(\tfrac12 C(450^2-400^2)=E\) ⇒ \(C\times 21250=240\times 10^{-6}\) ⇒ \(C=11.3\,\mathrm{nF}\).
### Answer
\(E=120\,\mu\mathrm{J}\), \(C=11.3\,\mathrm{nF}\)

## Q5
### Given
An SCR \(dv/dt\) limit is \(200\,\mathrm{V/\mu s}\). A capacitor \(C_s=0.22\,\mu\mathrm{F}\) is placed across it. Worst-case current into the capacitor is 4.0 A.
### Find
Resulting \(dv/dt\) and pass/fail.
### Solution
\(dv/dt=4.0/(0.22\times 10^{-6})=18.2\times 10^6\,\mathrm{V/s}=18.2\,\mathrm{V/\mu s}<200\). Pass.
### Answer
\(18.2\,\mathrm{V/\mu s}\) (pass)

## Q6
### Given
A CCM buck chopper, \(V_{in}=60\,\mathrm{V}\), \(D=0.25\), \(f_s=20\,\mathrm{kHz}\). An RC snubber of \(C_s=1.0\,\mathrm{nF}\) fully charges to \(V_{in}\) each cycle.
### Find
Average output voltage (ideal buck) and snubber loss.
### Solution
\(V_{out}=D V_{in}=15.0\,\mathrm{V}\). \(P_{\mathrm{snub}}=\tfrac12 C_s V_{in}^2 f_s=0.5\times 1.0\times 10^{-9}\times 3600\times 20000=0.036\,\mathrm{W}\).
### Answer
\(V_{out}=15.0\,\mathrm{V}\), \(P_{\mathrm{snub}}=36\,\mathrm{mW}\)

# Worked questions — diode, SCR, MOSFET, IGBT, SOA

## Q1
### Given
A silicon power diode is modelled as \(V_F=1.0\,\mathrm{V}\) plus \(r_f=8\,\mathrm{m}\Omega\). In a rectifier it carries \(I_{\mathrm{avg}}=12\,\mathrm{A}\) and \(I_{\mathrm{rms}}=18\,\mathrm{A}\).
### Find
Conduction loss in the diode.
### Solution
Constant-drop term: \(V_F I_{\mathrm{avg}}=1.0\times 12=12.0\,\mathrm{W}\). Resistive term: \(r_f I_{\mathrm{rms}}^2=0.008\times 18^2=2.59\,\mathrm{W}\). Total \(P_{\mathrm{cond}}=14.59\,\mathrm{W}\).
### Answer
\(P_{\mathrm{cond}}=14.6\,\mathrm{W}\)

## Q2
### Given
An SCR has \(I_L=80\,\mathrm{mA}\) and \(I_H=40\,\mathrm{mA}\). A gate pulse of width \(40\,\mu\mathrm{s}\) is applied while the anode circuit is a 200 V source in series with \(L=0.20\,\mathrm{H}\) and a 2 Ω resistor (initially \(i_A=0\)). Approximate \(di_A/dt\approx V/L\) during the pulse (neglect \(R\) for the short pulse).
### Find
Whether the SCR latches, and the anode current at the end of the gate pulse.
### Solution
\(di_A/dt=200/0.20=1000\,\mathrm{A/s}\). In \(40\,\mu\mathrm{s}\), \(i_A=1000\times 40\times 10^{-6}=0.040\,\mathrm{A}=40\,\mathrm{mA}\). This is below \(I_L=80\,\mathrm{mA}\), so when the gate pulse ends the device unlatches. Holding current is irrelevant because latching never occurred.
### Answer
Does not latch; \(i_A(t_g)=40\,\mathrm{mA}<I_L\)

## Q3
### Given
A MOSFET chopper switch sees \(V_{DS}=60\,\mathrm{V}\) when off and \(I_D=10\,\mathrm{A}\) when on. Switching frequency \(25\,\mathrm{kHz}\). Overlap times \(t_{on}=80\,\mathrm{ns}\), \(t_{off}=120\,\mathrm{ns}\). Use the triangular overlap model \(E=\tfrac12 V I t\) per edge. Conduction: \(R_{DS(on)}=40\,\mathrm{m}\Omega\), duty \(D=0.5\), current essentially flat at 10 A.
### Find
Switching loss, conduction loss, and total device loss (ignore drive).
### Solution
\(E_{\mathrm{on}}=\tfrac12\times 60\times 10\times 80\times 10^{-9}=24\,\mu\mathrm{J}\). \(E_{\mathrm{off}}=\tfrac12\times 60\times 10\times 120\times 10^{-9}=36\,\mu\mathrm{J}\). \(P_{\mathrm{sw}}=(24+36)\times 10^{-6}\times 25000=1.50\,\mathrm{W}\). \(I_{\mathrm{rms}}=10\sqrt{0.5}=7.071\,\mathrm{A}\). \(P_{\mathrm{cond}}=7.071^2\times 0.040=2.00\,\mathrm{W}\). Total \(3.50\,\mathrm{W}\).
### Answer
\(P_{\mathrm{sw}}=1.50\,\mathrm{W}\), \(P_{\mathrm{cond}}=2.00\,\mathrm{W}\), \(P_{\mathrm{tot}}=3.50\,\mathrm{W}\)

## Q4
### Given
An IGBT dissipates \(P_D=28\,\mathrm{W}\). \(\theta_{JC}=0.45\,\mathrm{K/W}\), \(\theta_{CS}=0.20\,\mathrm{K/W}\) (grease), \(\theta_{SA}=2.10\,\mathrm{K/W}\) (sink to ambient). Ambient \(T_A=40^\circ\mathrm{C}\). \(T_{J,\max}=150^\circ\mathrm{C}\).
### Find
Junction temperature and whether the thermal design is legal.
### Solution
\(\theta_{JA}=0.45+0.20+2.10=2.75\,\mathrm{K/W}\). \(T_J=40+28\times 2.75=40+77=117^\circ\mathrm{C}\). \(117<150\), so the thermal chain is legal with about \(33\,\mathrm{K}\) margin.
### Answer
\(T_J=117^\circ\mathrm{C}\) (legal)

## Q5
### Given
A 600 V IGBT module is used on a 400 V DC bus. Layout inductance and diode snap cause a turn-off spike of 180 V above the bus. Peak turn-off current is 80 A. The datasheet RBSOA at this pulse width allows 600 V at 80 A (clamped).
### Find
The peak collector voltage and whether the switching locus is inside the 600 V RBSOA clamp.
### Solution
Peak voltage \(400+180=580\,\mathrm{V}\). This is below 600 V, and the current is 80 A, so the clamped RBSOA point is not exceeded. Margin is only 20 V; a stiffer clamp or slower \(di/dt\) would be prudent, but the given SOA is satisfied.
### Answer
\(v_{\mathrm{peak}}=580\,\mathrm{V}\); inside the 600 V / 80 A RBSOA (20 V margin)

## Q6
### Given
An SCR must not see more than \((dv/dt)_{\mathrm{crit}}=200\,\mathrm{V/\mu s}\). A snubber capacitor \(C_s=0.10\,\mu\mathrm{F}\) sits across the device. The worst-case charging current available from the circuit at turn-off of the complementary path is \(I=2.5\,\mathrm{A}\) (treat as \(C\,dv/dt=I\)).
### Find
The resulting \(dv/dt\) and whether the SCR is protected.
### Solution
\(dv/dt=I/C_s=2.5/(0.10\times 10^{-6})=25\times 10^6\,\mathrm{V/s}=25\,\mathrm{V/\mu s}\). This is below \(200\,\mathrm{V/\mu s}\), so the capacitor snubber keeps \(dv/dt\) legal (a series resistor would still be needed in a full RCD to limit discharge current at turn-on).
### Answer
\(dv/dt=25\,\mathrm{V/\mu s}\) (protected)

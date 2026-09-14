# Worked questions — comparators, Schmitt, precision rectifiers

## Q1
### Given
Ideal op-amp open-loop comparator, \(V_{sat}=\pm 13\,\mathrm{V}\). Signal \(v_{in}=2\sin\omega t\) V on the inverting input, \(V_{ref}=0.50\,\mathrm{V}\) on the noninverting input.
### Find
The values of \(v_{in}\) at the switching instants and the duty cycle of the output (fraction of the period spent at \(+13\,\mathrm{V}\)).
### Solution
Output is high when \(v_+>v_-\), i.e. when \(0.50>v_{in}\). Switching instants satisfy \(2\sin\theta=0.50\), so \(\theta=14.48^\circ\) and \(165.52^\circ\). The sinusoid is above \(0.50\,\mathrm{V}\) only between those angles (\(151.04^\circ\)), so the output is low for \(151.04/360=0.420\) of the period and high for \(0.580\).
### Answer
Switching at \(v_{in}=0.50\,\mathrm{V}\); duty cycle (high) \(=0.580\)

## Q2
### Given
Inverting Schmitt, output clamped at \(V_{OH}=+10\,\mathrm{V}\), \(V_{OL}=-10\,\mathrm{V}\). \(R_1=10\,\mathrm{k}\Omega\) from \(+\) pin to ground, \(R_2=40\,\mathrm{k}\Omega\) from output to \(+\) pin. Signal into \(-\).
### Find
\(V_{T+}\), \(V_{T-}\), and hysteresis width.
### Solution
\(V_+=v_o\cdot 10/50=0.20 v_o\). \(V_{T+}=0.20\times 10=+2.0\,\mathrm{V}\), \(V_{T-}=0.20\times(-10)=-2.0\,\mathrm{V}\). Width \(4.0\,\mathrm{V}\).
### Answer
\(V_{T+}=+2.0\,\mathrm{V}\), \(V_{T-}=-2.0\,\mathrm{V}\), \(V_H=4.0\,\mathrm{V}\)

## Q3
### Given
Same Schmitt as Q2, \(\beta=R_1/(R_1+R_2)=0.20\), with \(R=22\,\mathrm{k}\Omega\) and \(C=100\,\mathrm{nF}\) from output to the inverting input (grounded capacitor at \(-\)), forming an astable.
### Find
Period \(T=2RC\ln[(1+\beta)/(1-\beta)]\).
### Solution
\(RC=2.2\,\mathrm{ms}\). \(\ln(1.2/0.8)=\ln 1.5=0.4055\). \(T=2\times 2.2\times 10^{-3}\times 0.4055=1.78\,\mathrm{ms}\). Frequency \(561\,\mathrm{Hz}\).
### Answer
\(T=1.78\,\mathrm{ms}\) (\(f=561\,\mathrm{Hz}\))

## Q4
### Given
Ideal superdiode half-wave rectifier (op-amp output through a silicon diode to the load node, feedback from the load node to \(-\), input to \(+\)). \(v_{in}=0.20\sin\omega t\) V, load \(R_L\) to ground. No saturation delay.
### Find
Peak output voltage and the output during the negative half-cycle.
### Solution
Positive half: loop closed, \(v_o=v_{in}\), peak \(+0.20\,\mathrm{V}\) (diode drop absorbed inside the loop). Negative half: diode off, load held at 0 by \(R_L\) (assuming no other path).
### Answer
Peak \(+0.20\,\mathrm{V}\); negative half \(v_o=0\)

## Q5
### Given
Inverting precision full-wave rectifier that realises \(v_o=-|v_{in}|\) with matched resistors. \(v_{in}=1.5\sin\omega t\) V, ideal op-amps.
### Find
Peak output and the DC average of \(v_o\).
### Solution
\(|v_{in}|\) is a full-wave rectified sinusoid of peak 1.5 V. \(v_o\) peak is \(-1.5\,\mathrm{V}\). Average of a full-wave rectified sine of peak \(V_m\) is \(2V_m/\pi\), then the minus sign: \(V_{dc}=-2\times 1.5/\pi=-0.955\,\mathrm{V}\).
### Answer
Peak \(v_o=-1.5\,\mathrm{V}\), \(V_{dc}=-0.955\,\mathrm{V}\)

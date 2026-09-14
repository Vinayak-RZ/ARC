# Worked questions — linear op-amps

## Q1
### Given
Ideal op-amp inverting amplifier, \(R_1=2.2\,\mathrm{k}\Omega\), \(R_f=33\,\mathrm{k}\Omega\), \(v_{in}=0.40\,\mathrm{V}\) DC. Supplies \(\pm 15\,\mathrm{V}\), output can reach the rails.
### Find
\(v_o\) and the input resistance seen by the source.
### Solution
\(v_o=-(33/2.2)\times 0.40=-6.00\,\mathrm{V}\). Input resistance is \(R_1=2.2\,\mathrm{k}\Omega\) because the inverting node is virtual ground.
### Answer
\(v_o=-6.00\,\mathrm{V}\), \(R_{in}=2.2\,\mathrm{k}\Omega\)

## Q2
### Given
Noninverting amplifier, \(R_1=4.7\,\mathrm{k}\Omega\) (grounded), \(R_f=18.8\,\mathrm{k}\Omega\), \(v_{in}=1.20\,\mathrm{V}\). Ideal op-amp.
### Find
Closed-loop gain and \(v_o\).
### Solution
\(A=1+18.8/4.7=5.00\). \(v_o=6.00\,\mathrm{V}\).
### Answer
\(A=5.00\), \(v_o=6.00\,\mathrm{V}\)

## Q3
### Given
Inverting summer, \(R_f=24\,\mathrm{k}\Omega\), \(R_a=12\,\mathrm{k}\Omega\) from \(v_a=0.50\,\mathrm{V}\), \(R_b=8.0\,\mathrm{k}\Omega\) from \(v_b=-0.20\,\mathrm{V}\), \(R_c=24\,\mathrm{k}\Omega\) from \(v_c=1.00\,\mathrm{V}\). Ideal op-amp.
### Find
\(v_o\).
### Solution
\(v_o=-24(0.50/12 + (-0.20)/8 + 1.00/24)=-24(0.04167-0.02500+0.04167)=-1.40\,\mathrm{V}\).
### Answer
\(v_o=-1.40\,\mathrm{V}\)

## Q4
### Given
Three-op-amp instrumentation amplifier with \(R=25\,\mathrm{k}\Omega\), \(R_G=5.0\,\mathrm{k}\Omega\), subtractor gain \(R_F/R_A=1\), \(v_2=2.010\,\mathrm{V}\), \(v_1=1.990\,\mathrm{V}\).
### Find
Differential gain and \(v_o\).
### Solution
Front-end gain \(1+2R/R_G=1+50/5=11\). Overall \(A_d=11\). \(v_2-v_1=20\,\mathrm{mV}\), \(v_o=0.220\,\mathrm{V}\).
### Answer
\(A_d=11\), \(v_o=0.220\,\mathrm{V}\)

## Q5
### Given
Ideal integrator, \(R=10\,\mathrm{k}\Omega\), \(C=100\,\mathrm{nF}\), \(v_{in}=0.50\,\mathrm{V}\) DC applied at \(t=0\) with \(v_C(0)=0\) (output initially 0). Supplies \(\pm 12\,\mathrm{V}\).
### Find
Time at which the output reaches a rail, and which rail.
### Solution
\(v_o(t)=-(1/RC) \times 0.50\, t=-(1/(10^4\times 10^{-7}))\times 0.50\, t=-500 t\) volts with \(t\) in seconds. Negative ramp. Hits \(-12\,\mathrm{V}\) at \(t=12/500=24\,\mathrm{ms}\).
### Answer
\(t=24\,\mathrm{ms}\), negative rail (\(-12\,\mathrm{V}\))

## Q6
### Given
Op-amp with \(\mathrm{SR}=0.50\,\mathrm{V/\mu s}\) must output \(v_o=8\sin 2\pi f t\) volts without slew limiting.
### Find
Maximum frequency.
### Solution
\(2\pi f \times 8 \le 0.50\times 10^6\). \(f\le 0.50\times 10^6/(16\pi)=9.95\,\mathrm{kHz}\).
### Answer
\(f_{\max}=9.95\,\mathrm{kHz}\)

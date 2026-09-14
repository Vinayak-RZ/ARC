# Worked questions — oscillators

## Q1
### Given
Wien-bridge, equal arms \(R=10.0\,\mathrm{k}\Omega\), \(C=15.0\,\mathrm{nF}\). Noninverting op-amp with \(R_g=5.10\,\mathrm{k}\Omega\).
### Find
\(f_0\) and the \(R_f\) that sets \(A=3.10\) (5 % above 3 for start-up).
### Solution
\(f_0=1/(2\pi RC)=1/(2\pi\times 10^4\times 15\times 10^{-9})=1.061\,\mathrm{kHz}\). \(A=1+R_f/R_g=3.10\Rightarrow R_f=2.10\times 5.10=10.7\,\mathrm{k}\Omega\).
### Answer
\(f_0=1.06\,\mathrm{kHz}\), \(R_f=10.7\,\mathrm{k}\Omega\)

## Q2
### Given
Three-section RC phase-shift oscillator, equal \(R=4.7\,\mathrm{k}\Omega\), equal \(C=10\,\mathrm{nF}\), inverting op-amp.
### Find
\(f_0\) and the minimum \(|A|\).
### Solution
\(f_0=1/(2\pi RC\sqrt{6})=1/(2\pi\times 4.7\times 10^3\times 10^{-8}\times 2.449)=1.38\,\mathrm{kHz}\). \(|A|_{\min}=29\).
### Answer
\(f_0=1.38\,\mathrm{kHz}\), \(|A|\ge 29\)

## Q3
### Given
Colpitts, \(L=22\,\mu\mathrm{H}\), \(C_1=220\,\mathrm{pF}\), \(C_2=680\,\mathrm{pF}\), neglect device capacitance and coil resistance.
### Find
\(f_0\), \(C_{eq}=C_1 C_2/(C_1+C_2)\), and the minimum \(|A|\) using \(\beta=C_1/C_2\).
### Solution
\(C_{eq}=(220\times 680)/(220+680)=166.2\,\mathrm{pF}\). \(\omega_0=1/\sqrt{22\times 10^{-6}\times 166.2\times 10^{-12}}=1.654\times 10^7\,\mathrm{rad/s}\). \(f_0=2.63\,\mathrm{MHz}\). Using \(\beta=C_1/C_2=220/680=0.324\), the amplifier must supply \(|A|\ge 1/\beta=3.09\).
### Answer
\(f_0=2.63\,\mathrm{MHz}\), \(C_{eq}=166\,\mathrm{pF}\), \(|A|\ge 3.09\)

## Q4
### Given
Quartz equivalent: \(L_s=12.0\,\mathrm{H}\), \(C_s=21.0\,\mathrm{fF}\), \(C_p=5.0\,\mathrm{pF}\), \(R_s=40\,\Omega\).
### Find
\(f_s\), \(f_p\), and \(Q\) at series resonance.
### Solution
\(f_s=1/(2\pi\sqrt{12\times 21\times 10^{-15}})=1/(2\pi\sqrt{2.52\times 10^{-13}})=1/(2\pi\times 5.020\times 10^{-7})=317\,\mathrm{kHz}\). \(f_p=f_s\sqrt{1+21\times 10^{-15}/5.0\times 10^{-12}}=f_s\sqrt{1.0042}=317.7\,\mathrm{kHz}\). \(Q=\omega_s L_s/R_s=2\pi\times 3.17\times 10^5\times 12/40=5.97\times 10^5\).
### Answer
\(f_s=317\,\mathrm{kHz}\), \(f_p=318\,\mathrm{kHz}\), \(Q=6.0\times 10^5\)

## Q5
### Given
555 astable, \(R_A=6.8\,\mathrm{k}\Omega\), \(R_B=3.3\,\mathrm{k}\Omega\), \(C=0.10\,\mu\mathrm{F}\).
### Find
\(T_H\), \(T_L\), frequency, and duty cycle \(T_H/(T_H+T_L)\).
### Solution
\(T_H=0.693(6.8+3.3)\times 10^3\times 0.10\times 10^{-6}=0.700\,\mathrm{ms}\). \(T_L=0.693\times 3.3\times 10^3\times 0.10\times 10^{-6}=0.229\,\mathrm{ms}\). \(T=0.929\,\mathrm{ms}\), \(f=1.08\,\mathrm{kHz}\). Duty \(=0.754\). Formula check: \(f=1.44/((6.8+6.6)\times 10^3\times 10^{-7})=1.07\,\mathrm{kHz}\).
### Answer
\(T_H=0.700\,\mathrm{ms}\), \(T_L=0.229\,\mathrm{ms}\), \(f=1.08\,\mathrm{kHz}\), duty \(=75.4\,\%\)

# Worked questions — feedback amplifiers

## Q1
### Given
Voltage-series feedback, open-loop \(A=800\) (dimensionless), \(\beta=0.12\). \(A\) later falls 25 % because \(\beta_{BJT}\) drifted.
### Find
Closed-loop gain before and after the drift, and the percent change in \(A_f\).
### Solution
\(L=800\times 0.12=96\). \(A_f=800/97=8.247\). After, \(A=600\), \(L=72\), \(A_f=600/73=8.219\). Change \((8.219-8.247)/8.247=-0.34\,\%\). Check: \(dA/A=-25\,\%\), \(1/(1+L)=1/97\), product \(-0.26\,\%\) (first-order); the exact finite-step value is \(-0.34\,\%\).
### Answer
\(A_f=8.25\) then \(8.22\); \(\Delta A_f/A_f=-0.34\,\%\)

## Q2
### Given
CE stage, \(g_m=40\,\mathrm{mS}\), \(r_\pi=2.5\,\mathrm{k}\Omega\), \(R_C=4.7\,\mathrm{k}\Omega\), unbypassed \(R_E=220\,\Omega\), \(R_L=\infty\), \(r_o=\infty\). Treat as current-series (transconductance) feedback with \(A=g_m\) of the naked device loaded by \(R_C\), \(\beta=R_E\) at the output-current to input-voltage port, or use the exact \(A_v\) formula.
### Find
Voltage gain \(v_c/v_b\) and resistance looking into the base.
### Solution
\(A_v=-g_m R_C/(1+g_m R_E)=-40\times 10^{-3}\times 4700/(1+40\times 10^{-3}\times 220)=-188/9.8=-19.18\). \(R_{ib}=r_\pi+(\beta_{\pi}+1)R_E\). \(\beta_{\pi}=g_m r_\pi=100\). \(R_{ib}=2500+101\times 220=24.7\,\mathrm{k}\Omega\).
### Answer
\(A_v=-19.2\), \(R_{ib}=24.7\,\mathrm{k}\Omega\)

## Q3
### Given
Ideal op-amp except finite \(A_{od}=8.0\times 10^4\). Noninverting closed-loop with \(R_1=1.0\,\mathrm{k}\Omega\), \(R_f=9.0\,\mathrm{k}\Omega\) (\(\beta=0.10\)).
### Find
Ideal \(A_f\), actual \(A_f\), and the relative error versus ideal.
### Solution
Ideal \(A_f=10\). Actual \(A_f=A_{od}/(1+A_{od}\beta)=8.0\times 10^4/(1+8000)=9.99875\). Relative error \((9.99875-10)/10=-0.0125\,\%\).
### Answer
Ideal 10; actual 9.9988; error \(-0.0125\,\%\)

## Q4
### Given
Voltage-series loop, naked amplifier \(R_{in}=5.0\,\mathrm{k}\Omega\), \(R_{out}=2.0\,\mathrm{k}\Omega\), \(L=40\) at mid-band (already includes loading).
### Find
Closed-loop \(R_{in,f}\) and \(R_{out,f}\).
### Solution
\(R_{in,f}=5.0\times(1+40)=205\,\mathrm{k}\Omega\). \(R_{out,f}=2.0/41=48.8\,\Omega\).
### Answer
\(R_{in,f}=205\,\mathrm{k}\Omega\), \(R_{out,f}=48.8\,\Omega\)

## Q5
### Given
Open-loop voltage gain \(A_0=2.0\times 10^5\) with a single pole at \(f_p=8.0\,\mathrm{Hz}\). Voltage-series \(\beta=0.050\).
### Find
Closed-loop mid-band gain and closed-loop 3 dB bandwidth.
### Solution
\(A_f\approx 1/\beta=20.0\) (check \(L_0=A_0\beta=10^4\gg 1\)). \(f_{cl}=f_p(1+A_0\beta)=8.0\times(1+10^4)=80.0\,\mathrm{kHz}\). GBW check: \(A_0 f_p=1.60\,\mathrm{MHz}\), \(A_f f_{cl}=1.60\,\mathrm{MHz}\).
### Answer
\(A_f=20.0\), \(f_{cl}=80.0\,\mathrm{kHz}\)

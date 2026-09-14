# Worked questions — CMOS inverter, delay, power

## Q1
### Given
CMOS inverter, \(V_{DD}=3.3\,\mathrm{V}\), \(V_{tn}=0.50\,\mathrm{V}\), \(V_{tp}=-0.50\,\mathrm{V}\), \(k_n=k_p=200\,\mu\mathrm{A/V^2}\), \(\lambda=0\).
### Find
Switching threshold \(V_M\).
### Solution
Matched \(k\) and matched \(|V_t|\) \(\Rightarrow V_M=V_{DD}/2=1.65\,\mathrm{V}\). (Check formula: \(V_M=(0.50+1\cdot(3.3-0.50))/(1+1)=3.30/2=1.65\,\mathrm{V}\).)
### Answer
\(V_M=1.65\,\mathrm{V}\)

## Q2
### Given
\(R_{eqn}=2.5\,\mathrm{k}\Omega\), \(R_{eqp}=5.0\,\mathrm{k}\Omega\), \(C_L=80\,\mathrm{fF}\). Use \(t=0.69 RC\).
### Find
\(t_{PHL}\), \(t_{PLH}\), and \(t_p\).
### Solution
\(t_{PHL}=0.69\times 2.5\times 10^3\times 80\times 10^{-15}=138\,\mathrm{ps}\). \(t_{PLH}=0.69\times 5.0\times 10^3\times 80\times 10^{-15}=276\,\mathrm{ps}\). \(t_p=207\,\mathrm{ps}\).
### Answer
\(t_{PHL}=138\,\mathrm{ps}\), \(t_{PLH}=276\,\mathrm{ps}\), \(t_p=207\,\mathrm{ps}\)

## Q3
### Given
Node \(C_L=2.0\,\mathrm{pF}\), \(V_{DD}=5.0\,\mathrm{V}\), activity \(\alpha=0.20\), clock/data rate \(f=10\,\mathrm{MHz}\). Static current negligible.
### Find
Dynamic power.
### Solution
\(P=\alpha C V^2 f=0.20\times 2.0\times 10^{-12}\times 25\times 10\times 10^6=0.100\,\mathrm{mW}\).
### Answer
\(P_{\mathrm{dyn}}=0.100\,\mathrm{mW}\)

## Q4
### Given
Minimum nMOS \(W_n=0.40\,\mu\mathrm{m}\), \(\mu_n/\mu_p=2.5\), same \(L\). Want equal rise and fall \(R_{eq}\) (hence \(k_n=k_p\)).
### Find
\(W_p\).
### Solution
\(k\propto \mu W\), so \(\mu_n W_n=\mu_p W_p\Rightarrow W_p=2.5 W_n=1.00\,\mu\mathrm{m}\).
### Answer
\(W_p=1.00\,\mu\mathrm{m}\)

## Q5
### Given
Inverter VTC unity-gain points \(V_{IL}=1.1\,\mathrm{V}\), \(V_{IH}=1.9\,\mathrm{V}\), \(V_{DD}=3.3\,\mathrm{V}\), static \(V_{OL}=0\), \(V_{OH}=3.3\,\mathrm{V}\).
### Find
\(NM_L\) and \(NM_H\).
### Solution
\(NM_L=1.1-0=1.1\,\mathrm{V}\). \(NM_H=3.3-1.9=1.4\,\mathrm{V}\).
### Answer
\(NM_L=1.1\,\mathrm{V}\), \(NM_H=1.4\,\mathrm{V}\)

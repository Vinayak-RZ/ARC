# Worked questions — BJT bias and hybrid-π

## Q1
### Given
NPN, \(\beta=120\), \(V_{BE}=0.7\,\mathrm{V}\), \(V_{CC}=15\,\mathrm{V}\), collector-to-base bias with \(R_C=4.7\,\mathrm{k}\Omega\), \(R_B=180\,\mathrm{k}\Omega\), emitter grounded. Active-region model \(I_C=\beta I_B\).
### Find
\(I_B\), \(I_C\), \(V_{CE}\). Confirm forward-active.
### Solution
KVL around \(V_{CC}\), \(R_C\), \(R_B\), BE: \(V_{CC}=I_C R_C+I_B R_B+V_{BE}\) with \(I_C=120 I_B\). \(15=I_B(120\cdot 4700+180000)+0.7\). \(14.3=I_B(744000)\), \(I_B=19.22\,\mu\mathrm{A}\), \(I_C=2.307\,\mathrm{mA}\). \(V_{CE}=15-2.307\times 4.7=4.16\,\mathrm{V}\). \(V_{CB}=V_{CE}-V_{BE}=3.46\,\mathrm{V}>0\), forward-active.
### Answer
\(I_B=19.2\,\mu\mathrm{A}\), \(I_C=2.31\,\mathrm{mA}\), \(V_{CE}=4.16\,\mathrm{V}\) (active)

## Q2
### Given
Voltage-divider NPN: \(V_{CC}=12\,\mathrm{V}\), \(R_1=39\,\mathrm{k}\Omega\), \(R_2=10\,\mathrm{k}\Omega\), \(R_C=3.3\,\mathrm{k}\Omega\), \(R_E=1.0\,\mathrm{k}\Omega\), \(\beta=80\), \(V_{BE}=0.7\,\mathrm{V}\).
### Find
\(I_C\) and \(V_{CE}\) using the Thevenin base network (do not neglect \(I_B\)).
### Solution
\(V_{Th}=12\times 10/49=2.449\,\mathrm{V}\), \(R_{Th}=39\mathrm{k}\parallel 10\mathrm{k}=7.959\,\mathrm{k}\Omega\). \(I_E=(2.449-0.7)/(1000+7959/81)=1.749\,\mathrm{mA}/1.0983\,\mathrm{k}\Omega=1.592\,\mathrm{mA}\). \(I_C=\alpha I_E=(80/81)I_E=1.573\,\mathrm{mA}\). \(V_{CE}=12-I_C R_C-I_E R_E=12-5.190-1.592=5.22\,\mathrm{V}\).
### Answer
\(I_C=1.57\,\mathrm{mA}\), \(V_{CE}=5.22\,\mathrm{V}\)

## Q3
### Given
The Q-point of Q2: \(I_C=1.57\,\mathrm{mA}\), \(\beta=80\), \(V_T=26\,\mathrm{mV}\). \(R_E\) is fully bypassed. Load \(R_L=4.7\,\mathrm{k}\Omega\) AC-coupled at the collector. Ignore \(r_o\).
### Find
\(g_m\), \(r_\pi\), and mid-band \(A_v=v_o/v_b\) from base to collector.
### Solution
\(g_m=1.57\times 10^{-3}/0.026=60.4\,\mathrm{mS}\). \(r_\pi=80/0.0604=1325\,\Omega\). \(R_L'=3.3\mathrm{k}\parallel 4.7\mathrm{k}=1.939\,\mathrm{k}\Omega\). \(A_v=-g_m R_L'=-117\).
### Answer
\(g_m=60.4\,\mathrm{mS}\), \(r_\pi=1.32\,\mathrm{k}\Omega\), \(A_v=-117\)

## Q4
### Given
NPN switch: \(V_{CC}=5.0\,\mathrm{V}\), \(R_C=330\,\Omega\), emitter grounded, \(V_{CE,sat}=0.2\,\mathrm{V}\), \(\beta_{\min}=50\). Base driven from 5.0 V through \(R_B\).
### Find
Maximum \(R_B\) that still saturates the transistor, using forced \(\beta=10\) as the design rule stated in the problem (not \(\beta_{\min}\)).
### Solution
\(I_{C,sat}=(5.0-0.2)/330=14.55\,\mathrm{mA}\). Forced \(\beta=10\) \(\Rightarrow I_B=1.455\,\mathrm{mA}\). \(R_B=(5.0-0.7)/1.455\times 10^{-3}=2956\,\Omega\). Any larger \(R_B\) reduces \(I_B\) and may leave the device out of saturation under the forced-\(\beta\) rule.
### Answer
\(R_B\le 2.96\,\mathrm{k}\Omega\)

## Q5
### Given
Emitter follower: \(I_E=2.0\,\mathrm{mA}\), \(\beta=99\), \(V_T=26\,\mathrm{mV}\), unbypassed \(R_E=2.2\,\mathrm{k}\Omega\), no external load, source resistance at the base \(R_s=1.0\,\mathrm{k}\Omega\) already including bias resistors.
### Find
Small-signal \(A_v=v_e/v_s\) and \(R_{out}\) looking into the emitter with \(R_s\) present.
### Solution
\(g_m=I_C/V_T\), \(I_C=\alpha I_E=(99/100)\times 2.0=1.98\,\mathrm{mA}\), \(g_m=76.2\,\mathrm{mS}\), \(r_\pi=\beta/g_m=1299\,\Omega\). \(A_v=\frac{(\beta+1)R_E}{r_\pi+R_s+(\beta+1)R_E}=\frac{100\times 2200}{1299+1000+220000}=0.989\). \(R_{out}=\frac{r_\pi+R_s}{\beta+1}\parallel R_E=23.0\,\Omega\parallel 2.2\,\mathrm{k}\Omega=22.7\,\Omega\).
### Answer
\(A_v=0.989\), \(R_{out}=22.7\,\Omega\)

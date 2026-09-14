# Worked questions — PWM techniques

## Q1
### Given
Three-phase linear SPWM, \(V_{dc}=600\,\mathrm{V}\), \(m_a=0.80\). Use \(V_{LL,1}=0.612\, m_a V_{dc}\).
### Find
RMS fundamental line-to-line voltage.
### Solution
\(V_{LL,1}=0.612\times 0.80\times 600=294\,\mathrm{V}\).
### Answer
\(V_{LL,1}=294\,\mathrm{V}\) RMS

## Q2
### Given
The same 600 V bus must produce 415 V RMS line fundamental if possible.
### Find
Required \(m_a\) in linear SPWM, whether it is feasible, and the SVPWM linear ceiling voltage.
### Solution
Linear SPWM would need \(m_a=415/(0.612\times 600)=1.13>1\), so linear SPWM cannot. SVPWM ceiling \(0.707\times 600=424\,\mathrm{V}>415\,\mathrm{V}\), so SVPWM (or third-harmonic injection) can, with \(415/424=0.98\) of that ceiling. Six-step would give \(0.780\times 600=468\,\mathrm{V}\).
### Answer
Linear SPWM infeasible (\(m_a=1.13\)); SVPWM ceiling \(424\,\mathrm{V}\) (OK)

## Q3
### Given
Single-phase full-bridge bipolar SPWM, \(V_{dc}=200\,\mathrm{V}\), \(m_a=0.90\). Pole formula \(\langle v_{ao}\rangle=(V_{dc}/2)m_a\sin\omega t\), opposite poles.
### Find
Peak fundamental of \(v_{ab}\) and its RMS.
### Solution
\(\hat V_{ab1}=m_a V_{dc}=0.90\times 200=180\,\mathrm{V}\). RMS \(180/\sqrt{2}=127.3\,\mathrm{V}\).
### Answer
\(\hat V_1=180\,\mathrm{V}\), \(V_{1,\mathrm{rms}}=127\,\mathrm{V}\)

## Q4
### Given
Carrier \(f_c=5.25\,\mathrm{kHz}\), modulating \(f_m=50\,\mathrm{Hz}\).
### Find
\(m_f\) and whether this is a synchronized odd-triple choice for three-phase SPWM.
### Solution
\(m_f=5250/50=105\). 105 is odd and \(105/3=35\), so it is an odd multiple of three: a legal synchronized three-phase index.
### Answer
\(m_f=105\) (odd triple, OK)

## Q5
### Given
Hysteresis current control, band \(h=0.40\,\mathrm{A}\) (total width \(2h=0.80\,\mathrm{A}\)), \(L=4.0\,\mathrm{mH}\), DC bus \(V_{dc}=200\,\mathrm{V}\), back-emf near zero. Estimate \(f_{sw}\approx V_{dc}/(4 h L)\) for a single-phase H-bridge that applies \(\pm V_{dc}\).
### Find
Estimated switching frequency.
### Solution
\(f_{sw}=200/(4\times 0.40\times 0.004)=200/0.0064=31.25\,\mathrm{kHz}\).
### Answer
\(f_{sw}\approx 31.3\,\mathrm{kHz}\)

## Q6
### Given
A CCM buck chopper uses triangle PWM, \(V_{in}=48\,\mathrm{V}\), the DC reference is 0.70 of the triangle peak (so \(D=0.70\)).
### Find
Average output voltage \(V_{out}\).
### Solution
Buck CCM: \(V_{out}=D V_{in}=0.70\times 48=33.6\,\mathrm{V}\).
### Answer
\(V_{out}=33.6\,\mathrm{V}\)

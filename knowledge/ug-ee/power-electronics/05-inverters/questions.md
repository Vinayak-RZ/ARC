# Worked questions — inverters

## Q1
### Given
A single-phase full-bridge VSI operates in square-wave mode with \(V_{dc}=180\,\mathrm{V}\). Ideal switches.
### Find
Fundamental peak voltage, fundamental RMS, waveform RMS, and voltage THD.
### Solution
\(V_{1,\mathrm{pk}}=4\times 180/\pi=229.2\,\mathrm{V}\). \(V_{1,\mathrm{rms}}=229.2/\sqrt{2}=162.1\,\mathrm{V}\). Waveform RMS \(=180\,\mathrm{V}\). \(\mathrm{THD}_v=\sqrt{(180/162.1)^2-1}=\sqrt{1.233-1}=0.483\).
### Answer
\(V_{1,\mathrm{pk}}=229\,\mathrm{V}\), \(V_{1,\mathrm{rms}}=162\,\mathrm{V}\), \(V_{\mathrm{rms}}=180\,\mathrm{V}\), \(\mathrm{THD}=48.3\%\)

## Q2
### Given
Three-phase 180° conduction VSI, \(V_{dc}=700\,\mathrm{V}\).
### Find
RMS fundamental line-to-line voltage.
### Solution
\(V_{LL,1}=\sqrt{6}\,V_{dc}/\pi=2.4495\times 700/3.1416=546\,\mathrm{V}\).
### Answer
\(V_{LL,1}=546\,\mathrm{V}\) RMS

## Q3
### Given
The inverter of Q1 feeds a series \(R=4\,\Omega\), \(L=25\,\mathrm{mH}\) at 50 Hz square wave. Consider the fundamental and the third harmonic only.
### Find
RMS current of the fundamental, of the third harmonic, and their combined RMS (ignore higher terms).
### Solution
\(\omega=314.16\). \(Z_1=\sqrt{4^2+(0.025\times 314.16)^2}=\sqrt{16+61.62}=\sqrt{77.62}=8.81\,\Omega\). \(I_1=162.1/8.81=18.40\,\mathrm{A}\). \(V_3=V_{1,\mathrm{rms}}/3=54.03\,\mathrm{V}\). \(Z_3=\sqrt{16+(3\times 7.854)^2}=\sqrt{16+555.3}=23.91\,\Omega\). \(I_3=2.26\,\mathrm{A}\). Combined \(\sqrt{18.40^2+2.26^2}=18.54\,\mathrm{A}\).
### Answer
\(I_1=18.4\,\mathrm{A}\), \(I_3=2.26\,\mathrm{A}\), \(I\approx 18.5\,\mathrm{A}\)

## Q4
### Given
A three-phase CSI delivers a 120° quasi-square current of amplitude \(I_{dc}=30\,\mathrm{A}\) into a balanced load.
### Find
Peak fundamental AC current (use \(I_{1,\mathrm{pk}}=(2\sqrt{3}/\pi)I_{dc}\)).
### Solution
\(I_{1,\mathrm{pk}}=(2\times 1.7321/3.1416)\times 30=33.07\,\mathrm{A}\). RMS fundamental \(33.07/\sqrt{2}=23.4\,\mathrm{A}\).
### Answer
\(I_{1,\mathrm{pk}}=33.1\,\mathrm{A}\) (\(I_{1,\mathrm{rms}}=23.4\,\mathrm{A}\))

## Q5
### Given
A 180° VSI with \(V_{dc}=500\,\mathrm{V}\) feeds an induction machine rated 415 V line RMS at 50 Hz. Square-wave (six-step) operation.
### Find
The fundamental line voltage and whether the machine is over- or under-fluxed relative to 415 V if frequency stays 50 Hz.
### Solution
\(V_{LL,1}=0.7797\times 500=390\,\mathrm{V}\) RMS. Rated is 415 V, so the fundamental is 6% low: slightly under-fluxed at 50 Hz (V/f = 390/50 = 7.80 versus 8.30 V/Hz).
### Answer
\(V_{LL,1}=390\,\mathrm{V}\); under-fluxed at 50 Hz

## Q6
### Given
Single-phase square-wave inverter, \(V_{dc}=100\,\mathrm{V}\), \(f=60\,\mathrm{Hz}\), purely inductive \(L=40\,\mathrm{mH}\). Include all odd harmonics in the current RMS via \(\sum_{k=0}^{\infty} I_{2k+1}^2\).
### Find
Fundamental current RMS and a lower bound using only \(n=1,3,5\).
### Solution
\(V_n^{\mathrm{rms}}=(4V_{dc}/(n\pi))/\sqrt{2}=90.05/n\,\mathrm{V}\). \(Z_n=n\omega L=n\times 15.08\,\Omega\). \(I_n=90.05/(n^2\times 15.08)=5.97/n^2\,\mathrm{A}\). \(I_1=5.97\,\mathrm{A}\), \(I_3=0.663\,\mathrm{A}\), \(I_5=0.239\,\mathrm{A}\). Combined \(\sqrt{5.97^2+0.663^2+0.239^2}=6.01\,\mathrm{A}\).
### Answer
\(I_1=5.97\,\mathrm{A}\); \(I_{1+3+5}=6.01\,\mathrm{A}\)

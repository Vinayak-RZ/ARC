# Worked questions — uncontrolled rectifiers

## Q1
### Given
A single-phase diode bridge, ideal diodes, feeds a resistive \(R=12\,\Omega\) from \(v_s=230\sqrt{2}\sin\omega t\) volts (50 Hz). No filter inductor or capacitor.
### Find
Average load voltage, average load current, and load voltage RMS.
### Solution
\(V_m=230\sqrt{2}=325.3\,\mathrm{V}\). \(V_{dc}=2V_m/\pi=207.1\,\mathrm{V}\). \(I_{dc}=207.1/12=17.26\,\mathrm{A}\). For full-wave rectified sinusoid, \(V_{\mathrm{rms}}=V_m/\sqrt{2}=230\,\mathrm{V}\) (same as the AC RMS).
### Answer
\(V_{dc}=207\,\mathrm{V}\), \(I_{dc}=17.3\,\mathrm{A}\), \(V_{\mathrm{rms}}=230\,\mathrm{V}\)

## Q2
### Given
A three-phase six-pulse diode bridge, no overlap, \(V_{LL}=400\,\mathrm{V}\) RMS. Highly inductive DC load, \(I_{dc}=25\,\mathrm{A}\).
### Find
Average DC voltage, average current per diode, and RMS current per diode.
### Solution
\(V_{dc}=(3\sqrt{2}/\pi)\times 400=540.2\,\mathrm{V}\). \(I_{D,\mathrm{avg}}=25/3=8.333\,\mathrm{A}\). \(I_{D,\mathrm{rms}}=25/\sqrt{3}=14.43\,\mathrm{A}\).
### Answer
\(V_{dc}=540\,\mathrm{V}\), \(I_{D,\mathrm{avg}}=8.33\,\mathrm{A}\), \(I_{D,\mathrm{rms}}=14.4\,\mathrm{A}\)

## Q3
### Given
Same 400 V three-phase bridge as Q2, now with source inductance \(L_s=1.2\,\mathrm{mH}\) per phase, \(I_{dc}=25\,\mathrm{A}\), \(f=50\,\mathrm{Hz}\). Continuous current.
### Find
DC voltage including overlap drop, and the overlap angle \(u\).
### Solution
\(\omega=314.16\,\mathrm{rad/s}\). Drop \(3\omega L_s I_{dc}/\pi=3\times 314.16\times 0.0012\times 25/\pi=8.99\,\mathrm{V}\). \(V_{dc}=540.2-8.99=531.2\,\mathrm{V}\). Argument of arccos: \(1-2\omega L_s I_{dc}/(\sqrt{2}V_{LL})=1-2\times 314.16\times 0.0012\times 25/(400\sqrt{2})=1-0.0333=0.9667\). \(u=\arccos(0.9667)=0.259\,\mathrm{rad}=14.8^\circ\).
### Answer
\(V_{dc}=531\,\mathrm{V}\), \(u=14.8^\circ\)

## Q4
### Given
A single-phase bridge with highly inductive load \(I_{dc}=10\,\mathrm{A}\), \(V_m=160\,\mathrm{V}\), source inductance \(L_s=4.0\,\mathrm{mH}\) in the AC loop model that uses drop \(2\omega L_s I_{dc}/\pi\), 50 Hz.
### Find
Ideal \(V_{dc}\) without overlap, the overlap drop, and \(V_{dc}\) with overlap.
### Solution
Ideal \(V_{dc}=2V_m/\pi=101.86\,\mathrm{V}\). Drop \(2\times 314.16\times 0.004\times 10/\pi=8.00\,\mathrm{V}\). With overlap \(V_{dc}=93.86\,\mathrm{V}\).
### Answer
\(V_{dc0}=102\,\mathrm{V}\), drop \(8.00\,\mathrm{V}\), \(V_{dc}=93.9\,\mathrm{V}\)

## Q5
### Given
Three-phase diode bridge, \(V_{LL}=415\,\mathrm{V}\). Unfiltered six-pulse envelope (no DC \(L\) or \(C\)), resistive load so current follows voltage. Peak DC voltage is \(\sqrt{2}V_{LL}\). Minimum of the envelope is \(\sqrt{2}V_{LL}\cos(\pi/6)\).
### Find
Peak DC voltage, minimum envelope voltage, and the unfiltered peak-to-peak ripple.
### Solution
\(V_{pk}=415\sqrt{2}=586.9\,\mathrm{V}\). \(V_{\min}=586.9\times\cos(30^\circ)=508.2\,\mathrm{V}\). Peak-to-peak ripple \(586.9-508.2=78.7\,\mathrm{V}\).
### Answer
\(V_{pk}=587\,\mathrm{V}\), \(V_{\min}=508\,\mathrm{V}\), \(V_{\mathrm{pp,ripple}}=78.7\,\mathrm{V}\)

## Q6
### Given
A single-phase half-wave diode feeds \(R=20\,\Omega\) in series with a large inductance that keeps \(i_L\) continuous and nearly flat. AC source 120 V RMS, 60 Hz. A freewheel diode is placed across the series \(R\)–\(L\) load.
### Find
Average load voltage and average load current with the freewheel diode present (ideal diodes).
### Solution
With a freewheel diode, the load voltage is the positive half of the source and zero on the negative half. \(V_m=120\sqrt{2}=169.7\,\mathrm{V}\). \(V_{dc}=V_m/\pi=54.0\,\mathrm{V}\). \(I_{dc}=54.0/20=2.70\,\mathrm{A}\). (Without freewheel, a large \(L\) would force the source diode to conduct into the negative half-cycle and \(V_{dc}\) would fall.)
### Answer
\(V_{dc}=54.0\,\mathrm{V}\), \(I_{dc}=2.70\,\mathrm{A}\)

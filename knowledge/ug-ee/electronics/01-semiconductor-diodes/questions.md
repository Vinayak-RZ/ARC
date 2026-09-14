# Worked questions — diodes, rectifiers, clippers, clampers

## Q1
### Given
A silicon diode (\(V_\gamma=0.7\,\mathrm{V}\)) is in series with \(R=2.2\,\mathrm{k}\Omega\) across a DC source \(V_s=9.0\,\mathrm{V}\), anode toward the positive terminal. \(I_S\) is unknown; use the constant-drop model.
### Find
The diode current and the voltage across the resistor.
### Solution
The source exceeds \(V_\gamma\), so the diode is ON. KVL: \(9.0=0.7+I_D\cdot 2200\). Thus \(I_D=(8.3)/2200=3.773\,\mathrm{mA}\). Voltage on the resistor is \(8.3\,\mathrm{V}\).
### Answer
\(I_D=3.77\,\mathrm{mA}\), \(V_R=8.3\,\mathrm{V}\)

## Q2
### Given
An ideal-diode half-wave rectifier feeds \(R_L=1.2\,\mathrm{k}\Omega\) from a 12 V RMS, 50 Hz secondary (sinusoid). No filter capacitor.
### Find
Peak load voltage, average load voltage, average load current, and diode PIV.
### Solution
\(V_m=12\sqrt{2}=16.97\,\mathrm{V}\). Half-wave average \(V_{dc}=V_m/\pi=5.40\,\mathrm{V}\). \(I_{dc}=5.40/1200=4.50\,\mathrm{mA}\). PIV for unloaded (no C) half-wave is \(V_m=16.97\,\mathrm{V}\).
### Answer
\(V_m=17.0\,\mathrm{V}\), \(V_{dc}=5.40\,\mathrm{V}\), \(I_{dc}=4.50\,\mathrm{mA}\), \(\mathrm{PIV}=17.0\,\mathrm{V}\)

## Q3
### Given
A bridge rectifier uses silicon diodes (\(V_\gamma=0.7\,\mathrm{V}\) each). Secondary is 18 V RMS. A capacitor \(C=2200\,\mu\mathrm{F}\) feeds \(R_L=75\,\Omega\). Line frequency 50 Hz. Use \(V_{dc}\approx V_{peak}-V_{r,\mathrm{pp}}/2\) with \(V_{r,\mathrm{pp}}=I_{dc}/(2fC)\) iterated once from \(I_{dc}\approx V_{peak}/R_L\).
### Find
Approximate DC load voltage and peak-to-peak ripple.
### Solution
Secondary peak \(18\sqrt{2}=25.46\,\mathrm{V}\). Two drops: \(V_{peak}=25.46-1.4=24.06\,\mathrm{V}\). \(I_{dc}\approx 24.06/75=0.321\,\mathrm{A}\). \(V_{r,\mathrm{pp}}=0.321/(2\cdot 50\cdot 2200\times 10^{-6})=1.46\,\mathrm{V}\). Then \(V_{dc}\approx 24.06-0.73=23.33\,\mathrm{V}\).
### Answer
\(V_{dc}\approx 23.3\,\mathrm{V}\), \(V_{r,\mathrm{pp}}\approx 1.46\,\mathrm{V}\)

## Q4
### Given
A shunt clipper: source \(v_i=8\sin\omega t\) volts in series with \(1\,\mathrm{k}\Omega\); a silicon diode (0.7 V) to ground at the output node, cathode grounded (anode at output). No other bias.
### Find
The positive and negative peak values of \(v_o\).
### Solution
When \(v_i\) is positive the diode is forward-biased (anode at \(v_o\), cathode at ground) and clamps \(v_o\) at \(+0.7\,\mathrm{V}\). When \(v_i\) is negative the diode is reverse-biased, no current flows in the 1 kΩ, and \(v_o=v_i\), so the negative peak is \(-8\,\mathrm{V}\).
### Answer
Positive peak \(+0.7\,\mathrm{V}\), negative peak \(-8\,\mathrm{V}\)

## Q5
### Given
A positive clamper: series capacitor, then a silicon diode to ground (anode grounded, cathode at the output node), load \(R_L\) with \(R_L C\gg T\). Input \(v_i=6\sin\omega t\) V (no DC).
### Find
The steady-state positive and negative peaks of \(v_o\).
### Solution
The diode conducts on the most negative input, charging the capacitor so that the output negative peak sits at \(-V_\gamma=-0.7\,\mathrm{V}\). Peak-to-peak of \(v_i\) is 12 V and is preserved, so the positive peak is \(-0.7+12=+11.3\,\mathrm{V}\). Equivalently \(v_C\) charges to \(6-0.7=5.3\,\mathrm{V}\) with polarity adding on positive half-cycles: \(v_o=v_i+5.3\), peaks \(11.3\) and \(-0.7\).
### Answer
Positive peak \(+11.3\,\mathrm{V}\), negative peak \(-0.7\,\mathrm{V}\)

## Q6
### Given
Zener \(V_Z=5.6\,\mathrm{V}\), \(P_{Z,\max}=400\,\mathrm{mW}\), series \(R_s=220\,\Omega\), \(V_{in}=12\,\mathrm{V}\) DC, load \(R_L=470\,\Omega\). Ideal Zener (\(r_z=0\)) in breakdown if \(I_Z>0\).
### Find
Whether the Zener is in breakdown, \(I_L\), \(I_Z\), and whether \(P_Z\) is within rating.
### Solution
Assume \(V_L=5.6\,\mathrm{V}\). \(I_L=5.6/470=11.91\,\mathrm{mA}\). \(I_s=(12-5.6)/220=29.09\,\mathrm{mA}\). \(I_Z=29.09-11.91=17.18\,\mathrm{mA}>0\), so breakdown is valid. \(P_Z=5.6\times 17.18\times 10^{-3}=96.2\,\mathrm{mW}<400\,\mathrm{mW}\).
### Answer
In breakdown; \(I_L=11.9\,\mathrm{mA}\); \(I_Z=17.2\,\mathrm{mA}\); \(P_Z=96\,\mathrm{mW}\) (OK)

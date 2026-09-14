# Diodes, rectifiers, clippers, and clampers

A pn junction diode is the first nonlinear device a UG electrical engineer is asked to analyse with the same seriousness as R, L, and C. Linear circuit theory still applies on either side of a piecewise model; the junction itself does not obey Ohm's law. This unit covers the Shockley equation, DC models used in exams, half-wave and full-wave rectifiers with capacitive filters, series and shunt clippers, clampers (DC restorers), and a short look at Zener regulation and special diodes that appear on the same syllabus.

## Concepts

A semiconductor diode is a two-terminal device that conducts easily in one polarity (forward) and almost not at all in the other (reverse) until breakdown. The metallurgical junction between p-type and n-type silicon forms a depletion region. Applying a forward voltage of about 0.7 V for silicon (about 0.3 V for germanium, about 0.2–0.4 V for a Schottky barrier) collapses that region enough for exponential current. Reverse bias widens the depletion region; only a nanoampere-to-microampere saturation current remains until avalanche or Zener breakdown.

The Shockley equation \(I = I_S(e^{v_D/(nV_T)}-1)\) is the device-physics truth. \(I_S\) doubles roughly every 10 °C; \(V_T = kT/q\) is about 26 mV at 300 K; the emission coefficient \(n\) is near 1 in the diffusion region and near 2 in the recombination region. For hand analysis nobody iterates the exponential at every node. Three DC models are used in UG courses:

1. Ideal switch: \(v_D=0\) when on, open when off. Good for first-cut rectifier waveforms.
2. Constant-drop (offset) model: \(v_D=V_\gamma\) (0.7 V Si) when on. The default for clippers, clampers, and rectifier DC levels.
3. Piecewise-linear: \(V_\gamma\) plus a small bulk resistance \(r_f\). Needed when the question gives a slope or a specified dynamic resistance.

Load-line construction on the exponential \(i\)–\(v\) curve is the graphical version of the same idea: the source–resistor Thevenin line intersects the diode curve at the Q-point.

Rectifiers convert AC to unipolar pulses. A half-wave rectifier uses one diode; the load sees only one polarity of the secondary. Peak inverse voltage (PIV) on that diode is \(V_m\) without a capacitor and \(2V_m\) with a large filter capacitor, because the capacitor holds \(+V_m\) while the AC trough is \(-V_m\). A full-wave centre-tap rectifier uses two diodes and a centre-tapped secondary; each diode sees \(2V_m\) PIV where \(V_m\) is the peak of one half-winding. A bridge rectifier uses four diodes, no centre tap, PIV \(V_m\) per diode, and two diode drops in the forward path. Average (DC) load voltage without filter is \(V_m/\pi\) (half-wave) or \(2V_m/\pi\) (full-wave). RMS of a half-wave sinusoid pulse train of peak \(V_m\) is \(V_m/2\); full-wave is \(V_m/\sqrt{2}\), the same as the original AC RMS if drops are neglected.

A reservoir capacitor across the load reduces ripple. In the large-\(RC\) approximation the capacitor charges near the peaks and discharges almost linearly through \(R_L\) between peaks. Ripple peak-to-peak is approximately \(V_r = V_{dc}/(f_{ripple} R_L C)\) or, equivalently, \(V_r \approx I_{dc}/(f C)\). For half-wave \(f_{ripple}=f_{line}\); for full-wave it is \(2f_{line}\). The conduction angle of the diodes shrinks as \(C\) grows, so diode peak current rises even if average current stays \(V_{dc}/R_L\). Transformer and diode surge ratings matter at turn-on, when \(C\) looks like a short.

Clippers (limiters) remove portions of a waveform that go beyond a threshold. A series clipper puts the diode in the signal path and blocks one polarity (with or without a bias battery). A shunt clipper puts the diode across the load; when the diode conducts it clamps the output to \(V_\gamma\) plus any bias. Biased clippers shift the clipping level to \(V_B\pm V_\gamma\). Double clippers using two biased diodes produce a crude saturating transfer characteristic — the analog of a logic clip or a protection clamp. Always redraw the circuit in each region: diode on (replace by \(V_\gamma\)) and diode off (open). Continuity of the capacitor voltage is not an issue in pure clippers that have no memory element; the transfer curve is memoryless.

Clampers shift the DC level of a periodic waveform without changing its peak-to-peak excursion (ideally). A capacitor in series with the source charges through a diode to a DC voltage that then adds to the AC. A positive clamper (diode orientation such that the output sits above a reference) forces the most negative peak to sit at about \(-V_\gamma\) or at a bias level. A negative clamper does the opposite. The time constant \(R_L C\) must be much larger than the period so the capacitor does not discharge appreciably during a cycle; otherwise the restored DC sags. Clampers are DC restorers in video and pulse circuits: the sync tip or a known peak is pinned, and the rest of the waveform rides relative to that pin.

Zener diodes are designed to operate in reverse breakdown at a specified \(V_Z\) with a dynamic resistance \(r_z\). In the simple regulator model, \(V_L = V_Z\) provided the Zener stays in breakdown, which requires \(I_Z\) between \(I_{zk}\) (knee) and \(I_{z,\max}=(P_Z-I_Z V_Z \text{ wait: } P_Z/V_Z)\). Line and load regulation follow from the voltage divider formed by \(R_s\) and \(r_z\) in parallel with \(R_L\). A Zener is not a rectifier; using it forward is just a silicon diode.

Special diodes that appear in the same chapter: Schottky (low \(V_\gamma\), fast recovery, higher leakage), LED (photon emission in forward, specified at a current, not a voltage source), photodiode (reverse-bias current proportional to light), varactor (voltage-dependent capacitance in reverse), and tunnel diode (negative resistance, historical). For UG circuit analysis, treat LEDs as \(V_F\approx 1.8\)–\(3.3\) V depending on colour plus a series resistor that sets current.

Temperature: \(V_\gamma\) of silicon falls about \(-2\) mV/°C. Reverse current roughly doubles every 10 °C. Zener voltages below about 5 V have a negative tempco (tunneling); above about 5 V avalanche dominates and the tempco is positive. 5.1 V parts are popular because the two effects nearly cancel.

## Equations

Shockley law:

\[
i_D = I_S\left(\exp\frac{v_D}{n V_T}-1\right),\qquad V_T=\frac{kT}{q}\approx 26\,\mathrm{mV}\ (300\,\mathrm{K}).
\]

Small-signal resistance at a DC current \(I_D\):

\[
r_d = \frac{n V_T}{I_D}.
\]

Half-wave, no filter, ideal diode, source peak \(V_m\):

\[
V_{dc}=\frac{V_m}{\pi},\quad V_{rms}=\frac{V_m}{2},\quad \mathrm{PIV}=V_m.
\]

Full-wave (centre-tap or bridge) no filter:

\[
V_{dc}=\frac{2V_m}{\pi},\quad V_{rms}=\frac{V_m}{\sqrt{2}}.
\]

With constant drop \(V_\gamma\), replace \(V_m\) by \(V_m-V_\gamma\) (half-wave or centre-tap) or \(V_m-2V_\gamma\) (bridge).

Capacitor-input ripple (full-wave, linear discharge approximation):

\[
V_{r,\mathrm{pp}}\approx \frac{V_{dc}}{2 f R_L C}\approx\frac{I_{dc}}{2f C}.
\]

Ripple factor \(\gamma = V_{r,\mathrm{rms}}/V_{dc}\) with \(V_{r,\mathrm{rms}}\approx V_{r,\mathrm{pp}}/(2\sqrt{3})\) for a sawtooth.

Transformer utilisation and diode current: average diode current is \(I_{dc}\) (half-wave) or \(I_{dc}/2\) (full-wave, each diode). Peak repetitive current is much larger with \(C\) filters.

Clipper threshold (shunt diode to ground, Si): \(v_o\) cannot exceed \(+0.7\,\mathrm{V}\) or go below \(-0.7\,\mathrm{V}\) according to orientation. With bias \(V_B\), the clamp is \(V_B\pm V_\gamma\).

Clamper (positive, no bias, Si): most negative output peak \(\approx -V_\gamma\); DC offset \(\approx V_m - V_\gamma\) added to a symmetric \(\pm V_m\) input.

Zener regulator, series resistor \(R_s\), load \(R_L\):

\[
I_s=\frac{V_{in}-V_Z}{R_s},\qquad I_Z=I_s-I_L,\qquad I_L=\frac{V_Z}{R_L}.
\]

Load regulation with \(r_z\): \(\Delta V_L \approx \Delta I_L\cdot (r_z\parallel R_s')\) in the usual small-signal model.

## Methods

1. Identify the nonlinear element's region. For each candidate interval of the source waveform, assume each diode ON or OFF, replace ON by \(V_\gamma\) (or 0) and OFF by open, then check consistency: ON diodes must have current in the forward direction; OFF diodes must have reverse voltage more negative than \(V_\gamma\) (or not exceeding \(V_\gamma\) in the forward sense).
2. Rectifier DC and RMS: sketch one period, integrate \(v_L(t)\) and \(v_L^2(t)\). If a capacitor is present, use the peak-minus-ripple picture; do not integrate a sinusoid as if the capacitor were absent.
3. PIV: find the maximum reverse voltage across each diode over the cycle, including capacitor voltages that add to the AC trough.
4. Clipper transfer curve: treat the circuit as a resistive network with piecewise sources. Plot \(v_o\) versus \(v_i\) as a broken line. Then compose with a given \(v_i(t)\) to get \(v_o(t)\).
5. Clamper: in steady state the capacitor voltage is constant on the scale of one period. Apply KVL at the peak that forward-biases the diode (the charging peak). That pins one peak of \(v_o\). The other peak follows because \(v_C\) is fixed and \(v_o = v_i + v_C\) or \(v_i - v_C\) according to the drawing.
6. Zener: first assume the Zener is in breakdown at \(V_Z\). Compute \(I_Z\). If \(I_Z<0\), the Zener is off (open) and you must re-solve as an ordinary divider. If \(I_Z>I_{z,\max}\), the part is overloaded — that is an answer, not a number to ignore.
7. Temperature and \(r_d\): when a question gives \(I_D\) and asks for small-signal resistance, use \(r_d=nV_T/I_D\). Do not use the DC ratio \(V_\gamma/I_D\).

Worked pattern — bridge rectifier with \(C\): secondary peak 18 V, two silicon drops, \(V_{peak}\approx 16.6\) V. Load 100 Ω, \(C=1000\,\mu\mathrm{F}\), 50 Hz. \(I_{dc}\approx 16.6/100=166\,\mathrm{mA}\). \(V_r\approx I_{dc}/(2fC)=1.66\,\mathrm{V}\) pp. Report both the DC (approximately \(V_{peak}-V_r/2\)) and the ripple, and state the approximation.

## Mistakes

- Using 0.7 V in an ideal-diode problem that explicitly says "ideal", or omitting 0.7 V when the problem says silicon.
- Assigning PIV \(=V_m\) to a capacitor-input half-wave rectifier; the capacitor holds nearly \(+V_m\) and PIV is \(2V_m\).
- Treating a bridge as one diode drop; there are two in series in the load path.
- Computing full-wave average as \(V_m/\pi\) (that is half-wave).
- Using line frequency instead of twice line frequency in full-wave ripple.
- Clipper: forgetting to check the assumed diode state against the actual voltage; writing \(v_o=0\) whenever a shunt diode is present, even when it is reverse-biased.
- Clamper: confusing clippers (which remove amplitude) with clampers (which add DC). A clamper does not change peak-to-peak in the ideal large-\(RC\) limit.
- Taking the capacitor voltage as zero in a clamper after many cycles; it is the whole point of the circuit that \(v_C\) is a stored DC.
- Zener: applying the breakdown model when \(I_Z\) comes out negative; the device is then an open circuit, and \(V_L\) is the unloaded divider, not \(V_Z\).
- LED: treating it as 0.7 V. It is not a silicon small-signal diode; use the specified forward voltage and set current with a resistor.
- Dynamic resistance: using \(V/I\) of the Q-point instead of \(nV_T/I_D\).
- Polarity of the diode symbol: the triangle points in the conventional-current forward direction (anode to cathode). Electron-flow stories from older texts reverse the arrows and cause sign errors in KCL.

This unit is the nonlinear foundation for every later analog block: BJT junctions are diodes, MOSFET body diodes appear in power stages, and op-amp precision rectifiers exist only because ordinary diodes have a 0.7 V error that feedback can hide.

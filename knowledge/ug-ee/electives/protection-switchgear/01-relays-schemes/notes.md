# Overcurrent, differential, and distance schemes

A protection-and-switchgear elective takes the core-course sketch of zones, CTs, and inverse-time overcurrent and turns it into schemes you can set. The three workhorses on UG papers are overcurrent (50/51/67), differential (87), and distance (21). Pilot communication, numerical firmware, and IEC 61850 are named so you know they exist; the arithmetic in this unit is pickup, time, operate/restrain, and apparent impedance.

The core pack `power/10-protection-overview` already defined zones, CT polarity, TMS, and the four adjectives selectivity, speed, dependability, security. This unit uses those words as tools. A scheme is a combination of measuring elements, a directional or restraint decision, and a trip logic that opens named breakers. Setting a scheme is converting a fault study (symmetrical and unsymmetrical, referred to CT secondary) into numbers that trip in-zone faults and sit still for load, inrush, and through faults.

## Concepts

Overcurrent is the default on radial MV feeders, transformer HV backup, and industrial motors. Instantaneous 50 trips with no intentional delay once \(|I|\) exceeds a high pickup; it covers close-in bolted faults. Time-delayed 51 (definite time or inverse) covers the rest of the feeder and provides backup for downstream fuses and relays. Inverse families are IEC standard / very / extremely inverse and IEEE moderately / very / extremely inverse. The IEC analytic form is \(t=\mathrm{TMS}\times\beta/((I/I_s)^\alpha-1)\). Plug setting multiplier \(\mathrm{PSM}=I/I_s\) is the same ratio; older electromechanical language still appears on Indian UG papers. Time multiplier TMS (0.05–1 typical) scales the whole curve. Coordination plots time against current on log-log paper. A downstream device must clear, including breaker time, before the upstream relay, with a coordination time interval (CTI) of about 0.2–0.4 s. Upstream pickup sits above maximum load plus a cold-load or motor-start margin. Instantaneous 50 on a feeder is set above the maximum through-fault at the remote bus if it must not overreach; that often means 50 covers only the near portion of the line.

Directional overcurrent 67 is overcurrent plus a polarizing quantity. On a looped or parallel feeder, fault current can flow either way; a non-directional 51 would trip both ends for a fault on one feeder. Phase directional 67P typically uses a quadrature voltage (90° connection) or a positive-sequence memory voltage with a maximum-torque angle near the line impedance angle. Residual 67N uses \(3I_0\) and a polarizing \(3V_0\) or a current from a grounded transformer. Dual-feed industrial buses and closed rings need 67; a true radial feeder does not. Memory voltage keeps directionality during a close-in three-phase fault that collapses the polarizing voltage.

Differential protection 87 compares current into a zone with current out. Polarities are marked into the zone: operate \(I_{\mathrm{op}}=|\sum I_k|\), restrain \(I_{\mathrm{res}}=(\sum|I_k|)/2\) (or a variant). Trip if \(I_{\mathrm{op}}>k I_{\mathrm{res}}+I_{\mathrm{pickup}}\). The slope \(k\) (typically 0.2–0.5) covers CT ratio error and saturation on through faults. High-impedance circulating-current differential (classic bus 87B) uses a high-burden relay across paralleled CTs; an external fault with one CT saturated still produces little voltage if the healthy CTs hold the bus; an internal fault drives voltage across the relay. Low-impedance numerical 87B uses per-feeder CTs and a software restrain law, and it copes with different ratios. Transformer 87T must compensate ratio, star–delta 30° shift, and zero-sequence trap (delta winding or software subtraction of \(I_0\)) so load and external earth faults do not operate. Magnetizing inrush is rich in second harmonic; a harmonic-restrained or waveform-blocked 87T stays secure on energization. Over-excitation (fifth harmonic) is a related block. Generator 87G is the most sensitive electrical scheme on a machine; CTs at the neutral and line terminals, with a small pickup, catch stator winding faults that overcurrent would miss.

Distance 21 measures \(Z=V/I\) at the line terminal. On a homogeneous radial line with a bolted fault at fraction \(m\) of the line, \(Z_{\mathrm{app}}=m Z_L\). Zone 1 is set to about 80% of the protected line and trips without intentional delay, leaving a 20% underreach margin for CT/VT/Z errors and mutual coupling. Zone 2 reaches about 120–150% of the protected line (into the next line) with a time delay of 0.3–0.5 s as remote backup. Zone 3 is longer still, slower, and is the element most likely to trip on load encroachment or a power swing. Characteristic shapes: impedance (circle centred at origin), mho (circle through the origin, diameter along the line angle — good load rejection), reactance (horizontal line, used with a directional blinder), quadrilateral (independent R and X reaches, preferred for earth faults with fault resistance). Earth-fault distance uses residual compensation \(Z=V_\phi/(I_\phi+k_0 I_0)\) with \(k_0=(Z_0-Z_1)/(3Z_1)\). Infeed from a remote source makes a mid-line fault look farther (overreach of the underreaching zone is not the usual worry — underreach is). Load encroachment: heavy load is a large \(R\) at a small angle; a fat zone-3 polygon can swallow it. Power-swing blocking (PSB) distinguishes a slow \(dZ/dt\) of a swing from a jump into the characteristic of a fault.

Pilot schemes close the 20% hole at the remote end. Permissive overreaching transfer trip (POTT): zone-2 looking across the whole line keys a permit; the local relay trips instantaneously if it also sees a forward fault. Blocking (DCB): a reverse-looking element at the remote end sends a block so that a fast overreaching element does not trip for a behind-the-remote-bus fault. Line current differential (87L) on fibre compares time-aligned samples; it is the modern default where communications exist. UG computes the no-pilot zones; pilot is a logic paragraph, not a latency budget.

Fuse–recloser coordination on distribution: the recloser fast curve saves the fuse on a transient fault (reclose before the fuse melts); the slow curve lets the fuse clear a persistent lateral fault so the feeder stays up. \(I^2t\) of the fuse is the melting and clearing numbers from a manufacturer curve, not a first-principles integral unless the problem gives \(t(I)\).

Breaker-failure (50BF): after a trip command, if current still flows past a margin (breaker time plus a short delay), trip adjacent breakers. Essential at EHV; named on UG schemes as local backup.

Instrument-transformer hygiene belongs in every scheme. Distance and 87 need CTs that do not saturate on offset fault current. Class PX (or equivalent) knee-point \(V_k\ge k I_f(R_{\mathrm{CT}}+R_L+R_r)\) is the inequality to check, not a CT redesign. VT and CVT ferroresonance and transient error affect distance at the first cycle; memory polarization is the mitigation. Never open a CT secondary. Secondary ohms for distance: \(Z_{\mathrm{sec}}=Z_{\mathrm{pri}}\times\mathrm{CTR}/\mathrm{VTR}\). Mixing 1 A and 5 A secondaries on one 87 without a matching CT or a tap is a classic maloperation.

Selectivity versus speed is a setting conversation, not a slogan. A radial industrial feeder can be slow and cheap (51 only). A 400 kV line needs zone-1 plus pilot because a three-phase fault near a large plant is a stability problem (swing equation in the core power pack). Transformer 87T is fast because through-fault mechanical force on windings accumulates. Motor 50/51 and 49 thermal are slow enough to ride starting current if pickup and TMS are not greedy.

Function numbers that belong on a one-line: 50/51, 67, 21, 87, 32 reverse power, 40 loss of field, 81 frequency, 27/59 voltage, 86 lockout, 64 earth fault, 46 negative sequence. A scheme drawing without function numbers is a cartoon.

Coordination across a transformer must refer all currents to one voltage. A 400 A fuse on 415 V is about \(400\times(0.415/11)=15\) A on an 11 kV primary if the transformer ratio is 11 kV/415 V; comparing 400 A to an 11 kV relay pickup of 200 A without scaling is meaningless. Inrush 8–12 pu for a fraction of a second forces HV 50 above inrush or a second-harmonic block, while 51 rides through if TMS is not tiny.

## Equations

IEC inverse-time family:

\[
t=\mathrm{TMS}\times\frac{\beta}{(I/I_s)^\alpha-1}\ \mathrm{s},
\]

with \((\alpha,\beta)=(0.02,0.14)\) standard inverse, \((1.0,13.5)\) very inverse, \((2.0,80)\) extremely inverse. IEEE/ANSI uses a different closed form; do not mix constants.

Definite time: \(t=T_{\mathrm{set}}\) if \(I>I_s\). Instantaneous 50: trip if \(I>I_{\mathrm{inst}}\) with no intentional delay.

CT ratio \(n=I_p^{\mathrm{rated}}/I_s^{\mathrm{rated}}\). Ideal \(I_s=I_p/n\).

Differential (two-terminal, currents into the zone):

\[
I_{\mathrm{op}}=|\mathbf{I}_1+\mathbf{I}_2|,\qquad I_{\mathrm{res}}=\frac{|I_1|+|I_2|}{2},
\]

trip if \(I_{\mathrm{op}}>k I_{\mathrm{res}}+I_{\mathrm{pu}}\).

Homogeneous-line distance, bolted fault at fraction \(m\), infeed only from behind the relay:

\[
Z_{\mathrm{app}}=m Z_L.
\]

Secondary ohms:

\[
Z_{\mathrm{sec}}=Z_{\mathrm{pri}}\frac{\mathrm{CTR}}{\mathrm{VTR}}.
\]

Residual compensation (phase–earth):

\[
k_0=\frac{Z_0-Z_1}{3Z_1},\qquad Z_{\phi\mathrm{g}}=\frac{V_\phi}{I_\phi+k_0 I_0}.
\]

Coordination inequality at a common through-current \(I\):

\[
t_{\mathrm{up}}(I)\ge t_{\mathrm{down}}(I)+t_{\mathrm{breaker}}+t_{\mathrm{margin}}.
\]

CT knee-point check (class PX style, no residual flux, sinusoidal):

\[
V_k \ge k_{\mathrm{sat}} I_f^{\mathrm{sec}}(R_{\mathrm{CT}}+R_{\mathrm{lead}}+R_{\mathrm{relay}}).
\]

Zone-1 reach (typical): \(Z_1=0.80 Z_L\) along the line angle.

## Methods

1. Draw the one-line with CT locations and overlapping zones. Name primary and backup for a chosen fault. Write ANSI numbers on each relay.
2. From a fault study, take the current through each relay, convert to secondary, and compare with pickup. Do this at maximum generation (max fault, speed/coordination) and minimum generation (sensitivity).
3. Overcurrent: set \(I_s\) above max load (margin 1.2–2 depending on element). Set TMS so that at the maximum through-fault of the downstream device, the CTI inequality holds. Set 50 above the far-end through-fault if it must not overreach.
4. Directional: confirm a polarizing source exists for the worst close-in fault. If the bus voltage collapses, specify memory or current polarization for 67N.
5. Differential: put all currents in one ampere-base (CT taps or software scaling). Apply vector group compensation for 87T. Check a through-fault point on the restrain characteristic and an internal-fault point on the operate side. Check \(V_k\) for the CT.
6. Distance: convert \(Z_L\) to secondary ohms. Set zone 1 to \(0.8 Z_L\), zone 2 to overreach the next bus with a delay. For earth fault, compute \(k_0\). Check that maximum load impedance stays outside the characteristic (especially zone 3).
7. Across transformers, refer every current and every fuse curve to one voltage before drawing the coordination graph.

Worked pattern — IEC SI: \(I_s=5\,\mathrm{A}\), \(\mathrm{TMS}=0.20\), \(I=20\,\mathrm{A}\). Then \(I/I_s=4\), \(4^{0.02}-1\approx 0.0281\), \(t=0.20\times 0.14/0.0281\approx 1.00\,\mathrm{s}\). If the downstream device plus breaker plus margin needs 0.70 s, this TMS is acceptable; if the downstream is 0.90 s, raise TMS or the downstream is too slow.

Worked pattern — 87T through fault: after ratio and 30° compensation, \(\mathbf{I}_1\approx -\mathbf{I}_2\). Operate is CT mismatch only; restrain is large; slope holds. Internal fault: both currents into the zone, operate \(\approx |I_1|+|I_2|\), trip.

## Mistakes

Setting zone 1 to 100% of the line. Using IEC \(\alpha,\beta\) in an IEEE formula. Coordinating 11 kV amperes against 415 V fuse amperes without a ratio. Wiring 87T without a 30° compensation on a Dyn transformer. Open-circuiting a CT. Setting 50 below transformer inrush. Treating a 67 as working with no VT on a phase directional element. Forgetting breaker time in the CTI. Mixing 1 A and 5 A secondaries on one differential. Computing \(Z_{\mathrm{app}}\) from a load-flow \(V/I\) during a swing and calling it a fault. Using a mho diameter along the R-axis (load) instead of the line angle. Ignoring \(k_0\) on an earth-fault distance numerical. Setting 87 pickup so low that CT mismatch on a through fault crosses the slope. Assuming a radial 51 scheme is fine on a closed ring. Taking PSM as TMS. Reporting secondary ohms as primary. Putting CTs so that a breaker is in a gap rather than in two overlapping zones.

Dependability versus security: failing to trip an in-zone fault is a dependability failure; tripping load or a through fault is a security failure. A sensitive 87 that maloperates on inrush is not “better protection.” A slow 51 that waits for a fuse is sometimes the correct security choice.

Pilot is not a substitute for a wrong zone-1 reach. If zone 1 is 80% and communications die, you still have delayed zone 2. If you set zone 1 to 120% and call it POTT without a received permit, you overreach the next bus on a channel failure. Permissive schemes fail safe toward non-trip; blocking schemes fail toward trip unless a current detector supervises. That distinction is UG-legitimate even without a channel-latency number.

Numerical relays still implement these laws. A sample-based 87L is the same operate/restrain idea with time alignment. A quadrilateral 21 is still \(R+jX\) compared with a polygon. Do not hide a wrong setting behind a vendor name.

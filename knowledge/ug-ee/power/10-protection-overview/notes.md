# Protection overview: zones, CTs/VTs, and overcurrent introduction

Protection is the art of detecting faults and opening the right circuit breakers quickly enough that equipment survives and the rest of the system stays stable. An undergraduate power course does not replace a protection-and-switchgear elective: it introduces zones of protection, instrument transformers, overcurrent (definite-time and inverse), a sketch of differential and distance ideas, and the language of pickup, time multiplier, and coordination. Numerical relay firmware, IEC 61850, and travelling-wave relays are named as later topics.

## Concepts

A protection zone is a region of plant (a line, a transformer, a bus, a generator) watched by a set of CTs and a relay, with breakers that can isolate that region. Zones overlap at CTs so that a fault at a breaker is inside at least one zone (no unprotected “blind” slice). Primary protection is the fast, selective scheme for that zone. Backup protection operates later if primary fails (stuck breaker, failed relay). Remote backup uses a relay in the next station; local backup uses breaker-failure protection at the same station.

Selectivity (discrimination): only the breakers needed to isolate the fault trip. Speed: faster is better for stability and damage, but too fast without direction or communication risks tripping unfaulted feeders. Reliability has two faces: dependability (trips when it should) and security (does not trip when it should not). Sensitivity: picks up the smallest in-zone fault. These four — selectivity, speed, reliability, sensitivity — trade off.

Instrument transformers:

Current transformers (CTs) produce a secondary current, typically 1 A or 5 A rated, proportional to primary current within a class and burden. They must not saturate during offset fault current if the relay needs an accurate waveform (differential, distance). Overcurrent relays are more forgiving but still need a knee-point adequate for the setting. CT ratio \(n=I_p^{\mathrm{rated}}/I_s^{\mathrm{rated}}\). Never open-circuit a CT secondary on a live primary: the core flux and secondary voltage can be lethal and can saturate/damage the CT. Short the secondary before disconnecting a burden. Polarity marks (P1/P2, S1/S2) define the direction for differential and directional overcurrent.

Voltage transformers (VTs / PTs) and capacitive voltage transformers (CVTs) provide 110 V line-to-line (or 110/√3 phase) secondaries. Burden, class, and ferroresonance of CVTs matter for distance relays. Fusing and grounding of VT secondaries follow a station standard so that a secondary earth is defined once.

Overcurrent protection:

A time-overcurrent relay (51) picks up when \(|I|\) exceeds pickup \(I_s\) (or \(I_p\)) and trips after a time that decreases as current increases (inverse, very inverse, extremely inverse IEC/IEEE curves) or after a fixed delay (definite time, 50/51TD). Instantaneous overcurrent (50) trips with essentially no intentional delay above a high setting, used to cover close-in high-current faults without waiting for the inverse curve.

IEC inverse time (one common family):

\[
t=\mathrm{TMS}\times\frac{\beta}{(I/I_s)^\alpha-1},
\]

with \((\alpha,\beta)=(0.02,0.14)\) for standard inverse, other pairs for very/extremely inverse. TMS is the time multiplier setting (0.05–1 typical). IEEE/ANSI uses a different analytic form. Do not mix the constants. Coordination: plot time-current curves (log-log). A downstream fuse or relay must clear before the upstream relay, with a coordination time interval (CTI) of roughly 0.2–0.4 s accounting for breaker time and errors. Upstream pickup must be above the downstream load plus a margin, and above transformer inrush if it should not trip on energization (or use a harmonic-restrained or time-delayed element).

Directional overcurrent (67) adds a torque or phase comparison with a polarizing voltage (or current from a grounded transformer) so that a relay on a loop or parallel feeder trips only for faults in the forward direction. Radial feeders often omit directionality.

Differential protection (87): compare current into and out of a zone. Ideal internal fault: the difference (operate) current is large; external fault: currents match (through current) and a restraint element prevents CT-error trips. Used on transformers (with ratio and phase-shift compensation, inrush second-harmonic block), generators, buses (high-impedance or low-impedance), and short lines. Long lines need communication (pilot) because CTs are kilometres apart.

Distance protection (21): measures \(Z=V/I\) seen from the terminal. A fault on a homogeneous line lies at a fraction of the line impedance. Zones: zone 1 typically 80% of the line, instantaneous; zone 2 overreaches into the next line with time delay as remote backup; zone 3 further. Load encroachment, power swings (unit 06), and infeed from remote sources complicate the apparent impedance. UG should compute \(Z_{\mathrm{app}}=V_{\mathrm{relay}}/I_{\mathrm{relay}}\) for a bolted fault on a radial line and see that it equals \(z\ell_{\mathrm{fault}}\).

Fuses: melting \(I^2 t\), cheap, one-shot, used on laterals and transformers. Coordination with a recloser (fast/slow curves) is a distribution classic: the recloser fast curve saves the fuse on a transient fault; slow curve lets the fuse clear a persistent lateral fault.

Breaker failure: if current still flows after a trip command plus a margin, trip adjacent breakers. Essential at EHV.

Pilot schemes (permissive overreach, blocking, current differential on fibre) make both ends of a line trip together for 100% coverage. Named only.

Generator protection is a list: differential, stator earth fault, loss of excitation, reverse power, negative sequence, over/under frequency. Transformer mechanical Buchholz and sudden-pressure sit beside electrical 87T. Bus 87B. Motor 49 thermal, 50/51, 46. UG memorizes the function numbers as a vocabulary, not as a complete setting file.

Function numbers (ANSI): 50/51 overcurrent, 67 directional OC, 21 distance, 87 differential, 32 reverse power, 40 loss of field, 81 frequency, 27/59 undervoltage/overvoltage, 86 lockout. Use them in sketches.

Coordination on a radial feeder with a transformer in between must refer all currents to one voltage level. A 400 A pickup on 11 kV is not comparable to a 400 A fuse on 400 V. Convert: \(I_{\mathrm{HV}}=I_{\mathrm{LV}}(V_{\mathrm{LV}}/V_{\mathrm{HV}})\) for a transformer (neglect magnetizing). Inrush of a transformer can be 8–12 times rated for a fraction of a second; an instantaneous 50 on the HV overcurrent must sit above that, or be delayed, or use second-harmonic restraint. Inverse 51 can ride through inrush if the TMS is not tiny.

Zone overlap: CTs on the line side of a breaker put the breaker in the line zone; CTs on the bus side put the breaker in the bus zone. Overlap means a fault in the breaker is in both, and both schemes trip — better than a gap. Dual-breaker line terminals (breaker-and-a-half) have a small extra zone for the diameter; mention in a substation-layout elective.

Directional polarization: 67P uses a phase voltage (or positive-sequence voltage) and a 30°/90° maximum-torque angle depending on the relay; 67N may use residual voltage \(3V_0\) or a current from a grounded transformer. On a strong infeed, a reverse fault can still produce large current; without 67 a looped feeder pair will both trip. Dual-feed industrial buses almost always need directionality.

Distance reach in secondary ohms must use the same CT and VT ratios the relay is wired with. A setting of \(0.8 Z_L\) in primary ohms converted with CTR/VTR is the relay’s zone-1. Mutual coupling on parallel lines distorts earth-fault distance; UG three-phase distance examples ignore mutuals. Load encroachment: heavy load looks like a large impedance at a small angle; a too-large zone-3 polygon can trip on load. That is a security failure, not a dependability failure.

CT knee-point \(V_k\) for a class-PX (or equivalent) differential CT is specified so that \(V_k \ge k I_f (R_{CT}+R_L+R_r)\). If the exam gives \(V_k\), \(R_{CT}\), and lead resistance, check the inequality rather than redesigning the CT.

## Equations

CT ratio: \(I_s=I_p/n\) (ideal). Relay current in the pickup formula is the secondary current unless the problem works on primary.

IEC standard inverse:

\[
t=\mathrm{TMS}\times\frac{0.14}{(I/I_s)^{0.02}-1}\quad\mathrm{s}.
\]

Definite time: \(t=T_{\mathrm{set}}\) if \(I>I_s\).

Distance seen on a radial bolted fault at location \(m\) (0 to 1) of line \(Z_L\), relay at sending end, infeed only from behind:

\[
Z_{\mathrm{app}}=m Z_L.
\]

Differential operate (simple): \(I_{\mathrm{op}}=|\mathbf{I}_1+\mathbf{I}_2|\) with marked polarities into the zone; restrain \(I_{\mathrm{res}}=(|I_1|+|I_2|)/2\); trip if \(I_{\mathrm{op}}>k I_{\mathrm{res}}+I_{\mathrm{pickup}}\).

Coordination inequality (downstream faster): \(t_{\mathrm{up}}(I)\ge t_{\mathrm{down}}(I)+t_{\mathrm{breaker}}+t_{\mathrm{margin}}\) at the maximum fault current through both.

## Methods

1. Draw zones overlapping at CT locations; list primary and backup for a chosen fault.
2. Convert fault currents from a unit-04/05 study to CT secondary. Compare to pickup.
3. For inverse-time, compute \(t\) at the fault current; adjust TMS to achieve a CTI with the downstream device.
4. For a radial line distance example, \(Z_{\mathrm{app}}=V/I\) in secondary ohms using VT and CT ratios: \(Z_{\mathrm{sec}}=Z_{\mathrm{pri}}(CTR)/(VTR)\).
5. Check CT saturation qualitatively: \(V_k > I_f^{\mathrm{sec}}(R_{CT}+R_{\mathrm{lead}}+R_{\mathrm{relay}})\) as a knee-point rule of thumb for a given offset-less RMS (full offset needs more).

Checks: pickup above max load with a margin (often 1.2–2× depending on the element); instantaneous 50 above the through-fault at the far end of the next zone if it must not overreach; zone-1 distance < 100% of protected line; CT secondary never open.

When coordinating fuse and relay, work in primary amperes on a log-log sheet. Do not compare a 5 A secondary TMS curve to a fuse’s primary curve without scaling.

## Mistakes

Open-circuiting a CT. Setting pickup below max load so that cold-load pickup or motors trip the feeder. Using IEC constants in an ANSI formula. Coordinating two relays at different voltages without referring both currents to the same side of a transformer. Putting zone-1 at 100% of the line (CT and Z errors can overreach). Using 87 without compensating transformer star-delta 30° shift. Treating a directional relay as working without a VT (some current-polarized earth-fault relays exist, but a 67P phase directional typically needs voltage). Forgetting breaker interrupting time in the CTI. Mixing 1 A and 5 A CT secondaries on one differential. Computing distance with load-flow \(V/I\) during a swing and calling it a fault. Setting 50 instantaneous below the maximum far-end fault of the protected line if the intent was not to overreach the next bus — actually 50 on a line must be above the through current for a remote-end fault if it is to stay selective, which may make 50 cover only part of the line. Confusing dependability with security.

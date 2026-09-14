# Instrument transformers: CT and PT ratio and phase errors

Instrument transformers scale large currents and voltages down to 5 A or 1 A and 110 V (or 100 V) so that meters, relays, and wattmeters can be standardized. They are not power transformers with a casual magnetizing current: the current transformer (CT) is a current-forced device that must not be open-circuited on the secondary, and the potential transformer (PT / VT) is a voltage-forced device whose burden is a high impedance. Ratio error and phase angle error are the two numbers that decide whether a wattmeter on the secondary is telling the truth about primary power. Composite error, accuracy class, knee-point, and burden (VA) are the specification language.

## Concepts

A CT has a primary of one or a few turns (often a bar through a window) carrying line current \( I_p \), and a secondary of many turns closed through a burden \( Z_b \) (meters plus leads). Ideal current ratio \( K_n = I_{pn}/I_{sn} \) (e.g. 200/5 = 40). Actual ratio \( R = I_p/I_s \). Ratio error (current error) is \( \varepsilon_i = (K_n I_s - I_p)/I_p \times 100\% \) in the usual IEC-ish form that is positive when the secondary current is high relative to the nominal mapping. Some older books write \( (K_n - R)/R \). Use the definition given on the paper; do not mix signs. Phase angle error \( \beta \) is the angle by which the reversed secondary current fails to be 180° from the primary (i.e. the small angle between \( -I_s \) referred and \( I_p \)). For a wattmeter, both ratio and phase errors of CT and PT enter \( P=VI\cos\phi \).

Why errors exist: the core needs magnetizing current \( I_m \) and a core-loss component \( I_c \). On the equivalent circuit (referred to secondary), \( I_p/N \) splits between the magnetizing branch and the secondary current. Turns compensation (slightly fewer secondary turns than the nominal ratio) is used to put ratio error near zero at a chosen burden and current. Phase error is set mostly by the loss angle of the core and leakage, and by burden power factor.

Burden is the VA the secondary is designed to drive at rated secondary current, e.g. 15 VA at 5 A means \( |Z_b|=0.6\,\Omega \). Too much burden (too high \( |Z_b| \), long thin leads, extra meters) increases the required flux and therefore \( I_m \), which worsens ratio and phase error and can saturate. Too little burden is usually fine for metering CTs (errors smaller); some protection CTs care about saturation on faults, not about 0.2% metering.

Never open the secondary of a CT while the primary is energized. The primary current still flows; with \( I_s=0 \) all of it magnetizes the core; flux and secondary voltage go to dangerous levels, the core saturates and remanence may ruin later accuracy, and the insulation can fail. Short the secondary before disconnecting a meter. A PT secondary may be open (it is then just a small magnetizing current on the primary); do not short a PT secondary.

PT (VT): primary across the line, secondary nominally 110 V. Ratio error and phase error analogous to the CT, with magnetizing current and winding drops causing them. Burden is voltmeters, pressure coils, relays — high Z, rated in VA (e.g. 50 VA). Class 0.5, 1.0, etc., as for CTs. Capacitor voltage transformers (CVT) on HV lines use a capacitor divider plus a tuning reactor; they have their own transient and ferroresonance issues, UG-intro only.

Accuracy class (metering): at rated current (or voltage) and specified burden, |ratio error| and |phase error| shall not exceed tabulated limits (phase often in minutes). Class 0.2, 0.5, 1.0 are metering. Protection classes (5P, 10P, or PS/PX) specify composite error at an accuracy-limit current (ALF × rated), not 0.5% at rated: a protection CT may be a poor meter and a good saturating-or-not device on faults. Composite error includes harmonics from saturation: it is the RMS of the difference between ideal and actual secondary current, as a percent of ideal. Knee-point voltage (IEC PS class) is where a 10% increase in voltage needs 50% more exciting current — a saturation marker for high-impedance differential schemes.

Power measurement: true primary power \( P=V_p I_p \cos\phi \). Using \( V_s, I_s \) you multiply by nominal ratios \( K_v K_i \) and hope. The fractional error in power is approximately the sum of PT and CT ratio errors plus the phase errors in radians times \( \tan\phi \) (small-angle, with signs depending on lag/lead and on whether \( \beta \) of the CT and \( \gamma \) of the PT add in the wattmeter’s \( \phi \)). At unity PF, phase errors barely show; at 0.2 lag they dominate. That is why metering CTs/PTs quote phase in minutes, and why you must know lag versus lead.

Nameplate: 200/5 A, 15 VA, Class 0.5, 50 Hz, ISF (instrument security factor) 5 or 10 for metering (a metering CT should saturate on a heavy fault so the meter is not destroyed — opposite instinct from protection). Protection: 200/5, 5P10, 15 VA means composite error ≤ 5% at 10× rated with that burden.

Construction: ring-core (window) CTs have one primary turn and excellent accuracy; wound primaries for smaller currents. Insulation and polarity marks (P1, P2 / S1, S2) must be consistent with wattmeter ± marks or the wattmeter reverses. Multiple-ratio CTs change secondary taps; never leave an unused tap in a way that creates an open secondary section.

DC: a CT does not pass a DC primary (the core just sits at a flux offset). A hall-effect or shunt is used for DC. Residual magnetism from a DC test or an asymmetric fault shifts the CT magnetizing curve; demagnetize if ratio tests look odd.

## Equations

Nominal ratios:

\[
K_n^{\mathrm{CT}}=\frac{I_{pn}}{I_{sn}},\qquad K_n^{\mathrm{PT}}=\frac{V_{pn}}{V_{sn}}.
\]

Current (ratio) error and phase error \( \beta \) (CT):

\[
\varepsilon_i=\frac{K_n I_s - I_p}{I_p}\times 100\%.
\]

Approximate CT errors from the equivalent-circuit magnetizing branch (secondary referred), burden \( Z_b=R_b+jX_b \), exciting \( I_e\angle \), winding resistance \( R_s \) and leakage \( X_s \):

\[
\varepsilon_i \approx -\frac{I_c(R_s+R_b)+I_m(X_s+X_b)}{I_s},\qquad
\beta \approx \frac{I_m(R_s+R_b)-I_c(X_s+X_b)}{I_s}
\]

(in radians for \( \beta \), small-angle; signs follow a stated phasor convention). Qualitatively: more burden or more \( I_m \) (low current, low µ) worsens errors.

Turns compensation: if secondary turns are reduced by \( n \) parts in \( N \), a positive offset appears in \( \varepsilon_i \) that can cancel the negative magnetizing contribution at one operating point.

Wattmeter power using secondaries:

\[
P_{\mathrm{indicated}}=K_n^{\mathrm{PT}} K_n^{\mathrm{CT}} V_s I_s \cos\phi_s.
\]

Small-error model (lagging load, \( \phi>0 \)):

\[
\frac{\Delta P}{P}\approx \varepsilon_v+\varepsilon_i+(\beta-\gamma)\tan\phi
\]

with \( \beta,\gamma \) in radians and the sign of PT phase \( \gamma \) as defined on the paper. At \( \phi=0 \), phase terms drop.

Burden VA: \( S_b = I_{sn}^2 |Z_b| \). Lead resistance of two-way cable \( 2\rho \ell/A \) adds to \( R_b \).

Knee-point (illustrative): \( V_k \) such that exciting current rises sharply; for a PS CT, \( V_k \ge (R_{CT}+2R_{lead}+R_r)I_f \) in a high-impedance differential, UG sketch only.

## Methods

To use a CT: confirm ratio, class, VA, frequency, and that the secondary circuit is closed before applying primary current. Put the meter common at earth if the installation requires earthed S2. Keep polarity P1–S1 consistent with the wattmeter.

To estimate whether leads ate the VA: compute \( I_s^2 R_{leads} \) and subtract from rated VA. 5 A through 0.2 Ω of leads is 5 VA already.

To reduce phase error on a metering CT: lower burden, better core (higher µ, lower loss), turns compensation cannot cancel phase the way it cancels ratio.

For a PT, treat it like a small power transformer: load (burden) causes voltage drop; magnetizing current causes phase shift. Keep burden ≤ rated. Fuse the primary (HV) per practice; never fuse only the secondary in a way that a blown fuse looks like zero voltage to a relay that then misoperates — protection PTs have specific rules.

When converting a wattmeter reading to primary power, use nominal ratios unless the problem gives measured ratios. If it gives ratio errors, apply them. Convert minutes to radians: \( 1'=2.9089\times 10^{-4} \) rad \( \approx \pi/(180\times 60) \).

Open-CT check: if a student “CT” circuit shows hundreds of volts on a tiny secondary burden resistor that came unclipped, de-energize; do not measure with a handheld DMM as your first move on an unknown HV secondary.

## Mistakes

Open-circuiting a CT secondary under load.

Short-circuiting a PT secondary.

Using a protection-class CT as if it were class 0.5 at rated current without checking the datasheet (it might be, but 5P10 does not promise 0.5%).

Adding CT VA and PT VA as if they shared a winding.

Forgetting lead resistance in 5 A circuits (1 A CTs are kinder to long runs: same VA is 25× the ohms).

Phase error in degrees when the table was in minutes (a factor of 60).

Ignoring \( \tan\phi \) so that a 20′ CT phase error looks harmless at PF 0.2 (\( \tan\phi\approx 4.9 \), 20′ is 0.0058 rad, contribution \( \approx 2.8\% \) to power).

Wrong polarity: negative power on an importing feeder.

Using \( K_n I_s \) as \( I_p \) when the ratio error is the quantity asked: the definition of \( \varepsilon_i \) is exactly that mismatch.

Window CT with the return conductor also through the window: net primary ampere-turns ≈ 0, secondary ≈ 0. The cable screen or a U-bend can do this by accident.

A worked CT: 100/5 A, measured \( I_p=80.0 \) A, \( I_s=3.92 \) A. \( K_n=20 \), \( K_n I_s=78.4 \) A, \( \varepsilon_i=(78.4-80)/80 \times 100\% = -2.0\% \).

Worked burden: 5 A, burden 0.4 Ω resistive, VA \( =25\times 0.4=10 \) VA. If rated 15 VA, you have margin. If leads add 0.3 Ω, total 0.7 Ω = 17.5 VA, over-burdened.

Worked power phase: \( \phi=\cos^{-1}0.5=60^\circ \), \( \tan\phi=\sqrt{3} \). CT phase error \( \beta=+10'=0.00291 \) rad, PT phase \( \gamma=0 \), ratio errors zero. \( \Delta P/P \approx 0.00291\times\sqrt{3}=0.50\% \).

Worked PT: 11 kV/110 V, \( K_n=100 \). Secondary 109.0 V when primary is 11.00 kV. Actual ratio \( R=11000/109=100.92 \). Ratio error \( (K_n V_s-V_p)/V_p=(100\times 109-11000)/11000=-0.91\% \).

Worked ISF idea: a class 0.5 metering CT with ISF 5 should have the secondary current not exceed about 5 pu when the primary is a heavy fault, because the core saturates — the meter stays safer. A 5P20 protection CT should still transform at 20 pu with composite error ≤ 5%. Do not swap those stories.

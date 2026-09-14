# Transmission lines: telegrapher equations, VSWR, reflection

A transmission line is a two-conductor structure long enough that voltage and current vary along its length at the frequency of interest. The telegrapher equations are Maxwell reduced to 1-D TEM. Characteristic impedance \( Z_0 \), reflection coefficient \(\Gamma\), standing-wave ratio, and input impedance of a length \(\ell\) are the UG toolkit. Matching with stubs is the next unit; this unit is the travelling-wave accounting.

## Concepts

Lumped model per length: series \( R',L' \), shunt \( G',C' \). Telegrapher: \(\partial v/\partial z= -R'i-L'\partial i/\partial t \), \(\partial i/\partial z=-G'v-C'\partial v/\partial t\). Phasor: \(\mathrm{d}V/\mathrm{d}z=-Z' I\), \(\mathrm{d}I/\mathrm{d}z=-Y' V\) with \( Z'=R'+j\omega L' \), \( Y'=G'+j\omega C' \). Then \(\mathrm{d}^2V/\mathrm{d}z^2=\gamma^2 V\), \(\gamma=\sqrt{Z'Y'}=\alpha+j\beta \). \( Z_0=\sqrt{Z'/Y'} \). Lossless: \(\gamma=j\omega\sqrt{L'C'} \), \( Z_0=\sqrt{L'/C'} \), \( v_p=1/\sqrt{L'C'} \). Coax, twin-lead, microstrip (quasi-TEM) have formulas for \( L',C' \) from electrostatics/magnetostatics of the cross-section.

Forward and reverse waves: \( V(z)=V_0^+ e^{-\gamma z}+V_0^- e^{+\gamma z} \), \( I(z)=(V_0^+ e^{-\gamma z}-V_0^- e^{+\gamma z})/Z_0 \). Load at \( z=0 \) (some books put load at \( z=\ell \)): \(\Gamma_L=(Z_L-Z_0)/(Z_L+Z_0)\), \( V_0^-=\Gamma_L V_0^+ \). Open: \(\Gamma=1\). Short: \(\Gamma=-1\). Match \( Z_L=Z_0 \): \(\Gamma=0\), no reflection. VSWR \( =(1+|\Gamma|)/(1-|\Gamma|) \), 1 for a match, \(\infty\) for a total reflection. Voltage maxima and minima spaced \(\lambda/4\).

Input impedance looking into a lossless line of length \(\ell\) toward \( Z_L \):

\[
Z_{\mathrm{in}}=Z_0\frac{Z_L+j Z_0\tan\beta\ell}{Z_0+j Z_L\tan\beta\ell}.
\]

Quarter-wave transformer: \(\ell=\lambda/4\), \( Z_{\mathrm{in}}=Z_0^2/Z_L \). Choose \( Z_0=\sqrt{Z_{\mathrm{in}}Z_L} \) to match a real load to a real generator impedance. Half-wave: \( Z_{\mathrm{in}}=Z_L \) regardless of \( Z_0 \). Shorted stub: \( Z_{\mathrm{in}}=j Z_0\tan\beta\ell \), a reactance from \( -j\infty \) to \( +j\infty \) as \(\ell\) goes 0 to \(\lambda/2\). Open stub: \( -j Z_0\cot\beta\ell \).

Power: average \( P=\frac12\mathrm{Re}(V I^*) \). For a matched lossless line, \( P=|V_0^+|^2/(2Z_0) \). With reflection, net power is incident minus reflected, \( P=P^+(1-|\Gamma|^2) \) if the line is lossless (no extra dissipation).

Lossy lines: \(\alpha>0\), \( Z_0 \) slightly complex, VSWR not constant along the line. UG often still uses lossless formulas then multiplies by \( e^{-2\alpha\ell} \) for power.

Time domain: bounce diagram, reflection of a step from \( R_L \). Lattice diagram. Rise-time versus delay \( t_d=\ell/v_p \). Digital SI (signal integrity) is this picture.

Smith chart is a plot of \(\Gamma\) (next unit). You can survive this unit without it; you should not survive matching without it.

## Equations

Lossless:

\[
Z_0=\sqrt{\frac{L'}{C'}},\quad \beta=\omega\sqrt{L'C'},\quad v_p=\frac{1}{\sqrt{L'C'}}=\frac{c}{\sqrt{\varepsilon_r,\mathrm{eff}}}.
\]

Reflection and VSWR:

\[
\Gamma=\frac{Z_L-Z_0}{Z_L+Z_0},\qquad s=\frac{1+|\Gamma|}{1-|\Gamma|}.
\]

Input impedance as above. Quarter wave: \( Z_{\mathrm{in}}=Z_0^2/Z_L \).

Coax (high-frequency, \(\varepsilon_r\)):

\[
Z_0=\frac{1}{2\pi}\sqrt{\frac{\mu}{\varepsilon}}\ln\frac{b}{a}\approx\frac{60}{\sqrt{\varepsilon_r}}\ln\frac{b}{a}.
\]

Propagation delay \( t_d=\ell\sqrt{L'C'} \).

## Methods

Normalize \( z=Z/Z_0 \). Compute \(\Gamma\), then \( s \), then \( Z_{\mathrm{in}} \) if length is given. Keep \(\beta\ell\) in radians (\( 2\pi\ell/\lambda \)).

To match a real \( R_L \) to \( R_g \) with a quarter-wave section: \( Z_0=\sqrt{R_g R_L} \). For complex loads, use a stub (unit 09) or two quarter-waves, or a lumped L-section if the line is short.

Generator with \( Z_g \): the line plus load looks like \( Z_{\mathrm{in}} \); voltage divider at the input; then find \( V_0^+ \) from the input voltage and the known \(\Gamma\) at the load. Do not assume \( V(0)=V_g/2 \) unless \( Z_{\mathrm{in}}=Z_g \).

Measure VSWR and position of a minimum to find \( Z_L \) (slotted line): classical microwave lab.

## Mistakes

\(\Gamma=(Z_0-Z_L)/(Z_0+Z_L)\) sign.

\(\tan\beta\ell\) with \(\ell\) in degrees without converting.

VSWR of a complex \(\Gamma\) using \(\mathrm{Re}\,\Gamma\).

Quarter-wave formula on a \(\lambda/2\) line.

Using \( 50\,\Omega \) as \( Z_0 \) of a coax whose geometry is not 50 Ω.

Power \( |V|^2/Z_0 \) with peak versus RMS confusion.

Ignoring that a shorted \(\lambda/4\) is an open (and vice versa).

A 50 Ω line, \( Z_L=150\,\Omega \): \(\Gamma=(150-50)/(150+50)=0.500 \), VSWR = 3.00.

\( Z_L=j50 \), \( Z_0=50 \): \(\Gamma=j \), \( |\Gamma|=1 \), VSWR \(\infty\).

Quarter-wave 50 Ω line, \( Z_L=200\,\Omega \): \( Z_{\mathrm{in}}=12.5\,\Omega \).

Lossless line 0.3\(\lambda\), \( Z_0=75\,\Omega \), \( Z_L=75+j75 \). \(\beta\ell=0.6\pi=108^\circ \), \(\tan\beta\ell=\tan 108^\circ=-3.078 \). \( Z_{\mathrm{in}}=75\frac{75+j75+j75(-3.078)}{75+j(75+j75)(-3.078)} \) — compute carefully in rectangular form, or use Smith. Numerical: \( Z_{\mathrm{in}}\approx 23.1-j20.6\,\Omega \) (work in the solution of a problem, not here as gospel without a calculator). For exams, 0.25\(\lambda\) and 0.5\(\lambda\) are the intended lengths.

Coax \( b/a=e \), \(\varepsilon_r=1\): \( Z_0=60\,\Omega \). For 50 Ω air, \( b/a=e^{50/60}=2.30 \).

Step into 50 Ω open line: first step \( V=V_g Z_0/(Z_g+Z_0) \), reflects + at the open, eventually 2× that if \( Z_g=Z_0 \).

Matched generator \( Z_g=Z_0 \), load \(\Gamma\): no re-reflection at the source; net is a single bounce.

Power: \( V_0^+=10 \) V peak on 50 Ω, \( P^+=10^2/(2\times 50)=1.00 \) W. \( |\Gamma|=0.3 \), \( P_{\mathrm{load}}=1-0.09=0.91 \) W lossless.

\(\lambda/4\) shorted stub: \( Z_{\mathrm{in}}=\infty \), DC short, RF open — a bias tee trick.


Telegrapher derivation in one paragraph: for \(\Delta z\), series drop \( (R'+j\omega L')\Delta z\, I \), shunt current \( (G'+j\omega C')\Delta z\, V \), divide by \(\Delta z\), limit. Field derivation: TEM \(\mathbf{E},\mathbf{H}\) in the cross-section look like 2-D statics, \( V=\int\mathbf{E}\cdot\mathrm{d}\mathbf{l} \), \( I=\oint\mathbf{H}\cdot\mathrm{d}\mathbf{l} \), \( C' \) and \( L' \) from those statics with \( L'C'=\mu\varepsilon \) for homogeneous fill. That last identity is why \( v_p=1/\sqrt{L'C'}=1/\sqrt{\mu\varepsilon} \). Microstrip is quasi-TEM: an effective \(\varepsilon_{r,\mathrm{eff}}\) between 1 and the substrate \(\varepsilon_r\).

Bounce diagram: a 12 V source, 50 Ω \( Z_g \), 50 Ω line, 150 Ω load. Launch 6 V forward. \(\Gamma_L=(150-50)/(200)=0.5 \), so +3 V comes back. \(\Gamma_g=0\) if \( Z_g=Z_0 \), no further bounce. Load voltage 9 V in steady state, which matches the divider \( 12\times 150/200=9 \). If \( Z_g\neq Z_0 \), infinite bounces, geometric series to the same divider.

Lattice of a shorted line: \(\Gamma_L=-1 \), the reflection inverts. A pulse comes back upside down after \( 2t_d \). TDR instruments use that: open, short, and mismatch look different on the scope (measurements CRO unit meets this pack).

Lossy line input impedance is the same formula with \(\tanh\gamma\ell\) replacing \( j\tan\beta\ell \): \( Z_{\mathrm{in}}=Z_0(Z_L+Z_0\tanh\gamma\ell)/(Z_0+Z_L\tanh\gamma\ell) \). For small loss, \( Z_0 \) still ≈ real.

Power on a lossy line: \( |V_0^+(z)|^2 \) decays as \( e^{-2\alpha z} \). VSWR is worse toward the load if you measure near a mismatched load on a lossy run — the reflected wave has been attenuated.

Multiple reflections and a mismatched generator: the input \(\Gamma_{\mathrm{in}}=\Gamma_L e^{-2\gamma\ell} \) in the simple “load only” formula for the wave ratio at the input; the generator then sees \( Z_{\mathrm{in}} \). Steady-state phasors already include all bounces. Time domain is for steps; frequency domain is for sinusoids. Do not mix a bounce diagram with phasor \( Z_{\mathrm{in}} \) in one equation.

Slotted line: measure \( s \), and the distance of a voltage minimum from the load. A min occurs where the reflected and forward cancel most, \( \theta_\Gamma \) related to \( 4\pi x_{\min}/\lambda \). Then \( \Gamma=|\Gamma|e^{j\theta} \) with \( |\Gamma|=(s-1)/(s+1) \), then \( Z_L \). This is how laboratories found \( Z_L \) before VNAs.

Even and odd modes of coupled lines, directional couplers: named, not required. Crosstalk is a coupled-line bounce.

Worked \( LC \) of coax: \( C'=2\pi\varepsilon/\ln(b/a) \), \( L'=\mu\ln(b/a)/(2\pi) \), product \(\mu\varepsilon\), \( Z_0=\sqrt{L'/C'}=(\eta/2\pi)\ln(b/a) \). Numbers: \( b/a=3.5 \), \(\varepsilon_r=2.3 \) (PE), \( Z_0=50.6\,\Omega \), a polyethylene 50 Ω recipe.

Worked delay: 20 m of \(\varepsilon_r=2.25\) (velocity factor 0.667), \( t_d=100 \) ns. A 10 MHz sine has \( \ell/\lambda=20/(20)=1.0 \) wavelength on the line (\( \lambda=v/f=20 \) m). Not lumped.

Worked unmatched generator: \( V_g=10\angle 0 \) peak, \( Z_g=50 \), \( Z_{\mathrm{in}}=100 \), \( V_{\mathrm{in}}=10\times 100/150=6.67 \) V. That is the line input, not \( V_0^+ \) unless \(\Gamma_{\mathrm{in}}=0\).

Smith chart (next unit) is how you avoid grinding the tan formula for arbitrary \(\ell\). This unit you should still compute \( \lambda/4 \), \( \lambda/2 \), short, open, and real loads by hand.

A matched line can still radiate if it is unbalanced (coax with the sheath carrying a net current). Baluns exist. UG TEM theory assumes a pure differential/coax return.

When is a pair of wires a line? When \(\ell > \lambda/10 \) roughly, you should at least check. A 50 Hz power line is a line for surge transients (µs edges, \(\lambda\) of the edge not of 50 Hz) and for travelling-wave protection; it is lumped for steady 50 Hz phasors on a 50 km line only as a π-model (power pack), which is the telegrapher solved and lumped. Same physics, different approximation.


Characteristic impedance is not the resistance of the copper. A 50 Ω line can have 0.01 Ω of loop resistance per metre and still be 50 Ω for waves. \( Z_0=\sqrt{L'/C'} \) is a ratio of wave voltage to wave current, equal to \(\sqrt{L'/C'}\) lossless. Measuring \( Z_0 \) with a DC ohmmeter between inner and outer of a short piece gives open (or the insulation resistance), not 50 Ω. TDR or a VNA, or geometry plus \(\varepsilon_r\), gives \( Z_0 \).

Reflections of current: \( I^-/I^+ = -\Gamma \) for the voltage \(\Gamma\). At a short, voltage wave flips, current wave does not; at an open, current flips. Power \( \frac12\mathrm{Re}(V I^*) \) still holds with both waves present; the reactive standing-wave energy sloshes and time-average power is the net.

A lossless line does not dissipate, but a mismatched transmitter may still see a high \( |Z_{\mathrm{in}}| \) and deliver less power from a given \( V_g,Z_g \). Matching (unit 09) maximizes that delivery for a fixed generator. The line’s \( 1-|\Gamma|^2 \) factor is the load’s absorption of whatever incident power exists.

Frequency-domain \( \beta(f) \) linear for lossless non-dispersive fill: a pulse keeps its shape. Microstrip and waveguide (unit 10) are dispersive; pulses smear. UG coaxial PE fill is treated as non-dispersive.

Write \( \ell/\lambda \) not “degrees” without \( \times 360 \). \( \beta\ell=90^\circ \) is \(\lambda/4\). A 90° hybrid is a different microwave component that happens to use \(\lambda/4\) lines. Do not confuse a 90° electrical length with a 90° hybrid coupler.

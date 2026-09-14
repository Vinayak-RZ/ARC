# Faraday’s law, Lenz, and inductance

A time-varying magnetic flux through a loop produces an emf: Faraday. Lenz’s law gives the sign: the induced current fights the change of flux. Inductance is the linear coefficient \(\lambda=LI\) that makes \( v=L\mathrm{d}i/\mathrm{d}t \) for a coil in a linear medium. Mutual inductance \( M \) is the flux in circuit 2 per ampere in circuit 1, and \( M_{12}=M_{21} \). This unit is the bridge from magnetostatics to Maxwell and to circuit inductors, transformers, and eddy-current losses.

## Concepts

Integral Faraday: \(\oint\mathbf{E}\cdot\mathrm{d}\mathbf{l}=-\mathrm{d}\Phi/\mathrm{d}t\) with \(\Phi=\int\mathbf{B}\cdot\mathrm{d}\mathbf{S}\) through a surface bounded by the loop. For \( N \) turns, \(\mathcal{E}=-N\mathrm{d}\Phi_1/\mathrm{d}t\) if each turn has flux \(\Phi_1\) (flux linkage \(\lambda=N\Phi_1\)). Stationary loop in a changing \(\mathbf{B}\), or a moving loop in a static \(\mathbf{B}\) (motional emf \( \oint(\mathbf{v}\times\mathbf{B})\cdot\mathrm{d}\mathbf{l} \)), or both. The differential form \(\nabla\times\mathbf{E}=-\partial\mathbf{B}/\partial t\) is unit 06; here the integral statement is enough to compute transformers and sliding bars.

Lenz: if you try to increase flux to the right through a loop, the induced current makes flux to the left. The minus sign is not optional. Eddy currents in a copper plate are Lenz currents distributed in the metal; they dissipate \( I^2R \) and produce drag (induction motor torque is the useful cousin). Laminations and powdered cores cut eddy paths.

Inductance: for a linear two-terminal coil, \(\lambda=Li\), \( v=\mathrm{d}\lambda/\mathrm{d}t=L\mathrm{d}i/\mathrm{d}t\) if \( L \) is constant. Internal inductance of a wire from flux inside the conductor is \(\mu_0/(8\pi)\) H/m for DC uniform current; external inductance depends on the return path. A coax’s inductance per metre is \( \mu/(2\pi)\ln(b/a) \) external plus internal. A solenoid \( L=\mu n^2 A \ell=\mu N^2 A/\ell \). A toroid \( L=\mu N^2 A/(2\pi\rho_{\mathrm{mean}}) \). Energy \( W=\frac12 Li^2=\frac12\int\mathbf{B}\cdot\mathbf{H}\,\mathrm{d}v \).

Mutual: \(\lambda_2=M i_1\), \( M=k\sqrt{L_1 L_2} \) with \( 0\le k\le 1 \). Dot convention: currents into dotted terminals produce aiding flux. Transformer \( v_1=L_1\mathrm{d}i_1/\mathrm{d}t+M\mathrm{d}i_2/\mathrm{d}t \). Neumann formula \( M=\frac{\mu_0}{4\pi}\oint\oint\mathrm{d}\mathbf{l}_1\cdot\mathrm{d}\mathbf{l}_2/R \). Reciprocity \( M_{12}=M_{21} \).

Motional emf: a bar sliding on rails in a uniform \(\mathbf{B}\) perpendicular to the plane, speed \( v \), width \(\ell\): \(\mathcal{E}=B\ell v\). Power \( \mathcal{E}I \) equals mechanical force times speed (energy conversion). Flux rule still works: \(\Phi=B\ell x \), \(\mathrm{d}\Phi/\mathrm{d}t=B\ell v\).

Time-varying \(\mathbf{B}\) in a stationary circuit: transformer emf. If the loop is not filamentary, you integrate \(\mathbf{E}\) along the actual path (a voltmeter’s leads can pick up loop area — measure the intended circuit).

Self-inductance is always positive. Mutual can be signed via the dots. Series aiding \( L=L_1+L_2+2M \), opposing \( L_1+L_2-2M \).

Skin effect (preview): high frequency current crowds to the surface, internal \( L \) drops, resistance rises. Not needed for the DC solenoid formula.

## Equations

Faraday:

\[
\mathcal{E}=\oint\mathbf{E}\cdot\mathrm{d}\mathbf{l}=-\frac{\mathrm{d}}{\mathrm{d}t}\int_S\mathbf{B}\cdot\mathrm{d}\mathbf{S}=-N\frac{\mathrm{d}\Phi}{\mathrm{d}t}.
\]

Motional:

\[
\mathcal{E}=\oint(\mathbf{v}\times\mathbf{B})\cdot\mathrm{d}\mathbf{l}.
\]

Inductance:

\[
L=\frac{\lambda}{I}=\frac{N\Phi}{I},\qquad v=L\frac{\mathrm{d}i}{\mathrm{d}t},\qquad W=\frac12 LI^2.
\]

Solenoid / coax per length:

\[
L=\frac{\mu N^2 A}{\ell},\qquad L'=\frac{\mu}{2\pi}\ln\frac{b}{a}.
\]

Mutual:

\[
M=\frac{\lambda_{21}}{I_1},\qquad k=\frac{M}{\sqrt{L_1 L_2}}.
\]

Sliding bar: \(\mathcal{E}=B\ell v\), \( F_{\mathrm{mag}}=B I\ell \) opposing motion if a closed circuit draws \( I \).

## Methods

Compute \(\Phi(t)\) through the circuit with a consistent normal (right-hand with the loop sense), differentiate, apply the minus sign, then interpret Lenz as a check.

For \( L \): assume \( I \), find \( B \) (Ampère), \(\Phi\), \(\lambda=N\Phi\), \( L=\lambda/I \). Ignore leakage if the problem is an ideal solenoid.

For \( M \): current in 1, flux through 2. Example: a small loop on the axis of a large loop.

Moving bar: decide area vs time; or use \(\mathbf{v}\times\mathbf{B}\) along the moving conductor only if the rails are ideal and \(\mathbf{B}\) is uniform.

Transformer emf with sinusoidal \( B_m \): \(\mathcal{E}_{\mathrm{rms}}=4.44 f N B_m A\) (the machines formula). Same Faraday.

## Mistakes

Dropping the minus and then also applying Lenz, or keeping both and double-reversing.

Using \( N\Phi \) when \(\Phi\) already included all turns.

Solenoid \( L=\mu N^2 A \) without dividing by length.

Mutual \( M=L_1 \) when \( k\neq 1 \).

Flux through a non-closed path.

Voltmeter leads enclosing extra area in a 50 Hz busbar measurement.

Internal inductance forgotten when someone wants nH of a 1 cm jumper (often comparable to external).

Energy \(\frac12\int B H\) with the wrong volume (only the core, forgetting the gap where energy actually sits).

A solenoid walk-through: \( N=200 \), \(\ell=20\) cm, \( A=4 \) cm², air. \( L=\mu_0\times 40000\times 4e-4/0.2=100.5 \) µH. At 2 A, \(\lambda=201 \) µWb-t, \( W=201 \) µJ.

Coax: \( a=1 \) mm, \( b=4 \) mm, \(\mu_0\), \( L'=(\mu_0/2\pi)\ln 4=277 \) nH/m.

Faraday loop: 20 turns, \( B=0.4\sin(377t) \) T, \( A=8 \) cm², \(\Phi_1=3.2\times 10^{-4}\sin(377t) \), \(\mathcal{E}=-20\times 3.2e-4\times 377\cos(377t)=-2.41\cos(377t) \) V.

Sliding bar: \( B=0.8 \) T, \(\ell=0.25 \) m, \( v=2 \) m/s, \(\mathcal{E}=0.40 \) V. If \( R=0.5\,\Omega \), \( I=0.80 \) A, \( F=B I\ell=0.16 \) N.

Mutual: two coaxial loops, far approximation \( M\approx\mu_0\pi a^2 b^2/(2 z^3) \) for \( z\gg a,b \). Plug \( a=b=3 \) cm, \( z=20 \) cm: \( M\approx 8.0 \) nH.

Series opposing: \( L_1=4 \) mH, \( L_2=9 \) mH, \( k=0.5 \), \( M=3 \) mH, \( L_{\mathrm{eq}}=4+9-6=7 \) mH.

4.44 formula: \( f=50 \) Hz, \( N=200 \), \( B_m=1.2 \) T, \( A=40 \) cm², \( E_{\mathrm{rms}}=4.44\times 50\times 200\times 1.2\times 0.004=21.3 \) V.

Lenz check: flux into the page increasing, induced current counterclockwise if that produces flux out of the page (right-hand).


Flux rule pitfalls. If the circuit’s identity changes (a sliding bar that opens a switch), draw the loop at each instant. If a conducting sheet is infinite, induced \(\mathbf{E}\) is azimuthal around a changing solenoid (the betatron field): \(\oint E\cdot dl= -A\mathrm{d}B/\mathrm{d}t \), \( E_\phi=-(r/2)\mathrm{d}B/\mathrm{d}t \) inside a uniform \( \dot B \) region. That \(\mathbf{E}\) exists in empty space, not only in wires. A voltmeter on radial leads can confuse you; state the path.

Transformer emf versus motional emf: in a homopolar generator (Faraday disc), the disc rotates in an axial \( B \), \(\mathcal{E}=\frac12 B\omega a^2 \) between centre and rim. The flux through a circuit that includes a stationary brush may look constant; the flux rule needs a carefully defined moving contour. UG: prefer \(\mathbf{v}\times\mathbf{B}\) in the disc. Do not claim the flux rule failed; claim you defined the loop poorly.

Mutual inductance of two coaxial solenoids, long outer, short inner: \( M=\mu n_1 N_2 A_{\mathrm{inner}} \) if the inner is in the uniform region. Coefficient \( k=M/\sqrt{L_1 L_2} \) is less than 1 because of leakage of the outer’s return flux.

Eddy current loss in a lamination: roughly \( P\sim (B_m f d)^2/\rho \) times a geometric factor, \( d \) thickness. That is why transformer steel is 0.3 mm, not 3 mm, at 50 Hz. Skin depth in steel at 50 Hz can be a millimetre-ish depending on \(\mu\); laminations also cut eddy paths geometrically.

Inductance of a loop: \( L=(\mu_0/\pi)[\ell\ln(2\ell/a)-2] \) or similar for a round-wire square — the logarithm of (size/wire radius) is the external inductance. Internal \(\mu_0 \ell/(8\pi)\). A 10 cm square of 1 mm wire is a few hundred nH, not zero. PCB return loops are the same story (EMI).

Dot convention example: two coils on a common core, dots at the top. Series aiding is dots far apart in the series string (current in both relative to dots the same way). If you series them with dots together, you subtract \( 2M \). Measuring \( L_{\mathrm{aiding}} \) and \( L_{\mathrm{opposing}} \) gives \( M=(L_a-L_o)/4 \).

Time-varying flux through a wattmeter’s loop (measurements pack) is a Faraday error: twist the voltage leads.

Displacement current is not needed to compute a transformer at 50 Hz; Faraday is. Displacement is why a capacitor current equals \( C\mathrm{d}v/\mathrm{d}t \) in Maxwell (next unit). Keep the labels straight.

Energy and force: a relay’s coil \( L(x) \), \( i \) constant (current source), force \(\frac12 i^2\mathrm{d}L/\mathrm{d}x\) closing the gap ( \( L \) increases). At constant flux linkage, the sign in the coenergy/energy formulas swaps; use coenergy for current-driven actuators.

Sinusoidal steady state: \( V=j\omega L I \), \( \omega L \) the reactance. Mutual \( V_2=j\omega M I_1 \) with the dot sign. A coupling capacitor is not an inductor; do not write \( j\omega M \) for electrostatic coupling.

Worked: 100-turn coil, \( B=0.02 t \) tesla through \( 40 \) cm², \( 0<t<0.1 \) s. \(\Phi_1=8\times 10^{-5} t \), \(\mathcal{E}=-N 8e-5=-8.0 \) mV, constant while \( B \) ramps.

Worked: two 5 mH coils, \( k=0.4 \), \( M=2 \) mH. Series opposing 6 mH. If someone measures 16 mH they connected aiding (\( 5+5+4 \)).

Worked: bar \( B=1.2 \) T, \(\ell=0.1 \) m, \( v=5 \) m/s, \( R=0.2\,\Omega \), mass 0.05 kg, frictionless. \( I=B\ell v/R=3 \) A at that speed, \( F=0.36 \) N. Not in equilibrium unless an external force supplies that. Terminal speed with a friction force would balance; without friction the bar slows until \( v=0 \) if it is coasting (energy dumped in \( R \)).

Lenz: a superconducting loop (ideal) conserves flux. An applied \( B \) induces a persistent current so that \(\Phi\) stays put. Perfect Lenz, zero resistance.

If the area vector and \(\mathbf{B}\) are at an angle, \(\Phi=BA\cos\theta\). A rotating machine \(\theta=\omega t\), \(\mathcal{E}=BA\omega\sin\omega t\). That is the elementary generator, Faraday every time.

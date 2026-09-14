# Complex arithmetic and Euler

Undergraduate electrical engineering treats a complex number as a packed pair: a real part that can stand for a cosine (in-phase) component and an imaginary part that can stand for a sine (quadrature) component. The same object later becomes a phasor, an impedance, a reflection coefficient, or a DFT bin. This unit is the arithmetic that those later courses assume is automatic. It is not a first course in complex analysis: contour integrals and residues wait for unit 10. Here the job is to add, multiply, invert, take roots, and convert between rectangular and polar form without dropping a sign on \(j\).

In EE the imaginary unit is \(j\), not \(i\), because \(i(t)\) is already current. The two letters are the same mathematical object, \(j^2 = -1\). Time-domain sinusoids stay real. Complex notation is a bookkeeping device that turns trigonometric identities into algebra. A student who can multiply \(3+j4\) by \(2-j2\) in both rectangular and polar form, and who can write \(e^{j\theta}\) as \(\cos\theta + j\sin\theta\) without looking it up, has the working skill this unit exists to install.

## Concepts

A complex number \(z\) may be written \(z = x + jy\) with real \(x,y \in \mathbb{R}\). The pair \((x,y)\) is a point in the Argand plane. Addition of complex numbers is vector addition of those points. Multiplication is not vector addition: it scales lengths and adds angles. That single geometric fact is why phasors work. If a voltage phasor has magnitude \(V_m/\sqrt{2}\) and angle \(\theta_v\), and a current phasor has magnitude \(I_m/\sqrt{2}\) and angle \(\theta_i\), their ratio is an impedance whose angle is \(\theta_v - \theta_i\). No trigonometry beyond the definition of cosine and sine is required once polar multiplication is trusted.

The modulus (magnitude, absolute value) is \(|z| = \sqrt{x^2 + y^2}\). It is never negative. The argument (angle, phase) is \(\arg z = \operatorname{atan2}(y,x)\), not \(\arctan(y/x)\) alone. The two-argument arctangent keeps the quadrant. A number in the second quadrant such as \(-3+j4\) has angle \(\pi - \arctan(4/3)\), not \(-\arctan(4/3)\). Principal argument is conventionally taken in \((-\pi,\pi]\) or sometimes \([0,2\pi)\). Circuit courses usually report degrees in \((-180^\circ, 180^\circ]\). When you add angles after a product of several impedances, reduce modulo \(360^\circ\) and then snap back into the principal interval. Leaving \(450^\circ\) on the page is a bookkeeping error, not a different physical state.

The complex conjugate \(z^* = x - jy\) reflects the point through the real axis. Conjugation is the algebraic stand-in for “reverse the direction of time-harmonic rotation.” In circuit power, average real power uses \(S = \mathbf{V}\mathbf{I}^*\), not \(\mathbf{V}\mathbf{I}\). The conjugate on current is required so that a lagging current (inductive load) produces a positive imaginary part of \(S\) under the EE sign convention that \(Q>0\) means lagging (inductive) VARs. Forgetting the conjugate is the most common complex-arithmetic bug in an AC power exam.

Euler’s formula \(e^{j\theta} = \cos\theta + j\sin\theta\) is the bridge between polar form and the exponential. Polar form is \(z = |z|(\cos\theta + j\sin\theta) = |z|e^{j\theta}\). EE shorthand \(z = |z|\angle\theta\) is the same object. Euler’s identity \(e^{j\pi} = -1\) is the special case \(\theta=\pi\). The exponential form makes differentiation and delay trivial: multiplying by \(j\omega\) is a \(+90^\circ\) rotation and a scale by \(\omega\); multiplying by \(e^{-j\omega\tau}\) is a time delay of \(\tau\) seconds in the Fourier transform of a delayed signal. Those two facts are why the Fourier and Laplace chapters later in this pack exist.

De Moivre’s theorem \((\cos\theta + j\sin\theta)^n = \cos(n\theta) + j\sin(n\theta)\) is Euler in integer clothing. It yields the \(n\) distinct \(n\)th roots of a nonzero complex number: if \(z = re^{j\theta}\), then
\[
z^{1/n} = r^{1/n}\exp\left(j\frac{\theta+2\pi k}{n}\right),\qquad k=0,1,\ldots,n-1.
\]
Roots lie equally spaced on a circle of radius \(r^{1/n}\). In power electronics and three-phase work the cube roots of unity \(1,\ \omega,\ \omega^2\) with \(\omega = e^{j2\pi/3}\) are the same statement. In control, the \(N\)th roots of \(-1\) locate the Butterworth pole angles.

Division is multiplication by the reciprocal. The reciprocal of a polar number is immediate: invert the magnitude and negate the angle. In rectangular form, multiply numerator and denominator by the conjugate of the denominator so the denominator becomes a positive real \(x^2+y^2\). Never “cancel \(j\)” as if it were a variable that might be zero; \(j\) is a constant.

A time-harmonic signal \(v(t) = V_m\cos(\omega t + \phi)\) is represented by the phasor \(\mathbf{V} = V_m e^{j\phi}\) (peak convention) or \(\mathbf{V}_{\mathrm{rms}} = (V_m/\sqrt{2})e^{j\phi}\) (RMS convention). The two conventions must not be mixed in one calculation. Kirchhoff’s laws remain linear over the complexes, so nodal and mesh analysis carry over from DC with \(R\) replaced by \(Z(j\omega)\). Impedance of a resistor is \(R\), of an inductor \(j\omega L\), of a capacitor \(1/(j\omega C) = -j/(\omega C)\). A series combination adds; a parallel combination uses the reciprocal-sum. That is the entire AC steady-state programme reduced to complex arithmetic.

Products of sinusoids are not phasor products. Instantaneous power \(p(t)=v(t)i(t)\) has a double-frequency term. Phasors linearize *linear* circuits in sinusoidal steady state; they do not linearize multiplication of two time functions. When a problem asks for average power, return to \(P = \operatorname{Re}(\mathbf{V}\mathbf{I}^*)\) (RMS phasors) or \(P = \tfrac12 V_m I_m\cos(\theta_v-\theta_i)\) (peak phasors).

Complex numbers are a field: every nonzero element has a multiplicative inverse, addition and multiplication are commutative and associative, and the distributive law holds. The complexes are not an ordered field. Statements such as \(z_1 > z_2\) are meaningless unless both numbers happen to be real. Comparing impedances “which is larger” must specify magnitude, real part, or some other real functional.

Branch cuts appear as soon as a multi-valued inverse (logarithm, square root) is treated as a function. UG EE almost always uses the principal branch. The logarithm \(\operatorname{Log} z = \ln|z| + j\operatorname{Arg} z\) with \(\operatorname{Arg} z \in (-\pi,\pi]\) jumps across the negative real axis. That jump is why a Bode phase plot of \(-1/(j\omega)\) is drawn as \(-90^\circ\) for \(\omega>0\), not \(+270^\circ\), unless a continuous unwrapped phase is requested.

In three-phase systems the operator \(a = e^{j2\pi/3} = -1/2 + j\sqrt{3}/2\) rotates a phasor by \(120^\circ\). The identities \(1+a+a^2=0\) and \(a^3=1\) are used constantly in symmetrical-component work. They are not extra theory; they are Euler’s formula at \(120^\circ\) and \(240^\circ\).

A last conceptual split: a *phasor* is a complex constant representing a real sinusoid at one known frequency. A *complex signal* \(e^{j\omega t}\) is a complex-valued function of time, used as an analysis tool (complex exponential eigenfunctions of LTI systems). A *complex envelope* in communications is yet a third object, a slowly varying complex function modulating a carrier. Using the same letter \(V\) for all three without saying which is meant is how sign errors propagate into later courses.

## Equations

Rectangular and polar conversion:

\[
z = x + jy = r e^{j\theta},\qquad r = \sqrt{x^2+y^2},\qquad \theta = \operatorname{atan2}(y,x).
\]

\[
x = r\cos\theta,\qquad y = r\sin\theta.
\]

Euler and the conjugate:

\[
e^{j\theta} = \cos\theta + j\sin\theta,\qquad \cos\theta = \frac{e^{j\theta}+e^{-j\theta}}{2},\qquad \sin\theta = \frac{e^{j\theta}-e^{-j\theta}}{2j}.
\]

\[
z + z^* = 2x,\qquad z - z^* = 2jy,\qquad zz^* = |z|^2.
\]

Arithmetic:

\[
z_1 z_2 = r_1 r_2 e^{j(\theta_1+\theta_2)},\qquad \frac{z_1}{z_2} = \frac{r_1}{r_2}e^{j(\theta_1-\theta_2)}\ (z_2\neq 0).
\]

\[
\frac{x_1+jy_1}{x_2+jy_2} = \frac{(x_1+jy_1)(x_2-jy_2)}{x_2^2+y_2^2}.
\]

Powers and roots (De Moivre):

\[
z^n = r^n e^{jn\theta},\qquad z^{1/n} = r^{1/n}\exp\left(j\frac{\theta+2\pi k}{n}\right),\ k=0,\ldots,n-1.
\]

Sinusoid and RMS phasor (EE convention):

\[
v(t) = V_m\cos(\omega t+\phi)\ \longleftrightarrow\ \mathbf{V}_{\mathrm{peak}} = V_m e^{j\phi},\quad \mathbf{V}_{\mathrm{rms}} = \frac{V_m}{\sqrt{2}}e^{j\phi}.
\]

Device impedances at a single frequency \(\omega>0\):

\[
Z_R = R,\qquad Z_L = j\omega L,\qquad Z_C = \frac{1}{j\omega C} = -\frac{j}{\omega C}.
\]

Complex power with RMS phasors:

\[
S = \mathbf{V}\mathbf{I}^* = P + jQ,\qquad P = VI\cos\phi,\qquad Q = VI\sin\phi,\qquad \phi = \theta_v-\theta_i.
\]

Rotation operator and cube roots of unity:

\[
a = e^{j2\pi/3},\qquad a^2 = e^{-j2\pi/3},\qquad 1+a+a^2 = 0,\qquad a^3 = 1.
\]

## Methods

Convert every mixed-form expression to one form before combining. If the next operation is addition or subtraction, use rectangular form. If the next operation is multiplication, division, power, or root, use polar or exponential form. Convert back only at the end, and state the angle unit.

To convert rectangular to polar by hand: compute \(r=\sqrt{x^2+y^2}\). Sketch the point, then compute the reference angle \(\alpha = \arctan(|y|/|x|)\) and place \(\theta\) in the correct quadrant from the signs of \(x\) and \(y\). Do not feed \(y/x\) to a calculator’s single-argument arctan when \(x<0\).

To multiply in rectangular form expand \((x_1+jy_1)(x_2+jy_2) = (x_1x_2-y_1y_2)+j(x_1y_2+y_1x_2)\). The minus on the real part is the \(j^2=-1\) contribution. To divide, multiply by the conjugate of the denominator, then simplify.

To invert an impedance \(R+jX\), use
\[
Y = \frac{1}{R+jX} = \frac{R}{R^2+X^2} - j\frac{X}{R^2+X^2}.
\]
The imaginary part of admittance has the opposite sign of \(X\). An inductive impedance (\(X>0\)) has a negative susceptance.

For a series RLC at a stated \(\omega\), write each device as a complex number, add, then convert the sum to polar if a magnitude and phase of current \(\mathbf{I}=\mathbf{V}/Z\) are required. For parallel elements, convert each impedance to admittance, add, invert the sum.

When extracting a time-domain sinusoid from a phasor, restore the \(e^{j\omega t}\) factor and take the real part if the original source was a cosine (or the imaginary part if it was a sine, consistently). Mixing cosine-as-real with sine-as-real in one problem is a method error.

To find \(n\)th roots, convert to polar including a full set of arguments \(\theta+2\pi k\), divide angles by \(n\), take the positive real \(n\)th root of \(r\), and list \(k=0,\ldots,n-1\). Plotting the roots on a circle is the check: they must be equally spaced.

For three-phase balanced sets, generate the b and c phasors from a by multiplying by \(a^2\) and \(a\) (ABC sequence) rather than subtracting \(120^\circ\) in your head three times. The operator method drops fewer signs.

Keep RMS and peak conventions in a header line of the scratch work. Convert a given peak voltage to RMS before using \(S=\mathbf{V}\mathbf{I}^*\) if the formula you memorized was the RMS one. The factor of two between \(\tfrac12 V_m I_m\) and \(V_{\mathrm{rms}}I_{\mathrm{rms}}\) is the same \(\sqrt{2}\times\sqrt{2}\).

## Mistakes

Writing \(\arg(-1+j0) = 0\) or \(\arctan(0/-1)=0\). The point is on the negative real axis; the principal argument is \(\pi\) (or \(180^\circ\)).

Using \(\arctan(y/x)\) for a second- or third-quadrant number and dropping the angle into the fourth quadrant. Always restore the quadrant from the signs, or use \(\operatorname{atan2}\).

Adding polar magnitudes as if they were real numbers: \(|z_1+z_2|\neq |z_1|+|z_2|\) in general. Convert to rectangular, add, then take magnitude.

Computing complex power as \(\mathbf{V}\mathbf{I}\) without conjugating current. Then \(Q\) has the wrong sign and the power factor angle is reversed.

Mixing peak and RMS phasors in \(S=\mathbf{V}\mathbf{I}^*\). If both are peak, the product is twice the average complex power.

Treating \(1/j\) as \(j\) rather than \(-j\). The identity is \(1/j = -j\), because \(j\cdot(-j) = -j^2 = 1\). Capacitive reactance is negative: \(Z_C = -j/(\omega C)\).

Reporting only one square root of a complex number when the problem asks for all roots. There are two square roots, three cube roots, and so on, equally spaced.

Cancelling a factor \(s+j\omega\) from a transfer function without checking that it is not also a pole, or cancelling \(j\) from a numerator and denominator as if \(j\) could be zero.

Writing \(e^{j\theta} = \cos\theta + \sin\theta\) and dropping the \(j\) on the sine. The sine term is imaginary.

Comparing two impedances with an inequality. Compare magnitudes, real parts, or \(|Z|\) explicitly.

Using degrees in \(e^{j\theta}\) while the exponential expects radians. \(e^{j90}\) is not \(j\). Convert: \(90^\circ=\pi/2\). Calculators in degree mode still need the exponential in radians if you type `exp(j*theta)`.

Forgetting that a phasor hides \(\omega\). Two phasors at different frequencies cannot be added. Superposition in the time domain is required, then each frequency is converted separately.

Sign error on the three-phase operator: \(a = -1/2 + j\sqrt{3}/2\), not \(-1/2 + j\sqrt{3}\). The imaginary part is \(\sqrt{3}/2\).

# Digital control intro: sampling, hold, discrete equivalents

A digital controller samples a continuous error, computes a new \(u[k]\), and holds it on the actuator between samples. The loop is hybrid: continuous plant, discrete controller. UG analysis uses the discrete transfer function of plant-plus-hold, the \(z\)-plane stability disk, and simple equivalents (forward Euler, backward Euler, Tustin) of a designed analog \(C(s)\). This unit is those maps, aliasing, and the Jury/Routh-via-bilinear tests at intro depth — not MIMO sampled-data theory.

## Concepts

Sampling a signal \(y(t)\) at period \(T\) produces \(y[k]=y(kT)\). If \(y\) contains frequencies above the Nyquist frequency \(\pi/T\) rad/s, those components alias to lower discrete-time frequencies and cannot be undone. Anti-alias filters belong before the sampler. Shannon reconstruction is not what a drive amplifier does: the standard actuator interface is a zero-order hold (ZOH) that holds \(u(t)=u[k]\) for \(t\in[kT,(k+1)T)\).

The exact discrete plant with ZOH and sampler is
\[
G_d(z)=\bigl(1-z^{-1}\bigr)\mathcal{Z}\left\{\mathcal{L}^{-1}\frac{G(s)}{s}\Big|_{t=kT}\right\}=(z-1)\mathcal{Z}\left\{\frac{G(s)}{s}\right\}
\]
in the common shift-operator form, equivalently \(G_d(z)=C(zI-\Phi)^{-1}\Gamma\) with \(\Phi=e^{AT}\), \(\Gamma=\int_0^T e^{A\tau}\,d\tau\, B\) when \(G\) has a realization \((A,B,C,0)\). For \(G=a/(s+a)\),
\[
G_d(z)=\frac{1-e^{-aT}}{z-e^{-aT}}.
\]
For \(G=1/s\), \(G_d=T/(z-1)\). For \(G=1/s^2\), \(G_d=T^2(z+1)/(2(z-1)^2)\). Poles map as \(z=e^{sT}\). Zeros do not map that simply; a relative-degree-two continuous plant typically acquires a zero (sometimes in the left \(z\) half, sometimes on the negative real axis — the famous sampling zero).

Stability of a discrete closed loop: all poles of \(T(z)\) strictly inside the unit disk \(|z|<1\). The unit circle is the analog of the \(j\omega\) axis. Mapping \(s=\sigma+j\omega\) gives \(z=e^{\sigma T}e^{j\omega T}\): vertical lines (constant \(\sigma\)) become circles of radius \(e^{\sigma T}\); the \(j\omega\) axis becomes \(|z|=1\). Fast continuous poles (\(\sigma\ll 0\)) sit near \(z=0\). A continuous integrator \(s=0\) becomes \(z=1\).

Jury test is the discrete Routh. For a quadratic \(z^2+a z+b\), the disk conditions are \(|b|<1\), \(1+a+b>0\), \(1-a+b>0\). For higher order, use Jury tables or bilinear
\[
z=\frac{1+w}{1-w}
\]
and Routh in \(w\). The bilinear (Tustin) map sends the analog left half-plane to \(|z|<1\) and is also the trapezoidal integrator used to discretize controllers.

Discrete equivalents of a given \(C(s)\), none of which is the ZOH equivalent of the plant:

- Forward Euler: \(s=(z-1)/T\). Cheap, can map a stable analog pole outside the disk if \(T\) is large.
- Backward Euler: \(s=(z-1)/(T z)\). Stiff-stable; maps the analog LHP into a subset of the disk.
- Tustin: \(s=(2/T)(z-1)/(z+1)\). Maps LHP onto the disk. Frequency warping \(\omega_a=(2/T)\tan(\omega_d T/2)\); prewarp a notch or a crossover by using that formula when matching one analog frequency.

A digital PID is the analog PID after one of those substitutions, plus a filtered derivative. Sampling slower than about \(1/10\) of the desired closed-loop bandwidth (rule of thumb: 8–20 samples per rise) makes the hold’s delay (about \(T/2\)) eat phase margin. Sampling too fast amplifies quantization and requires larger wordlength; it also makes \(z\approx 1+sT\) poorly conditioned (all poles cluster at \(z=1\)).

Deadbeat: place all discrete closed-loop poles at \(z=0\). Finite settling in \(n\) samples for an order-\(n\) controllable discrete plant, with violent controls and no intersample error spec. UG should know the name and the cost, not design it as a default.

Delay of one sample (\(z^{-1}\)) in the controller or in computation adds phase \(-\omega T\) on the unit circle, same as a continuous delay of \(T\) at the sample instants. Computational delay is often modelled as an extra \(z^{-1}\).

## Equations

ZOH discrete plant (state):
\[
\Phi=e^{AT},\qquad \Gamma=\int_0^T e^{A\tau}\,d\tau\, B,\qquad G_d(z)=C(zI-\Phi)^{-1}\Gamma.
\]
Pole map: \(z=e^{sT}\).

Tustin:
\[
s=\frac{2}{T}\frac{z-1}{z+1},\qquad \omega_a=\frac{2}{T}\tan\bigl(\tfrac{\omega_d T}{2}\bigr).
\]
Forward / backward:
\[
s=\frac{z-1}{T},\qquad s=\frac{z-1}{Tz}.
\]

Quadratic Jury:
\[
|b|<1,\quad 1+a+b>0,\quad 1-a+b>0
\]
for \(z^2+a z+b=0\).

First-order ZOH:
\[
G(s)=\frac{a}{s+a}\ \Rightarrow\ G_d(z)=\frac{1-e^{-aT}}{z-e^{-aT}}.
\]

Hold delay (approx. for Bode): \(e^{-s T/2}\).

## Methods

To discretize a plant for analysis: if the problem gives \(G(s)\) and \(T\), use the ZOH formula or the tables for \(1/s\), \(1/s^2\), \(a/(s+a)\). Do not Tustin the plant when the hardware is a ZOH; Tustin is for the controller (usually).

To discretize a controller: pick Tustin unless the exam specifies Euler. Prewarp the critical frequency. Realize the resulting \(C(z)\) as a difference equation \(u[k]=\cdots\) in causal form (positive powers of \(z^{-1}\)).

Stability: form \(1+C(z)G_d(z)=0\), get a polynomial in \(z\), apply Jury or bilinear+Routh.

Choose \(T\): start from analog bandwidth \(\omega_b\), set \(T\) so that \(\omega_b T \approx 0.2\) to \(0.5\) rad/sample (several samples per radian of bandwidth). Check that no plant resonance aliases.

Intersample ripple: discrete poles in the disk can still hide oscillatory continuous output between samples if a sampling zero or a hold interacts with a lightly damped plant. Inspect \(y(t)\), not only \(y[k]\), in a simulation course; in a sit-down exam, mention the issue when poles are near \(z=-1\).

When using forward Euler on \(C(s)=K/s\), \(C(z)=K T/(z-1)\), a discrete integrator. Backward Euler: \(K T z/(z-1)\). They differ by a zero at the origin.

Bilinear Routh on a discrete polynomial, one cubic. Closed-loop \(z^2-1.2z+0.5=0\) is quadratic; skip to \(z^3-0.5z^2+0.1z-0.02=0\) as a fake example of the substitution. Set \(z=(1+w)/(1-w)\), multiply by \((1-w)^3\), collect \(w^3,w^2,w,1\), then run the ordinary Routh array. The number of \(w\)-RHP roots equals the number of \(z\)-roots outside the disk. This is slower than Jury for a quadratic and worth it when Jury’s table has been forgotten. For the quadratic \(z^2+a z+b\), the three inequalities listed above are exactly the bilinear+Routh conditions after some algebra; memorize those three, not the substitution, at this level.

DC matching after discretization: a type-0 analog \(G(0)\) should equal \(G_d(1)\) for ZOH and for Tustin (if \(G\) is finite at 0). A type-1 analog has \(G_d(1)=\infty\) with a pole at \(z=1\). If your Tustin of a PI lost the pole at \(z=1\), the algebra dropped a \((z-1)\) factor incorrectly. Check \(C_d(1)\) against \(C(0)\).

Quantization and finite wordlength are the next layer: a 12-bit ADC on a ±10 V range has an LSB of about 5 mV; a high-gain discrete PID will chatter on that LSB if the derivative is unfiltered. UG intro stops at mentioning it; implement a filter pole as in analog PID.

## Mistakes

Using \(|s|<1\) as the discrete stability region, or \(|z|\) in the LHP.

Tustin on the plant while the DAC is a ZOH, then wondering why the DC gain of \(G_d\) is wrong. (ZOH \(G_d(1)=G(0)\) for type 0; Tustin of \(G(s)\) also matches DC if done carefully, but the poles are not \(e^{sT}\).)

Forward Euler with \(T>2/|\lambda|\) on a real analog pole \(\lambda<0\), mapping outside the disk.

Forgetting \(z=e^{sT}\) is in radians, with \(T\) in seconds: a pole at \(s=-10\) with \(T=0.1\) is \(z=e^{-1}=0.368\), not \(e^{-10}\).

Jury inequalities with the wrong sign on the middle coefficient.

Placing analog-designed \(\omega_g\) near Nyquist (\(\pi/T\)) so the phase of the hold and the warping are both severe.

Implementing Tustin \(C(z)\) with future samples (\(z\) in the numerator of higher degree than the denominator). Proper analog \(C\) stays proper after Tustin.

Ignoring computational delay of one sample when the processor is slow.

Treating \(G_d(z)=G(s)|_{s=(z-1)/T}\) as “exact sampling.”

Worked ZOH of \(G=1/[s(s+2)]\), a type-1 plant. Partial fractions \(G/s=1/[s^2(s+2)]=A/s+B/s^2+C/(s+2)\). \(B=G\cdot s|_{s=0}\) wait: \(1/[s^2(s+2)]= (1/2)/s^2 + (-1/4)/s + (1/4)/(s+2)\). Inverse Laplace: \((1/2)t -1/4 +(1/4)e^{-2t}\). Sample: \(g_s[k]=(1/2)kT-1/4+(1/4)e^{-2kT}\). Then \(G_d(z)=(1-z^{-1})\mathcal{Z}\{g_s\}\). Using the state method is cleaner: \(A=\begin{bmatrix}0&1\\0&-2\end{bmatrix}\), \(B=\begin{bmatrix}0\\1\end{bmatrix}\), \(C=[1,0]\). \(\Phi=e^{AT}\) can be computed by Laplace of \((sI-A)^{-1}\) sampled, or by \(\Phi=\begin{bmatrix}1&(1-e^{-2T})/2\\0&e^{-2T}\end{bmatrix}\). \(\Gamma=\int_0^T e^{A\tau}B\,d\tau\). For \(T=0.2\), \(e^{-2T}=e^{-0.4}=0.6703\), \(\Phi_{12}=(1-0.6703)/2=0.1648\), \(\Phi_{22}=0.6703\). The discrete pole at \(z=1\) (the integrator) remains, and the pole at \(e^{-2T}=0.670\). DC velocity constant: \(K_v\) analog is \(1/2\); discrete \(K_v^d=\lim_{z\to 1}(z-1)G_d(z)/T\) matches in the sense that a unit ramp sequence of slope 1 per second is \(r[k]=kT\), and the same steady lag appears as \(T\to 0\). For finite \(T\), the number is close but not identical; report the discrete \(K_v\) from \(G_d\) if the spec is digital.

Tustin numerical: analog PI \(C=2(s+0.5)/s\), \(T=0.1\), prewarp at \(\omega_d=5\) rad/s if that is crossover. Without prewarp, \(s=20(z-1)/(z+1)\), \(C_d=2[20(z-1)/(z+1)+0.5]/(20(z-1)/(z+1))=2(20(z-1)+0.5(z+1))/(20(z-1))=(40z-40+0.5z+0.5)/(20z-20)=(40.5z-39.5)/(20(z-1))\). Causal form: \(u[k]=u[k-1]+(40.5 e[k]-39.5 e[k-1])/20\). That difference equation is what gets typed into a microcontroller. Forward Euler of the same PI is \(C=2(1+0.5 T/(z-1))=2+1\cdot T/(z-1)\) wait \(2(s+0.5)/s=2+1/s\), forward \(2+T/(z-1)\), \(u[k]=u[k-1]+2(e[k]-e[k-1])+T e[k]\), a different map. At this \(T\) both are stable; at \(T=1\) the analog pole at 0 is still on the circle, but a lead pole might have left the disk under forward Euler.

Sampling zeros: a continuous double integrator plus ZOH has \(G_d(z)=T^2(z+1)/(2(z-1)^2)\), a zero at \(z=-1\). That zero sits on the unit circle; cancelling it with a pole of \(C(z)\) is cancelling a marginally stable mode of the *hold*, a bad idea. Leave it. Fast sampling of higher relative-degree plants pushes sampling zeros toward the negative real axis, sometimes outside the disk (non-minimum-phase discrete zeros). Discrete inverses then cannot be used; analog relative degree already warned you.

Jury table for a cubic \(z^3+a z^2+b z+c\): necessary \(|c|<1\), and a few more bilinear-type inequalities. If the exam is UG intro, they usually stay at quadratics or they ask you to substitute \(z=(1+w)/(1-w)\), clear \((1-w)^n\), and Routh the \(w\)-polynomial. Example: \(z+0.5=0\) is already inside. Example: \(z-1.2=0\) is outside. Example: \(z^2+1=0\) is on the circle (\(z=\pm j\)), marginally oscillatory at 4 samples per cycle — the discrete analog of a \(j\omega\) pair, and the usual place a too-slow sample rate plus a plant resonance lands.

Bandwidth versus \(T\): if analog design had \(\omega_g=8\,\mathrm{rad/s}\), a sample rate of 8 Hz (\(T=0.125\), Nyquist \(25\,\mathrm{rad/s}\)) is barely 3×, poor; 40 Hz is comfortable. Hold phase at \(\omega_g\) is about \(\omega_g T/2=8\times 0.025=0.2\,\mathrm{rad}\approx 11^\circ\) at 40 Hz, versus \(29^\circ\) at 8 Hz. That 29° may have been your entire PM budget. Design analog with extra PM, then discretize, then recompute discrete PM on \(C(e^{j\omega T})G_d(e^{j\omega T})\).

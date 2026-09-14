# BIBO, causality, ROC implications

Bounded-input bounded-output (BIBO) stability and causality are the two system properties that most tightly constrain impulse responses and regions of convergence. Together they decide whether a frequency response \(H(j\omega)\) or \(H(e^{j\Omega})\) exists, whether a real-time implementation is possible, and which inverse Laplace or Z pair is legal. This unit states the tests, proves the LTI equivalences used in UG courses, and works through ROC pictures for rational transforms.

## Concepts

A system is BIBO stable if every input satisfying \(\sup_t |x(t)|\le M_x<\infty\) produces an output with \(\sup_t |y(t)|\le M_y<\infty\) (and likewise in discrete time). The bound \(M_y\) may depend on the system and on \(M_x\) but not on further details of \(x\) beyond the bound. Internal (Lyapunov, asymptotic) stability of a state realization is a different notion: an unstable internal mode that is cancelled and unobservable might still leave an input–output BIBO-stable map, while a hidden unstable mode can ruin a realization even if a cancelled \(H(s)\) looks stable. This unit stays with input–output BIBO unless a cancellation is the point of a problem.

For an LTI system with impulse response \(h\), BIBO stability is equivalent to absolute integrability \(\int_{-\infty}^{\infty}|h(t)|\,dt<\infty\) in CT, and to \(\sum_n |h[n]|<\infty\) in DT. Necessity: the input \(x(t)=\operatorname{sgn}(h(-t))\) (with a convention at zeros) is bounded by 1 and produces \(y(0)=\int|h|\). Sufficiency: \(|y(t)|\le\|h\|_1\|x\|_\infty\). The same argument uses a sum in discrete time. Finite-energy impulse responses are not automatically BIBO (\(h(t)=1/(t\log^2 t)\) style pathologies exist, but UG examples are exponentials and steps). A unit step is not in \(L^1\); an integrator is not BIBO stable. A decaying causal exponential \(e^{-at}u(t)\) with \(a>0\) is BIBO stable. A growing causal exponential is not. An anticausal decaying exponential \(e^{at}u(-t)\) with \(a>0\) is in \(L^1\) and is BIBO stable but noncausal.

Causality: \(y(t_0)\) depends only on \(x(t)\) for \(t\le t_0\). For LTI systems this is \(h(t)=0\) for \(t<0\) (or \(h[n]=0\) for \(n<0\)). A system can be causal and unstable, stable and noncausal, both, or neither. Real-time analog hardware is causal. Smoothing a recorded file with a two-sided exponential is stable and noncausal.

ROC implications, Laplace: a right-sided \(h\) has a right half-plane ROC. Causality is a strict form of right-sidedness (support in \([0,\infty)\)). If \(H(s)\) is rational and the system is causal, the ROC is \(\operatorname{Re}s>\sigma_{\max}\), to the right of the rightmost pole. BIBO stability requires the \(j\omega\) axis in the ROC (so that \(H(j\omega)\) is the CTFT of an \(L^1\) function). Causal plus BIBO therefore forces every pole into \(\operatorname{Re}s<0\). If the system is anticausal (left-sided), stability still needs the axis in the ROC, hence all poles to the right of the axis, \(\operatorname{Re}s>0\), with ROC a left half-plane that still includes \(\operatorname{Re}s=0\). Two-sided stable systems have a strip ROC containing the axis, poles on both sides, and a two-sided \(h\).

ROC implications, Z-transform: right-sided (causal) sequences have ROC \(|z|>r\). Stability needs \(|z|=1\) inside the ROC. Causal plus BIBO: all poles strictly inside the unit circle. Left-sided stable: all poles outside the unit circle, ROC \(|z|<R\) with \(R>1\). Two-sided stable: an annulus containing the unit circle.

Poles on the stability boundary: a simple pole on the \(j\omega\) axis with causal ROC does not give an \(L^1\) impulse response (everlasting sinusoid or step). The frequency response may exist as a distribution (principal value plus impulses) but BIBO fails: a resonant cosine input at the pole frequency produces a ramp envelope. Repeated boundary poles are worse.

Invertibility versus stability: a causal stable \(H(s)\) may have zeros in the right half-plane (non-minimum-phase). The inverse then has those zeros as poles and cannot be both causal and stable. A minimum-phase system has a causal stable inverse. Allpass factors move zeros to mirror poles without changing \(|H(j\omega)|\).

Initial-rest LTI systems described by ODEs with constant coefficients are causal. The same ODE with a different ROC (anticausal impulse response) is another LTI system sharing the same algebra \(H(s)\) but not the same \(h\). Never read causality from the differential equation alone without a rest or ROC condition.

Finite-dimensional discrete FIR filters are always BIBO stable and can be made causal by indexing taps at \(n\ge 0\). Noncausal FIR (negative indices) is stable and used in offline processing. IIR stability is a pole-radius question.

A marginally stable oscillator as a system from a frequency-control input is a different linearization; as a map from additive input to output with \(H(s)=\omega_n/(s^2+\omega_n^2)\), it is not BIBO.

Necessity of \(\|h\|_1<\infty\) is worth proving once in a course because it exhibits the worst-case bounded input: the sign-aligned copy of \(h(-t)\). Any other bounded input gives \(|y|\le\|h\|_1 M_x\), so the test is sharp. If \(\|h\|_1=\infty\), that particular input (or a truncated approximation of it) already drives \(|y(0)|\) arbitrarily large, which is the failure.

Causality does not imply that \(y(t)\) is zero before \(t=0\). It implies that if \(x(t)=0\) for \(t<0\), then \(y(t)=0\) for \(t<0\) when the system is initially at rest. A causal system can output a nonzero value at negative time if the input was nonzero even earlier. Exam language that says “causal so \(y(t)=0\) for \(t<0\)” is assuming a rest, right-sided input.

ROC pictures should be drawn every time. A pole on the imaginary axis with a causal ROC touching the axis from the right does not include the axis (ROC is open). Fourier transforms in ordinary functions require the axis in the ROC, hence strict inequality \(\operatorname{Re}p<0\) for causal BIBO. Poles with negative real parts of \(-10^{-18}\) are theoretically BIBO and practically delicate.

Internal cancellations: \(H(s)=(s-1)/(s-1)(s+2)=1/(s+2)\) after cancellation is causal BIBO as an input–output map if implemented as a first-order filter. If implemented as a cascaded right-half-plane pole and zero in separate blocks, the internal signal can grow until the later block saturates. Input–output BIBO of the ideal math map is not a license to realize unstable cancellations.

Discrete \(\ell^1\) versus \(\ell^2\): \(h[n]=1/(n\log^2 n)\) style examples are not needed; \(h[n]=u[n]/n\) is already not \(\ell^1\) (harmonic series) while decaying. Causal \(1/n\) is a borderline that UG can mention as not BIBO.

Nonlinear systems with memory, such as \(y'=y^2+x\), can explode from small bounded \(x\). BIBO then fails even though a linearized pole might look safe. Linearization BIBO is local.

A finite-dimensional linear state-space model is BIBO stable if all eigenvalues of \(A\) have negative real parts (CT) or magnitude less than one (DT) and there are no hidden issues from the \(B,C,D\) maps producing polynomial factors—equivalently if the transfer-function poles (after cancellation) satisfy the same and the realization is not required. UG signals courses typically stay with \(h\) and \(H\).

Time-varying linear systems do not have a single \(h(\tau)\). BIBO can still be defined. A gain \(y(t)=t x(t)\) is linear, causal, and not BIBO: a bounded \(x=1\) produces a ramp. The LTI \(\|h\|_1\) test does not apply.

## Equations

BIBO \(\iff\) \(\|h\|_1<\infty\) for LTI CT/DT.

Causal LTI: \(h(t)=0\) for \(t<0\).

Rational causal Laplace: \(\mathrm{ROC}=\{\operatorname{Re}s>\sigma_{\max}\}\).

Causal and BIBO, Laplace: all poles satisfy \(\operatorname{Re}p<0\), and the ROC includes \(\operatorname{Re}s=0\).

Causal and BIBO, Z: all poles satisfy \(|p|<1\), ROC includes \(|z|=1\).

Young: \(\|h*x\|_\infty\le\|h\|_1\|x\|_\infty\).

Integrator: \(h(t)=u(t)\), \(\|h\|_1=\infty\), not BIBO. Counterexample input \(x=u(t)\) gives \(y(t)=t u(t)\), unbounded.

## Methods

To test BIBO for a given LTI formula, find \(h\), then integrate or sum \(|h|\). If \(h\) is not given, invert \(H(s)\) or \(H(z)\) using the ROC (or causality assumption), then test \(\|h\|_1\).

To disprove BIBO for a possibly nonlinear system, exhibit one bounded input with unbounded output. To prove BIBO for a nonlinear memoryless map, show that a bound on \(|x|\) implies a bound on \(|f(x)|\) (e.g. \(\arctan\) is BIBO; \(x^2\) is not, because large bounded inputs... wait: \(x^2\) on a bounded input is bounded. \(x^2\) is BIBO! Unbounded growth of \(x^2\) as \(|x|\to\infty\) does not violate BIBO, which only quantifies over already-bounded inputs. The squarer is BIBO and nonlinear. An analog multiplier with one input held at a constant is a gain. This is a standard trick question: BIBO is not “linear and poles on the left.”)

For systems specified by recurrences, take the causal ROC unless told otherwise, invert \(H(z)\), test pole radii.

When poles cancel, test the cancelled \(h\), not the uncancelled algebra, for input–output BIBO. Then mention that a non-minimal realization may still be internally unstable.

To read causality from ROC: right half-plane including infinity (Laplace) or exterior of a circle including infinity (Z) for rational proper transforms. An improper \(H(s)\) with a polynomial part is still causal (contains differentiators) but the differentiator is not BIBO.

Sketch poles, shade ROC, check whether the stability contour (\(j\omega\) axis or unit circle) lies in the shade, and check whether the shade is a causal type.

To disprove causality, it is enough to find one time \(t_0\) and two inputs that coincide up to \(t_0\) but produce different outputs at \(t_0\). An impulse response with a bump at \(t=-1\) is such a witness for LTI systems.

When both properties are asked for a rational \(H\) with a stated ROC, answer in the order: support of \(h\) from ROC (causal?), then contour in ROC (BIBO?). Do not use Routh arrays until the ROC is known to be the causal one.

## Mistakes

Concluding that \(y=x^2\) is not BIBO because it is nonlinear. It is BIBO. \(y=e^{x}\) is BIBO as well: bounded \(x\) gives bounded \(e^{x}\). \(y=\int_{-\infty}^{t}x\) is linear and not BIBO.

Using energy \(\int|h|^2<\infty\) as a BIBO test. \(L^2\) is the wrong space; \(L^1\) is required. A slow \(1/t\) tail can be \(L^2\) off a compact set or not; stick to \(L^1\).

Taking poles with \(\operatorname{Re}p=0\) as BIBO stable for causal systems.

Assuming the ROC of a product \(H_1 H_2\) is the intersection even after pole-zero cancellation that enlarges it.

Reading a two-sided inverse as causal because the problem said “system function \(1/(s-1)\).” That algebra needs an ROC.

Using Jury/Routh tests on the reversed polynomial without stating causality.

Claiming discrete \(|p|=1\) simple poles are BIBO. The causal \(h[n]=e^{j\Omega_0 n}u[n]\) is not \(\ell^1\).

Confusing “bounded for the specific input \(e^{-t}u(t)\)” with BIBO, which quantifies over all bounded inputs.

Treating a differentiator as BIBO because a sinusoid maps to a sinusoid. The input \(\sin(t^2)\) or a series of narrower unit-height triangles can produce arbitrarily large derivative peaks; the distributional differentiator is not BIBO on ordinary bounded continuous functions in the uniform norm (unbounded high-frequency gain). Undergraduate statement: \(H(j\omega)=j\omega\) is unbounded, so not BIBO.

Forgetting Hermitian conjugates: a complex pole \(p\) of a real system comes with \(p^*\); both must lie in the stable region.

# Random variables, expectation, and Gaussian noise

Probability in UG EE is the language of measurement noise, thermal noise, bit errors, and random loads. This unit is discrete and continuous random variables, pdf/pmf/cdf, expectation and variance, independent versus uncorrelated, the Gaussian (normal) law, and the simplest statements about sums (mean adds, variance adds when uncorrelated). Stochastic processes as full time-indexed families, PSDs, and Wiener filtering wait for a communications or DSP elective. Thermal noise as \(4kTR\Delta f\) is a circuit model that uses the variance result of this unit; it is not derived from statistical mechanics here.

The sample space of an experiment is the set of outcomes. Electrical engineers almost never list it. They name a random variable \(X\) (a voltage sample, a noise current, a photon count) and work with its distribution. That is enough for GATE-style and UG coursework if the axioms are not violated: probabilities are nonnegative, the certain event has probability 1, and countable additivity holds for disjoint events.

## Concepts

A discrete random variable takes a countable set of values \(\{x_i\}\) with probability mass function \(p_X(x_i)=P(X=x_i)\), \(\sum_i p_X(x_i)=1\). Examples: number of photons in a bin, number of bit errors in a packet, a fair bit in \(\{0,1\}\). A continuous random variable is described by a probability density \(f_X(x)\) with \(P(a\le X\le b)=\int_a^b f_X(x)\,dx\) and \(\int_{-\infty}^\infty f_X=1\). The density is not a probability: \(f_X(x)\) can exceed 1. The cdf \(F_X(x)=P(X\le x)\) is right-continuous, nondecreasing, from 0 to 1. For a continuous RV, \(f_X=F_X'\). Mixed variables (a discrete atom plus a density) appear as a rectifier output with a pile-up at zero; UG problems usually stay purely discrete or purely continuous.

Expectation \(E[X]=\sum x_i p(x_i)\) or \(\int x f(x)\,dx\) is the centre of mass of the distribution. It need not be a value the RV can take (a fair bit has mean \(1/2\)). Linearity \(E[aX+bY]=aE[X]+bE[Y]\) does **not** require independence. This is the most useful theorem in the subject. Variance \(\operatorname{Var}(X)=E[(X-\mu)^2]=E[X^2]-\mu^2\) is nonnegative. Standard deviation \(\sigma=\sqrt{\operatorname{Var}}\) has the same units as \(X\) (volts, not volts squared). RMS of a zero-mean noise voltage is \(\sigma\).

Independence of \(X\) and \(Y\) means the joint density (or pmf) factors: \(f_{X,Y}=f_X f_Y\). Then \(E[XY]=E[X]E[Y]\) and \(\operatorname{Var}(X+Y)=\operatorname{Var}X+\operatorname{Var}Y\). Uncorrelated means \(E[XY]=E[X]E[Y]\) only (covariance zero). Independent implies uncorrelated; the converse is false in general, but it is true for jointly Gaussian pairs. EE noise calculations often assume independent thermal sources in different resistors; superposition of powers then uses adding variances.

Covariance \(\operatorname{Cov}(X,Y)=E[(X-\mu_X)(Y-\mu_Y)]\). The correlation coefficient \(\rho=\operatorname{Cov}/(\sigma_X\sigma_Y)\) lies in \([-1,1]\). A linear estimator of \(Y\) from \(X\) has error variance \((1-\rho^2)\sigma_Y^2\). That is the mathematics of a one-tap correlator, not a full Wiener filter.

The Gaussian law
\[
f(x)=\frac{1}{\sqrt{2\pi}\sigma}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
\]
is the default model for thermal noise, for quantization noise after a central-limit argument, and for the real or imaginary part of a circular complex baseband noise. It is determined by \(\mu\) and \(\sigma^2\) only. Linear transformations of Gaussians are Gaussian: if \(X\sim\mathcal{N}(\mu,\sigma^2)\), then \(aX+b\sim\mathcal{N}(a\mu,a^2\sigma^2)\). Sums of independent Gaussians are Gaussian with added means and variances. The cdf is written in terms of the error function or the \(Q\)-function
\[
Q(z)=\frac{1}{\sqrt{2\pi}}\int_z^\infty e^{-t^2/2}\,dt=P(Z>z),\qquad Z\sim\mathcal{N}(0,1).
\]
Bit-error probabilities for binary signalling in AWGN are \(Q(\sqrt{2E_b/N_0})\) or a variant; the communications elective uses that formula, this unit supplies \(Q\).

The uniform density on \([a,b]\) models a quantization error under the usual textbook hypothesis, and a random phase \(\Theta\sim\mathrm{Unif}[0,2\pi)\) for a harmonic with unknown origin. A random cosine \(A\cos(\omega t+\Theta)\) with uniform \(\Theta\) has mean zero and average power \(A^2/2\), matching the deterministic RMS of a sinusoid. That calculation is an expectation over phase, not a time average, though ergodicity makes them equal.

Bernoulli, binomial, and Poisson: a bit-flip with probability \(p\); \(n\) independent bits; rare events in a window (photons, particle clicks). Poisson with mean \(\lambda\) has \(P(K=k)=e^{-\lambda}\lambda^k/k!\) and variance \(\lambda\). In a time \(\tau\) at rate \(\nu\), \(\lambda=\nu\tau\). Exponential waiting times (memoryless) are the continuous counterpart of a Poisson process; the memoryless property \(P(T>s+t\mid T>s)=P(T>t)\) is unique to the exponential among continuous positive laws.

Conditioning: \(f_{X|Y}(x|y)=f_{X,Y}(x,y)/f_Y(y)\). Bayes and total probability convert measurements into posterior densities in a first estimation lecture. UG EE often stops at discrete Bayes (a binary hypothesis, a likelihood ratio). The law of total expectation \(E[X]=E[E[X|Y]]\) is how one computes the mean of a rectifier output by first conditioning on the sign, or the mean of a randomly selected Gaussian mixture.

Chebyshev’s inequality \(P(|X-\mu|\ge k\sigma)\le 1/k^2\) is distribution-free and usually loose. The central limit theorem says that a normalised sum of i.i.d. variables with finite variance converges in distribution to \(\mathcal{N}(0,1)\). It is the excuse for modelling the sum of many small independent disturbances as Gaussian. It does not justify a Gaussian model for a single heavy-tailed interferer.

A random process \(N(t)\) in this unit is mentioned only as a family of random variables indexed by time. White noise in engineering is a process with \(E[N(t)]=0\) and autocorrelation \(q\delta(\tau)\), a model, not a measurable function. Passing white noise through a linear filter produces a coloured process whose variance is \(q\int |h|^2\) (Parseval). That one formula connects this unit to Fourier and Laplace.

Complex Gaussian noise: a circularly symmetric complex RV \(Z=X+jY\) with i.i.d. real/imaginary \(\mathcal{N}(0,\sigma^2/2)\) has \(E[|Z|^2]=\sigma^2\) and is the baseband model of bandpass thermal noise. Do not assign variance \(\sigma^2\) to each of \(X\) and \(Y\) and also to \(Z\) without stating which.

## Equations

Axioms (events \(A,B\)): \(P(A)\ge 0\), \(P(\Omega)=1\), \(P(A\cup B)=P(A)+P(B)\) if \(A\cap B=\emptyset\).

Discrete / continuous:

\[
E[g(X)]=\sum g(x_i)p(x_i)\quad\text{or}\quad \int g(x)f_X(x)\,dx.
\]

\[
\operatorname{Var}(X)=E[X^2]-(E[X])^2,\qquad \operatorname{Var}(aX+b)=a^2\operatorname{Var}(X).
\]

Independent sum:

\[
\operatorname{Var}(X+Y)=\operatorname{Var}X+\operatorname{Var}Y\qquad\text{if uncorrelated}.
\]

Gaussian density: as in Concepts. Standardisation: \(Z=(X-\mu)/\sigma\sim\mathcal{N}(0,1)\) if \(X\sim\mathcal{N}(\mu,\sigma^2)\).

\[
P(X>x)=Q\left(\frac{x-\mu}{\sigma}\right),\qquad Q(-z)=1-Q(z).
\]

Uniform \([a,b]\):

\[
f=\frac{1}{b-a},\quad E[X]=\frac{a+b}{2},\quad \operatorname{Var}(X)=\frac{(b-a)^2}{12}.
\]

Bernoulli(\(p\)): \(E[X]=p\), \(\operatorname{Var}(X)=p(1-p)\). Binomial(\(n,p\)): mean \(np\), variance \(np(1-p)\).

Poisson(\(\lambda\)): mean and variance \(\lambda\). Exponential with mean \(1/\lambda\): \(f(t)=\lambda e^{-\lambda t}u(t)\), memoryless.

Covariance matrix of a vector \(\mathbf{X}\): \(R=E[(\mathbf{X}-\mu)(\mathbf{X}-\mu)^T]\) (real case), SPD, used as the quadratic-form weight in a Gaussian pdf
\[
f(\mathbf{x})=\frac{1}{(2\pi)^{n/2}(\det R)^{1/2}}\exp\big(-\tfrac12(\mathbf{x}-\mu)^T R^{-1}(\mathbf{x}-\mu)\big).
\]

## Methods

Always name the RV, its type (discrete/continuous), and the numerical parameters before computing. Draw the density if continuous; check that it integrates to 1. Translate English (“noise voltage exceeds 2 mV”) into \(P(|X|>2\times 10^{-3})\) or a one-sided tail, as the problem states.

To compute \(E[g(X)]\), do not find \(g(X)\)’s density first if the integral \(\int g(x)f_X(x)\,dx\) is easier (LOTUS: law of the unconscious statistician). For \(E[X^2]\) of a Gaussian, use \(E[X^2]=\sigma^2+\mu^2\) rather than integrating \(x^2\) against the bell curve.

Independent thermal resistors: convert each noise source to a Thévenin voltage with variance \(4kTR\Delta f\) in a band \(\Delta f\), refer to the output by a squared transfer gain \(|H|^2\), add variances. Do not add sigmas. Do not add independent noise voltages as if they were DC.

For a threshold problem with Gaussian noise, standardise and look up \(Q(z)\) or \(\operatorname{erf}\). Keep the inequality direction: \(P(X\le x)=\Phi((x-\mu)/\sigma)=1-Q((x-\mu)/\sigma)\).

When two variables are jointly described, write the joint density domain (the rectangle or the triangle) before integrating. Independence can fail even if the support looks like a product; check factorisation on that support.

For a linear transformation \(Y=aX+b\), map the cdf: \(F_Y(y)=F_X((y-b)/a)\) if \(a>0\), and watch the inequality flip if \(a<0\). Then differentiate for the density: \(f_Y(y)=f_X((y-b)/a)/|a|\).

Poisson and binomial: if \(n\) is large, \(p\) small, \(np=\lambda\) fixed, binomial \(\approx\) Poisson. If \(\lambda\) is large, Poisson \(\approx\) Gaussian with mean and variance \(\lambda\). State the approximation when using it.

Monte Carlo in a lab: sample mean estimates \(\mu\), sample variance \(s^2=\frac{1}{n-1}\sum(x_i-\bar{x})^2\) estimates \(\sigma^2\). Standard error of the mean is \(s/\sqrt{n}\). That is why averaging 100 independent noise snapshots reduces rms scatter by 10.

For a thermal-noise voltage referred through a transfer \(H(j\omega)\), the output variance in a band is not \(\sigma_{\mathrm{in}}|H|\) at one frequency unless the input is a line. Integrate \(S_{\mathrm{in}}(\omega)|H(j\omega)|^2\) (one-sided or two-sided, consistently) over the band. White \(4kTR\) times an equivalent noise bandwidth \(B_n=\frac{1}{2\pi|H_0|^2}\int|H|^2 d\omega\) is the shortcut used in analog front-end estimates. State whether \(B_n\) is one-sided hertz.

## Mistakes

Treating a pdf value as a probability: “\(f(0)=2\), so probability 2 at zero.” Continuous points have probability zero; only intervals have positive probability.

Adding standard deviations of independent noises instead of variances. Powers add for uncorrelated zero-mean sources; sigmas do not.

Using \(\sigma\) as the variance. Variance is \(\sigma^2\). Thermal-noise formulae are in V\(^2\)/Hz.

Applying \(Q(z)\) with \(z=(x-\mu)/\sigma^2\) or forgetting to standardise.

Assuming uncorrelated implies independent for uniform or binary variables. Counterexamples are standard; jointly Gaussian is the safe case where they coincide.

Writing \(P(A\ \mathrm{or}\ B)=P(A)+P(B)\) for overlapping events (a voltage both \(>1\) and \(>0\)). Use inclusion-exclusion.

Confusing time average of a particular noise waveform with ensemble expectation. They agree under ergodicity; a single short record of a slow drift does not.

Using two-sided \(\Delta f\) with a one-sided noise density or vice versa, dropping a factor of 2 in \(4kTR\Delta f\).

Taking \(E[1/X]=1/E[X]\). Jensen’s inequality forbids this except in degenerate cases. Resistance measurement ratios need delta-method or a proper density.

Normalising a Gaussian with \(\sigma\) in the exponent as \(2\sigma\) rather than \(2\sigma^2\). The exponent is \(-(x-\mu)^2/(2\sigma^2)\).

Declaring a sample mean of 10 points “equal to the true mean.” Report uncertainty \(s/\sqrt{n}\).

Mixing \(\operatorname{erf}\) and \(Q\) conversions: \(\operatorname{erf}(u)=\frac{2}{\sqrt{\pi}}\int_0^u e^{-t^2}dt\), and \(Q(z)=\tfrac12\operatorname{erfc}(z/\sqrt{2})\). Using \(\operatorname{erf}(z)\) as if it were \(\Phi(z)\) mis-scales the argument by \(\sqrt{2}\).

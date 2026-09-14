# Continuous and discrete convolution

Convolution is the explicit input–output map of every linear time-invariant system that admits an impulse response. In continuous time it is an integral; in discrete time it is a sum. The same algebraic pattern appears in polynomial multiplication, in FIR filtering, and in the overlap of a reversed, shifted copy of one waveform with another. This unit treats convolution as an operation on signals, then as the LTI representation, then as a computational procedure with graphical and algebraic methods.

## Concepts

If \(h\) is the response of a CT LTI system to \(\delta(t)\), linearity and time-invariance expand a general input as a superposition of impulses \(x(\tau)\delta(t-\tau)\,d\tau\) and produce

\[
y(t)=\int_{-\infty}^{\infty}h(\tau)x(t-\tau)\,d\tau=(h*x)(t).
\]

The integrand is the product of \(h\) with a reversed and shifted copy of \(x\), or the other way around: convolution is commutative, \(h*x=x*h\), when the integral exists. Associativity \((a*b)*c=a*(b*c)\) lets cascaded LTI systems multiply impulse responses by convolution. Distributivity over addition matches parallel LTI combination.

The discrete formula \(y[n]=\sum_k h[k]x[n-k]\) is an ordinary sum. No distributions are required. An FIR filter with taps \(h[0],\ldots,h[M]\) is exactly this sum with finite limits. An IIR filter has infinite \(h\) and the sum is infinite; in practice one uses a recurrence, which is a different computational realization of the same LTI map.

Existence: if \(x\) and \(h\) are both absolutely integrable, \(y\) exists everywhere, is bounded, and is absolutely integrable (Young’s inequality at the \(L^1\) endpoint). If one is \(L^1\) and the other is bounded, \(y\) is bounded. Energy signals in \(L^2\) need more care; convolution of two \(L^2\) CT signals need not be \(L^2\), but \(L^1*L^2\subset L^2\). Undergraduate problems usually give piecewise polynomials, exponentials, and steps, for which the integral is elementary on a few intervals.

Graphical convolution tracks the overlap of \(x(\tau)\) and \(h(t-\tau)\) as a function of the slide parameter \(t\). Breakpoints occur when an edge of the reversed, shifted waveform crosses an edge of the other. On each interval between breakpoints the product is a simple function and the integral is evaluated in closed form. The same picture in discrete time is a slide of one stem sequence across the other, multiplying and adding.

Convolution with \(\delta\) is the identity: \(x*\delta=x\). Convolution with \(\delta(t-t_0)\) is a delay of \(t_0\). Convolution with \(u(t)\) is running integration from \(-\infty\) to \(t\). Convolution with a rectangular pulse is a moving average. Differentiation under the integral gives \(\frac{d}{dt}(x*h)=x*h'=x'*h\) when the derivatives exist in the required sense. In discrete time, convolution with \(u[n]\) is the accumulator; convolution with \(\delta[n]-\delta[n-1]\) is a first difference.

Support: if \(x\) lives on \([a,b]\) and \(h\) lives on \([c,d]\), then \(x*h\) lives on \([a+c,b+d]\). Lengths add. For finite sequences of lengths \(L_x\) and \(L_h\), the convolution has length \(L_x+L_h-1\). This is the same rule as the degree of a product of polynomials.

Periodic convolution applies to periodic signals or to one period of a circular wrap. It is not the same as linear convolution. DFT-based multiplication implements circular convolution; linear convolution of finite sequences is recovered by zero-padding so that the circular length is at least \(L_x+L_h-1\).

Eigenfunctions: convolving \(h\) with \(e^{st}\) multiplies by \(H(s)=\int h(t)e^{-st}\,dt\) when the ROC contains \(s\). That is why Fourier and Laplace transforms turn convolution into multiplication. The computational strategy in this unit is to stay in time when both signals are short piecewise functions, and to move to a transform when they are everlasting exponentials or when a property (Parseval, modulation) is the point of a later unit.

Step response and impulse response are related by integration or summation. If \(s(t)\) is the response to \(u(t)\), then \(h(t)=s'(t)\) distributionally, and \(s=h*u\). Measuring a step response in the lab and differentiating it (carefully) estimates \(h\).

A matched filter for a known finite-energy pulse \(p\) in white noise convolves with \(p(-t)\) (or correlates with \(p(t)\)). That is still LTI convolution; the “matching” is the choice of \(h\).

Impulse responses that are sums of delayed exponentials produce piecewise exponential outputs when the input is a pulse: each breakpoint of the input, shifted by each delay in \(h\), starts or stops a term. Superposition lets you convolve each piece separately and add. That is often faster than one giant overlap integral.

Dimension check: if \(x\) is volts and \(h\) is 1/seconds (an impulse response of a voltage-to-voltage system), \(y\) is volts. Discrete convolution of two dimensionless sequences is dimensionless. Mixing a CT integral with a DT sum in the same formula is a category error.

Edge values of piecewise results should be checked from both sides. Convolution of ordinary functions is continuous if one factor is \(L^1\) and the other is bounded with compact support, even if the factors have jumps: the overlap area cannot jump. If your piecewise formula has a discontinuity in \(y\) while \(x\) and \(h\) are ordinary pulses, an endpoint was mis-assigned. Impulses in \(x\) or \(h\) do produce jumps or impulses in \(y\).

The same convolution integral is the output of a transversal analog delay line with tap weights, and of a digital FIR filter. Changing the independent variable from \(t\) to \(n\) does not change the algebra of commutativity and associativity. What changes is existence theory (integrals versus sums) and the meaning of “length.”

When both signals are everlasting two-sided exponentials, the integral may diverge. Transforms with ROCs are then the correct language: convolution in time becomes a product on the intersection of ROCs, and the time-domain integral is recovered only when that product is inverted. Do not blindly write \(\int e^{at}e^{b(t-\tau)}\,d\tau\) over the whole line.

Random signals: the output autocorrelation of an LTI filter is \(h(-t)*h(t)*R_{xx}(t)\) in the wide-sense-stationary setting. That is still convolution, now of correlation functions. UG problems that stay deterministic can ignore this, but it explains why power spectral densities multiply by \(|H|^2\).

## Equations

CT convolution and commutativity:

\[
(x*h)(t)=\int_{-\infty}^{\infty}x(\tau)h(t-\tau)\,d\tau
=\int_{-\infty}^{\infty}h(\tau)x(t-\tau)\,d\tau.
\]

DT convolution:

\[
(x*h)[n]=\sum_{k=-\infty}^{\infty}x[k]h[n-k].
\]

Identity and delay:

\[
x*\delta=x, \qquad (x*\delta(\,\cdot\,-t_0))(t)=x(t-t_0).
\]

Support addition: \(\operatorname{supp}(x*h)\subset\operatorname{supp}(x)+\operatorname{supp}(h)\).

Rectangle of width \(T\) with itself: the convolution is a triangular pulse of width \(2T\) (the Bartlett tent), piecewise quadratic becoming piecewise linear for indicator functions.

Exponential: \((e^{at}u(t))*(e^{bt}u(t))=\frac{e^{at}-e^{bt}}{a-b}u(t)\) for \(a\neq b\), and \(t e^{at}u(t)\) for \(a=b\).

Young’s inequality (statement used qualitatively): \(\|x*h\|_1\le\|x\|_1\|h\|_1\).

Periodic (circular) DT convolution of period \(N\):

\[
(x\circledast h)[n]=\sum_{k=0}^{N-1}x[k]h[(n-k)\bmod N].
\]

Derivative of a convolution:

\[
\frac{d}{dt}(x*h)=x*\frac{dh}{dt}
\]

when \(h\) is absolutely continuous or the derivative is taken in the distribution sense (jumps of \(h\) produce copies of \(x\) at those instants).

## Methods

Algebraic method: write both signals with steps and windows, insert into the integral, and split the \(\tau\)-axis according to the product of the windows. Evaluate each piece.

Graphical method, CT:

1. Draw \(x(\tau)\) and \(h(\tau)\) against \(\tau\).
2. Reverse \(h\) to \(h(-\tau)\), then slide to \(h(t-\tau)\).
3. Mark values of \(t\) where overlap starts, changes shape, and ends.
4. On each interval, write the product and integrate.
5. Assemble the piecewise formula and sketch.

Graphical method, DT: reverse one stem plot, slide it in integer steps, multiply overlapping stems, add. Tabulate \(n\) versus \(y[n]\). For short FIR, a table with shifts of \(x\) weighted by taps is the same algorithm as polynomial multiplication.

Using properties: peel off delays with \(x(t-t_0)*h(t)=y(t-t_0)\); peel off derivatives; reduce a step input to integrating \(h\).

Checking: evaluate \(y\) at a convenient point by a one-dimensional integral; check support; check area \(\int y=\bigl(\int x\bigr)\bigl(\int h\bigr)\) when all three integrals exist; check a known eigenfunction if an exponential input is easy.

Cascades: convolve impulse responses, or multiply system functions later. Do not convolve the outputs of two systems unless one of them is being used as a signal into the next, which is the definition of cascade and already covered by associativity.

For numerical work, discrete convolution is a double loop or a library `convolve`. FFT convolution is an implementation of circular convolution plus padding, not a different mathematical object.

Worked pattern for two causal pulses of heights \(A,B\) and widths \(T_x,T_h\): the output is a trapezoid (or a triangle if the widths are equal). Rise time is the shorter width, plateau length is the absolute difference of widths, fall time is the shorter width again, and the total support is \(T_x+T_h\). The plateau height is \(A B\) times the shorter width. Memorizing that shape catches algebraic mistakes.

If the input is \(\delta'(t)\), convolution differentiates \(h\). If the input is \(u(t)\), convolution integrates \(h\) from \(-\infty\) to \(t\). Those identities convert lab step-response sketches into estimated impulse responses, provided noise is not differentiated blindly.

In discrete time, an accumulator \(h=u[n]\) convolved with a finite sequence is the running sum, which is the discrete analog of a step response. A first difference after that running sum recovers the original finite sequence except possibly at endpoints, illustrating that accumulator and difference are inverses on the appropriate space (sequences with a zero “constant of integration”).

Always write the dummy variable. Students who reuse \(t\) as both the output instant and the integrator variable drop a Jacobian of 1 that happens to be 1, then fail on scaled axes \(x(2\tau)\). Substitute fully: if you reverse and scale, the differential \(d\tau\) stays \(d\tau\).

## Mistakes

Integrating in \(t\) instead of the dummy \(\tau\). The output time is a parameter; the integration variable is the dummy.

Forgetting to reverse one signal. Correlation without reversal is a different operation (\(x(\tau)h(\tau+t)\) up to a sign in the lag).

Using circular convolution when linear convolution was asked, especially after multiplying DFTs of unpadded vectors.

Writing infinite limits but using finite overlap limits inconsistently, or dropping a factor from a unit-height pulse of width not equal to 1.

Claiming \(x*h=xh\) (pointwise product). Transforms swap the two operations; they are not the same in one domain.

Applying convolution to a nonlinear system because “the lab plot looks like a pulse response.” Only LTI systems are characterized by a single \(h\).

Off-by-one in DT support: two sequences on \(0,\ldots,M\) and \(0,\ldots,N\) produce output on \(0,\ldots,M+N\), which is \(M+N+1\) samples, not \(M+N\).

Differentiating a step response as if it were an ordinary function when it contains jumps; the jumps contribute impulses in \(h\).

Sign errors in the delay: \(h(t-\tau)\) versus \(h(\tau-t)\). The second is a reverse of the first. Pick one convention and stay with it.

Treating associativity as a license to rearrange nonlinear blocks. Only LTI blocks freely commute in cascade (and even then, in floating-point or with quantization they do not exactly commute).

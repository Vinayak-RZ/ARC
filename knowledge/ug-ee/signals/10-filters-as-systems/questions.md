## Q1
### Given
\(H(j\omega)=4e^{-j6\omega}\) for all \(\omega\), and \(x(t)=\operatorname{sinc}(t/\pi)\) with \(\operatorname{sinc}\theta=\sin(\pi\theta)/(\pi\theta)\).
### Find
\(y(t)\).
### Solution
The frequency response is exactly distortionless with \(K=4\), \(t_d=6\). Therefore \(y(t)=4x(t-6)=4\operatorname{sinc}\bigl((t-6)/\pi\bigr)\).
### Answer
\(y(t)=4\operatorname{sinc}((t-6)/\pi)\).

## Q2
### Given
An ideal LPF: \(H(j\omega)=e^{-j2\omega}\) for \(|\omega|<5\) and \(0\) otherwise. Input \(x(t)=3+2\cos(3t)+4\cos(8t)\).
### Find
The output \(y(t)\).
### Solution
DC (\(0\)) and the \(3\,\mathrm{rad/s}\) cosine lie inside \(|\omega|<5\). The \(8\,\mathrm{rad/s}\) cosine is rejected. Each kept term is delayed by 2:

\[
y(t)=3+2\cos\bigl(3(t-2)\bigr)=3+2\cos(3t-6).
\]
### Answer
\(y(t)=3+2\cos(3t-6)\).

## Q3
### Given
\(H(j\omega)=\frac{1-j\omega}{1+j\omega}\) (a causal analog allpass up to sign: actually \(\frac{1-s}{1+s}\) at \(s=j\omega\)).
### Find
\(|H(j\omega)|\) and \(t_g(\omega)\).
### Solution
Numerator is the conjugate of the denominator on the \(j\omega\) axis, so \(|H|=1\).

Phase: \(\theta(\omega)=\arg(1-j\omega)-\arg(1+j\omega)=-2\arctan(\omega)\) for \(\omega\) in a principal range starting at \(\theta(0)=0\). Then \(t_g(\omega)=-d\theta/d\omega=2/(1+\omega^2)\).
### Answer
\(|H|=1\), \(t_g(\omega)=2/(1+\omega^2)\).

## Q4
### Given
A length-5 FIR filter with taps \(h[n]=\{1,2,3,2,1\}\) for \(n=0,\ldots,4\).
### Find
Whether the filter has generalized linear phase, the group delay in samples, and \(H(e^{j0})\).
### Solution
Taps are even-symmetric about \(n=2\). Generalized linear phase holds, delay \(t_d=2\) samples, \(\theta(\Omega)=-2\Omega\) on frequencies where the real amplitude is positive.

DC gain: \(H(e^{j0})=\sum h[n]=9\).
### Answer
Yes, linear phase; delay 2 samples; \(H(e^{j0})=9\).

## Q5
### Given
A cosine \(x(t)=\cos(10t)\) through \(H(j\omega)=2e^{-j(\omega/2+\pi/4)}\) (the phase formula used for all \(\omega>0\), and Hermitian extension for \(\omega<0\)).
### Find
\(y(t)\), the phase delay at \(\omega=10\), and the group delay.
### Solution
For \(\omega>0\), \(\theta(\omega)=-\omega/2-\pi/4\). Phase delay \(t_p(10)=-\theta(10)/10=(5+\pi/4)/10=1/2+\pi/40\).

Group delay \(t_g=-d\theta/d\omega=1/2\), constant.

The output is \(2\cos\bigl(10t+\theta(10)\bigr)=2\cos(10t-5-\pi/4)\). Equivalently \(2\cos\bigl(10(t-t_p)\bigr)\).
### Answer
\(y(t)=2\cos(10t-5-\pi/4)\); \(t_p=1/2+\pi/40\); \(t_g=1/2\).

## Q6
### Given
Ideal DT lowpass with \(H(e^{j\Omega})=e^{-j4\Omega}\) for \(|\Omega|<\pi/3\) and \(0\) for \(\pi/3<|\Omega|\le\pi\). Input \(x[n]=\cos(\pi n/6)+\cos(2\pi n/3)\).
### Find
\(y[n]\).
### Solution
\(\Omega=\pi/6<\pi/3\): passed with delay 4, so \(\cos(\pi(n-4)/6)\).

\(\Omega=2\pi/3>\pi/3\): stopped.

Thus \(y[n]=\cos\bigl(\pi(n-4)/6\bigr)\).
### Answer
\(y[n]=\cos(\pi(n-4)/6)\).

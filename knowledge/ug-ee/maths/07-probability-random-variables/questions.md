# Questions — RV, expectation, Gaussian noise intro

## Q1

### Given

A discrete voltage (volts) with \(P(X=0)=0.2\), \(P(X=1)=0.5\), \(P(X=2)=0.3\).

### Find

\(E[X]\), \(E[X^2]\), and \(\operatorname{Var}(X)\).

### Solution

\[
E[X]=0\cdot 0.2+1\cdot 0.5+2\cdot 0.3=1.1.
\]
\[
E[X^2]=0+1\cdot 0.5+4\cdot 0.3=0.5+1.2=1.7.
\]
\[
\operatorname{Var}(X)=1.7-(1.1)^2=1.7-1.21=0.49.
\]
So \(\sigma=0.7\ \mathrm{V}\).

### Answer

\(E[X]=1.1\ \mathrm{V}\), \(E[X^2]=1.7\ \mathrm{V}^2\), \(\operatorname{Var}(X)=0.49\ \mathrm{V}^2\)

## Q2

### Given

\(X\sim\mathcal{N}(\mu=2,\ \sigma^2=16)\) (volts). Threshold \(6\ \mathrm{V}\).

### Find

\(P(X>6)\) as a \(Q\)-function value (do not numerically approximate \(Q\)).

### Solution

Standardise:
\[
P(X>6)=P\left(\frac{X-2}{4}>\frac{6-2}{4}\right)=P(Z>1)=Q(1).
\]

### Answer

\(Q(1)\)

## Q3

### Given

Two uncorrelated zero-mean noise voltages \(N_1,N_2\) with \(\operatorname{Var}(N_1)=9\times 10^{-6}\ \mathrm{V}^2\), \(\operatorname{Var}(N_2)=16\times 10^{-6}\ \mathrm{V}^2\), sum \(N=N_1+N_2\).

### Find

\(\operatorname{Var}(N)\) and the rms of \(N\).

### Solution

Uncorrelated ⇒ variances add:
\[
\operatorname{Var}(N)=(9+16)\times 10^{-6}=25\times 10^{-6}\ \mathrm{V}^2.
\]
\[
N_{\mathrm{rms}}=\sigma_N=5\times 10^{-3}\ \mathrm{V}=5\ \mathrm{mV}.
\]
(If someone added rms values \(3+4=7\ \mathrm{mV}\), that would be wrong.)

### Answer

\(\operatorname{Var}(N)=25\times 10^{-6}\ \mathrm{V}^2\), rms \(=5\ \mathrm{mV}\)

## Q4

### Given

Quantization error modelled as \(E\sim\mathrm{Unif}[-q/2,q/2]\) with \(q=0.02\ \mathrm{V}\).

### Find

\(E[E]\) (mean) and \(\operatorname{Var}(E)\).

### Solution

Uniform on \([-0.01,0.01]\), mean is the midpoint \(0\).
\[
\operatorname{Var}(E)=\frac{(q)^2}{12}=\frac{0.0004}{12}=\frac{1}{30000}=3.333\times 10^{-5}\ \mathrm{V}^2.
\]
RMS \(\approx 5.774\ \mathrm{mV}\).

### Answer

mean \(0\); variance \(q^2/12=3.333\times 10^{-5}\ \mathrm{V}^2\)

## Q5

### Given

Independent bits, each in error with probability \(p=0.01\), packet of \(n=20\) bits. Let \(K\) be the number of errors (binomial).

### Find

\(E[K]\), \(\operatorname{Var}(K)\), and \(P(K=0)\).

### Solution

\[
E[K]=np=0.2,\qquad \operatorname{Var}(K)=np(1-p)=20\cdot 0.01\cdot 0.99=0.198.
\]
\[
P(K=0)=(1-p)^{20}=(0.99)^{20}.
\]
Compute: \((0.99)^{20}=e^{20\ln 0.99}\). \(\ln 0.99\approx -0.010050335\), \(20\times\) that \(\approx -0.2010067\), \(e^{-0.2010067}\approx 0.8179\).

### Answer

\(E[K]=0.2\), \(\operatorname{Var}(K)=0.198\), \(P(K=0)=(0.99)^{20}\approx 0.8179\)

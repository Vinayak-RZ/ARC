## Q1
### Given
\(x[n]=\bigl(\frac13\bigr)^n u[n]\).
### Find
The DTFT \(X(e^{j\Omega})\).
### Solution
Geometric sum \(\sum_{n=0}^{\infty}(e^{-j\Omega}/3)^n=1/(1-\frac13 e^{-j\Omega})\), valid because \(|1/3|<1\).
### Answer
\(X(e^{j\Omega})=1/(1-\frac13 e^{-j\Omega})\).

## Q2
### Given
Length-\(4\) vector \(x=\{1,2,1,0\}\).
### Find
The DFT \(X[k]\) for \(k=0,1,2,3\) using \(X[k]=\sum_{n=0}^{3}x[n]e^{-j2\pi kn/4}\).
### Solution
\(X[0]=1+2+1+0=4\).

\(X[1]=1+2e^{-j\pi/2}+1\cdot e^{-j\pi}+0=1+2(-j)+(-1)= -j2\).

\(X[2]=1+2e^{-j\pi}+e^{-j2\pi}=1+2(-1)+1=0\).

\(X[3]=1+2e^{-j3\pi/2}+e^{-j3\pi}=1+2(j)+(-1)=2j\).

(Hermitian check: \(X[3]=X[1]^*\) since \(x\) is real.)
### Answer
\(X=\{4,-2j,0,2j\}\).

## Q3
### Given
The same \(x=\{1,2,1,0\}\) and \(h=\{1,1,0,0\}\), both length 4.
### Find
Linear convolution of the unpadded sequences (lengths 3 and 2) and 4-point circular convolution.
### Solution
Unpadded linear: \((1+2z^{-1}+z^{-2})(1+z^{-1})=1+3z^{-1}+3z^{-2}+z^{-3}\), i.e. \(\{1,3,3,1\}\).

4-point circular: time-alias the linear result of length 4, which already fits in 4, so circular equals linear: \(\{1,3,3,1\}\). (If linear had length 5, the last sample would wrap onto index 0.)
### Answer
Linear \(\{1,3,3,1\}\); 4-point circular \(\{1,3,3,1\}\).

## Q4
### Given
An \(N=6\) periodic sequence with one period \((4,0,0,0,0,0)\).
### Find
DTFS coefficients \(a_k\) with \(a_k=\frac{1}{N}\sum x[n]e^{-j2\pi kn/N}\), and the DFT of that one period.
### Solution
Only \(n=0\) contributes: \(a_k=4/6=2/3\) for every \(k\). DFT \(X[k]=4\) for every \(k\), and \(X[k]=N a_k=4\).
### Answer
\(a_k=2/3\) for all \(k\); \(X[k]=4\) for all \(k\).

## Q5
### Given
A finite sequence of length \(L=5\), zero elsewhere. Its DTFT is sampled at \(N=4\) frequencies \(\Omega=2\pi k/4\).
### Find
Whether those samples determine the length-5 sequence uniquely, and what time-domain object the 4-point IDFT returns.
### Solution
\(N=4<5\), so frequency sampling is coarser than the length. The IDFT returns the time-aliased wrap \(x[n]+x[n+4]\) on \(n=0,1,2,3\). In particular \(x[0]+x[4]\) occupy the same bin. Not unique.
### Answer
Not unique; IDFT yields \(x_{\mathrm{alias}}[n]=x[n]+x[n+4]\) on \(0\le n\le 3\).

## Q6
### Given
\(x[n]=\{1,-1\}\) at \(n=0,1\), and an 8-point DFT obtained by padding six zeros.
### Find
\(X[0]\), \(X[4]\), and a formula for \(X[k]\).
### Solution
\(X[k]=\sum_{n=0}^{1}x[n]e^{-j2\pi kn/8}=1-e^{-j\pi k/4}\).

\(X[0]=1-1=0\). \(X[4]=1-e^{-j\pi}=1-(-1)=2\).
### Answer
\(X[k]=1-e^{-j\pi k/4}\), \(X[0]=0\), \(X[4]=2\).

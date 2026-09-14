# Questions — DFT/FFT, FIR/IIR design intro

Original pedagogical numbers.

## Q1

### Given

\(N=4\), \(x[n]=\{1,2,3,4\}\) for \(n=0,1,2,3\).

### Find

\(X[0]\) and \(X[2]\).

### Solution

\(X[0]=\sum x[n]=10\). \(X[2]=\sum x[n](-1)^n=1-2+3-4=-2\) because \(W_4^{2n}=e^{-j\pi n}=(-1)^n\).

### Answer

\(X[0]=10\), \(X[2]=-2\).

## Q2

### Given

Radix-2 complex FFT, \(N=64\). Direct DFT costs \(N^2\) complex multiplies.

### Find

FFT complex multiplies \((N/2)\log_2 N\) and the ratio DFT/FFT.

### Solution

\(\log_2 64=6\). FFT muls \(=32\times 6=192\). DFT muls \(=4096\). Ratio \(4096/192=21.33\).

### Answer

\(192\) FFT multiplies; DFT/FFT \(\approx 21.3\).

## Q3

### Given

\(x\) length \(8\), \(h\) length \(5\). Linear convolution is implemented as an \(N\)-point circular convolution via DFT products.

### Find

Minimum \(N\) so the circular result equals the linear convolution, and a convenient radix-2 \(N\).

### Solution

Linear length \(8+5-1=12\). Need \(N\ge 12\). Next power of two is \(16\).

### Answer

\(N\ge 12\); radix-2 choice \(N=16\).

## Q4

### Given

Type-I FIR, \(M=4\) (five taps), ideal lowpass \(\omega_c=\pi/2\), rectangular window.

### Find

\(h[n]=h_d[n]\) for \(n=0,1,2,3,4\).

### Solution

\(\alpha=2\). \(h_d[2]=\omega_c/\pi=1/2\). For \(n\neq 2\), \(h_d[n]=\sin\bigl((\pi/2)(n-2)\bigr)/(\pi(n-2))\). \(n=1\): \(\sin(-\pi/2)/(-\pi)=1/\pi\). \(n=3\): \(1/\pi\). \(n=0\): \(\sin(-\pi)/(-2\pi)=0\). \(n=4\): \(0\). Symmetric: \(\{0,1/\pi,1/2,1/\pi,0\}\).

### Answer

\(h=\{0,\,1/\pi,\,0.5,\,1/\pi,\,0\}\).

## Q5

### Given

Analog \(H(s)=1/(s+1)\), bilinear map with \(T=1\), no extra prewarp (prototype already at \(\Omega=1\)).

### Find

\(H(z)\).

### Solution

\(s=2(z-1)/(z+1)\). \(H(z)=1/\bigl(2(z-1)/(z+1)+1\bigr)=(z+1)/(2z-2+z+1)=(z+1)/(3z-1)\). DC: \(H(1)=2/2=1=H_a(0)\).

### Answer

\(H(z)=(z+1)/(3z-1)\).

## Q6

### Given

Same analog pole \(s=-1\), now prewarp so that analog \(\Omega=1\) maps to digital \(\omega=\pi/2\), still \(T=1\).

### Find

The prewarped analog cutoff \(\Omega_c\) used before bilinear substitution.

### Solution

\(\Omega=(2/T)\tan(\omega T/2)=2\tan(\pi/4)=2\cdot 1=2\). Design analog at \(\Omega_c=2\), i.e. \(H(s)=2/(s+2)\) if matching that cutoff, then bilinear. The question asked only \(\Omega_c\).

### Answer

\(\Omega_c=2\).

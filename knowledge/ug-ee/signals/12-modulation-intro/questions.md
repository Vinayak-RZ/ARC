## Q1
### Given
Baseband \(X(j\omega)=0\) for \(|\omega|>5\), and \(y(t)=x(t)\cos(40 t)\).
### Find
The support of \(Y(j\omega)\) and whether the two sideband clusters overlap.
### Solution
Copies of \(X\) appear around \(\pm 40\), each occupying \((40-5,40+5)\) and \((-40-5,-40+5)\), i.e. \((35,45)\) and \((-45,-35)\). The clusters do not overlap, and they do not reach DC, because \(40>5\).
### Answer
Support in \([-45,-35]\cup[35,45]\) (plus possibly endpoints); no overlap.

## Q2
### Given
\(x(t)=4\cos(8t)\) and carrier \(\cos(100 t)\). DSB-SC \(y=x\cos(100 t)\).
### Find
A trigonometric expansion of \(y(t)\) and the frequencies present.
### Solution
Product-to-sum: \(y(t)=2\bigl[\cos(108 t)+\cos(92 t)\bigr]\). Frequencies \(108\) and \(92\,\mathrm{rad/s}\).
### Answer
\(y(t)=2\cos(108t)+2\cos(92t)\); frequencies \(92\) and \(108\,\mathrm{rad/s}\).

## Q3
### Given
DSB-SC \(y(t)=x(t)\cos(50 t)\) with \(x\) bandlimited to \(10\,\mathrm{rad/s}\). Demodulate by multiplying by \(\cos(50 t+\pi/3)\) then ideal LPF of cutoff \(20\,\mathrm{rad/s}\) and passband gain \(2\).
### Find
The LPF output in terms of \(x(t)\).
### Solution
\(\cos(50t)\cos(50t+\pi/3)=\frac12\cos(\pi/3)+\frac12\cos(100t+\pi/3)=\frac14+\frac12\cos(100t+\pi/3)\).

After \(\times 2\) LPF that kills the \(100\,\mathrm{rad/s}\) copy: \(2\cdot\frac12\cos(\pi/3)\,x(t)=\frac12 x(t)\), because \(\cos(\pi/3)=1/2\).
### Answer
\(\frac12 x(t)\).

## Q4
### Given
Conventional AM \(y(t)=\bigl(5+2\cos(3t)\bigr)\cos(80 t)\).
### Find
The modulation index and whether envelope detection can recover a scaled copy of \(2\cos(3t)\) plus DC.
### Solution
Message amplitude \(2\), carrier amplitude \(A=5\), \(\mu=2/5=0.4<1\). Envelope \(5+2\cos(3t)\) stays between \(3\) and \(7\), always positive. A peak detector followed by DC blocking yields a scaled cosine; with DC kept, the envelope is exactly \(5+2\cos(3t)\).
### Answer
\(\mu=0.4\); yes, envelope is \(5+2\cos(3t)\).

## Q5
### Given
\(x(t)\) real with CTFT \(X(j\omega)\), and \(v(t)=x(t)e^{j 30 t}\).
### Find
\(V(j\omega)\) and \(w(t)=\operatorname{Re}\{v(t)\}\) in terms of a cosine modulation.
### Solution
\(V(j\omega)=X\bigl(j(\omega-30)\bigr)\). Then \(\operatorname{Re}\{x e^{j30 t}\}=x(t)\cos(30 t)\) because \(x\) is real.
### Answer
\(V(j\omega)=X(j(\omega-30))\); \(w(t)=x(t)\cos(30 t)\).

## Q6
### Given
Two messages, each bandlimited to \(4\,\mathrm{kHz}\), to be DSB-SC multiplexed with carriers \(20\,\mathrm{kHz}\) and \(30\,\mathrm{kHz}\) (cosine carriers).
### Find
Whether the sideband clusters overlap, and the minimum extra carrier spacing that would be needed if both carriers were raised while keeping the same difference if overlap occurs—or state the occupied analog bands.
### Solution
Each DSB-SC cluster pair occupies \(\pm(f_c\pm 4)\,\mathrm{kHz}\) about each carrier, i.e. width \(8\,\mathrm{kHz}\) per side of DC for each carrier’s positive-frequency pair.

Positive-frequency bands: \(20\pm 4\to[16,24]\,\mathrm{kHz}\) and \(30\pm 4\to[26,34]\,\mathrm{kHz}\). They do not overlap; a \(2\,\mathrm{kHz}\) gap \((24,26)\) remains. Negative frequencies mirror. No extra spacing is required for ideal brick-wall separation.
### Answer
No overlap; bands \([16,24]\) and \([26,34]\,\mathrm{kHz}\) (and negatives).

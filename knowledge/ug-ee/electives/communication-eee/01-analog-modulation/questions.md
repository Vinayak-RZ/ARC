# Questions — AM, DSB, SSB, FM, SNR intro

Original pedagogical numbers.

## Q1

### Given

Tone AM, \(\mu=0.6\), unmodulated carrier power \(P_c=10\,\mathrm{kW}\).

### Find

Total transmitted power, total sideband power, and efficiency \(\eta\).

### Solution

\(P_t=P_c(1+\mu^2/2)=10(1+0.36/2)=10(1.18)=11.8\,\mathrm{kW}\). \(P_{\mathrm{SB}}=P_c\mu^2/2=1.8\,\mathrm{kW}\). \(\eta=P_{\mathrm{SB}}/P_t=1.8/11.8=0.1525=15.25\%\). Also \(\eta=\mu^2/(\mu^2+2)=0.36/2.36=0.1525\).

### Answer

\(P_t=11.8\,\mathrm{kW}\); \(P_{\mathrm{SB}}=1.8\,\mathrm{kW}\); \(\eta=15.3\%\).

## Q2

### Given

Message bandlimited to \(W=15\,\mathrm{kHz}\). Compare DSB-SC and SSB.

### Find

RF bandwidths.

### Solution

DSB-SC: \(B=2W=30\,\mathrm{kHz}\). SSB: \(B=W=15\,\mathrm{kHz}\).

### Answer

DSB-SC \(30\,\mathrm{kHz}\); SSB \(15\,\mathrm{kHz}\).

## Q3

### Given

FM, peak deviation \(\Delta f=75\,\mathrm{kHz}\), highest message frequency \(f_m=15\,\mathrm{kHz}\).

### Find

\(\beta\) and Carson bandwidth.

### Solution

\(\beta=\Delta f/f_m=75/15=5\). \(B_{\mathrm{C}}=2(\beta+1)f_m=2\times 6\times 15=180\,\mathrm{kHz}\). Equivalently \(2(\Delta f+f_m)=2(90)=180\,\mathrm{kHz}\).

### Answer

\(\beta=5\); \(B_{\mathrm{C}}=180\,\mathrm{kHz}\).

## Q4

### Given

FM \(s=A_c\cos\bigl(2\pi f_c t+2\pi k_f\int m\bigr)\) with \(k_f=5\,\mathrm{kHz/V}\), tone \(m(t)=4\cos(2\pi\cdot 10^3 t)\) volts.

### Find

Peak deviation and \(\beta\).

### Solution

\(A_m=4\,\mathrm{V}\). \(\Delta f=k_f A_m=5\,\mathrm{kHz/V}\times 4\,\mathrm{V}=20\,\mathrm{kHz}\). \(f_m=1\,\mathrm{kHz}\). \(\beta=20/1=20\).

### Answer

\(\Delta f=20\,\mathrm{kHz}\); \(\beta=20\).

## Q5

### Given

AM superhet, \(f_c=1200\,\mathrm{kHz}\), \(f_{IF}=455\,\mathrm{kHz}\), high-side injection.

### Find

LO frequency and image frequency.

### Solution

\(f_{LO}=f_c+f_{IF}=1655\,\mathrm{kHz}\). \(f_{\mathrm{im}}=f_c+2f_{IF}=2110\,\mathrm{kHz}\). (Check: \(|1655-2110|=455\).)

### Answer

\(f_{LO}=1655\,\mathrm{kHz}\); \(f_{\mathrm{im}}=2110\,\mathrm{kHz}\).

## Q6

### Given

Same total sideband power, coherent demodulation, high CNR. Compare output SNR of tone AM at \(\mu=1\) versus DSB-SC.

### Find

The ratio \(\mathrm{SNR}_{\mathrm{AM}}/\mathrm{SNR}_{\mathrm{DSB}}\) when AM’s *total* transmitted power equals DSB-SC’s transmitted power (carrier included in the AM budget).

### Solution

For AM \(\mu=1\), fraction of power in sidebands is \(\eta=1/3\). DSB-SC puts all power in sidebands. Coherent AM (or envelope at high CNR) output SNR is that fraction times the SNR DSB would have with the same *total* \(P_t\). Ratio \(=1/3\).

### Answer

\(\mathrm{SNR}_{\mathrm{AM}}/\mathrm{SNR}_{\mathrm{DSB}}=1/3\).

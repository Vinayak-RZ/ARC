# Questions — Sampling, PCM, line codes, ISI intro

Original pedagogical numbers.

## Q1

### Given

Speech treated as bandlimited to \(W=3.4\,\mathrm{kHz}\). PCM uses \(f_s=8\,\mathrm{kHz}\), \(n=8\) bits/sample.

### Find

Whether \(f_s\) meets Nyquist, and the bit rate of one channel.

### Solution

Nyquist rate \(2W=6.8\,\mathrm{kHz}\). \(8>6.8\), yes (margin for the anti-alias transition). \(R_b=n f_s=8\times 8000=64\,\mathrm{kbit/s}\).

### Answer

Yes; \(64\,\mathrm{kbit/s}\).

## Q2

### Given

Uniform PCM, \(n=7\) bits, full-scale sine, rounding model.

### Find

Number of levels and SQNR in dB.

### Solution

\(L=2^7=128\). SQNR \(\approx 6.02\times 7+1.76=43.9\,\mathrm{dB}\).

### Answer

\(128\) levels; \(\approx 43.9\,\mathrm{dB}\).

## Q3

### Given

Binary raised-cosine pulses, \(R_b=1\,\mathrm{Mbit/s}\), roll-off \(\alpha=0.5\).

### Find

Occupied RF-baseband bandwidth \(B=(1+\alpha)R_b/2\).

### Solution

\(B=(1.5)\times 10^6/2=0.75\,\mathrm{MHz}\). Nyquist minimum would be \(0.50\,\mathrm{MHz}\) at \(\alpha=0\).

### Answer

\(0.75\,\mathrm{MHz}\).

## Q4

### Given

Bits \(1\,0\,1\,1\,0\) to be AMI-encoded, first \(1\) mapped to \(+A\).

### Find

The amplitude sequence.

### Solution

Ones alternate; zeros are 0. Sequence: \(+A,\ 0,\ -A,\ +A,\ 0\).

### Answer

\(+A,\ 0,\ -A,\ +A,\ 0\).

## Q5

### Given

Four identical 12-bit loggers sampled at \(1\,\mathrm{kHz}\), TDM with no framing overhead.

### Find

Aggregate bit rate.

### Solution

\(R=4\times 12\times 1000=48\,\mathrm{kbit/s}\).

### Answer

\(48\,\mathrm{kbit/s}\).

## Q6

### Given

A channel of usable bandwidth \(4\,\mathrm{kHz}\) must carry binary raised-cosine pulses. Maximum \(\alpha=1\).

### Find

The maximum bit rate for zero-ISI Nyquist pulses at \(\alpha=1\), and at \(\alpha=0\).

### Solution

\(B=(1+\alpha)R_b/2\Rightarrow R_b=2B/(1+\alpha)\). At \(\alpha=1\), \(R_b=2\cdot 4\,\mathrm{kHz}/2=4\,\mathrm{kbit/s}\). At \(\alpha=0\), \(R_b=2B=8\,\mathrm{kbit/s}\).

### Answer

\(4\,\mathrm{kbit/s}\) at \(\alpha=1\); \(8\,\mathrm{kbit/s}\) at \(\alpha=0\).

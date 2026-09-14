# Worked questions — DAC, ADC, TTL/CMOS

## Q1
### Given
8-bit unipolar DAC, \(V_{\mathrm{ref}}=4.096\,\mathrm{V}\), \(V_{\mathrm{LSB}}=V_{\mathrm{ref}}/256\). Input code \(1100\,1010_2\).
### Find
\(V_{\mathrm{LSB}}\) and \(V_{\mathrm{out}}\).
### Solution
\(V_{\mathrm{LSB}}=4.096/256=16.0\,\mathrm{mV}\). \(D=202\). \(V_{\mathrm{out}}=202\times 16.0\,\mathrm{mV}=3.232\,\mathrm{V}\).
### Answer
\(V_{\mathrm{LSB}}=16.0\,\mathrm{mV}\), \(V_{\mathrm{out}}=3.232\,\mathrm{V}\)

## Q2
### Given
10-bit ADC, \(V_{\mathrm{ref}}=5.00\,\mathrm{V}\), \(V_{\mathrm{LSB}}=5/1024\), rounding to nearest code (mid-riser at \(n+0.5\) LSB). \(V_{in}=1.500\,\mathrm{V}\).
### Find
The decimal code and its 10-bit binary.
### Solution
\(V_{\mathrm{LSB}}=4.883\,\mathrm{mV}\). \(1.500/0.004883=307.2\). Nearest code 307. \(307=256+51=256+32+16+2+1=0100110011_2\).
### Answer
Code 307 \(=0100110011_2\)

## Q3
### Given
Ideal 12-bit ADC, full-scale sine.
### Find
Quantisation SNR in dB from \(6.02N+1.76\).
### Solution
\(6.02\times 12+1.76=74.00\,\mathrm{dB}\).
### Answer
\(74.0\,\mathrm{dB}\)

## Q4
### Given
Standard TTL: \(V_{OH,\min}=2.4\,\mathrm{V}\), \(V_{IH,\min}=2.0\,\mathrm{V}\), \(V_{OL,\max}=0.4\,\mathrm{V}\), \(V_{IL,\max}=0.8\,\mathrm{V}\). \(I_{OL}=16\,\mathrm{mA}\), \(I_{IL}=1.6\,\mathrm{mA}\), \(I_{OH}=400\,\mu\mathrm{A}\), \(I_{IH}=40\,\mu\mathrm{A}\).
### Find
\(NM_H\), \(NM_L\), and fan-out (the limiting of the high and low calculations).
### Solution
\(NM_H=2.4-2.0=0.4\,\mathrm{V}\), \(NM_L=0.8-0.4=0.4\,\mathrm{V}\). \(N_L=16/1.6=10\), \(N_H=400/40=10\). Fan-out 10. (The 74-family "16" often quoted is for a different \(I_{OL}\) grade; here the given currents yield 10.)
### Answer
\(NM_H=NM_L=0.4\,\mathrm{V}\), fan-out \(=10\)

## Q5
### Given
74LS driving 74HC at \(V_{CC}=5.0\,\mathrm{V}\). 74LS \(V_{OH,\min}=2.4\,\mathrm{V}\). 74HC \(V_{IH,\min}=3.5\,\mathrm{V}\).
### Find
Whether the high-level voltage contract is met, and name one legal fix.
### Solution
\(2.4<3.5\), so the high-level voltage contract is not met. A legal fix is to receive the signal with 74HCT (TTL-level CMOS inputs). Alternatives: a dedicated translator, or an open-collector LS output with a pull-up to 5 V.
### Answer
Not met; use 74HCT (or a level translator / pull-up on open-collector)

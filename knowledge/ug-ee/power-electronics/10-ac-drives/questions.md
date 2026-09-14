# Worked questions — AC drives

## Q1
### Given
A 415 V, 50 Hz, 4-pole induction motor is run open-loop V/f at 40 Hz with voltage scaled from rated (no boost).
### Find
Applied line voltage and synchronous speed.
### Solution
\(V=415\times 40/50=332\,\mathrm{V}\). \(n_s=120\times 40/4=1200\,\mathrm{r/min}\).
### Answer
\(V=332\,\mathrm{V}\), \(n_s=1200\,\mathrm{r/min}\)

## Q2
### Given
Diode-rectifier DC bus from 400 V AC three-phase, \(V_{dc}=1.35\times 400=540\,\mathrm{V}\). Linear SPWM inverter.
### Find
Maximum RMS line voltage in linear SPWM, and the highest V/f-scaled frequency for a 400 V, 50 Hz motor if voltage must stay in linear SPWM.
### Solution
\(V_{LL,\max}=0.612\times 540=330\,\mathrm{V}\). That is \(330/400=0.825\) of rated voltage, so \(f_{\max}=0.825\times 50=41.3\,\mathrm{Hz}\) if flux is held and overmodulation is forbidden. (In practice one would use SVPWM or overmodulate to reach 50 Hz.)
### Answer
\(330\,\mathrm{V}\) max; \(f_{\max}=41.3\,\mathrm{Hz}\) at constant flux without overmodulation

## Q3
### Given
Low-frequency boost: \(V_0=18\,\mathrm{V}\), rated 415 V at 50 Hz.
### Find
Voltage command at 5 Hz.
### Solution
\(k=(415-18)/50=7.94\,\mathrm{V/Hz}\). \(V=18+7.94\times 5=57.7\,\mathrm{V}\). (Pure V/f without boost would be \(41.5\,\mathrm{V}\).)
### Answer
\(V=57.7\,\mathrm{V}\)

## Q4
### Given
A CSI drive, \(I_{dc}=80\,\mathrm{A}\). Use \(I_{1,\mathrm{pk}}=(2\sqrt{3}/\pi)I_{dc}\).
### Find
RMS fundamental motor current.
### Solution
\(I_{1,\mathrm{pk}}=88.2\,\mathrm{A}\). \(I_{1,\mathrm{rms}}=62.4\,\mathrm{A}\).
### Answer
\(I_{1,\mathrm{rms}}=62.4\,\mathrm{A}\)

## Q5
### Given
Cycloconverter rule of thumb \(f_o\le f_i/3\), \(f_i=50\,\mathrm{Hz}\). A 20-pole synchronous mill motor.
### Find
Maximum output frequency and the corresponding synchronous speed.
### Solution
\(f_o\le 16.7\,\mathrm{Hz}\). \(n_s=120\times 16.7/20=100\,\mathrm{r/min}\).
### Answer
\(f_o\le 16.7\,\mathrm{Hz}\), \(n_s\le 100\,\mathrm{r/min}\)

## Q6
### Given
A V/f VSI uses a DC-link brake chopper. Bus \(V_{dc}=650\,\mathrm{V}\) (regulation threshold), brake resistor \(R_b=15\,\Omega\).
### Find
Chopper current and dissipation when the brake switch is fully on.
### Solution
\(I=650/15=43.3\,\mathrm{A}\). \(P=650^2/15=28.2\,\mathrm{kW}\). Duty of the brake chopper would then modulate this to match regenerated power.
### Answer
\(I=43.3\,\mathrm{A}\), \(P=28.2\,\mathrm{kW}\) (at \(D=1\))

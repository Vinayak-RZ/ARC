# Questions — Digital/analog IO, interlocks (study-level)

Original pedagogical numbers.

## Q1

### Given

A temperature transmitter, 4–20 mA \(\leftrightarrow\) \(0\)–\(100^\circ\mathrm{C}\). Loop current \(I=12\,\mathrm{mA}\).

### Find

Indicated temperature.

### Solution

\(x=0+(12-4)/16\times 100=50^\circ\mathrm{C}\).

### Answer

\(50^\circ\mathrm{C}\).

## Q2

### Given

Same span. Wanted setpoint \(75^\circ\mathrm{C}\) as a 4–20 mA output.

### Find

The current.

### Solution

\(I=4+16\times(75-0)/100=4+12=16\,\mathrm{mA}\).

### Answer

\(16\,\mathrm{mA}\).

## Q3

### Given

0–10 V analog input, 10-bit ADC spanning exactly 0–10 V, process \(0\)–\(500\,\mathrm{kPa}\).

### Find

Voltage LSB and pressure LSB.

### Solution

\(\Delta V=10/1024=9.766\,\mathrm{mV}\). \(\Delta P=500/1024=0.488\,\mathrm{kPa}\).

### Answer

\(9.77\,\mathrm{mV}\); \(0.488\,\mathrm{kPa}\).

## Q4

### Given

Mechanical bounce up to \(18\,\mathrm{ms}\), PLC scan \(5\,\mathrm{ms}\). Debounce by requiring \(N\) consecutive true scans.

### Find

The smallest \(N\) with \(N T_s\ge 18\,\mathrm{ms}\).

### Solution

\(N\times 5\ge 18\Rightarrow N\ge 3.6\Rightarrow N=4\). Debounce time \(20\,\mathrm{ms}\).

### Answer

\(N=4\) (\(20\,\mathrm{ms}\)).

## Q5

### Given

4–20 mA loop. Measured \(I=1.2\,\mathrm{mA}\). Process range \(0\)–\(10\,\mathrm{bar}\).

### Find

Whether to report a process value, and why.

### Solution

\(1.2\,\mathrm{mA}<3.6\,\mathrm{mA}\) (NE43 underscale / break). This is a fault (open loop), not \(x=0\) bar. Do not scale as if \(I=4\,\mathrm{mA}\).

### Answer

Fault (broken loop); do not report \(0\,\mathrm{bar}\).

## Q6

### Given

Study-level e-stop: a mushroom switch must stop a motor if the operator hits it *or* if the switch wire falls off the terminal.

### Find

Whether the field contact should be NO or NC in the energized-to-run 24 V loop, and the Boolean for `OK` in the ladder input image if `ES` is 1 when the loop is closed.

### Solution

Use an NC mushroom in series with the coil supply (or safety-relay input) so a hit *or* a broken wire opens the loop. PLC input `ES=1` means loop closed. `OK = ES`. Motor permissives include `OK`. An NO e-stop would fail silent on a broken wire.

### Answer

NC field contact, fail-safe open on break; `OK=\mathrm{ES}` with \(\mathrm{ES}=1\) when healthy.

# Questions — Scan cycle, ladder, timers/counters

Original pedagogical numbers.

## Q1

### Given

Scan time \(T_s=8\,\mathrm{ms}\), TON preset \(\mathrm{PRE}=1.000\,\mathrm{s}\), IN becomes true at the start of a scan. Time base is finer than the scan.

### Find

Number of scans until DN can be true, and a bound on the actual delay.

### Solution

\(N=\mathrm{ceil}(1.000/0.008)=125\). DN is evaluated after ACC reaches PRE, so the done flag is seen in the output image at \(t\in[1.000,\ 1.008]\,\mathrm{s}\) after IN.

### Answer

\(125\) scans; delay in \([1.000,1.008]\,\mathrm{s}\).

## Q2

### Given

Start/stop seal-in: `Run = (Start OR Run) AND NOT Stop`. At scan \(k\), Start=1, Stop=0, Run=0.

### Find

Run at the end of scans \(k\) and \(k+1\) if Start returns to 0 for scan \(k+1\) and Stop stays 0.

### Solution

Scan \(k\): \((1\lor 0)\land \lnot 0=1\), so Run becomes 1 and is written to the output image. Scan \(k+1\): Start=0, Run image is already 1, \((0\lor 1)\land 1=1\). Run stays 1 (seal-in).

### Answer

\(\mathrm{Run}=1\) on both scans.

## Q3

### Given

CTU, PRE=10, ACC=9, DN=0. CU has a clean rising edge this scan. Next scan CU stays 1 (no extra edge).

### Find

ACC and DN after this scan and after the next scan.

### Solution

Rising edge: ACC=10, DN=1. Next scan: no rising edge, ACC stays 10, DN stays 1 until RES.

### Answer

This scan ACC=10, DN=1; next scan unchanged.

## Q4

### Given

A conveyor photoeye is true for \(200\,\mathrm{ms}\) each box. Scan \(10\,\mathrm{ms}\). A CTU is driven directly from the photoeye *level* (not a one-shot).

### Find

Approximate counts added per box, and the fix.

### Solution

Level true for \(200/10=20\) scans \(\Rightarrow\) about 20 increments per box if the firmware counts every scan the rung is true. (Edge-triggered CTU would count 1; a non-edge “add while true” instruction would add 20.) Fix: rising-edge one-shot (or CTU that specifies rising CU) plus optional debounce TON.

### Answer

\(\sim 20\) counts/box if level-counted; use a rising one-shot.

## Q5

### Given

Motor starter should stay energized 5 s after Stop goes true (fan cool-down). Run is already off. Choose TON, TOF, or RTO.

### Find

Which timer and what IN/DN connection in one sentence.

### Solution

TOF: IN follows “motor was running” (or NOT Stop, depending on the desired trigger). DN (or the TOF output) keeps the fan coil true for PRE=5 s after IN falls.

### Answer

TOF, PRE \(=5\,\mathrm{s}\), fan coil on TOF.DN.

## Q6

### Given

Watchdog \(T_{\mathrm{WD}}=100\,\mathrm{ms}\). A program path sometimes takes \(T_s=120\,\mathrm{ms}\).

### Find

The CPU’s expected safety action at UG study level.

### Solution

Scan exceeds watchdog \(\Rightarrow\) fault, user program stops, outputs go to the configured fail-safe (typically de-energize). Lengthen the watchdog only after measuring a legitimate scan; better: split the program or fix the loop.

### Answer

Watchdog fault; outputs to fail-safe (usually de-energized).

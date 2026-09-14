# Questions — 8085 architecture, timing, interrupts

Original pedagogical numbers.

## Q1

### Given

8085 crystal \(6\,\mathrm{MHz}\) (internal clock \(3\,\mathrm{MHz}\)). Instruction `MOV A,M` uses one opcode-fetch machine cycle of \(4\) T-states and one memory-read machine cycle of \(3\) T-states.

### Find

T-state duration and the instruction execution time.

### Solution

\(f_{\mathrm{clk}}=3\times 10^6\,\mathrm{Hz}\). \(T=1/f_{\mathrm{clk}}=333.3\,\mathrm{ns}\). \(N_T=4+3=7\). \(t=7T=7/3\times 10^{-6}\,\mathrm{s}=2.333\,\mu\mathrm{s}\).

### Answer

\(T=333\,\mathrm{ns}\); \(t_{\mathrm{ins}}=2.33\,\mu\mathrm{s}\).

## Q2

### Given

`LDA 2050H` on the same \(3\,\mathrm{MHz}\) 8085: machine cycles opcode fetch (\(4\) T), memory read of low address (\(3\) T), memory read of high address (\(3\) T), memory read of data (\(3\) T).

### Find

Number of machine cycles, total T-states, and execution time.

### Solution

Four machine cycles. \(N_T=4+3+3+3=13\). \(t=13/(3\times 10^6)=4.333\,\mu\mathrm{s}\).

### Answer

\(4\) machine cycles, \(13\) T, \(4.33\,\mu\mathrm{s}\).

## Q3

### Given

Hardware interrupts TRAP, RST 7.5, RST 6.5, RST 5.5.

### Find

Vector addresses and, for a simultaneous arrival of RST 7.5 and RST 5.5 with both unmasked and IE=1, which service starts first.

### Solution

TRAP \(\to 0024\mathrm{H}\). RST 7.5 \(\to 8\times 7.5=60=003C\mathrm{H}\). RST 6.5 \(\to 0034\mathrm{H}\). RST 5.5 \(\to 002C\mathrm{H}\). Priority: TRAP, then 7.5, then 6.5, then 5.5, then INTR. Between 7.5 and 5.5, RST 7.5 wins.

### Answer

Vectors \(0024\mathrm{H}\), \(003C\mathrm{H}\), \(0034\mathrm{H}\), \(002C\mathrm{H}\); RST 7.5 is serviced first.

## Q4

### Given

SP \(=2000\mathrm{H}\), \(B=3A\mathrm{H}\), \(C=5C\mathrm{H}\). Execute `PUSH B`.

### Find

New SP and the bytes stored at \(1FFF\mathrm{H}\) and \(1FFE\mathrm{H}\).

### Solution

PUSH BC stores high byte B at \(SP-1\) and low byte C at \(SP-2\), then \(SP\leftarrow SP-2\). \([1FFF\mathrm{H}]=3A\mathrm{H}\), \([1FFE\mathrm{H}]=5C\mathrm{H}\), \(SP=1FFE\mathrm{H}\).

### Answer

\(SP=1FFE\mathrm{H}\); \([1FFF\mathrm{H}]=3A\mathrm{H}\); \([1FFE\mathrm{H}]=5C\mathrm{H}\).

## Q5

### Given

Need to unmask RST 6.5, mask RST 7.5 and RST 5.5, update the mask latch, and leave SOD unused. Bits: \(b_0=\)M5.5, \(b_1=\)M6.5, \(b_2=\)M7.5, \(b_3=\)MSE, \(b_4=\)R7.5, \(b_6=\)SOD, \(b_7=\)SDE. Mask bit \(1\) means masked.

### Find

Accumulator value to load before `SIM`.

### Solution

MSE must be \(1\). M5.5 \(=1\), M6.5 \(=0\), M7.5 \(=1\). R7.5 \(=0\), SDE \(=0\), SOD \(=0\), unused \(b_5=0\). \(A=0000\,1101_2=0D\mathrm{H}\).

### Answer

\(A=0D\mathrm{H}\) then `SIM`.

## Q6

### Given

An INTR device jams the opcode for `RST 5` (\(EF\mathrm{H}\) is RST 5? RST 5 opcode is \(EF\mathrm{H}\): RST \(n\) opcode \(C7+8n\). RST 5: \(C7+40=EF\mathrm{H}\)) during INTA.

### Find

The ISR start address.

### Solution

`RST 5` vectors to \(8\times 5=40=0028\mathrm{H}\). (This is not RST 5.5, whose vector is \(002C\mathrm{H}\).)

### Answer

\(0028\mathrm{H}\).

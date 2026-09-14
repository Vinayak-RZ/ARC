# Questions — Memory/IO interfacing, 8051 intro

Original pedagogical numbers.

## Q1

### Given

An 8 KiB EPROM must occupy \(0000\mathrm{H}\)–\(1FFF\mathrm{H}\) on an 8085. CS is active low.

### Find

The logic of \(\overline{\mathrm{CS}}\) in terms of A15, A14, A13 (full decoding of the 8 KiB block).

### Solution

8 KiB \(=2^{13}\) uses A12–A0 on the chip. The block \(0000\)–\(1FFF\) has A15=A14=A13=0. Active-low CS: \(\overline{\mathrm{CS}}=\overline{\overline{A15}\,\overline{A14}\,\overline{A13}}=A15+A14+A13\) (OR of the three high bits). Equivalently \(\overline{\mathrm{CS}}\) is the NAND of three inverted highs, i.e. low only when A15=A14=A13=0.

### Answer

\(\overline{\mathrm{CS}}=A15\lor A14\lor A13\) (low only on \(0000\mathrm{H}\)–\(1FFF\mathrm{H}\)).

## Q2

### Given

8255 Mode 0: Port A output, Port B input, Port C (both nybbles) output.

### Find

The I/O-mode control word.

### Solution

Bit7=1. Group A mode 00, A direction 0 (out), CU 0 (out), Group B mode 0, B direction 1 (in), CL 0 (out). \(\mathrm{CW}=1000\,0010_2=82\mathrm{H}\).

### Answer

\(82\mathrm{H}\).

## Q3

### Given

Classic 8051, \(f_{\mathrm{osc}}=12\,\mathrm{MHz}\), Timer 0 Mode 1, delay \(1.0\,\mathrm{ms}\) (ignore ISR overhead).

### Find

\(T_{\mathrm{mc}}\), count \(N\), and TH0:TL0 load value.

### Solution

\(T_{\mathrm{mc}}=12/12\times 10^{-6}=1\,\mu\mathrm{s}\). \(N=1000\). Load \(65536-1000=64536=FC18\mathrm{H}\). TH0 \(=FC\mathrm{H}\), TL0 \(=18\mathrm{H}\).

### Answer

\(T_{\mathrm{mc}}=1\,\mu\mathrm{s}\); load \(FC18\mathrm{H}\).

## Q4

### Given

UART Mode 1, Timer 1 Mode 2, SMOD=0, \(f_{\mathrm{osc}}=11.0592\,\mathrm{MHz}\), baud \(9600\).

### Find

TH1.

### Solution

\(\mathrm{TH1}=256-f_{\mathrm{osc}}/(384\cdot\mathrm{baud})=256-11.0592\times 10^6/(384\times 9600)\). Denominator \(3.6864\times 10^6\). Quotient \(3.000\). TH1 \(=256-3=253=FD\mathrm{H}\).

### Answer

\(\mathrm{TH1}=FD\mathrm{H}\).

## Q5

### Given

8255 mapped at isolated I/O ports \(20\mathrm{H}\)–\(23\mathrm{H}\) (A, B, C, control). Need to set Port C bit 3 using BSR.

### Find

Port address of the control register and the BSR control byte.

### Solution

Control register is \(23\mathrm{H}\). BSR: bit7=0, bit-select \(011\) for bit 3, S=1. \(\mathrm{CW}=0000\,0111_2=07\mathrm{H}\). OUT \(23\mathrm{H}\) of \(07\mathrm{H}\) sets PC3.

### Answer

Address \(23\mathrm{H}\); BSR byte \(07\mathrm{H}\).

## Q6

### Given

8051 PSW with RS1=1, RS0=0. Instruction `MOV A,R3` in that bank.

### Find

The internal-RAM address of R3.

### Solution

Bank \(=2\cdot\mathrm{RS1}+\mathrm{RS0}=2\). Bank 2 occupies \(10\mathrm{H}\)–\(17\mathrm{H}\). R3 is at \(10\mathrm{H}+3=13\mathrm{H}\).

### Answer

\(13\mathrm{H}\).

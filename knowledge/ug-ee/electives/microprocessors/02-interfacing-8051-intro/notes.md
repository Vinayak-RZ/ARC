# Memory and I/O interfacing, and 8051 introduction

An 8085 CPU is useless until ROM, RAM and peripherals share the multiplexed bus with correctly timed chip-selects. This unit is address decoding, isolated versus memory-mapped I/O, the 8255 PPI at Mode 0, a sketch of 8253/54 and 8259, then the MCS-51 (8051) programmer’s model that most EEE electives use as the microcontroller follow-on. It is not an ARM Cortex-M HAL, a PCB SI course, or a live plant PLC.

## Concepts

The 8085 presents a 16-bit address, an 8-bit data bus (after the ALE latch), RD, WR, IO/M, and READY. Memory chips enable when CS is true and OE/WE follow RD/WR. The designer’s job is to generate CS from A15–A0 (usually just the high bits) so that each device occupies a unique range.

A decoder (74LS138 for 3-to-8, or a few gates) partitions the 64 KiB space. Example: ROM \(0000\mathrm{H}\)–\(1FFF\mathrm{H}\) (8 KiB) needs A15=A14=A13=0 and a 13-bit chip (A12–A0). RAM \(2000\mathrm{H}\)–\(27FF\mathrm{H}\) (2 KiB) needs A15–A11 encoding \(00100\) and A10–A0 into the RAM. Partial decoding omits some address lines: the same RAM then appears as aliases every \(2^{k}\) where \(k\) unused bits. Examiners love aliases: “the RAM also responds at \(A000\mathrm{H}\)” means A15 was left out of CS.

Isolated I/O: IN/OUT put the 8-bit port address on both halves of the address bus, IO/M=1, RD or WR. A device CS is qualified with IO/M. Two hundred fifty-six port addresses. Memory-mapped I/O: the device CS is qualified with IO/M=0 (or the designer ignores IO/M and uses a memory hole). Any memory instruction then talks to the device; address space is consumed.

**8255 PPI.** Three 8-bit ports A, B, C (C split as CU and CL nybbles) plus a control register. Four addresses: base, base+1, base+2, base+3 for A, B, C, control if A1 A0 decode the register. Mode 0 is simple I/O: each of A, B, CU, CL independently input or output, no handshaking. Mode 1 strobed I/O, Mode 2 bidirectional on A — UG numericals are almost always Mode 0. Control word bit 7=1 selects I/O mode (bit 7=0 is BSR, bit-set/reset of a C pin). Bits 6–5 group-A mode, bit 4 Port A direction (1=input), bit 3 CU, bit 2 group-B mode, bit 1 Port B, bit 0 CL. Example: A out, B in, C out, Mode 0 \(\Rightarrow 1000\,0010_2=82\mathrm{H}\). BSR: control \(0xxx xbbb\) with the bit number in 3–1 and the value in bit 0.

**8253/54 PIT.** Three 16-bit counters. Mode 3 square wave is the usual baud or scan clock. OUT of a counter can clock the next. UG needs “load LSW then MSW” and the idea that a 1.5 MHz PCLK and a divisor of 1500 give 1 kHz, not the full Intel mode table.

**8259 PIC.** Cascades IRQs into INTR and supplies the RST or call vector during INTA. Mentioned so the INTR story in unit 01 has a chip; programming OCW/ICW is usually beyond a first EEE elective.

Wait states: if RAM t_ACC is 450 ns and T is 333 ns, the CPU may need READY stretched so T2 lasts another T. Compute \(t_{\mathrm{acc}}\) against the data-setup window in T3; this is a lab numerical, not a JEDEC timing-closure job.

The **8051** (MCS-51) is an 8-bit microcontroller with *on-chip* ROM/RAM, four ports, two 16-bit timers, a UART, and a 5-source interrupt controller. Harvard-ish: separate code (up to 64 KiB external via PSEN) and data (internal 128 or 256 bytes plus 64 KiB external via RD/WR). The CPU uses a 12-clock machine cycle on the classic part: at \(12\,\mathrm{MHz}\), one machine cycle is \(1\,\mu\mathrm{s}\). (Later 6-clock and 1-clock 8051s exist; UG numbers use 12 clocks unless stated.)

Registers: A, B (also MUL/DIV), R0–R7 in four banks selected by PSW.RS1,RS0, 16-bit DPTR for external data, PC, SP (reset \(07\mathrm{H}\), so the first PUSH uses \(08\mathrm{H}\)). PSW bits: CY, AC, F0, RS1, RS0, OV, —, P. Internal RAM \(00\mathrm{H}\)–\(7F\mathrm{H}\) on the 128-byte parts: \(00\)–\(1F\) register banks, \(20\)–\(2F\) bit-addressable, \(30\)–\(7F\) scratch. SFRs occupy \(80\mathrm{H}\)–\(FF\mathrm{H}\) on the direct-address path: P0–P3, PCON, TCON, TMOD, TL0/TH0, TL1/TH1, SCON, SBUF, IE, IP, ACC, B, DPH/DPL, SP, PSW.

Ports: P0 is open-drain (needs pull-ups, multiplexed with AD0–AD7 when external memory is used). P2 supplies A8–A15 for external memory. P1 is a quasi-bidirectional I/O port. P3 has alternate functions: RXD/TXD, INT0/INT1, T0/T1, WR/RD. Writing 1 to a pin lets an external device pull it down; that is why you write \(0xFF\) to a port before using it as input.

Timers: TMOD bits per timer: GATE, C/T (0=timer from oscillator/12, 1=counter from T0/T1 pin), M1 M0. Mode 1 is 16-bit; Mode 2 is 8-bit auto-reload (TH copied to TL on overflow) — the UART baud generator. Mode 0 is 13-bit (legacy), Mode 3 splits timer 0. TCON has TF0/TR0/TF1/TR1 and the external-interrupt edge/level bits.

Delay in Mode 1: desired time \(\tau\), machine-cycle period \(T_{\mathrm{mc}}=12/f_{\mathrm{osc}}\), counts \(N=\tau/T_{\mathrm{mc}}\). Load \(65536-N\) into TH:TL. For \(1\,\mathrm{ms}\) at \(12\,\mathrm{MHz}\), \(N=1000\), load \(FC18\mathrm{H}\). Overflow sets TF, which can interrupt if ET0 and EA are set.

Serial: SCON Mode 1 is 8-bit UART, baud from Timer 1 Mode 2:
\[
\mathrm{baud}=\frac{2^{\mathrm{SMOD}}}{32}\cdot\frac{f_{\mathrm{osc}}}{12\,(256-\mathrm{TH1})}.
\]
Standard crystal \(11.0592\,\mathrm{MHz}\) makes integer TH1 for 9600, 4800, 2400. SMOD is PCON.7. SBUF write starts a send; TI flag. RI on receive.

Interrupts (8051): IE bits EA, ET2 (on 8052), ES, ET1, EX1, ET0, EX0. Vectors: reset \(0000\mathrm{H}\), EX0 \(0003\mathrm{H}\), TF0 \(000B\mathrm{H}\), EX1 \(0013\mathrm{H}\), TF1 \(001B\mathrm{H}\), serial \(0023\mathrm{H}\). Low/high priority via IP; two levels only. RETI, not RET, from hardware ISRs (restores the priority stack).

External memory: MOVX @DPTR,A / MOVX A,@DPTR with RD/WR; MOVC A,@A+DPTR for code space (tables in ROM). EA pin low forces all code external.

Interfacing the 8051 to an 8255 is the same decoder story with ALE, PSEN, WR, RD. Chip-select still comes from high address bits of the MOVX address.

This unit’s exam jobs: write a CS equation, compute an 8255 control word, compute TH0 for a delay, compute TH1 for a baud rate, and not confuse 8085 IN/OUT ports with 8051 P1 pins.

## Equations

Address span of \(n\) decoded lines:
\[
\text{block size}=2^{n_{\mathrm{inside}}},\quad \text{CS true on a unique combination of }A_{15}\ldots A_{n_{\mathrm{inside}}}.
\]
8255 Mode-0 control (I/O map):
\[
\mathrm{CW}=1\,M_A1 M_A0\,A\,CU\,M_B\,B\,CL
\]
with each direction bit \(1=\) input.

8255 BSR:
\[
\mathrm{CW}=0\,0\,0\,0\,b_2 b_1 b_0\,S,\quad S=1\text{ set},\;0\text{ reset}.
\]

8051 machine cycle (classic):
\[
T_{\mathrm{mc}}=\frac{12}{f_{\mathrm{osc}}}.
\]
Timer-1 Mode-1 reload:
\[
\mathrm{TH:TL}=65536-\frac{\tau}{T_{\mathrm{mc}}}.
\]
Baud, Mode 1, Timer 1 Mode 2:
\[
\mathrm{TH1}=256-\frac{2^{\mathrm{SMOD}}f_{\mathrm{osc}}}{32\cdot 12\cdot \mathrm{baud}}=256-\frac{2^{\mathrm{SMOD}}f_{\mathrm{osc}}}{384\cdot \mathrm{baud}}.
\]

Register-bank base:
\[
\text{base}=8\times(2\,\mathrm{RS1}+\mathrm{RS0}).
\]

## Methods

To decode memory: write the start and end addresses in binary, find the bits that stay constant, AND/NAND those bits (and IO/M if isolated I/O) into CS. Check an alias: flip an unused bit, see if CS still true.

To talk to 8255: align the chip on a 4-byte boundary. OUT (or MOV M / MOVX) the control word once at reset. Thereafter write A/B/C. For a switch-to-LED lab, A input B output, CW \(90\mathrm{H}\) if C is output Mode 0 (A in, B out, CU out, CL out: \(1001\,0000\)).

To time an 8051 delay: convert \(\tau\) to machine cycles, subtract from 65536, split high/low bytes, set TMOD, load TH/TL, TR=1, poll TF or enable the interrupt. For loops inside the ISR, remember the ISR itself costs cycles; exam problems usually ignore that unless they say “including overhead.”

To set baud: pick \(11.0592\,\mathrm{MHz}\) if you need exact 9600. Compute \(256-\mathrm{TH1}=f_{\mathrm{osc}}/(384\cdot\mathrm{baud})\) for SMOD=0. If the result is not integer, either change crystal, set SMOD=1 (doubles baud for the same TH1), or accept error. Never use \(12\,\mathrm{MHz}\) and claim exact 9600 (TH1 would be \(256-3.255\), not integer).

To read a port: write 1s, then read. To use P0 as I/O with no external memory, still fit pull-ups.

When mixing 8085 and 8051 in one paper: 8085 T-state is crystal/2; 8051 machine cycle is 12 oscillator periods. Do not time 8051 instructions in 8085 T-states.

## Mistakes

Generating CS from data bits or from ALE alone.

8255 control word with bit 7=0 accidentally entering BSR, then wondering why Port A direction did not change.

Port A input coded as 0 in the control word (0 is output).

Loading 8051 timer with \(N\) instead of \(65536-N\), or using \(2^{16}=65535\).

Using \(f_{\mathrm{osc}}\) as the timer clock without dividing by 12.

Baud-rate formula with 32 omitted, or SMOD applied as a divide instead of a multiply.

RET from an 8051 hardware ISR (should be RETI) — nested same-level interrupts then stick.

Mapping 8051 internal RAM and SFRs as if they were one 256-byte RAM that MOVX can see. MOVX is *external* data; MOV is internal/SFR.

Forgetting P0/P2 are eaten by the external memory bus when EA=0 or when MOVX runs.

8085 IN port address 16-bit (it is 8-bit, duplicated).

Partial decoding “works in the lab” then fails when a new RAM is added in an alias hole.

Writing the 8255 control register every time you write Port A — wasteful, and BSR versus I/O mode mistakes creep in. Write CW once.

A last trainer check: after RESET the 8051 SP is \(07\mathrm{H}\) and PC is \(0000\mathrm{H}\). Put a JMP at \(0000\mathrm{H}\) over the interrupt vectors, initialize SP into scratch RAM (often \(30\mathrm{H}\) or higher), set TMOD/SCON, then enable EA. If the stack sits in a register bank, a PUSH will clobber R0–R7 and the program looks possessed.

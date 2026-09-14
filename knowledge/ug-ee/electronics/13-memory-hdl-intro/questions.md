# Worked questions — memory, PLA, HDL

## Q1
### Given
A part labelled 8 K × 16 SRAM.
### Find
Capacity in bits, number of address pins, number of data pins, and how many such chips make a 32 K × 32 memory.
### Solution
Capacity \(8192\times 16=131\,072\) bits. Address pins \(n=\log_2 8192=13\). Data pins 16. Depth 32 K / 8 K = 4, width 32/16 = 2, so \(4\times 2=8\) chips. A 2-to-4 decoder on two extra address bits selects among four banks of two chips.
### Answer
131072 bits; 13 address; 16 data; 8 chips

## Q2
### Given
Combinational function of 4 inputs and 3 outputs, specified as a full truth table with no don't-cares.
### Find
ROM size needed (words × bits). If a PLA is used and the three outputs together contain only 6 distinct product terms after minimisation, the number of AND-rows required.
### Solution
ROM: \(2^4\times 3=16\times 3\). PLA: 6 product rows (AND plane 6 wide), OR plane 3 outputs.
### Answer
ROM \(16\times 3\); PLA 6 product terms

## Q3
### Given
Verilog fragment intended as combinational:
```verilog
always @(a or b)
  if (sel) y = a;
```
`sel` and `b` exist; `y` is a reg.
### Find
What hardware is inferred, and name two bugs.
### Solution
`y` is not assigned when `sel=0` → a latch is inferred. Sensitivity list omits `sel`, so simulation misses `sel` edges. `b` is unused. Intended MUX needs `else y=b` (or a default) and `always @*` / `@(*)`.
### Answer
Latch on `y`; bugs: inferred latch, incomplete sensitivity list

## Q4
### Given
DRAM array 4096 rows, refresh interval 64 ms for the whole array, distributed refresh.
### Find
Time between successive row-refresh commands.
### Solution
\(64\times 10^{-3}/4096=15.6\,\mu\mathrm{s}\).
### Answer
\(15.6\,\mu\mathrm{s}\)

## Q5
### Given
Two 4-input LUTs. One must implement \(f=AB+CD\), the other \(g=A\oplus B\oplus C\oplus D\).
### Find
Whether each function fits in a single 4-LUT, and the number of SRAM bits in one 4-LUT.
### Solution
Both are 4-input functions, so each fits in one 4-LUT (any Boolean of 4 variables does). Bits per LUT \(=16\).
### Answer
Both fit; 16 bits per LUT

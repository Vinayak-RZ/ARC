# P05 — XLPE cable derating

**Answer:** `derated_ampacity_a` = **31.7 A**

## Arc

- No cable ampacity table record for 25 mm² tray install in library
- Python: I = 96 × Ca × Ci with **problem-stated** Ca = 0.87, Ci = 0.38

## Web verification (factors)

- [IEC 60364-5-52 Table B.52.14 via TiSoft](https://www.ti-soft.com/en/support/help/electricaldesign/standards/iec-60364-5-52/cables-installed-in-air/correction-factor-k1/table-b_52_14) — XLPE/PVC at **40 °C → 0.87** (PVC column; aligns with given Ca)
- [ZeroAndSpan IEC 60364 derating guide](https://zeroandspan.com/electrical/cable-ampacity-derating-calculator/) — confirms ambient × grouping product workflow (Ci = 0.38 taken from problem/IS 732 grouping table for six circuits)

## Disagreements

None with Arc (no library row). Used exam-given 96 A base and factors.

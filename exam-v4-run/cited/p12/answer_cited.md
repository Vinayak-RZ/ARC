# P12 — IGBT conduction loss (FGH40N60SFD)

**Answer:** `conduction_loss_w` = **116.0 W**

## Arc

- `reference search FGH` — **no semiconductor record** for this part (library has IRF540N only)
- Python: P = I_C · V_CE(sat)_max

## Web verification

- [onsemi FGH40N60SFD datasheet](https://www.onsemi.com/download/data-sheet/pdf/fgh40n60sfdtu-f085-d.pdf) — V_CE(sat) **max 2.9 V** @ I_C = 40 A, V_GE = 15 V, T_C = 25 °C
- [Fairchild legacy FGH40N60SFD PDF](https://storage.ua.prom.st/820848_40n60sfd.pdf) — same max 2.9 V row

P = 40 A × 2.9 V = **116.0 W** (not 2.3 V typ)

## Disagreements

No Arc device entry; trusted datasheet max over typ.

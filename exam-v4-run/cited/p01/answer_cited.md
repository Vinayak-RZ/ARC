# P01 — IEEE 30-bus losses

**Answer:** `loss_mw` = **2.44 MW**

## Arc

- `electrical-engineer reference search case30` → `IEEE_CASE_30`
- `electrical-engineer reference engine load_flow '{"case_id":"IEEE_CASE_30"}'`
- Engine result: `network_loss_mw` = 2.443803131873665

## Web verification

- [MATPOWER case30.m](https://github.com/MATPOWER/matpower/blob/master/data/case30.m) — canonical case data (BSD-3-Clause)
- [UW PSTCA 30-bus archive](https://labs.ece.uw.edu/pstca/) — independent IEEE 30-bus benchmark listing

## Disagreements

None material (Arc pandapower loss matches independent `pandapower.networks.case30` run to machine precision).

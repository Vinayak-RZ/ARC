# P10 — New England 39-bus losses

**Answer:** `loss_mw` = **43.64 MW**

## Arc

- `reference search case39` — **no `IEEE_CASE_39` catalog record**
- Python + pandapower (same stack as `load_flow` engine): `pandapower.networks.case39()`, `runpp`, loss = P_gen + P_ext_grid − P_load

## Web verification

- [MATPOWER case39.m](https://github.com/MATPOWER/matpower/blob/master/data/case39.m) — canonical 39-bus New England case
- [UW PSTCA](https://labs.ece.uw.edu/pstca/) — 39-bus benchmark listing

## Disagreements

Arc has no case39 record; pandapower loss **43.6411 MW** used (would match `load_flow` if record existed).

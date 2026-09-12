# Cross-cutting — unmatched, multi-pack, honesty

Load with a pack skill when the prompt spans packs or matches nothing.

## Unmatched

No auto-simulate. If there is no pack match **and** no typed model artifact
(netlist, TF/SS, network case), use retrieve-optional → `label-unverified`.
Numerics without a verifier use the exact token `unchecked`.

Text that “looks like a netlist” is not a netlist port.

## Multi-pack

At most two packs. Example: power + machines for a transformer feeding a
feeder; circuits + electronics for a biased amplifier. Maths-for-EE may ride
with any pack as the second slot when the unknown is an ODE/Fourier identity.

A third discipline (civil, mechanical, plant PLC) is out of product — say so;
do not silently leave EE.

## Honesty

Peer MATLAB Copilot scalars stay `unchecked` until an EE provider recomputes.
BYO PDFs cannot override gates. Fluent method in chat is never a checked ohm.

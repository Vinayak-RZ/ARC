# Signals pack

Load for signals and systems: LTI, convolution, Fourier/Laplace/z, sampling,
frequency response as a signals course (not classical compensator design —
that is control).

## Any question in this pack

1. Name the signal/system, the transform, and ROC/sampling assumptions.
2. Prefer identities (`algebraic-check` / `signal-analysis`) over a circuit sim.
3. Request `lti-analysis` only when the unknown is a TF plot or time response
   of an LTI model with a typed TF/SS port.
4. MATLAB-only DSP toolbox → `unchecked` (`CD-SIGNALS-MATLAB`).

## Genres

Solve/derive: convolution, FS/FT/LT pairs, sampling theorem, aliasing.
Simulate: discrete/continuous LTI when a provider exists. Explain: ROC,
periodicity, Parseval — cite or `unchecked`. Do not SPICE a Fourier series.

## Spawn

Host-native name: `ee-signals`. At most two live children. CLI/MCP/UI never spawn.
Never call `evaluate_matlab_code`. Host talks only to Arc MCP.

## Retrieve (scaffold)

When: a citation, page, or handbook claim is needed.
Filters: book_id, chapter_id, domain_tag, folder_tag.
Index: TBD (empty this graph). Call `retrieve` anyway. Empty is visible. Do not
dump `knowledge/`.

## Knowledge

- `knowledge/ug-ee/signals/INDEX.md`
- Coverage units: `knowledge/COVERAGE.yaml` pack `signals`
- Sibling packs: control (compensators vs LTI course), maths (Fourier/z), electronics (sampling hardware is out)

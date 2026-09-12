# UG electrical engineering curriculum map

**Role:** Defines the **product bound** for Electrical Engineer. Not an eval gold set.  
**Rule:** GATE EE is an **eval overlay** (a check that we can see capability). It is **not** the syllabus ceiling and not the only source of tasks.  
**Date:** 2026-09-09

## How to use this map

1. Public promise = typical **core UG EE / EEE** subjects that recur across the institutes below (India first, global must not be missing).
2. A question is in-scope if it is normal coursework in that union (assignment, lab numerical, diagram, exam-style), not only if it appears on GATE.
3. GATE section labels may still tag eval items so we can *measure* coverage. Missing a GATE topic that the programmes teach is a product gap. Extra GATE trick questions that programmes do not teach are optional eval spice, not the bound.

## Institutes consulted (public pages)

| Region | Institute | Programme signal | Core EE subjects named on the source | URL | Retrieved |
|--------|-----------|------------------|--------------------------------------|-----|-----------|
| India | IIT Roorkee | EE programmes: power, machines, drives, control, power electronics | Power, machines, drives, control, power electronics (NEP PCC EEC-* 2023–24) | https://iitr.ac.in/Departments/Electrical%20Engineering%20Department/Academics/Programmes.html | 2026-09-11 |
| India | IIT Madras | EE course descriptions (Jan–May 2026) | Department UG EE slate (circuits through energy/electronics as offered that term) | https://www.ee.iitm.ac.in/assets/documents/2026-Jan-May-Course-description.pdf | 2026-09-07 |
| India | NIT Tiruchirappalli | B.Tech EEE flexible curriculum 2024–25 | Circuit theory, signals and systems, DC machines and transformers, electron devices, digital electronics, AC machines, analog electronic circuits, T&D, power system analysis, power electronics, control systems, linear ICs, microprocessors, measurements, protection and switchgear | https://www.nitt.edu/home/academics/curriculum/B.Tech-EE-2024.pdf | 2026-09-09 |
| India | NIT Trichy EEE programme page | B.Tech EEE aims: machines, power systems, applied electronics | Machines, power systems, applied electronics | https://www.nitt.edu/home/academics/departments/eee/programmes/btech/curriculum/ | 2026-09-09 |
| India | AICTE (older published model UG EE, still widely mirrored) | Model UG Electrical Engineering | Basic electrical, circuits, machines, power, control, electronics, measurements (document family) | https://www.klnce.edu/download/2021%20-%202022/EEE/AICTE_UG_%20Curriculum.pdf | 2026-09-09 |
| Global | MIT | Course 6 / EECS undergraduate subjects | Circuits, signals, devices; energy and control as tracks/electives | https://catalog.mit.edu/subjects/6/ | 2026-09-07 |
| Global | UC Berkeley | ECE upper-division major | Circuits, signals, devices; energy/control tracks | https://eecs.berkeley.edu/resources/undergrads/ece-major-information/ece-major-upper-division-degree-requirements/ | 2026-09-07 |
| Global | ETH Zürich | Electric Energy Engineering track | Power electronics, machines, power system analysis, control | https://ethz.ch/content/dam/ethz/special-interest/itet/department/Studies/Electric%20Energy%20Engineering.pdf | 2026-09-07 |

AICTE also announced a newer UG EE model curriculum (late 2024 news). The **downloadable** model used here is the older published PDF until an official current PDF is cited. News pages are not treated as a course list.

## Union of core subjects (product bound)

These packs are in the public UG promise. Depth order for implementation is a P1 default (circuits, then control), not a claim that other packs are out of the product. Architecture coverage: every pack × genre has a complete path ([`ARCHITECTURE.md`](ARCHITECTURE.md) §0).

| Pack | What UG students actually take (union) | Present in |
|------|----------------------------------------|------------|
| Circuits | Circuit theory, network theorems, transients, AC phasors, resonance | NITT, AICTE-family, MIT/Berkeley |
| Signals | Signals and systems, Fourier/Laplace in EE programmes | NITT, MIT/Berkeley |
| Electronics | Devices, analog circuits, digital electronics, linear ICs | NITT, IITM slate, MIT/Berkeley |
| Machines | Transformers, DC/AC machines, equivalent-circuit tests | NITT, IITR, ETH |
| Power | T&D, power system analysis, protection (study-level) | NITT, IITR, ETH |
| Control | Classical control, feedback, stability | NITT, IITR, ETH, MIT/Berkeley tracks |
| Power electronics | Converters, drives-adjacent UG courses | NITT, IITR, ETH |
| Measurements | Measurements and instrumentation | NITT, GATE overlay, AICTE-family |
| EM / fields | As taught in UG EE (not a research EM programme) | GATE overlay, MIT/Berkeley devices/fields |
| Maths for EE | Complex analysis, ODE, Fourier, numerical methods as used in EE cores | NITT GIR, all programmes |

**Labs** that attach to those cores (circuits lab, machines lab, control lab) are in-scope as *assignment/lab numerical + report genre*, not as a separate product.

**Out of this map (never this product):** civil, mechanical, manufacturing programmes.  
**Out of the public promise:** PG-only courses (optimal control as a graduate core, analog IC research flows, control-room operations).

## GATE overlay (eval only)

GATE EE technical sections remain a convenient **check** that an Indian UG student might still face. Map them onto packs; do not drop a pack because GATE weights it lightly, and do not skip a programme core because GATE omitted a lab.

| GATE EE section (eval tag) | Primary pack |
|----------------------------|--------------|
| Engineering Mathematics | Maths for EE |
| Electric Circuits | Circuits |
| Electromagnetic Fields | EM / fields |
| Signals and Systems | Signals |
| Electrical Machines | Machines |
| Power Systems | Power |
| Control Systems | Control |
| Electrical and Electronic Measurements | Measurements |
| Analog and Digital Electronics | Electronics |
| Power Electronics | Power electronics |

Source: GATE EE syllabus mirror used in research (`research/source-ledger.md` S11).

## What this does not decide

- Gold-task counts per pack (eval design).
- v1 implementation order beyond the P1 default (circuits, then control).
- Whether a specific IIT elective is in v1.

## IIT Roorkee book list

Per-course IITR-listed texts vs author-free/OER stand-ins (BYO commercial PDFs; no book binaries in git): [`../research/notes/iitr-ee-book-catalog.md`](../research/notes/iitr-ee-book-catalog.md).

## Sources

- Institute URLs in the table above — retrieved as dated — reliability: primary except GATE mirror and AICTE mirror (secondary)
- [`../research/notes/ee-task-taxonomy-draft.md`](../research/notes/ee-task-taxonomy-draft.md) — genres, not the bound
- IITR NEP structure + 2022 suggested-books syllabus — 2026-09-11 — see the book catalog note

## Confidence

High that these programmes share the union above. Medium on AICTE 2024 revision details until an official current PDF is linked.

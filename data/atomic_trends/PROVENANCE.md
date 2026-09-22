# Periodic trends teaching-data specification

## Purpose and scope

The Periodic trends experience supports CHEM1011 students to inspect evidence
for periodic patterns and compare atomic properties. It exposes evidence; it
does not automatically explain periodic trends.

This document is the canonical specification for the next data-curation task.
It does **not** certify the current CSV as conforming to that specification.

The intended source architecture is:

```text
authoritative scientific sources
            ↓
curated local project dataset
            ↓
Streamlit experience
```

The deployed learner experience must use the curated local data; it must not
require live calls to external scientific APIs.

## Canonical learner-facing properties

| Learner-facing property | Units / scale | Data status | Canonical basis for future curation |
| --- | --- | --- | --- |
| Covalent atomic radius | pm | Reference / source-derived | Cordero *et al.* (2008) covalent radii |
| First ionisation energy | kJ mol⁻¹ | Reference / source-derived | NIST Atomic Spectra Database (ASD) evaluated neutral-atom data |
| Electron affinity | kJ mol⁻¹ | Reference / source-derived | NIST Chemistry WebBook SRD 69 gas-phase electron-affinity data, normalised to the CHEM1011 thermochemical convention below |
| Pauling electronegativity | Pauling scale (dimensionless) | Reference / source-derived | PubChem’s explicitly identified Pauling-scale periodic-table values |
| Effective nuclear charge, Z_eff | elementary nuclear-charge units (dimensionless) | Literature-derived model data | Clementi–Raimondi self-consistent-field screening / effective-nuclear-charge data |

Ionic radius is deliberately **out of scope** for this scalar element-property
explorer. It depends on ion/oxidation state and coordination environment, so
one scalar value per element would be scientifically misleading. This does not
make ionic radius unimportant to CHEM1011 or exclude it from a future,
appropriately specified experience.

Shielding constant `S` is not a separate learner-facing property here. It is
part of the explanatory chemistry underlying Z_eff rather than an additional
independent scalar for this explorer.

## Property definitions and sources

### Covalent atomic radius — pm

The property is specifically **covalent atomic radius**, not an unspecified
generic “atomic radius” and not van der Waals radius. The canonical source is:

> B. Cordero, V. Gómez, A. E. Platero-Prats, M. Revés, J. Echeverría,
> E. Cremades, F. Barragán, and S. Alvarez, “Covalent radii revisited”,
> *Dalton Transactions* (2008), 2832–2838.
> [https://doi.org/10.1039/B801115J](https://doi.org/10.1039/B801115J)

Task 2 will reconcile or replace stored values against that dataset. The
current Bokeh-derived `atomic_radius_pm` values are historical implementation
data and must not be described as the Cordero dataset unless verified
value-by-value.

### First ionisation energy — kJ mol⁻¹

First ionisation energy is the energy required to remove the first electron
from a neutral gas-phase atom. The canonical source is NIST’s critically
evaluated Atomic Spectra Database (ASD), Standard Reference Database 78:

> A. Kramida, Yu. Ralchenko, J. Reader, and NIST ASD Team, *NIST Atomic
> Spectra Database* (ver. 5.12, 2024), National Institute of Standards and
> Technology. [https://doi.org/10.18434/T4W30F](https://doi.org/10.18434/T4W30F)
> — [ionisation-energy interface](https://physics.nist.gov/PhysRefData/ASD/ionEnergy.html).

If Task 2 retrieves values in eV, it must document the conversion to
kJ mol⁻¹. ASD output can identify estimated/interpolated or theoretical
values; that status must be retained rather than silently represented as a
measurement.

### Electron affinity — kJ mol⁻¹

The learner-facing convention is the CHEM1011 thermochemical reaction:

```text
X(g) + e⁻ → X⁻(g)
```

Favourable (exothermic) attachment is **negative**. This must be recorded
with every curated value: many sources report electron affinity as a positive
electron-binding/released-energy quantity. Task 2 must explicitly convert
source values to this CHEM1011 sign convention. The canonical source is NIST
Chemistry WebBook SRD 69, which provides literature-cited gas-phase
electron-affinity determinations:

> NIST Chemistry WebBook, SRD 69, [Ion Energetics / electron affinity]
> (https://webbook.nist.gov/chemistry/ion/), National Institute of Standards
> and Technology.

Missing, unbound, or unsupported values remain missing; they are never
fabricated, interpolated, or coerced to zero.

### Pauling electronegativity — Pauling scale

This is dimensionless Pauling-scale electronegativity. The canonical reference
source is PubChem’s explicitly identified Pauling-scale table:

> PubChem, “Electronegativity in the Periodic Table of Elements”,
> [https://pubchem.ncbi.nlm.nih.gov/periodic-table/electronegativity](https://pubchem.ncbi.nlm.nih.gov/periodic-table/electronegativity).

Values undefined by the chosen canonical source remain missing; no values are
invented to make a continuous plot.

### Effective nuclear charge, Z_eff

Z_eff is **literature-derived model data**. It is neither a direct
experimental measurement nor a universal scalar intrinsic to an element, and
it is not calculated by this Streamlit app using Slater’s rules. Its canonical
basis is the Clementi–Raimondi self-consistent-field screening / effective
nuclear-charge data, including the continuation for heavier atoms:

> E. Clementi and D. L. Raimondi, “Atomic Screening Constants from SCF
> Functions”, *The Journal of Chemical Physics* **38** (1963), 2686–2689.
> [https://doi.org/10.1063/1.1733573](https://doi.org/10.1063/1.1733573)
>
> E. Clementi, D. L. Raimondi, and W. P. Reinhardt, “Atomic Screening
> Constants from SCF Functions. II. Atoms with 37 to 86 Electrons”, *The
> Journal of Chemical Physics* **47** (1967), 1300–1307.
> [https://doi.org/10.1063/1.1712084](https://doi.org/10.1063/1.1712084)

CHEM1011 shielding material treats Z_eff as orbital-specific, and the dataset
must preserve that meaning. For this simple scalar surface, Task 2 will use
the following outer-orbital selection rule for **main-group** elements:

| Elements | Selected value |
| --- | --- |
| H, He | outer 1s |
| Groups 1–2 | outer valence ns |
| Groups 13–18 | outer valence np |

Thus Li and Be use 2s; B–Ne use 2p; Na and Mg use 3s; and Al–Ar use 3p.
Transition-metal Z_eff remains missing in this scalar dataset: ns and
(n−1)d values are genuinely distinct, and flattening them would conceal
chemistry relevant to the course. A later design may introduce
orbital-resolved exploration instead.

## Missingness and source status

Reference / source-derived data comprises covalent atomic radius, first
ionisation energy, electron affinity, and Pauling electronegativity. Z_eff
is literature-derived model data. Missing values always remain missing: they
are not interpolated, replaced with zero, or fabricated for continuous plots.
Where a source reports a value as estimated or interpolated, the local curation
must retain that source status.

## Current proof-of-principle implementation

`elements.csv` remains a local, static copy of elemental-property fields
bundled with the Bokeh sample dataset (`bokeh.sampledata._data.elements.csv`),
accessed for this proof of principle on 2026-09-22. It contains one row for
each element with atomic number 1–118. Bokeh sample data and the historical
SciX CSV are useful historical cross-checks, not the canonical authorities for
the future curated dataset.

The historical source field `IE-1` contains values such as H 1312, He 2372,
and Li 520. Those magnitudes are first ionisation energies in **kJ mol⁻¹**;
the old notebook incorrectly labelled them as eV. The current local field is
therefore named `first_ionisation_energy_kj_mol`. Blank historical source
fields remain blank rather than estimated.

The historical SciX CSV URL was unavailable from the build environment, so
this local Bokeh copy remains the inspectable classroom asset for the existing
proof of principle. Task 2 will curate or rebuild the local data against the
canonical specification above.

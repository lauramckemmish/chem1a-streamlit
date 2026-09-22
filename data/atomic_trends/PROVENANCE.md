# Periodic trends teaching-data specification

## Purpose and scope

The Periodic trends experience supports CHEM1011 students to inspect evidence
for periodic patterns and compare atomic properties. It exposes evidence; it
does not automatically explain periodic trends.

This document specifies and records the curated local dataset in
`elements.csv`.

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
| Electron affinity | kJ mol⁻¹ | Reference / source-derived | Andersen, Haugen, and Hotop (1999) recommended atomic electron affinities, normalised to the CHEM1011 thermochemical convention below |
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

The active `covalent_atomic_radius_pm` snapshot uses the explicit
`covalent_radius_cordero` field from the `mendeleev` scientific-data package,
which transcribes this Cordero dataset. It covers Z = 1–96; later elements are
left missing. The historical Bokeh `atomic_radius_pm` field was retired rather
than relabelled.

### First ionisation energy — kJ mol⁻¹

First ionisation energy is the energy required to remove the first electron
from a neutral gas-phase atom. The canonical source is NIST’s critically
evaluated Atomic Spectra Database (ASD), Standard Reference Database 78:

> A. Kramida, Yu. Ralchenko, J. Reader, and NIST ASD Team, *NIST Atomic
> Spectra Database* (ver. 5.12, 2024), National Institute of Standards and
> Technology. [https://doi.org/10.18434/T4W30F](https://doi.org/10.18434/T4W30F)
> — [ionisation-energy interface](https://physics.nist.gov/PhysRefData/ASD/ionEnergy.html).

The active local snapshot uses the PubChem PUG periodic-table `IonizationEnergy`
field as a practical periodic-table compilation consistent with NIST values,
then converts eV to kJ mol⁻¹ with `96.4853321233 kJ mol⁻¹ eV⁻¹`. NIST ASD
remains the primary evaluated reference and the scientific cross-check. Blank
PubChem values remain blank locally.

### Electron affinity — kJ mol⁻¹

The learner-facing convention is the CHEM1011 thermochemical reaction:

```text
X(g) + e⁻ → X⁻(g)
```

Favourable (exothermic) attachment is **negative**. Andersen–Haugen–Hotop is
the primary reference-data background:

> T. Andersen, H. K. Haugen, and H. Hotop, “Binding Energies in Atomic
> Negative Ions: III”, *Journal of Physical and Chemical Reference Data*
> **28** (1999), 1511–1533.
> [https://doi.org/10.1063/1.556047](https://doi.org/10.1063/1.556047)

That survey covers electron-affinity determinations through Z = 94 and
establishes recommended atomic values. The operational teaching-data source is
the PubChem PUG periodic-table `ElectronAffinity` field, which presents a
positive electron-binding-energy convention. The preparation script converts
each available source value to the CHEM1011 convention:

```text
EA_CHEM1011 (kJ mol⁻¹) = −EA_source (eV) × 96.4853321233 kJ mol⁻¹ eV⁻¹
```

The conversion constant is the exact molar energy equivalent of 1 eV using the
2019 SI definition of the elementary charge and Avogadro constant. Values
absent from PubChem remain missing; they are not interpolated, fabricated, or
replaced with zero.

The local teaching snapshot is not a direct transcription of the Andersen table;
the paper remains the scientific reference and a cross-check for the source
definition and positive-binding-energy convention.

### Pauling electronegativity — Pauling scale

This is dimensionless Pauling-scale electronegativity. The active source is
PubChem’s explicitly identified Pauling-scale table, retrieved through its PUG
periodic-table response:

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
preserves that meaning. The operational values use the `mendeleev` scientific
data package's Clementi–Raimondi screening-constant transcription; the
preparation script stores `Z − screening` and the selected orbital. For this
simple scalar surface, it uses
the following outer-orbital selection rule for **main-group** elements:

| Elements | Selected value |
| --- | --- |
| H, He | outer 1s |
| Groups 1–2 | outer valence ns |
| Groups 13–18 | outer valence np |

Thus Li and Be use 2s; B–Ne use 2p; Na and Mg use 3s; and Al–Ar use 3p.
Transition-metal Z_eff is missing in this scalar dataset: ns and
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

## Local snapshot and reproducibility

`elements.csv` is a checked local static teaching-data snapshot with one row
for each atomic number 1–118. It is generated by
`prepare_dataset.py`: PubChem PUG JSON supplies ionisation energy, electron
affinity, and Pauling electronegativity; `mendeleev` supplies its explicit
Cordero and Clementi–Raimondi-transcription fields; the script makes the eV
conversions, electron-affinity sign inversion, and orbital selection visible.
Neither source is accessed by the deployed Streamlit app.

The Bokeh sample data and historical SciX CSV are now historical cross-checks,
not authorities for the active dataset.

The historical source field `IE-1` contains values such as H 1312, He 2372,
and Li 520. Those magnitudes are first ionisation energies in **kJ mol⁻¹**;
the old notebook incorrectly labelled them as eV. The current local field is
therefore named `first_ionisation_energy_kj_mol`. Blank historical source
fields remain blank rather than estimated.

The historical SciX CSV URL was unavailable from the build environment. It is
not needed by the active local dataset.

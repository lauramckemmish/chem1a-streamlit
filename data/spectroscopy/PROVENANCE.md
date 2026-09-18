# CHEM 1A Week 01 spectroscopy provenance

Retrieved/accessed: 2026-09-18.

## Scope and schema

This is a bounded scientific source layer for CHEM 1A Week 01, not an exhaustive atomic-spectrum catalogue.

- `source_lines.csv` contains retained NIST source/reference rows required for the current display curation. `source_reported_intensity` is copied only as source-dependent selection metadata; it is not a cross-species or learner-consumed physical intensity scale.
- `display_features.csv` contains pedagogical teaching features and explicit links to one or more source rows. It has no intensity field.
- `hydrogen_series.csv` contains bounded reference data for five Lyman, Balmer, and Paschen members for later Stage 4 use. These values are transcribed from the named NIST main-series table, not calculated with the Rydberg equation.

All stored wavelengths are nm. When a NIST table reports Å, conversion is exact: **1 Å = 0.1 nm**. Source values are retained before conversion in `wavelength_source_value`.

## NIST source family

| Species/dataset | Source | Ionisation state | Source units and medium |
| --- | --- | --- | --- |
| H Stage 1/2 features | [NIST Persistent Lines of Neutral Hydrogen](https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable3.htm); [NIST Strong Lines of Hydrogen](https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable2.htm) | H I | Å; persistent table values in the retained visible region are air wavelengths; strong-lines page labels its visible rows as air |
| He comparison | [NIST Persistent Lines of Neutral Helium](https://physics.nist.gov/PhysRefData/Handbook/Tables/heliumtable3.htm) | He I | Å; retained visible values stored as air |
| Na comparison | [NIST Persistent Lines of Neutral Sodium](https://physics.nist.gov/PhysRefData/Handbook/Tables/sodiumtable3.htm) | Na I | Å; retained visible values stored as air |
| Ne comparison | [NIST Persistent Lines of Neutral Neon](https://physics.nist.gov/PhysRefData/Handbook/Tables/neontable3.htm) | Ne I | Å; retained visible values stored as air |
| Hg comparison | [NIST Persistent Lines of Neutral Mercury](https://physics.nist.gov/PhysRefData/Handbook/Tables/mercurytable3.htm) | Hg I | Å; retained visible values stored as air |
| Hydrogen series | [NIST Atomic Spectroscopy Compendium: main hydrogen series](https://www.nist.gov/pml/atomic-spectroscopy-compendium-basic-ideas-notation-data-and-formulas/atomic-spectroscopy-atomic) | H I | Å; below 2000 Å vacuum, above 2000 Å air |

The [NIST Atomic Data for Hydrogen](https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable1.htm) explains that Lyman-α, Balmer-α, and Balmer-β have resolved Ritz fine-structure wavelengths, while other tabulated multiplets use weighted-average energies. That distinction is retained in `reference_status` and grouping notes.

## Curation and grouping

The Stage 1 teaching/display window is 380–780 nm. It is a display window, not an exact physical definition of visible light.

For He I, Na I, Ne I, and Hg I, `source_lines.csv` retains every NIST Persistent Lines row in that window. `display_features.csv` then represents selected teaching features. Closely spaced He I triplet components at approximately 388.9, 587.6, and 706.5 nm are each represented as one unresolved teaching feature, with every source component retained and a documented NIST source-row representative; no arbitrary average is calculated. The Na I D doublet remains two separate features at 588.9950 and 589.5924 nm.

Hydrogen Stage 1 selects four Balmer features: Hα, Hβ, Hγ, and Hδ. Stage 2 selects those four plus Hε and Hζ, giving transitions 3→2 through 8→2. The Stage 1 subset is deliberate progressive resolution, not an exhaustive claim. For Hα and Hβ, the display representative is the specified NIST resolved component; Hγ is NIST's unresolved weighted-average feature; Hδ–Hζ use NIST strong-line air values.

No universal numerical grouping threshold is asserted. All grouping is explicit, bounded, and traceable by source ID.

## Intensity and limitations

No quantitative learner-consumed intensity values are supplied. NIST table intensity values are source-reported, source-dependent metadata only; they are neither normalised nor comparable as a universal line-strength scale. The Read the spectrum equal-height position-mapping graph is presentation-layer behaviour and is not encoded as scientific intensity here: its wavelength positions use the existing NIST-backed Balmer references, while its equal peak heights are illustrative teaching geometry only.

This layer does not model source conditions, line broadening, detector response, resolution, molecular spectra, or a complete atomic-line inventory. Air/vacuum medium is recorded as metadata, but conversion between media and learner-facing convention controls are intentionally out of scope.

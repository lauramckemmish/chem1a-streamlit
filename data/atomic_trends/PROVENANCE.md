# Atomic trends teaching data

`elements.csv` is a local, static copy of the elemental-property fields bundled
with the Bokeh sample dataset (`bokeh.sampledata._data.elements.csv`), accessed
for this proof of principle on 2026-09-22. It contains one row for each element
with atomic number 1–118. Values are reference data, not measurements made in
this experience.

The original field `IE-1` uses values such as H 1312, He 2372, and Li 520.
These are first ionisation energies in **kJ mol⁻¹**; the locally stored field is
therefore named `first_ionisation_energy_kj_mol`. The historical notebook's
`ioninsation energy, eV` label is not carried forward because it conflicts with
those magnitudes. `atomic radius` is stored in pm and electronegativity uses the
Pauling scale. Blank source fields remain blank rather than being estimated.

The historical SCIX CSV URL was unavailable from the build environment, so this
local Bokeh copy is the retained, inspectable classroom asset. Its matching
column names and values (including H 1312, He 2372, Li 520) provided the unit
cross-check.

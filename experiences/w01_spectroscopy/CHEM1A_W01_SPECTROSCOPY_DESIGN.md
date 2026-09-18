# CHEM 1A Week 01 — Spectroscopy Experience Design

Status: DESIGN v0.2 — agreed learning direction and scientific/data decisions, pre-implementation.

## Purpose

This is a lightweight digital spectroscopy experience embedded within the CHEM 1A Week 1 workshop.

It is not intended to independently teach all of spectroscopy, replace the workshop, or perform students' required calculations.

Its role is to make a small number of scientific representations easy to inspect and compare while the surrounding workshop supplies calculation, discussion, explanation and synthesis.

Core journey:

notice spectral patterns
→ return to hydrogen
→ connect energy-level reasoning to observed lines
→ translate barcode to intensity-vs-wavelength
→ extend beyond visible light

## Audience

Primary learners:
first-year university chemistry students in CHEM 1A.

Do not assume prior understanding of why atomic spectra are discrete.

Primary facilitators:
CHEM 1A teaching staff/tutors with variable spectroscopy and pedagogical familiarity.

## Intended learning

Students should understand that:

- atomic emission spectra contain discrete lines;
- different atoms show different structured spectral patterns;
- hydrogen energy-level differences can be connected quantitatively to observed wavelengths;
- barcode/line-spectrum and intensity-vs-wavelength representations can encode the same wavelengths;
- a line corresponds to a peak at the same wavelength;
- intensity can add information on a y-axis while wavelength remains the horizontal coordinate;
- hydrogen emission extends beyond visible light;
- qualitatively, Lyman is UV, Balmer includes visible wavelengths, and Paschen is IR;
- larger energy gap means higher photon energy and shorter wavelength;
- smaller energy gap means lower photon energy and longer wavelength.

Core learner reasoning sequence:

notice → compare → predict → check → translate → generalise

## Stage 1 — Compare atoms

Main cognitive job:
notice and compare.

Core species:
H, He, Na, Ne, Hg.

For v1, use neutral species only: H I, He I, Na I, Ne I and Hg I.

Students compare separately stacked atomic line/barcode spectra on a common 380–780 nm wavelength scale. This is a teaching/display window for visible comparison, not a claim that visible-light boundaries are physically exact.

Hydrogen should show a reduced set of approximately four prominent visible Balmer features: enough structure to recognise a pattern, but not so much detail that H dominates the comparison. The interface should describe these as selected prominent lines/features and must not imply that they are exhaustive.

Protected mechanism:
observation comes before explanation.

Do not initially explain the origin of line structure or place an energy-level/Rydberg explanation beside the comparison.

### Reused Screen 1 — Explore spectra

**OBSERVATION:** Rendered inspection found a single-hydrogen default too visually sparse to make the barcode-comparison task obvious.

**DECISION:** Explore spectra is one reusable phenomenon surface with an intentional representational progression. On the first visit (Move A), learners inspect all five visual/barcode emission spectra: dark fields with bright coloured lines, where the phenomenon and pattern come before numerical measurement. Learners encounter the evidence before configuring the app. “What changes? What stays the same?” is the sole comparison prompt; atom controls sit below it as secondary “Spectra in view” controls. All five start selected, and learners may remove spectra to isolate a comparison without resetting the representational progression. Their calmer indigo selected state avoids cumulative yellow surface area.

After workshop work reconnecting wavelength, frequency and photon energy (Move B, outside the app), learners return in Move C and intentionally reveal the quantitative wavelength representation. The same selected features are transformed/enriched into a labelled 380–780 nm line spectrum; this is not an arbitrary display preference or a duplicated second spectrum for every atom. The barcode and wavelength-axis spectrum are scientifically close but cognitively distinct: the first asks, “What does the emitted light look like?” while the second asks, “Where exactly are those features?”

Only after that wavelength reveal can learners intentionally reveal the absorption comparison. Each selected atom's quantitative emission and absorption representations are paired together. The absorption reveal cannot precede the wavelength representation, and both reveals persist for the session.

**OBSERVATION:** The first per-atom absorption rendering was scientifically correct but vertically repetitive.

**DECISION:** Emission and absorption remain paired by atom as compact comparison blocks, with atom identity outside the two plots and no repeated feature-count chrome. The previous observation prompt is replaced by the forward question, “Emission and absorption lines occur at the same wavelengths. Why?” This creates the need for the subsequent energy-level model without asking learners to explain it prematurely.

For this bounded first-year representation, absorption deliberately uses the same selected teaching-feature wavelengths as emission. It is a comparison of characteristic positions, not a model of relative line strength. The absorption display is a continuous illustrative visible-spectrum band with equal dark lines at those positions.

Separate aligned atomic spectra are the current core representation. Combined spectra are removed from the learner-facing design and parked only as a possible future composition/mixture feature if a real learning need emerges. The hard reveal persists for the session; after it is activated, each selected atom's emission and absorption representations are paired together. Screen 1 stops before explanatory models, transitions, calculations, or line assignments.

The wider representational progression is visual/barcode spectrum → quantitative wavelength line spectrum → later intensity-vs-wavelength graph. The graph belongs to the future Read the spectrum surface and is not specified in detail here. Once multiple real learner surfaces exist, tab navigation is the app-stage grammar. The sidebar provides shared CHEM 1A shell and verified resource/source context; it is not stage navigation.

**DECISION:** The shared CHEM 1A shell uses compact course/week/experience context so the active learner surface and scientific evidence dominate the main-page hierarchy. Course identity remains available in both the compact main context and sidebar because the sidebar may be collapsed.

## Stage 2 — Hydrogen

Main cognitive job:
check a prediction against observed evidence.

### App boundary

Whiteboard and paper remain the thinking surfaces for reasoning about energy levels, reading gaps, and calculating a hydrogen wavelength. The app does not reproduce that work with an energy-level diagram or calculator. **DECISION:** Hydrogen uses a prediction-first hard evidence reveal: a valid submitted prediction reveals the observed six-line Balmer spectrum and places the learner-entered in-range value unchanged against it. Evidence persists for the session, transition labels appear only after the reveal, and the deliberately quantitative line spectrum is retained because barcode → quantitative translation already occurred earlier.

Transition labels are an optional reference reveal, not a gate or reward. A collapsed bottom extension locates selected NIST Lyman, Balmer, and Paschen references across UV, visible, and IR, with readable local series views. This establishes that visible Balmer features are only part of hydrogen's spectrum without becoming a series calculator.

Hydrogen-like-ion comparison remains an optional later extension whose representation is not yet settled. Read the spectrum remains a separate future cognitive surface.

Students return to the same hydrogen spectral representation encountered earlier.

When students return to hydrogen, increase the visible detail deliberately. Target approximately six Balmer features in the useful visible/near-visible sequence around Hα ~656.3 nm, Hβ ~486.1 nm, Hγ ~434.0 nm, Hδ ~410.2 nm, ~397.0 nm and ~388.9 nm. This progressive spectral resolution is not inconsistent data: the earlier view uses selected prominent features for comparison; the later view lets students look more closely at hydrogen and see more structure. Exact reference values and source metadata belong in the later data/provenance layer.

Students may test predictions such as:

4 → 2 should have shorter wavelength than 3 → 2.

Students calculate wavelengths elsewhere in the workshop and use the app to inspect observational evidence.

**PROTECTED DECISION:** the app must **not** calculate the required hydrogen transition wavelength for the learner.

Do not add a transition calculator or automatically reveal the calculated answer.

## Stage 3 — Read the spectrum

**DECISION:** Read the spectrum is a separate third learner surface. Its main cognitive job is quantitative line spectrum → intensity-vs-wavelength graph; the earlier barcode transition is not repeated here.

Students inspect the established six-line hydrogen Balmer detail in both representations, vertically aligned on exactly the same wavelength coordinate system. One 3→2 line ↔ peak mapping is explicit; learners then trace another selected transition.

### Critical visual constraint

When both appear, they must share exactly the same wavelength scale and horizontal coordinate system.

A line at wavelength λ must sit vertically above the corresponding peak at wavelength λ.

Students should understand:

- horizontal position = wavelength in both;
- a line corresponds to a peak at the same wavelength;
- the graph provides a y-axis for intensity; the initial equal-height representation deliberately holds that information constant to focus on position mapping.

The experience may explicitly demonstrate one line/peak correspondence.

Students should then translate at least one further correspondence themselves through the workshop.

Do not annotate every mapping so completely that the representation-reading task disappears.

### Position-mapping representation v1

The initial graph uses equal-height peaks as an explicitly simplified **position-mapping** representation. Its purpose is to isolate:

line at wavelength λ
→ peak at the same wavelength λ

Equal-height peaks deliberately suppress intensity information and must be clearly described as illustrative rather than physical relative intensities. A brief optional “What about peak height?” reveal notes that real observed intensity can depend on physical conditions and how the spectrum is produced or measured. Do not present this as a realistic intensity spectrum or invent plausible-looking intensity ratios.

### Optional intensity extension

An optional later learner extension, such as “What about peak height?”, may introduce the idea that real spectra contain additional information in peak intensity. It may show unequal heights only when appropriately supported.

Do not imply that peak height equals transition probability. Observed relative line intensity may also depend on populations, excitation/source conditions, measurement context and other physical/experimental factors.

This is optional depth for students ready for more spectroscopy, not part of the mandatory representation-mapping pathway.

## Stage 4 — Beyond visible

Main cognitive job:
generalise beyond the human-visible window.

Extend hydrogen beyond the visible region.

Students should encounter qualitatively:

Lyman → UV
Balmer → visible
Paschen → IR

Core idea:

the spectrum does not stop where human vision stops.

Do not turn this into a comprehensive hydrogen-series calculator.

Lyman, Balmer and Paschen reference wavelengths should come from NIST reference/tabulated data. The learner-facing app must not generate these wavelengths by performing the student's Rydberg calculation.

## Optional extension — Hydrogenic ions

Optional, not part of the mandatory CHEM 1A pathway.

Possible one-electron species:

H, Z=1
He+, Z=2
Li2+, Z=3

Purpose:
make the Z² dependence physically meaningful by observing how a one-electron spectrum changes with nuclear charge.

Critical distinction:

neutral helium is **not** the Z=2 version of hydrogen.

Do not give this extension equal visual weight to the required four-stage journey.

## Molecular spectra

**Out of scope for v1.**

Do not add CO2, H2O or other molecules to the atomic selector.

Atomic line spectra and molecular vibrational spectra should not be visually conflated.

A separate future molecular/IR experience may be considered only if there is a genuine teaching need.

## Interaction direction

Likely learner navigation:

Compare atoms
Hydrogen
Read the spectrum
Beyond visible

with a clearly secondary optional extension:

Explore further

These are working labels, not final learner copy.

Avoid a large control dashboard.

Controls should exist only when changing them causes an intellectually useful change.

## Learner voice

Use the mature Data Science Streamlit learner-voice principles where appropriate for the university context:

- intelligent scientist speaking naturally to a capable learner;
- curious;
- direct;
- concise;
- evidence-minded;
- scientifically confident without pretending certainty;
- conversational but not juvenile;
- react to the science more often than praising the learner;
- no generic edtech enthusiasm;
- protect learner reasoning.

Exact learner-facing copy has not yet been authorised.

## Facilitator support

Facilitator support is part of the intended experience.

It should help tutors understand:

- what students are doing intellectually;
- what moments need protecting;
- why some explanations/calculations are deliberately absent;
- consequential learner responses or misconceptions;
- what they need to understand;
- what they do not need to teach;
- what can be compressed under time pressure;
- useful extensions if time permits.

Potential local categories:

What students are doing
Protect this
Watch for
Enough understanding
You do not need to teach
If time is short
If you have time

Do not turn facilitator material into a spectroscopy textbook or rigid script.

## Accessibility

Design accessibility into the representations.

In particular:

- wavelength must not be communicated by colour alone;
- spectra need meaningful numerical axis/tick information;
- line/peak correspondence must remain intelligible without hue;
- important information must not require hover alone;
- controls should use clear/native semantics where practical;
- alternative access should preserve evidence and reasoning rather than simply state the answer.

## Scientific data and provenance

### Data source

**DECISION:** Use NIST atomic spectroscopy data as the authoritative source family for v1. For pedagogical curation, prefer NIST Persistent Lines / strong reference material over the complete Atomic Spectra Database line inventory. Do not expose a complete atomic line catalogue.

### Source data and display features

Preserve a distinction between:

1. source/reference spectral-line data; and
2. pedagogically displayed spectral features.

The source layer retains scientific provenance and original values. The display layer may group or select features for the CHEM 1A teaching representation. Simplifying display features must not destroy source provenance.

### Fine structure and useful resolution

Do not expose atomic fine structure irrelevant to the CHEM 1A learning task. Closely spaced components may be represented as one unresolved teaching feature when their separation is below the useful resolution of this experience, while retaining recoverable underlying source rows/provenance.

Do not make atomic fine structure a learner-facing v1 topic. Do not hard-code a universal numerical grouping threshold unless implementation evidence shows one is necessary and scientifically appropriate.

Every dataset eventually used must record:

- source;
- quantity;
- units;
- measured/reference/calculated status;
- transformations/filtering;
- relevant air/vacuum wavelength distinction;
- retained spectral region;
- limitations.

Illustrative quantities must remain explicitly identifiable as illustrative.

Record wavelength-medium conventions such as air/vacuum in provenance. Do not make the air/vacuum convention a learner-facing control or required CHEM 1A concept in v1.

## Architecture

Do not design a generic CHEM 1A framework now.

Keep stable scientific/data machinery separate from experience-specific pedagogy where useful.

If future experiences are genuinely created, use:

`experiences/wNN_short_descriptive_name/`

and design files:

`CHEM1A_WNN_TOPIC_DESIGN.md`

These conventions reserve sensible namespace only. They do not authorise creation of future experiences.

## Protected design decisions

Record these as **DECISIONS**:

- university CHEM 1A context;
- facilitated workshop companion;
- observation before explanation in Stage 1;
- return to the same hydrogen representation;
- app does not perform the required transition calculation;
- barcode and graph share an aligned wavelength scale;
- equal-height position mapping is acceptable only when clearly identified as simplified/illustrative rather than intensity information;
- NIST atomic spectroscopy data is the authoritative v1 source family;
- Stage 1 uses neutral H I, He I, Na I, Ne I and Hg I in a 380–780 nm teaching/display window;
- source/reference lines remain distinct from pedagogically displayed features;
- irrelevant fine structure may be represented as unresolved teaching features while retaining provenance;
- opening comparison and later hydrogen views may deliberately show different hydrogen detail;
- the equal-height graph is a simplified position-mapping representation that suppresses intensity information;
- real peak-height discussion is an optional extension and must not equate peak height with transition probability;
- hydrogen spectrum extends into UV and IR;
- hydrogenic ions are optional;
- neutral He and He+ must not be conflated;
- molecular spectra are out of v1;
- reuse mature project interaction, voice, accessibility and facilitation principles only where they fit.

## Hypotheses / tests

Keep these explicitly unsettled:

- how much prompting Stage 1 needs;
- best layout for simultaneous atomic spectra;
- exact amount of annotation for barcode → graph;
- whether one demonstrated mapping is enough;
- exact UV/visible/IR labelling needed;
- whether hydrogenic mode earns its place;
- which live facilitator cues prove useful.

## Explicitly out of scope for initial implementation

- molecular spectroscopy;
- molecular vibrational modes;
- spectrum identification games;
- quizzes;
- marks/LMS integration;
- transition/Rydberg calculator;
- exhaustive atomic spectral database;
- line broadening;
- selection rules;
- fine structure;
- invented realistic intensities;
- arbitrary plotting controls;
- generic CHEM 1A framework;
- speculative Week 2+ experiences.

## Success criterion

A successful v1 makes the workshop spectroscopy representations easier to see, compare and reason with without moving consequential intellectual work from students into software.

The app should feel small.
The science should feel clearer.
The learner should still have something consequential to work out.

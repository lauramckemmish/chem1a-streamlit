# CHEM 1A Week 01 — Spectroscopy Experience Design

Status: DESIGN v0.1 — agreed learning direction, pre-implementation.

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
- intensity adds information on a y-axis while wavelength remains the horizontal coordinate;
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

Lithium may later be retained if convenient but is not pedagogically required.

Students compare several atomic line/barcode spectra on a common wavelength scale.

Protected mechanism:
observation comes before explanation.

Do not initially explain the origin of line structure or place an energy-level/Rydberg explanation beside the comparison.

## Stage 2 — Hydrogen

Main cognitive job:
check a prediction against observed evidence.

Students return to the same hydrogen spectral representation encountered earlier.

Students may test predictions such as:

4 → 2 should have shorter wavelength than 3 → 2.

Students calculate wavelengths elsewhere in the workshop and use the app to inspect observational evidence.

**PROTECTED DECISION:** the app must **not** calculate the required hydrogen transition wavelength for the learner.

Do not add a transition calculator or automatically reveal the calculated answer.

## Stage 3 — Barcode to graph

Main cognitive job:
translate between representations.

Students should be able to inspect:

1. coloured barcode / line spectrum;
2. intensity-vs-wavelength graph;
3. preferably both together.

### Critical visual constraint

When both appear, they must share exactly the same wavelength scale and horizontal coordinate system.

A line at wavelength λ must sit vertically above the corresponding peak at wavelength λ.

Students should understand:

- horizontal position = wavelength in both;
- a line corresponds to a peak at the same wavelength;
- the graph adds intensity on the y-axis.

The experience may explicitly demonstrate one line/peak correspondence.

Students should then translate at least one further correspondence themselves through the workshop.

Do not annotate every mapping so completely that the representation-reading task disappears.

### Intensity v1

If validated relative line strengths are unavailable, equal-height/simple peaks are acceptable.

Any such heights must be clearly described as **illustrative**.

Do not invent realistic-looking intensity ratios.

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
- illustrative intensity is acceptable if clearly labelled;
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

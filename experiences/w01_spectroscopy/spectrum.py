"""Position-only SVG line spectra for the bounded Week 01 comparison data.

Colour is a deterministic, illustrative wavelength cue. Horizontal position on the
labelled 380–780 nm axis remains the authoritative representation; line marks have
uniform geometry and do not encode source intensity.
"""

from __future__ import annotations

from html import escape
from typing import Iterable

from experiences.w01_spectroscopy import data


WAVELENGTH_MIN_NM = 380.0
WAVELENGTH_MAX_NM = 780.0
PLOT_LEFT = 112.0
PLOT_RIGHT = 1180.0
SPECIES_ORDER = ("H", "He", "Na", "Ne", "Hg")
SPECIES_NAMES = {"H": "Hydrogen", "He": "Helium", "Na": "Sodium", "Ne": "Neon", "Hg": "Mercury"}


def wavelength_to_colour(wavelength_nm: float) -> str:
    """Return an illustrative visible-colour cue for a wavelength in nm."""
    if wavelength_nm < 440:
        red, green, blue = -(wavelength_nm - 440) / 60, 0.0, 1.0
    elif wavelength_nm < 490:
        red, green, blue = 0.0, (wavelength_nm - 440) / 50, 1.0
    elif wavelength_nm < 510:
        red, green, blue = 0.0, 1.0, -(wavelength_nm - 510) / 20
    elif wavelength_nm < 580:
        red, green, blue = (wavelength_nm - 510) / 70, 1.0, 0.0
    elif wavelength_nm < 645:
        red, green, blue = 1.0, -(wavelength_nm - 645) / 65, 0.0
    else:
        red, green, blue = 1.0, 0.0, 0.0
    return f"rgb({round(red * 255)}, {round(green * 255)}, {round(blue * 255)})"


def wavelength_x(wavelength_nm: float) -> float:
    """Map a wavelength onto the fixed shared Stage 1 axis."""
    if not WAVELENGTH_MIN_NM <= wavelength_nm <= WAVELENGTH_MAX_NM:
        raise ValueError("Stage 1 wavelength is outside the 380–780 nm domain.")
    return PLOT_LEFT + (wavelength_nm - WAVELENGTH_MIN_NM) * (PLOT_RIGHT - PLOT_LEFT) / (
        WAVELENGTH_MAX_NM - WAVELENGTH_MIN_NM
    )


def features_for_species(species: Iterable[str]) -> dict[str, list[dict[str, str]]]:
    """Select Stage 1 features from the scientific data layer, in display order."""
    selected = tuple(species)
    unknown = set(selected) - set(SPECIES_ORDER)
    if unknown:
        raise ValueError(f"Unknown Stage 1 species: {', '.join(sorted(unknown))}")
    stage_1 = data.stage_1_comparison_features()
    return {
        symbol: [feature for feature in stage_1 if feature["species"] == symbol]
        for symbol in SPECIES_ORDER
        if symbol in selected
    }


def render_comparison_svg(species: Iterable[str]) -> str:
    """Render equal-geometry, shared-axis barcode rows for selected species."""
    rows = features_for_species(species)
    row_height = 96
    height = 62 + row_height * len(rows)
    svg_rows: list[str] = []
    for index, (symbol, features) in enumerate(rows.items()):
        top = 18 + index * row_height
        baseline = top + 59
        values = ", ".join(f"{float(feature['wavelength_nm']):.3f}" for feature in features)
        ticks = "".join(
            f'<line x1="{wavelength_x(tick):.2f}" y1="{baseline}" '
            f'x2="{wavelength_x(tick):.2f}" y2="{baseline + 8}" class="tick" />'
            f'<text x="{wavelength_x(tick):.2f}" y="{baseline + 27}" class="tick-label">{tick}</text>'
            for tick in range(400, 781, 100)
        )
        lines = "".join(
            f'<line x1="{wavelength_x(float(feature["wavelength_nm"])):.2f}" y1="{top + 5}" '
            f'x2="{wavelength_x(float(feature["wavelength_nm"])):.2f}" y2="{baseline}" '
            f'stroke="{wavelength_to_colour(float(feature["wavelength_nm"]))}" class="spectral-line" />'
            for feature in features
        )
        svg_rows.append(
            f'<g aria-label="{escape(SPECIES_NAMES[symbol])}: {values} nm">'
            f'<text x="18" y="{top + 37}" class="species">{escape(SPECIES_NAMES[symbol])}</text>'
            f'<text x="18" y="{top + 57}" class="feature-count">{len(features)} selected features</text>'
            f'<line x1="{PLOT_LEFT}" y1="{baseline}" x2="{PLOT_RIGHT}" y2="{baseline}" class="axis" />'
            f'{ticks}{lines}</g>'
        )
    return f'''<style>
.spectrum-svg {{ display: block; width: 100%; height: auto; background: #ffffff; font-family: "Source Sans Pro", Arial, sans-serif; color: #17212b; }}
.axis, .tick {{ stroke: #64748b; stroke-width: 1.3; }}
.tick-label {{ fill: #334155; font-size: 15px; text-anchor: middle; }}
.species {{ fill: #17212b; font-size: 19px; font-weight: 650; }}
.feature-count {{ fill: #475569; font-size: 13px; }}
.spectral-line {{ stroke-width: 1.1; vector-effect: non-scaling-stroke; stroke-linecap: square; }}
</style>
<svg class="spectrum-svg" viewBox="0 0 1200 {height}" role="img" aria-label="Selected atomic emission-line positions on the shared 380 to 780 nanometre scale">
<title>Selected atomic spectral features on a shared wavelength scale</title>
<desc>Each row uses the same labelled wavelength axis. Line marks have uniform height and width, so they show position only.</desc>
{''.join(svg_rows)}
</svg>'''

"""Position-only SVG line spectra for the bounded Week 01 comparison data.

The visual barcode and quantitative line-spectrum renderers intentionally share the
same curated features and wavelength-to-position mapping. Colour is a deterministic,
illustrative wavelength cue; line geometry never encodes source intensity.
"""

from __future__ import annotations

from html import escape
from typing import Iterable

from experiences.w01_spectroscopy import data


WAVELENGTH_MIN_NM = 380.0
WAVELENGTH_MAX_NM = 780.0
PLOT_LEFT = 112.0
PLOT_RIGHT = 1180.0
QUANTITATIVE_PLOT_LEFT = 88.0
QUANTITATIVE_PLOT_RIGHT = 1180.0
SPECIES_ORDER = ("H", "He", "Na", "Ne", "Hg")
SPECIES_NAMES = {"H": "Hydrogen", "He": "Helium", "Na": "Sodium", "Ne": "Neon", "Hg": "Mercury"}
DEFAULT_SELECTED_SPECIES = ("H",)


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


def quantitative_wavelength_x(wavelength_nm: float) -> float:
    """Map a wavelength onto the compact quantitative comparison axis."""
    if not WAVELENGTH_MIN_NM <= wavelength_nm <= WAVELENGTH_MAX_NM:
        raise ValueError("Stage 1 wavelength is outside the 380–780 nm domain.")
    return QUANTITATIVE_PLOT_LEFT + (wavelength_nm - WAVELENGTH_MIN_NM) * (
        QUANTITATIVE_PLOT_RIGHT - QUANTITATIVE_PLOT_LEFT
    ) / (WAVELENGTH_MAX_NM - WAVELENGTH_MIN_NM)


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


def combined_features_for_species(species: Iterable[str]) -> list[dict[str, str]]:
    """Return unique selected feature positions for the non-quantitative combined row."""
    features = [feature for rows in features_for_species(species).values() for feature in rows]
    by_wavelength = {feature["wavelength_nm"]: feature for feature in features}
    return [by_wavelength[wavelength] for wavelength in sorted(by_wavelength, key=float)]


def absorption_features_for_species(species: Iterable[str]) -> dict[str, list[dict[str, str]]]:
    """Return the same selected teaching features for the position-comparison absorption view."""
    return features_for_species(species)


def combined_absorption_features_for_species(species: Iterable[str]) -> list[dict[str, str]]:
    """Return the same de-duplicated union for combined absorption and emission views."""
    return combined_features_for_species(species)


def _render_rows_svg(
    rows: dict[str, list[dict[str, str]]], names: dict[str, str], *, show_identity: bool = True,
    line_colour: str | None = None, spectrum_type: str = "emission"
) -> str:
    """Render equal-geometry quantitative rows on the shared wavelength axis."""
    row_height = 96 if show_identity else 78
    height = (62 if show_identity else 26) + row_height * len(rows)
    svg_rows: list[str] = []
    for index, (symbol, features) in enumerate(rows.items()):
        top = (18 if show_identity else 6) + index * row_height
        baseline = top + (59 if show_identity else 42)
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
            f'stroke="{line_colour or wavelength_to_colour(float(feature["wavelength_nm"]))}" class="spectral-line" />'
            for feature in features
        )
        identity = (
            f'<text x="18" y="{top + 37}" class="species">{escape(names[symbol])}</text>'
            f'<text x="18" y="{top + 57}" class="feature-count">{len(features)} selected features</text>'
            if show_identity
            else ""
        )
        svg_rows.append(
            f'<g aria-label="{escape(names[symbol])}: {values} nm">{identity}'
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
<svg class="spectrum-svg" viewBox="0 0 1200 {height}" role="img" aria-label="Selected atomic {spectrum_type}-line positions on the shared 380 to 780 nanometre scale">
<title>Selected atomic {spectrum_type} features on a shared wavelength scale</title>
<desc>Each row uses the same labelled wavelength axis. Line marks have uniform height and width, so they show position only.</desc>
{''.join(svg_rows)}
</svg>'''


def render_comparison_svg(species: Iterable[str], *, show_identity: bool = True) -> str:
    """Render separate selected-atom quantitative rows on the shared Stage 1 axis."""
    rows = features_for_species(species)
    return _render_rows_svg(rows, SPECIES_NAMES, show_identity=show_identity)


def render_quantitative_emission_svg(species: Iterable[str]) -> str:
    """Render monochrome emission positions so the labelled axis carries wavelength."""
    return render_quantitative_line_positions_svg(species)


def render_quantitative_absorption_svg(species: Iterable[str]) -> str:
    """Render monochrome absorption positions without inventing depth or intensity."""
    return render_quantitative_line_positions_svg(species)


def render_quantitative_line_positions_svg(species: Iterable[str]) -> str:
    """Render compact shared-axis monochrome rows for the selected line positions."""
    rows = features_for_species(species)
    row_height = 50
    top_margin = 8
    axis_baseline = top_margin + row_height * len(rows) + 4
    height = axis_baseline + 42
    svg_rows: list[str] = []
    for index, (symbol, features) in enumerate(rows.items()):
        top = top_margin + index * row_height
        baseline = top + 34
        values = ", ".join(f"{float(feature['wavelength_nm']):.3f}" for feature in features)
        lines = "".join(
            f'<line x1="{quantitative_wavelength_x(float(feature["wavelength_nm"])):.2f}" y1="{top + 4}" '
            f'x2="{quantitative_wavelength_x(float(feature["wavelength_nm"])):.2f}" y2="{baseline}" '
            'stroke="#334155" class="spectral-line" />'
            for feature in features
        )
        svg_rows.append(
            f'<g aria-label="{escape(SPECIES_NAMES[symbol])}: {values} nm">'
            f'<text x="10" y="{top + 25}" class="species">{escape(SPECIES_NAMES[symbol])}</text>'
            f'<line x1="{QUANTITATIVE_PLOT_LEFT}" y1="{baseline}" '
            f'x2="{QUANTITATIVE_PLOT_RIGHT}" y2="{baseline}" class="row-axis" />'
            f'{lines}</g>'
        )
    ticks = "".join(
        f'<line x1="{quantitative_wavelength_x(tick):.2f}" y1="{axis_baseline}" '
        f'x2="{quantitative_wavelength_x(tick):.2f}" y2="{axis_baseline + 7}" class="tick" />'
        f'<text x="{quantitative_wavelength_x(tick):.2f}" y="{axis_baseline + 25}" class="tick-label">{tick}</text>'
        for tick in range(400, 781, 100)
    )
    return f'''<style>
.compact-spectrum-svg {{ display: block; width: 100%; height: auto; background: #ffffff; font-family: "Source Sans Pro", Arial, sans-serif; color: #17212b; }}
.row-axis {{ stroke: #cbd5e1; stroke-width: 1; }}
.axis, .tick {{ stroke: #64748b; stroke-width: 1.3; }}
.tick-label {{ fill: #334155; font-size: 15px; text-anchor: middle; }}
.species {{ fill: #17212b; font-size: 17px; font-weight: 650; }}
.spectral-line {{ stroke: #334155; stroke-width: 1.2; vector-effect: non-scaling-stroke; stroke-linecap: square; }}
</style>
<svg class="compact-spectrum-svg" viewBox="0 0 1200 {height}" role="img" aria-label="Selected atomic line positions on the shared 380 to 780 nanometre scale">
<title>Selected atomic line positions on a shared wavelength scale</title>
<desc>Each compact row uses the same wavelength mapping. Monochrome line marks have uniform height and width, so they show position only.</desc>
{''.join(svg_rows)}
<line x1="{QUANTITATIVE_PLOT_LEFT}" y1="{axis_baseline}" x2="{QUANTITATIVE_PLOT_RIGHT}" y2="{axis_baseline}" class="axis" />
{ticks}
</svg>'''


def _render_visual_rows_svg(rows: dict[str, list[dict[str, str]]], names: dict[str, str]) -> str:
    """Render dark-field visual spectra using the shared feature positions.

    This deliberately omits axes and numerical labels for the initial phenomenon-first
    view. Each line has identical geometry, so brightness and height do not imply
    relative line strength.
    """
    row_height = 88
    height = 20 + row_height * len(rows)
    svg_rows: list[str] = []
    for index, (symbol, features) in enumerate(rows.items()):
        top = 10 + index * row_height
        field_top = top
        field_height = 66
        values = ", ".join(f"{float(feature['wavelength_nm']):.3f}" for feature in features)
        lines = "".join(
            f'<line x1="{wavelength_x(float(feature["wavelength_nm"])):.2f}" y1="{field_top + 7}" '
            f'x2="{wavelength_x(float(feature["wavelength_nm"])):.2f}" y2="{field_top + field_height - 7}" '
            f'stroke="{wavelength_to_colour(float(feature["wavelength_nm"]))}" class="visual-spectral-line" />'
            for feature in features
        )
        svg_rows.append(
            f'<g aria-label="{escape(names[symbol])}: {values} nm">'
            f'<text x="18" y="{field_top + 35}" class="visual-species">{escape(names[symbol])}</text>'
            f'<rect x="{PLOT_LEFT}" y="{field_top}" width="{PLOT_RIGHT - PLOT_LEFT}" height="{field_height}" '
            f'class="visual-field" />'
            f'{lines}</g>'
        )
    return f'''<style>
.visual-spectrum-svg {{ display: block; width: 100%; height: auto; background: #ffffff; font-family: "Source Sans Pro", Arial, sans-serif; color: #17212b; }}
.visual-field {{ fill: #080b12; stroke: #1f2937; stroke-width: 1; }}
.visual-species {{ fill: #17212b; font-size: 19px; font-weight: 650; }}
.visual-spectral-line {{ stroke-width: 2.6; vector-effect: non-scaling-stroke; stroke-linecap: square; }}
</style>
<svg class="visual-spectrum-svg" viewBox="0 0 1200 {height}" role="img" aria-label="Selected atomic visual emission spectra">
<title>Selected atomic visual emission spectra</title>
<desc>Each dark field contains equal-geometry coloured emission lines at selected shared wavelength positions. No wavelength axis is shown in this visual spectrum.</desc>
{''.join(svg_rows)}
</svg>'''


def render_visual_comparison_svg(species: Iterable[str]) -> str:
    """Render initial dark-field visual spectra from the Stage 1 feature layer."""
    return _render_visual_rows_svg(features_for_species(species), SPECIES_NAMES)


def render_combined_svg(species: Iterable[str]) -> str:
    """Render the union of selected feature positions without intensity encoding."""
    return _render_rows_svg(
        {"combined": combined_features_for_species(species)},
        {"combined": "Combined selected lines"},
    )


def _render_absorption_rows_svg(
    rows: dict[str, list[dict[str, str]]], names: dict[str, str], *, show_identity: bool = True
) -> str:
    """Render the shared-position absorption comparison: a visible band with equal dark lines."""
    row_height = 116 if show_identity else 84
    height = (72 if show_identity else 30) + row_height * len(rows)
    gradient_stops = "".join(
        f'<stop offset="{(wavelength - WAVELENGTH_MIN_NM) / (WAVELENGTH_MAX_NM - WAVELENGTH_MIN_NM) * 100:.2f}%" '
        f'stop-color="{wavelength_to_colour(wavelength)}" />'
        for wavelength in (WAVELENGTH_MIN_NM, 440.0, 490.0, 510.0, 580.0, 645.0, WAVELENGTH_MAX_NM)
    )
    svg_rows: list[str] = []
    for index, (symbol, features) in enumerate(rows.items()):
        top = (14 if show_identity else 5) + index * row_height
        band_top = top + (43 if show_identity else 8)
        band_height = 34
        baseline = top + (85 if show_identity else 52)
        values = ", ".join(f"{float(feature['wavelength_nm']):.3f}" for feature in features)
        ticks = "".join(
            f'<line x1="{wavelength_x(tick):.2f}" y1="{baseline}" '
            f'x2="{wavelength_x(tick):.2f}" y2="{baseline + 8}" class="tick" />'
            f'<text x="{wavelength_x(tick):.2f}" y="{baseline + 27}" class="tick-label">{tick}</text>'
            for tick in range(400, 781, 100)
        )
        lines = "".join(
            f'<line x1="{wavelength_x(float(feature["wavelength_nm"])):.2f}" y1="{band_top}" '
            f'x2="{wavelength_x(float(feature["wavelength_nm"])):.2f}" y2="{band_top + band_height}" '
            f'class="absorption-line" />'
            for feature in features
        )
        identity = (
            f'<text x="18" y="{top + 19}" class="species">{escape(names[symbol])}</text>'
            f'<text x="18" y="{top + 36}" class="feature-count">{len(features)} selected features</text>'
            if show_identity
            else ""
        )
        svg_rows.append(
            f'<g aria-label="{escape(names[symbol])} absorption: dark lines at {values} nm">{identity}'
            f'<rect x="{PLOT_LEFT}" y="{band_top}" width="{PLOT_RIGHT - PLOT_LEFT}" height="{band_height}" '
            f'fill="url(#visible-spectrum-band)" class="visible-band" />'
            f'<line x1="{PLOT_LEFT}" y1="{baseline}" x2="{PLOT_RIGHT}" y2="{baseline}" class="axis" />'
            f'{ticks}{lines}</g>'
        )
    return f'''<style>
.absorption-svg {{ display: block; width: 100%; height: auto; background: #ffffff; font-family: "Source Sans Pro", Arial, sans-serif; color: #17212b; }}
.axis, .tick {{ stroke: #64748b; stroke-width: 1.3; }}
.tick-label {{ fill: #334155; font-size: 15px; text-anchor: middle; }}
.species {{ fill: #17212b; font-size: 19px; font-weight: 650; }}
.feature-count {{ fill: #475569; font-size: 13px; }}
.visible-band {{ shape-rendering: crispEdges; }}
.absorption-line {{ stroke: #111827; stroke-width: 2.2; vector-effect: non-scaling-stroke; }}
</style>
<svg class="absorption-svg" viewBox="0 0 1200 {height}" role="img" aria-label="Selected atomic absorption-line positions on the shared 380 to 780 nanometre scale">
<title>Selected atomic absorption features on a shared wavelength scale</title>
<desc>A continuous illustrative visible-spectrum band has equal dark lines at the selected wavelength positions. Line darkness and width do not encode relative strength.</desc>
<defs><linearGradient id="visible-spectrum-band" x1="0%" y1="0%" x2="100%" y2="0%">{gradient_stops}</linearGradient></defs>
{''.join(svg_rows)}
</svg>'''


def render_absorption_comparison_svg(species: Iterable[str], *, show_identity: bool = True) -> str:
    """Render separate selected-atom absorption rows on the shared Stage 1 axis."""
    return _render_absorption_rows_svg(
        absorption_features_for_species(species), SPECIES_NAMES, show_identity=show_identity
    )


def render_visual_absorption_comparison_svg(species: Iterable[str]) -> str:
    """Render the continuous visible band and dark positions without a wavelength axis."""
    rows = absorption_features_for_species(species)
    row_height = 88
    height = 20 + row_height * len(rows)
    gradient_stops = "".join(
        f'<stop offset="{(wavelength - WAVELENGTH_MIN_NM) / (WAVELENGTH_MAX_NM - WAVELENGTH_MIN_NM) * 100:.2f}%" '
        f'stop-color="{wavelength_to_colour(wavelength)}" />'
        for wavelength in (WAVELENGTH_MIN_NM, 440.0, 490.0, 510.0, 580.0, 645.0, WAVELENGTH_MAX_NM)
    )
    svg_rows: list[str] = []
    for index, (symbol, features) in enumerate(rows.items()):
        top = 10 + index * row_height
        values = ", ".join(f"{float(feature['wavelength_nm']):.3f}" for feature in features)
        lines = "".join(
            f'<line x1="{wavelength_x(float(feature["wavelength_nm"])):.2f}" y1="{top + 7}" '
            f'x2="{wavelength_x(float(feature["wavelength_nm"])):.2f}" y2="{top + 59}" class="absorption-line" />'
            for feature in features
        )
        svg_rows.append(
            f'<g aria-label="{escape(SPECIES_NAMES[symbol])} absorption: dark lines at {values} nm">'
            f'<text x="18" y="{top + 35}" class="visual-species">{escape(SPECIES_NAMES[symbol])}</text>'
            f'<rect x="{PLOT_LEFT}" y="{top}" width="{PLOT_RIGHT - PLOT_LEFT}" height="66" fill="url(#visible-spectrum-band)" />'
            f'{lines}</g>'
        )
    return f'''<style>
.visual-absorption-svg {{ display: block; width: 100%; height: auto; background: #ffffff; font-family: "Source Sans Pro", Arial, sans-serif; color: #17212b; }}
.visual-species {{ fill: #17212b; font-size: 19px; font-weight: 650; }}
.absorption-line {{ stroke: #111827; stroke-width: 2.6; vector-effect: non-scaling-stroke; }}
</style>
<svg class="visual-absorption-svg" viewBox="0 0 1200 {height}" role="img" aria-label="Selected atomic visual absorption spectra">
<title>Selected atomic visual absorption spectra</title>
<desc>Each continuous illustrative visible-spectrum band has equal dark lines at selected positions. No wavelength axis is shown.</desc>
<defs><linearGradient id="visible-spectrum-band" x1="0%" y1="0%" x2="100%" y2="0%">{gradient_stops}</linearGradient></defs>
{''.join(svg_rows)}
</svg>'''


def render_combined_absorption_svg(species: Iterable[str]) -> str:
    """Render the selected combined absorption positions without strength encoding."""
    return _render_absorption_rows_svg(
        {"combined": combined_absorption_features_for_species(species)},
        {"combined": "Combined"},
    )

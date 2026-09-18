"""Hydrogen evidence renderers for Week 01.

These views consume the established NIST-backed data layer. They deliberately do
not calculate wavelengths, model energy levels, or encode line intensity.
"""

from __future__ import annotations

from html import escape
from math import ceil, floor

from experiences.w01_spectroscopy import data, spectrum


SERIES_REGIONS = {"Lyman": "UV", "Balmer": "visible", "Paschen": "IR"}


def balmer_detail_features() -> list[dict[str, str]]:
    """Return the deliberate six-feature hydrogen detail selection."""
    return data.hydrogen_detail_features()


def transition_label(feature: dict[str, str]) -> str:
    """Return the reference transition label retained in the display metadata."""
    return f"{feature['upper_n']}→{feature['lower_n']}"


def prediction_is_in_display_range(wavelength_nm: float) -> bool:
    """Check whether a positive learner prediction can be placed on the detail axis."""
    return 0 < wavelength_nm and spectrum.WAVELENGTH_MIN_NM <= wavelength_nm <= spectrum.WAVELENGTH_MAX_NM


def series_features(series: str) -> list[dict[str, str]]:
    """Return one named NIST main-series subset without calculation."""
    if series not in SERIES_REGIONS:
        raise ValueError(f"Unknown hydrogen series: {series}")
    return [feature for feature in data.hydrogen_series_features() if feature["series"] == series]


def series_overview_bounds() -> tuple[float, float]:
    """Return rounded context bounds derived from the stored series references."""
    values = [float(feature["wavelength_nm"]) for feature in data.hydrogen_series_features()]
    return float(floor(min(values) / 10) * 10), float(ceil(max(values) / 100) * 100)


def _axis_ticks(minimum: float, maximum: float, values: tuple[float, ...], baseline: float) -> str:
    return "".join(
        f'<line x1="{_x(value, minimum, maximum):.2f}" y1="{baseline}" x2="{_x(value, minimum, maximum):.2f}" '
        f'y2="{baseline + 8}" class="tick" /><text x="{_x(value, minimum, maximum):.2f}" y="{baseline + 27}" '
        f'class="tick-label">{value:g}</text>'
        for value in values
    )


def _x(wavelength_nm: float, minimum: float, maximum: float) -> float:
    return spectrum.PLOT_LEFT + (wavelength_nm - minimum) * (spectrum.PLOT_RIGHT - spectrum.PLOT_LEFT) / (maximum - minimum)


def render_balmer_detail_svg(*, prediction_nm: float | None = None, show_transition_labels: bool = False) -> str:
    """Render six observed Balmer features, optionally with a learner prediction marker."""
    features = balmer_detail_features()
    line_top = 52
    baseline = 116
    lines = "".join(
        f'<line x1="{spectrum.wavelength_x(float(feature["wavelength_nm"])):.2f}" y1="{line_top}" '
        f'x2="{spectrum.wavelength_x(float(feature["wavelength_nm"])):.2f}" y2="{baseline}" '
        f'stroke="{spectrum.wavelength_to_colour(float(feature["wavelength_nm"]))}" class="spectral-line" />'
        for feature in features
    )
    labels = ""
    if show_transition_labels:
        labels = "".join(
            f'<text x="{spectrum.wavelength_x(float(feature["wavelength_nm"])):.2f}" '
            f'y="{22 if index % 2 == 0 else 41}" class="transition-label">{transition_label(feature)}</text>'
            for index, feature in enumerate(features)
        )
    prediction = ""
    description = "Six selected observed hydrogen Balmer features on a shared wavelength scale."
    if prediction_nm is not None:
        marker_x = spectrum.wavelength_x(prediction_nm)
        text_anchor = "end" if marker_x > spectrum.PLOT_RIGHT - 150 else "start"
        text_x = marker_x - 8 if text_anchor == "end" else marker_x + 8
        prediction = (
            f'<line x1="{marker_x:.2f}" y1="{line_top - 4}" x2="{marker_x:.2f}" y2="{baseline}" '
            f'class="prediction-marker" /><circle cx="{marker_x:.2f}" cy="{line_top - 4}" r="4" class="prediction-dot" />'
            f'<text x="{text_x:.2f}" y="{line_top - 13}" text-anchor="{text_anchor}" class="prediction-label">'
            f'Your prediction: {prediction_nm:.3f} nm</text>'
        )
        description += f" Learner prediction is marked at {prediction_nm:.3f} nm."
    ticks = "".join(
        f'<line x1="{spectrum.wavelength_x(tick):.2f}" y1="{baseline}" x2="{spectrum.wavelength_x(tick):.2f}" '
        f'y2="{baseline + 8}" class="tick" /><text x="{spectrum.wavelength_x(tick):.2f}" '
        f'y="{baseline + 27}" class="tick-label">{tick}</text>'
        for tick in range(400, 781, 100)
    )
    return f'''<style>
.hydrogen-detail-svg {{ display: block; width: 100%; height: auto; background: #ffffff; font-family: "Source Sans Pro", Arial, sans-serif; }}
.axis, .tick {{ stroke: #64748b; stroke-width: 1.3; }}
.tick-label {{ fill: #334155; font-size: 15px; text-anchor: middle; }}
.species {{ fill: #17212b; font-size: 19px; font-weight: 650; }}
.feature-count {{ fill: #475569; font-size: 13px; }}
.spectral-line {{ stroke-width: 1.1; vector-effect: non-scaling-stroke; }}
.transition-label {{ fill: #17212b; font-size: 14px; font-weight: 650; text-anchor: middle; }}
.prediction-marker {{ stroke: #111827; stroke-width: 2.4; stroke-dasharray: 5 3; vector-effect: non-scaling-stroke; }}
.prediction-dot {{ fill: #ffffff; stroke: #111827; stroke-width: 2.2; vector-effect: non-scaling-stroke; }}
.prediction-label {{ fill: #111827; font-size: 13px; font-weight: 650; }}
</style>
<svg class="hydrogen-detail-svg" viewBox="0 0 1200 158" role="img" aria-label="Observed hydrogen Balmer features and optional learner prediction">
<title>Observed hydrogen Balmer features</title>
<desc>{escape(description)}</desc>
<text x="18" y="72" class="species">Hydrogen</text>
<text x="18" y="92" class="feature-count">6 selected Balmer features</text>
<line x1="{spectrum.PLOT_LEFT}" y1="{baseline}" x2="{spectrum.PLOT_RIGHT}" y2="{baseline}" class="axis" />
{ticks}{lines}{labels}{prediction}
</svg>'''


def render_series_overview_svg() -> str:
    """Render location context for NIST Lyman, Balmer, and Paschen reference rows."""
    minimum, maximum = series_overview_bounds()
    rows = (("Lyman", 70), ("Balmer", 112), ("Paschen", 154))
    region_bands = (
        (minimum, 380.0, "#eee9fb", "UV"),
        (380.0, 780.0, "#fff5c7", "visible"),
        (780.0, maximum, "#e4f4f3", "IR"),
    )
    bands = "".join(
        f'<rect x="{_x(start, minimum, maximum):.2f}" y="24" '
        f'width="{_x(end, minimum, maximum) - _x(start, minimum, maximum):.2f}" height="154" fill="{colour}" />'
        f'<text x="{(_x(start, minimum, maximum) + _x(end, minimum, maximum)) / 2:.2f}" y="42" class="region-label">{label}</text>'
        for start, end, colour, label in region_bands
    )
    markers = "".join(
        f'<text x="18" y="{y + 5}" class="series-label">{series} · {SERIES_REGIONS[series]}</text>'
        + "".join(
            f'<line x1="{_x(float(feature["wavelength_nm"]), minimum, maximum):.2f}" y1="{y - 13}" '
            f'x2="{_x(float(feature["wavelength_nm"]), minimum, maximum):.2f}" y2="{y + 13}" class="series-marker" />'
            for feature in series_features(series)
        )
        for series, y in rows
    )
    tick_values = (minimum, 500.0, 1000.0, 1500.0, maximum)
    return f'''<style>
.series-overview-svg {{ display: block; width: 100%; height: auto; font-family: "Source Sans Pro", Arial, sans-serif; }}
.overview-axis {{ stroke: #475569; stroke-width: 1.3; }}
.overview-tick {{ stroke: #64748b; stroke-width: 1.2; }}
.overview-tick-label, .series-label {{ fill: #17212b; font-size: 14px; }}
.overview-tick-label {{ text-anchor: middle; }}
.series-label {{ font-weight: 650; }}
.region-label {{ fill: #17212b; font-size: 13px; font-weight: 700; text-anchor: middle; letter-spacing: 0.06em; }}
.series-marker {{ stroke: #17212b; stroke-width: 2; vector-effect: non-scaling-stroke; }}
</style>
<svg class="series-overview-svg" viewBox="0 0 1200 218" role="img" aria-label="Hydrogen Lyman ultraviolet, Balmer visible, and Paschen infrared series locations">
<title>Where selected hydrogen series occur</title>
<desc>Rows locate selected Lyman features in ultraviolet, Balmer features in visible light, and Paschen features in infrared. The markers have uniform geometry and do not encode intensity.</desc>
{bands}{markers}
<line x1="{spectrum.PLOT_LEFT}" y1="188" x2="{spectrum.PLOT_RIGHT}" y2="188" class="overview-axis" />
{''.join(f'<line x1="{_x(value, minimum, maximum):.2f}" y1="188" x2="{_x(value, minimum, maximum):.2f}" y2="196" class="overview-tick" /><text x="{_x(value, minimum, maximum):.2f}" y="213" class="overview-tick-label">{value:g}</text>' for value in tick_values)}
</svg>'''


def _series_detail_bounds(features: list[dict[str, str]]) -> tuple[float, float]:
    values = [float(feature["wavelength_nm"]) for feature in features]
    spread = max(values) - min(values)
    padding = max(spread * 0.12, 5.0)
    return floor((min(values) - padding) / 5) * 5, ceil((max(values) + padding) / 5) * 5


def render_series_detail_svg(series: str) -> str:
    """Render one selected reference series on a readable local wavelength scale."""
    features = series_features(series)
    minimum, maximum = _series_detail_bounds(features)
    baseline = 105
    line_top = 43
    markers = "".join(
        f'<line x1="{_x(float(feature["wavelength_nm"]), minimum, maximum):.2f}" y1="{line_top}" '
        f'x2="{_x(float(feature["wavelength_nm"]), minimum, maximum):.2f}" y2="{baseline}" class="series-detail-line" />'
        f'<text x="{_x(float(feature["wavelength_nm"]), minimum, maximum):.2f}" y="{24 if index % 2 == 0 else 39}" '
        f'class="member-label">{escape(feature["member"])} {float(feature["wavelength_nm"]):g}</text>'
        for index, feature in enumerate(features)
    )
    tick_values = tuple(round(minimum + index * (maximum - minimum) / 4, 1) for index in range(5))
    return f'''<style>
.series-detail-svg {{ display: block; width: 100%; height: auto; background: #ffffff; font-family: "Source Sans Pro", Arial, sans-serif; }}
.axis, .tick {{ stroke: #64748b; stroke-width: 1.3; }}
.tick-label {{ fill: #334155; font-size: 14px; text-anchor: middle; }}
.series-detail-line {{ stroke: #17212b; stroke-width: 2; vector-effect: non-scaling-stroke; }}
.member-label {{ fill: #17212b; font-size: 12px; text-anchor: middle; }}
</style>
<svg class="series-detail-svg" viewBox="0 0 1200 150" role="img" aria-label="Selected {series} hydrogen reference features in the {SERIES_REGIONS[series]} region">
<title>{series} hydrogen reference features</title>
<desc>Five selected NIST reference wavelengths on a local {SERIES_REGIONS[series]} scale. Lines have uniform geometry and do not encode intensity.</desc>
<line x1="{spectrum.PLOT_LEFT}" y1="{baseline}" x2="{spectrum.PLOT_RIGHT}" y2="{baseline}" class="axis" />
{_axis_ticks(minimum, maximum, tick_values, baseline)}{markers}
</svg>'''

"""Position-mapping renderers for the Week 01 Read the spectrum surface.

Both representations consume the same six NIST-backed Balmer features and the
shared Stage 1 wavelength geometry. Equal graph peaks are illustrative only.
Learner-facing labels deliberately identify features without exposing the
Hydrogen transition or wavelength answer key.
"""

from __future__ import annotations

from html import escape

from experiences.w01_spectroscopy import hydrogen, spectrum


ILLUSTRATIVE_PEAK_HEIGHT = 88.0
FEATURE_LABELS = ("Line A", "Line B", "Line C", "Line D", "Line E", "Line F")
EXAMPLE_FEATURE_LABEL = "Line F"
PLOT_TOP = 94.0
PLOT_BASELINE = 210.0
SVG_HEIGHT = 290.0


def balmer_features() -> list[dict[str, str]]:
    """Return the established six hydrogen features without new scientific data."""
    return hydrogen.balmer_detail_features()


def labelled_features() -> dict[str, dict[str, str]]:
    """Assign stable neutral labels in increasing wavelength order."""
    ordered_features = sorted(balmer_features(), key=lambda feature: float(feature["wavelength_nm"]))
    return dict(zip(FEATURE_LABELS, ordered_features, strict=True))


def feature_options() -> list[str]:
    """Return the neutral learner-facing feature identifiers."""
    return list(FEATURE_LABELS)


def feature_for_label(label: str) -> dict[str, str]:
    """Resolve a neutral feature identifier to its stored reference feature."""
    try:
        return labelled_features()[label]
    except KeyError as error:
        raise ValueError(f"Unknown hydrogen feature label: {label}") from error


def _ticks(baseline: float) -> str:
    return "".join(
        f'<line x1="{spectrum.wavelength_x(tick):.2f}" y1="{baseline}" x2="{spectrum.wavelength_x(tick):.2f}" y2="{baseline + 10}" class="tick" />'
        f'<text x="{spectrum.wavelength_x(tick):.2f}" y="{baseline + 34}" class="tick-label">{tick}</text>'
        for tick in range(400, 781, 100)
    )


def _guide(
    feature: dict[str, str],
    *,
    label: str,
    label_y: float,
    line_top: float,
    baseline: float,
    css_class: str,
    label_offset_x: float = 0.0,
    text_anchor: str = "middle",
) -> str:
    x = spectrum.wavelength_x(float(feature["wavelength_nm"]))
    return (
        f'<line x1="{x:.2f}" y1="{line_top}" x2="{x:.2f}" y2="{baseline}" class="{css_class}" />'
        f'<text x="{x + label_offset_x:.2f}" y="{label_y}" text-anchor="{text_anchor}" '
        f'class="guide-label">{escape(label)}</text>'
    )


def _guides(selected_feature_label: str, *, baseline: float) -> str:
    """Render independent guides, or offset labels when both guides share a line."""
    example = feature_for_label(EXAMPLE_FEATURE_LABEL)
    selected = feature_for_label(selected_feature_label)
    if selected_feature_label == EXAMPLE_FEATURE_LABEL:
        return (
            _guide(
                example,
                label="Example line",
                label_y=30,
                line_top=76,
                baseline=baseline,
                css_class="trace-example",
                label_offset_x=-16,
                text_anchor="end",
            )
            + _guide(
                selected,
                label="Your trace",
                label_y=58,
                line_top=82,
                baseline=baseline,
                css_class="trace-selected",
                label_offset_x=16,
                text_anchor="start",
            )
        )
    return (
        _guide(example, label="Example line", label_y=30, line_top=76, baseline=baseline, css_class="trace-example")
        + _guide(selected, label="Your trace", label_y=58, line_top=82, baseline=baseline, css_class="trace-selected")
    )


def render_line_spectrum_svg(selected_feature_label: str) -> str:
    """Render the familiar six-line spectrum with one example and one learner trace."""
    features = balmer_features()
    lines = "".join(
        f'<line x1="{spectrum.wavelength_x(float(feature["wavelength_nm"])):.2f}" y1="{PLOT_TOP}" '
        f'x2="{spectrum.wavelength_x(float(feature["wavelength_nm"])):.2f}" y2="{PLOT_BASELINE}" '
        f'stroke="{spectrum.wavelength_to_colour(float(feature["wavelength_nm"]))}" class="spectral-line" />'
        for feature in features
    )
    return f'''<style>
.read-line-svg {{ display:block; width:100%; height:auto; font-family:"Source Sans Pro",Arial,sans-serif; }}
.axis,.tick {{ stroke:#64748b; stroke-width:1.5; }} .tick-label {{ fill:#334155; font-size:19px; text-anchor:middle; }}
.spectral-line {{ stroke-width:2.6; vector-effect:non-scaling-stroke; }}
.trace-example {{ stroke:#111827; stroke-width:2.5; stroke-dasharray:6 4; vector-effect:non-scaling-stroke; }}
.trace-selected {{ stroke:#8A68C8; stroke-width:3; stroke-dasharray:4 4; vector-effect:non-scaling-stroke; }}
.guide-label {{ fill:#17212b; font-size:20px; font-weight:650; }} .axis-label {{ fill:#17212b; font-size:22px; font-weight:650; text-anchor:middle; }}
</style><svg class="read-line-svg" viewBox="0 0 1200 {SVG_HEIGHT}" role="img" aria-label="Six selected hydrogen lines on a wavelength axis">
<title>Hydrogen line spectrum</title><desc>Six selected hydrogen features share a 380 to 780 nanometre wavelength axis. One guide marks the example line and another marks the learner trace.</desc>
<line x1="{spectrum.PLOT_LEFT}" y1="{PLOT_BASELINE}" x2="{spectrum.PLOT_RIGHT}" y2="{PLOT_BASELINE}" class="axis" />{_ticks(PLOT_BASELINE)}{lines}
{_guides(selected_feature_label, baseline=PLOT_BASELINE)}
<text x="{(spectrum.PLOT_LEFT + spectrum.PLOT_RIGHT) / 2}" y="280" class="axis-label">Wavelength / nm</text></svg>'''


def render_intensity_graph_svg(selected_feature_label: str) -> str:
    """Render equal illustrative peaks at exactly the stored line coordinates."""
    features = balmer_features()
    baseline, peak = PLOT_BASELINE, PLOT_BASELINE - ILLUSTRATIVE_PEAK_HEIGHT
    peaks = "".join(
        f'<path d="M {spectrum.wavelength_x(float(feature["wavelength_nm"])) - 10:.2f} {baseline} '
        f'L {spectrum.wavelength_x(float(feature["wavelength_nm"])):.2f} {peak} '
        f'L {spectrum.wavelength_x(float(feature["wavelength_nm"])) + 10:.2f} {baseline}" class="illustrative-peak" />'
        for feature in features
    )
    return f'''<style>
.intensity-graph-svg {{ display:block; width:100%; height:auto; font-family:"Source Sans Pro",Arial,sans-serif; }}
.axis,.tick {{ stroke:#64748b; stroke-width:1.5; }} .tick-label {{ fill:#334155; font-size:19px; text-anchor:middle; }}
.illustrative-peak {{ fill:none; stroke:#3F61C4; stroke-width:2.8; vector-effect:non-scaling-stroke; }}
.trace-example {{ stroke:#111827; stroke-width:2.5; stroke-dasharray:6 4; vector-effect:non-scaling-stroke; }}
.trace-selected {{ stroke:#8A68C8; stroke-width:3; stroke-dasharray:4 4; vector-effect:non-scaling-stroke; }}
.guide-label {{ fill:#17212b; font-size:20px; font-weight:650; }} .axis-label {{ fill:#17212b; font-size:22px; font-weight:650; text-anchor:middle; }}
</style><svg class="intensity-graph-svg" viewBox="0 0 1200 {SVG_HEIGHT}" role="img" aria-label="Illustrative equal-height hydrogen intensity peaks on a wavelength axis">
<title>Hydrogen intensity versus wavelength</title><desc>Six equal-height illustrative peaks are centred at the same wavelengths as the selected hydrogen features. Peak height is not measured intensity.</desc>
<line x1="{spectrum.PLOT_LEFT}" y1="{baseline}" x2="{spectrum.PLOT_RIGHT}" y2="{baseline}" class="axis" /><line x1="{spectrum.PLOT_LEFT}" y1="{peak - 5}" x2="{spectrum.PLOT_LEFT}" y2="{baseline}" class="axis" />{_ticks(baseline)}{peaks}
{_guides(selected_feature_label, baseline=baseline)}
<text x="30" y="{(peak + baseline) / 2}" transform="rotate(-90 30 {(peak + baseline) / 2})" class="axis-label">Intensity</text>
<text x="{(spectrum.PLOT_LEFT + spectrum.PLOT_RIGHT) / 2}" y="280" class="axis-label">Wavelength / nm</text></svg>'''

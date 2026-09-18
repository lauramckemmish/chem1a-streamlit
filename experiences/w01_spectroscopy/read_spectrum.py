"""Position-mapping renderers for the Week 01 Read the spectrum surface.

Both representations consume the same six NIST-backed Balmer features and the
shared Stage 1 wavelength geometry. Equal graph peaks are illustrative only.
"""

from __future__ import annotations

from html import escape

from experiences.w01_spectroscopy import hydrogen, spectrum


ILLUSTRATIVE_PEAK_HEIGHT = 64.0
EXAMPLE_TRANSITION = "3→2"


def balmer_features() -> list[dict[str, str]]:
    """Return the established six hydrogen features without new scientific data."""
    return hydrogen.balmer_detail_features()


def transition_options() -> list[str]:
    """Return selectable non-example transitions for a learner-driven trace."""
    return [hydrogen.transition_label(feature) for feature in balmer_features() if hydrogen.transition_label(feature) != EXAMPLE_TRANSITION]


def feature_for_transition(transition: str) -> dict[str, str]:
    """Resolve an established transition label to its reference feature."""
    for feature in balmer_features():
        if hydrogen.transition_label(feature) == transition:
            return feature
    raise ValueError(f"Unknown Balmer transition: {transition}")


def _ticks(baseline: float) -> str:
    return "".join(
        f'<line x1="{spectrum.wavelength_x(tick):.2f}" y1="{baseline}" x2="{spectrum.wavelength_x(tick):.2f}" y2="{baseline + 8}" class="tick" /><text x="{spectrum.wavelength_x(tick):.2f}" y="{baseline + 27}" class="tick-label">{tick}</text>'
        for tick in range(400, 781, 100)
    )


def _guide(feature: dict[str, str], *, label: str, line_top: float, baseline: float, css_class: str) -> str:
    wavelength = float(feature["wavelength_nm"])
    x = spectrum.wavelength_x(wavelength)
    return f'<line x1="{x:.2f}" y1="{line_top}" x2="{x:.2f}" y2="{baseline}" class="{css_class}" /><text x="{x:.2f}" y="24" class="guide-label">{escape(label)} · {wavelength:.3f} nm</text>'


def render_line_spectrum_svg(selected_transition: str) -> str:
    """Render the familiar six-line Balmer spectrum with two explicit traces."""
    features = balmer_features()
    example, selected = feature_for_transition(EXAMPLE_TRANSITION), feature_for_transition(selected_transition)
    top, baseline = 52.0, 116.0
    lines = "".join(
        f'<line x1="{spectrum.wavelength_x(float(feature["wavelength_nm"])):.2f}" y1="{top}" x2="{spectrum.wavelength_x(float(feature["wavelength_nm"])):.2f}" y2="{baseline}" stroke="{spectrum.wavelength_to_colour(float(feature["wavelength_nm"]))}" class="spectral-line" />'
        for feature in features
    )
    return f'''<style>
.read-line-svg {{ display:block; width:100%; height:auto; font-family:"Source Sans Pro",Arial,sans-serif; }} .axis,.tick {{ stroke:#64748b; stroke-width:1.3; }} .tick-label {{ fill:#334155; font-size:15px; text-anchor:middle; }} .spectral-line {{ stroke-width:1.6; vector-effect:non-scaling-stroke; }} .trace-example {{ stroke:#111827; stroke-width:2; stroke-dasharray:5 3; }} .trace-selected {{ stroke:#8A68C8; stroke-width:2.4; stroke-dasharray:3 3; }} .guide-label {{ fill:#17212b; font-size:13px; font-weight:650; text-anchor:middle; }}
</style><svg class="read-line-svg" viewBox="0 0 1200 158" role="img" aria-label="Six selected hydrogen Balmer lines on a wavelength axis"><title>Hydrogen line spectrum</title><desc>Six selected Balmer lines share a 380 to 780 nanometre wavelength axis. The solid dashed guide is the example mapping and the dotted guide is the learner-selected trace.</desc><line x1="{spectrum.PLOT_LEFT}" y1="{baseline}" x2="{spectrum.PLOT_RIGHT}" y2="{baseline}" class="axis" />{_ticks(baseline)}{lines}{_guide(example, label="Example 3→2", line_top=34, baseline=baseline, css_class="trace-example")}{_guide(selected, label=f"Trace {selected_transition}", line_top=34, baseline=baseline, css_class="trace-selected")}<text x="{(spectrum.PLOT_LEFT + spectrum.PLOT_RIGHT) / 2}" y="153" class="guide-label">Wavelength / nm</text></svg>'''


def render_intensity_graph_svg(selected_transition: str) -> str:
    """Render equal illustrative peaks at exactly the Balmer line coordinates."""
    features = balmer_features()
    example, selected = feature_for_transition(EXAMPLE_TRANSITION), feature_for_transition(selected_transition)
    baseline, peak = 116.0, 116.0 - ILLUSTRATIVE_PEAK_HEIGHT
    peaks = "".join(
        f'<path d="M {spectrum.wavelength_x(float(feature["wavelength_nm"])) - 8:.2f} {baseline} L {spectrum.wavelength_x(float(feature["wavelength_nm"])):.2f} {peak} L {spectrum.wavelength_x(float(feature["wavelength_nm"])) + 8:.2f} {baseline}" class="illustrative-peak" />'
        for feature in features
    )
    return f'''<style>
.intensity-graph-svg {{ display:block; width:100%; height:auto; font-family:"Source Sans Pro",Arial,sans-serif; }} .axis,.tick {{ stroke:#64748b; stroke-width:1.3; }} .tick-label {{ fill:#334155; font-size:15px; text-anchor:middle; }} .illustrative-peak {{ fill:none; stroke:#3F61C4; stroke-width:2.2; vector-effect:non-scaling-stroke; }} .trace-example {{ stroke:#111827; stroke-width:2; stroke-dasharray:5 3; }} .trace-selected {{ stroke:#8A68C8; stroke-width:2.4; stroke-dasharray:3 3; }} .guide-label {{ fill:#17212b; font-size:13px; font-weight:650; text-anchor:middle; }}
</style><svg class="intensity-graph-svg" viewBox="0 0 1200 158" role="img" aria-label="Illustrative equal-height hydrogen intensity peaks on a wavelength axis"><title>Hydrogen intensity versus wavelength</title><desc>Six equal-height illustrative peaks are centred at the same wavelengths as the selected Balmer lines. Peak height is not measured intensity.</desc><line x1="{spectrum.PLOT_LEFT}" y1="{baseline}" x2="{spectrum.PLOT_RIGHT}" y2="{baseline}" class="axis" /><line x1="{spectrum.PLOT_LEFT}" y1="32" x2="{spectrum.PLOT_LEFT}" y2="{baseline}" class="axis" />{_ticks(baseline)}{peaks}{_guide(example, label="Example 3→2", line_top=34, baseline=baseline, css_class="trace-example")}{_guide(selected, label=f"Trace {selected_transition}", line_top=34, baseline=baseline, css_class="trace-selected")}<text x="28" y="82" transform="rotate(-90 28 82)" class="guide-label">Intensity</text><text x="{(spectrum.PLOT_LEFT + spectrum.PLOT_RIGHT) / 2}" y="153" class="guide-label">Wavelength / nm</text></svg>'''

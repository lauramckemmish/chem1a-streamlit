"""Illustrative intensity translations for the Explore spectra position data.

Stored reference wavelengths remain the evidence. Gaussian width, peak height,
and dip depth in this module are display geometry only, not measured properties.
"""

from __future__ import annotations

from math import exp

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from experiences.w01_spectroscopy import spectrum


ILLUSTRATIVE_SIGMA_NM = 0.8
ILLUSTRATIVE_PEAK_HEIGHT = 1.0
ILLUSTRATIVE_DIP_DEPTH = 0.35
SAMPLE_STEP_NM = 0.1
PLOTLY_CONFIG = {
    "scrollZoom": False,
    "displaylogo": False,
    "modeBarButtonsToRemove": [
        "pan2d", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d",
        "hoverClosestCartesian", "hoverCompareCartesian", "toggleSpikelines",
    ],
}


def sample_wavelengths() -> list[float]:
    """Return a display grid that explicitly retains every stored line centre."""
    grid = [
        spectrum.WAVELENGTH_MIN_NM + index * SAMPLE_STEP_NM
        for index in range(round((spectrum.WAVELENGTH_MAX_NM - spectrum.WAVELENGTH_MIN_NM) / SAMPLE_STEP_NM) + 1)
    ]
    centres = [
        float(feature["wavelength_nm"])
        for feature in spectrum.features_for_species(spectrum.SPECIES_ORDER).values()
        for feature in feature
    ]
    return sorted(set(grid + centres))


def gaussian(wavelength_nm: float, centre_nm: float) -> float:
    """Return a unit illustrative Gaussian centred exactly on a stored wavelength."""
    return exp(-0.5 * ((wavelength_nm - centre_nm) / ILLUSTRATIVE_SIGMA_NM) ** 2)


def illustrative_signal(features: list[dict[str, str]], spectrum_type: str) -> tuple[list[float], list[float]]:
    """Translate selected positions into equal illustrative peaks or dips."""
    if spectrum_type not in {"Emission", "Absorption"}:
        raise ValueError(f"Unknown spectrum type: {spectrum_type}")
    wavelengths = sample_wavelengths()
    centres = [float(feature["wavelength_nm"]) for feature in features]
    contributions = [sum(gaussian(wavelength, centre) for centre in centres) for wavelength in wavelengths]
    if spectrum_type == "Emission":
        return wavelengths, [ILLUSTRATIVE_PEAK_HEIGHT * value for value in contributions]
    return wavelengths, [1.0 - ILLUSTRATIVE_DIP_DEPTH * value for value in contributions]


def figure_for_species(species: list[str], spectrum_type: str, *, show_species_labels: bool = True) -> go.Figure:
    """Render one shared-axis row per selected species without combining their data."""
    rows = spectrum.features_for_species(species)
    figure = make_subplots(rows=len(rows), cols=1, shared_xaxes=True, vertical_spacing=0.05)
    for index, (symbol, features) in enumerate(rows.items(), start=1):
        wavelengths, signal = illustrative_signal(features, spectrum_type)
        figure.add_trace(
            go.Scatter(
                x=wavelengths,
                y=signal,
                mode="lines",
                name=spectrum.SPECIES_NAMES[symbol],
                line={"color": "#3F61C4", "width": 2},
                hovertemplate=(
                    f"<b>{spectrum.SPECIES_NAMES[symbol]} {spectrum_type.lower()}</b><br>"
                    "Wavelength: %{x:.3f} nm<extra></extra>"
                ),
            ),
            row=index,
            col=1,
        )
        figure.update_yaxes(
            showticklabels=False,
            zeroline=False,
            showgrid=False,
            row=index,
            col=1,
        )
        if show_species_labels:
            axis_reference = "y domain" if index == 1 else f"y{index} domain"
            figure.add_annotation(
                xref="paper",
                yref=axis_reference,
                x=-0.02,
                y=0.5,
                text=spectrum.SPECIES_NAMES[symbol],
                showarrow=False,
                xanchor="right",
                font={"color": "#17212b", "size": 13},
            )
        figure.update_xaxes(
            range=[spectrum.WAVELENGTH_MIN_NM, spectrum.WAVELENGTH_MAX_NM],
            showgrid=True,
            gridcolor="#E5E7EB",
            showticklabels=index == len(rows),
            row=index,
            col=1,
        )
    figure.update_xaxes(
        title_text="Wavelength / nm",
        row=len(rows),
        col=1,
    )
    figure.update_layout(
        height=max(170, 130 * len(rows)),
        dragmode="zoom",
        hovermode="closest",
        template="plotly_white",
        showlegend=False,
        margin={"l": 100, "r": 25, "t": 12, "b": 45},
    )
    return figure

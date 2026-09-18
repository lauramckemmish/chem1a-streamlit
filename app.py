import streamlit as st

from chem1a_ui import apply_shared_visual_system, compare_prompt, hard_reveal, stage_tabs
from experiences.w01_spectroscopy import hydrogen, spectrum


def remember_explore_control(control_key: str) -> None:
    """Keep Explore controls available while the learner temporarily visits Hydrogen."""
    st.session_state[f"saved_{control_key}"] = st.session_state[control_key]


def explore_control_value(control_key: str, default: bool) -> bool:
    """Read a persisted Explore control value without changing the control's meaning."""
    return bool(st.session_state.get(f"saved_{control_key}", default))


def render_explore_spectra() -> None:
    """Render the established first spectroscopy phenomenon surface."""
    st.header("Explore atomic spectra")
    st.write("Select atoms to add their selected prominent lines. Every view uses the same wavelength scale.")

    with st.container(key="chem1a_stage_controls"):
        st.markdown('<p class="chem1a-control-label">Atoms to compare</p>', unsafe_allow_html=True)
        atom_columns = (*st.columns(3), *st.columns(3))
        selected_species = [
            symbol
            for column, symbol in zip(atom_columns, spectrum.SPECIES_ORDER)
            if column.checkbox(
                spectrum.SPECIES_NAMES[symbol],
                value=explore_control_value(f"atom_{symbol}", symbol in spectrum.DEFAULT_SELECTED_SPECIES),
                key=f"atom_{symbol}",
                on_change=remember_explore_control,
                args=(f"atom_{symbol}",),
            )
        ]

    if selected_species:
        st.markdown(spectrum.render_comparison_svg(selected_species), unsafe_allow_html=True)
        st.caption("Colour is an illustrative wavelength cue. The labelled horizontal position is the evidence to compare.")
        if "Na" in selected_species:
            st.caption("Sodium includes two selected lines at 588.995 nm and 589.592 nm; on this shared scale they sit very close together.")
        compare_prompt("What changes? What stays the same?")

        if hard_reveal(
            "Return to these same atoms and compare their absorption features.",
            key="absorption",
            reveal_label="Reveal absorption spectra",
        ):
            st.caption("This simplified view compares line positions. Relative line strength is not represented.")
            for symbol in selected_species:
                st.markdown(f"**{spectrum.SPECIES_NAMES[symbol]} — emission**")
                st.markdown(spectrum.render_comparison_svg([symbol]), unsafe_allow_html=True)
                st.markdown(f"**{spectrum.SPECIES_NAMES[symbol]} — absorption**")
                st.markdown(spectrum.render_absorption_comparison_svg([symbol]), unsafe_allow_html=True)
            compare_prompt(
                "What do you notice about where the absorption and emission lines appear?",
                key="chem1a_absorption_prompt",
            )
    else:
        st.info("Select an atom to begin.")


def render_hydrogen() -> None:
    """Render the spectral-evidence surface learners revisit after paper-based reasoning."""
    st.header("Hydrogen")
    st.write("Look more closely at hydrogen. This view includes six selected Balmer lines.")

    prediction_column, action_column = st.columns((3, 1))
    predicted_wavelength = prediction_column.number_input(
        "Your predicted wavelength (nm)",
        value=None,
        step=0.1,
        placeholder="e.g. 656.3",
        key="hydrogen_prediction_input",
    )
    plot_prediction = action_column.button("Plot my prediction", key="plot_hydrogen_prediction")
    if plot_prediction:
        st.session_state.pop("hydrogen_prediction_nm", None)
        if predicted_wavelength is None:
            st.info("Enter a wavelength in nm to place your prediction on the spectrum.")
        elif not hydrogen.prediction_is_in_display_range(float(predicted_wavelength)):
            st.info("This prediction is outside the displayed 380–780 nm spectrum.")
        else:
            st.session_state["hydrogen_prediction_nm"] = float(predicted_wavelength)

    show_transition_labels = st.checkbox("Show transition labels", value=False, key="show_hydrogen_transition_labels")
    st.markdown(
        hydrogen.render_balmer_detail_svg(
            prediction_nm=st.session_state.get("hydrogen_prediction_nm"),
            show_transition_labels=show_transition_labels,
        ),
        unsafe_allow_html=True,
    )
    st.caption("Observed lines have uniform geometry here: position is the evidence, not relative line strength.")
    compare_prompt("Does your prediction match an observed line?", key="chem1a_hydrogen_prediction_prompt")

    with st.expander("See more of hydrogen", expanded=False):
        st.write("Visible Balmer lines are only part of the hydrogen spectrum.")
        st.markdown("**Where the selected series occur**")
        st.markdown(hydrogen.render_series_overview_svg(), unsafe_allow_html=True)
        st.caption("The overview locates the series. Use the local views below to inspect selected reference lines.")

        series_columns = st.columns(3)
        selected_series = [
            series
            for column, series, default in zip(
                series_columns,
                ("Lyman", "Balmer", "Paschen"),
                (False, True, False),
            )
            if column.checkbox(f"{series} · {hydrogen.SERIES_REGIONS[series]}", value=default, key=f"series_{series}")
        ]
        for series in selected_series:
            st.markdown(f"**{series} · {hydrogen.SERIES_REGIONS[series]}**")
            st.markdown(hydrogen.render_series_detail_svg(series), unsafe_allow_html=True)


st.set_page_config(page_title="CHEM 1A — Spectroscopy", layout="wide")
apply_shared_visual_system()

with st.sidebar:
    with st.container(key="chem1a_sidebar_brand"):
        st.markdown("### CHEM 1A")
        st.caption("Week 01 · Spectroscopy")
    with st.container(key="chem1a_sidebar_source"):
        st.markdown("**Scientific source**")
        st.caption("Bounded NIST atomic-spectroscopy references")
        st.caption("Selected teaching features; provenance is recorded in this repository.")

st.title("CHEM 1A")
st.subheader("Week 01 — Spectroscopy")
explore_tab, hydrogen_tab = stage_tabs(
    ["Explore spectra", "Hydrogen"],
    key="spectroscopy_stage_tabs",
)
with explore_tab:
    render_explore_spectra()
with hydrogen_tab:
    render_hydrogen()

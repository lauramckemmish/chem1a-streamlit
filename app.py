import streamlit as st

from chem1a_ui import apply_shared_visual_system, compare_prompt, stage_selector
from experiences.atomic_trends import view as atomic_trends
from experiences.w01_spectroscopy import hydrogen, intensity, spectrum


EXPLORE_DEFAULT_SELECTED_SPECIES = spectrum.SPECIES_ORDER
EXPLORE_SPECTRUM_TYPES = ("Emission", "Absorption")
EXPLORE_REPRESENTATIONS = ("Visual spectrum", "Wavelength spectrum", "Intensity vs wavelength")


def remember_explore_control(control_key: str) -> None:
    """Keep Explore controls available while the learner temporarily visits Hydrogen."""
    st.session_state[f"saved_{control_key}"] = st.session_state[control_key]


def explore_control_value(control_key: str, default: bool) -> bool:
    """Read a persisted Explore control value without changing the control's meaning."""
    return bool(st.session_state.get(f"saved_{control_key}", default))


def hydrogen_evidence_revealed() -> bool:
    """Return the persistent prediction-first evidence state for Hydrogen."""
    return bool(st.session_state.setdefault("hydrogen_evidence_revealed", False))


def render_explore_representation(
    representation: str, selected_species: list[str], spectrum_type: str
) -> None:
    """Render one existing representation for one selected spectrum type."""
    if representation == "Visual spectrum":
        visual = (
            spectrum.render_visual_comparison_svg
            if spectrum_type == "Emission"
            else spectrum.render_visual_absorption_comparison_svg
        )
        st.markdown(visual(selected_species), unsafe_allow_html=True)
    elif representation == "Wavelength spectrum":
        quantitative = (
            spectrum.render_quantitative_emission_svg
            if spectrum_type == "Emission"
            else spectrum.render_quantitative_absorption_svg
        )
        st.markdown(quantitative(selected_species), unsafe_allow_html=True)
    else:
        st.plotly_chart(
            intensity.figure_for_species(selected_species, spectrum_type),
            width="stretch",
            config=intensity.PLOTLY_CONFIG,
        )


def render_explore_evidence(
    selected_species: list[str], selected_spectrum_types: set[str], selected_representations: set[str], arrangement: str
) -> None:
    """Compose the established renderers by the learner's chosen comparison dimension."""
    if arrangement == "Representation":
        for representation in EXPLORE_REPRESENTATIONS:
            if representation not in selected_representations:
                continue
            if representation == "Wavelength spectrum":
                st.markdown("#### Line positions")
                st.markdown(spectrum.render_quantitative_line_positions_svg(selected_species), unsafe_allow_html=True)
                continue
            st.markdown(f"#### {representation}")
            for spectrum_type in EXPLORE_SPECTRUM_TYPES:
                if spectrum_type in selected_spectrum_types:
                    if len(selected_spectrum_types) > 1:
                        st.markdown(f"**{spectrum_type}**")
                    render_explore_representation(representation, selected_species, spectrum_type)
    else:
        for symbol in selected_species:
            st.markdown(f"#### {spectrum.SPECIES_NAMES[symbol]}")
            for representation in EXPLORE_REPRESENTATIONS:
                if representation not in selected_representations:
                    continue
                if representation == "Wavelength spectrum":
                    st.markdown("##### Line positions")
                    st.markdown(spectrum.render_quantitative_line_positions_svg([symbol]), unsafe_allow_html=True)
                    continue
                st.markdown(f"##### {representation}")
                for spectrum_type in EXPLORE_SPECTRUM_TYPES:
                    if spectrum_type in selected_spectrum_types:
                        if len(selected_spectrum_types) > 1:
                            st.markdown(f"**{spectrum_type}**")
                        render_explore_representation(representation, [symbol], spectrum_type)


def render_explore_spectra() -> None:
    """Render the established first spectroscopy phenomenon surface."""
    st.header("Explore atomic spectra")
    with st.container(key="chem1a_stage_controls"):
        st.markdown('<p class="chem1a-control-label">Spectrum type</p>', unsafe_allow_html=True)
        spectrum_type_columns = st.columns(2)
        selected_spectrum_types = {
            spectrum_type
            for column, spectrum_type in zip(spectrum_type_columns, EXPLORE_SPECTRUM_TYPES)
            if column.checkbox(
                spectrum_type,
                value=explore_control_value(f"spectrum_type_{spectrum_type}", spectrum_type == "Emission"),
                key=f"spectrum_type_{spectrum_type}",
                on_change=remember_explore_control,
                args=(f"spectrum_type_{spectrum_type}",),
            )
        }
        st.markdown('<p class="chem1a-control-label">Atoms in view</p>', unsafe_allow_html=True)
        atom_columns = st.columns(5)
        for column, symbol in zip(atom_columns, spectrum.SPECIES_ORDER):
            column.checkbox(
                spectrum.SPECIES_NAMES[symbol],
                value=explore_control_value(f"atom_{symbol}", symbol in EXPLORE_DEFAULT_SELECTED_SPECIES),
                key=f"atom_{symbol}",
                on_change=remember_explore_control,
                args=(f"atom_{symbol}",),
            )

        st.markdown('<p class="chem1a-control-label">Representations</p>', unsafe_allow_html=True)
        representation_columns = st.columns(3)
        selected_representations = {
            representation
            for column, representation in zip(representation_columns, EXPLORE_REPRESENTATIONS)
            if column.checkbox(
                representation,
                value=explore_control_value(
                    f"representation_{representation}", representation == "Visual spectrum"
                ),
                key=f"representation_{representation}",
                on_change=remember_explore_control,
                args=(f"representation_{representation}",),
            )
        }
        arrangement = st.segmented_control(
            "Arrange by", ["Atom", "Representation"], default="Representation", key="explore_arrangement"
        )

    selected_species = [
        symbol
        for symbol in spectrum.SPECIES_ORDER
        if explore_control_value(f"atom_{symbol}", symbol in EXPLORE_DEFAULT_SELECTED_SPECIES)
    ]

    if not selected_spectrum_types:
        st.info("Choose at least one spectrum type to display.")
    elif not selected_species:
        st.info("Choose at least one spectrum to keep in view.")
    elif not selected_representations:
        st.info("Choose at least one representation to display.")
    else:
        render_explore_evidence(selected_species, selected_spectrum_types, selected_representations, arrangement)
        if "Intensity vs wavelength" in selected_representations:
            st.caption("Intensity curves are illustrative; line positions come from the reference data.")



def render_hydrogen() -> None:
    """Render the spectral-evidence surface learners revisit after paper-based reasoning."""
    st.header("Hydrogen")
    st.write("You have a predicted wavelength. Now test the model against the hydrogen spectrum.")
    if not hydrogen_evidence_revealed():
        st.markdown(hydrogen.render_balmer_barcode_svg(), unsafe_allow_html=True)
    st.caption("Nearest nm is accurate enough for this comparison.")

    transition_columns = st.columns((0.85, 0.12, 0.85, 3.2))
    from_n = transition_columns[0].number_input(
        "From level n",
        min_value=1,
        max_value=20,
        value=5,
        step=1,
        key="hydrogen_from_n_input",
    )
    transition_columns[1].markdown("→")
    to_n = transition_columns[2].number_input(
        "To level n",
        min_value=1,
        max_value=20,
        value=2,
        step=1,
        key="hydrogen_to_n_input",
    )
    prediction_column, action_column = st.columns((1.5, 2.5))
    predicted_wavelength = prediction_column.number_input(
        "Your predicted wavelength (nm)",
        value=None,
        step=1.0,
        placeholder="e.g. 123",
        key="hydrogen_prediction_input",
    )
    plot_prediction = action_column.button("Plot my prediction", key="plot_hydrogen_prediction")
    if plot_prediction:
        target_feature = hydrogen.observed_feature_for_transition(int(from_n), int(to_n))
        if int(from_n) <= int(to_n):
            st.info("For emission, the starting level n must be greater than the ending level.")
        elif target_feature is None:
            st.info("This comparison currently uses the selected Balmer transitions available in the app.")
        elif predicted_wavelength is None:
            st.info("Enter your predicted wavelength in nm first.")
        elif float(predicted_wavelength) <= 0:
            st.info("Enter a positive wavelength in nm.")
        elif not hydrogen.prediction_is_plausible_for_comparison(float(predicted_wavelength)):
            st.info("This value is well outside the wavelength range expected for this comparison. Check that your final wavelength is in nm.")
        else:
            st.session_state["hydrogen_evidence_revealed"] = True
            st.session_state["hydrogen_submitted_from_n"] = int(from_n)
            st.session_state["hydrogen_submitted_to_n"] = int(to_n)
            st.session_state["hydrogen_submitted_prediction_nm"] = float(predicted_wavelength)

    if hydrogen_evidence_revealed():
        submitted_from_n = int(st.session_state["hydrogen_submitted_from_n"])
        submitted_to_n = int(st.session_state["hydrogen_submitted_to_n"])
        submitted_prediction = st.session_state.get("hydrogen_submitted_prediction_nm")
        target_feature = hydrogen.observed_feature_for_transition(submitted_from_n, submitted_to_n)
        if submitted_prediction is None or target_feature is None:
            st.error("The submitted Hydrogen comparison could not be restored.")
            return
        show_transition_labels = st.checkbox("Show transition labels", value=False, key="show_hydrogen_transition_labels")
        st.markdown(
            hydrogen.render_local_comparison_svg(
                prediction_nm=float(submitted_prediction),
                observed_feature=target_feature,
                show_transition_labels=show_transition_labels,
            ),
            unsafe_allow_html=True,
        )
        target_nm = float(target_feature["wavelength_nm"])
        st.write(f"Your prediction: {hydrogen.display_wavelength_nm(float(submitted_prediction))} nm")
        st.write(
            f"Observed {hydrogen.transition_label(target_feature)} line: "
            f"{hydrogen.display_wavelength_nm(target_nm)} nm"
        )
        match_kind, other_feature = hydrogen.prediction_match(target_feature, float(submitted_prediction))
        if match_kind == "other_line" and other_feature is not None:
            st.info(
                f"Your prediction is close to another observed hydrogen line: "
                f"{hydrogen.transition_label(other_feature)} at "
                f"{hydrogen.display_wavelength_nm(float(other_feature['wavelength_nm']))} nm. "
                "Check which energy levels you used."
            )
        elif match_kind == "mismatch":
            st.info(
                "Your prediction does not line up closely with the observed line for this transition. "
                "Check ΔE, your units, and the wavelength conversion."
            )
        st.caption("Line height is simplified here. Compare wavelength position, not relative line strength.")
        compare_prompt("This is the test: does your prediction match an observed line?", key="chem1a_hydrogen_prediction_prompt")

        with st.expander("See more of hydrogen", expanded=False):
            st.write("Visible Balmer lines are only part of the hydrogen spectrum.")
            st.markdown("**Where the series appear**")
            st.markdown(hydrogen.render_series_overview_svg(), unsafe_allow_html=True)

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


st.set_page_config(page_title="CHEM 1A", layout="wide")
apply_shared_visual_system()

spectroscopy_tab, periodic_trends_tab = st.tabs(["Spectroscopy", "Periodic trends"])
with spectroscopy_tab:
    selected_stage = stage_selector(
        ["Explore spectra", "Hydrogen"],
        key="spectroscopy_stage_tabs",
    )
    if selected_stage == "Explore spectra":
        render_explore_spectra()
    elif selected_stage == "Hydrogen":
        render_hydrogen()
with periodic_trends_tab:
    atomic_trends.render()

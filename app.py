import streamlit as st

from chem1a_ui import apply_shared_visual_system, compare_prompt
from experiences.w01_spectroscopy import spectrum


st.set_page_config(page_title="CHEM 1A — Explore spectra", layout="wide")
apply_shared_visual_system()

st.title("CHEM 1A")
st.subheader("Week 01 — Spectroscopy")
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
            value=symbol in spectrum.DEFAULT_SELECTED_SPECIES,
            key=f"atom_{symbol}",
        )
    ]

    st.markdown('<p class="chem1a-control-label">Views</p>', unsafe_allow_html=True)
    combined_view, separate_view = st.columns(2)
    show_combined = combined_view.checkbox("Combined spectrum", value=True)
    show_separate = separate_view.checkbox("Separate spectra", value=False)

if selected_species:
    if show_combined:
        st.subheader("Combined selected lines")
        st.markdown(spectrum.render_combined_svg(selected_species), unsafe_allow_html=True)
    if show_separate:
        st.subheader("Separate spectra")
        st.markdown(spectrum.render_comparison_svg(selected_species), unsafe_allow_html=True)
    if not show_combined and not show_separate:
        st.info("Choose a view to inspect the selected line positions.")
    st.caption("Colour is an illustrative wavelength cue. The labelled horizontal position is the evidence to compare.")
    if "Na" in selected_species:
        st.caption("Sodium includes two selected lines at 588.995 nm and 589.592 nm; on this shared scale they sit very close together.")
    compare_prompt("What changes? What stays the same?")

    with st.expander("Explore absorption spectra", expanded=False):
        st.caption("This simplified view compares line positions. Relative line strength is not represented.")
        if show_combined:
            st.markdown("**Combined selected lines — emission**")
            st.markdown(spectrum.render_combined_svg(selected_species), unsafe_allow_html=True)
            st.markdown("**Combined selected lines — absorption**")
            st.markdown(spectrum.render_combined_absorption_svg(selected_species), unsafe_allow_html=True)
        if show_separate:
            st.markdown("**Separate selected atoms**")
            for symbol in selected_species:
                st.markdown(f"**{spectrum.SPECIES_NAMES[symbol]} — emission**")
                st.markdown(spectrum.render_comparison_svg([symbol]), unsafe_allow_html=True)
                st.markdown(f"**{spectrum.SPECIES_NAMES[symbol]} — absorption**")
                st.markdown(spectrum.render_absorption_comparison_svg([symbol]), unsafe_allow_html=True)
        if not show_combined and not show_separate:
            st.info("Choose a view to inspect matched emission and absorption line positions.")
        compare_prompt(
            "What do you notice about where the absorption and emission lines appear?",
            key="chem1a_absorption_prompt",
        )
else:
    st.info("Select an atom to begin.")

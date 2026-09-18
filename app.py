import streamlit as st

from chem1a_ui import apply_shared_visual_system, compare_prompt
from experiences.w01_spectroscopy import spectrum


st.set_page_config(page_title="CHEM 1A — Compare atoms", layout="wide")
apply_shared_visual_system()

st.title("CHEM 1A")
st.subheader("Week 01 — Spectroscopy")
st.header("Compare atomic spectra")
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
    compare_prompt("What do you notice when you compare the patterns?")
else:
    st.info("Select an atom to begin.")

import streamlit as st

from experiences.w01_spectroscopy import spectrum


st.set_page_config(page_title="CHEM 1A — Compare atoms", layout="wide")

st.title("CHEM 1A")
st.subheader("Week 01 — Spectroscopy")
st.header("Compare atomic spectra")
st.write("Each row shows selected prominent lines from a different atom. They all use the same wavelength scale.")

selected_species = st.multiselect(
    "Atoms to compare",
    options=list(spectrum.SPECIES_ORDER),
    default=list(spectrum.SPECIES_ORDER),
    format_func=lambda symbol: spectrum.SPECIES_NAMES[symbol],
    help="Choose one or more neutral atoms. The line positions are selected features, not an exhaustive spectrum.",
)

if selected_species:
    st.markdown(spectrum.render_comparison_svg(selected_species), unsafe_allow_html=True)
    st.caption("Colour is an illustrative wavelength cue. The labelled horizontal position is the evidence to compare.")
    if "Na" in selected_species:
        st.caption("Sodium includes two selected lines at 588.995 nm and 589.592 nm; on this shared scale they sit very close together.")
    st.write("What do you notice when you compare the patterns?")
else:
    st.info("Choose at least one atom to inspect its selected spectral features.")
